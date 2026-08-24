from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "Setting"
OUTPUT_DIR = PROJECT_ROOT / "merged" / "notebooklm"

NOTEBOOKLM_SOURCE_LIMIT = 50
LONG_NOTE_CHARS = 10_000
MAX_CHARS_PER_MERGED_FILE = 300_000

EXCLUDE_FOLDERS = {
    ".obsidian",
    ".git",
    ".smart-env",
    ".venv",
    "copilot",
    "Excalidraw",
    "Markwhen",
    "Templates",
    "trash",
    "archive",
    "00_總覽",
}
EXCLUDE_FILES = {"README.md"}

FRONTMATTER_PATTERN = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
WIKILINK_PATTERN = re.compile(
    r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]"
)
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
INVALID_FILENAME = re.compile(r'[<>:"/\\|?*]+')
EMPTY_FIELD_PATTERN = re.compile(r"^(?:[-*]\s*)?[^:#]+:\s*$")
EMPTY_MARKERS = {"", "-", "none", "null", "description", "無"}


@dataclass(frozen=True)
class Note:
    path: Path
    group: str
    title: str
    body_chars: int
    rendered: str


@dataclass(frozen=True)
class OutputSource:
    filename: str
    content: str
    kind: str
    notes: tuple[Note, ...]


def extract_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return {}, text
    try:
        metadata = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        metadata = {}
    return metadata if isinstance(metadata, dict) else {}, text[match.end():]


def resolve_wikilinks(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        alias = (match.group(2) or "").strip()
        if alias and alias.casefold() != target.casefold():
            return f"{alias} ({target})"
        return alias or target

    return WIKILINK_PATTERN.sub(replace, text)


def _meaningful(lines: list[str]) -> bool:
    return any(
        line.strip().casefold() not in EMPTY_MARKERS
        and line.strip() != "---"
        and not EMPTY_FIELD_PATTERN.match(line.strip())
        for line in lines
    )


def _drop_empty_sections(lines: list[str]) -> list[str]:
    output: list[str] = []
    index = 0
    while index < len(lines):
        match = HEADING_PATTERN.match(lines[index])
        if not match:
            output.append(lines[index])
            index += 1
            continue

        end = index + 1
        while end < len(lines) and not HEADING_PATTERN.match(lines[end]):
            end += 1
        section = lines[index + 1:end]
        heading = match.group(2).strip().casefold()
        if heading not in EMPTY_MARKERS and _meaningful(section):
            output.extend([lines[index], *section])
        index = end
    return output


def _demote_headings(lines: list[str]) -> list[str]:
    output = []
    for line in lines:
        match = HEADING_PATTERN.match(line)
        if not match:
            output.append(line)
            continue
        level = min(6, len(match.group(1)) + 2)
        output.append(f"{'#' * level} {match.group(2).strip()}")
    return output


def clean_body(text: str, title: str) -> str:
    text = resolve_wikilinks(text).replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()

    if lines:
        first_heading = HEADING_PATTERN.match(lines[0])
        if (
            first_heading
            and len(first_heading.group(1)) == 1
            and first_heading.group(2).strip().casefold() == title.casefold()
        ):
            lines = lines[1:]

    lines = _drop_empty_sections(lines)
    lines = _demote_headings(lines)

    compact: list[str] = []
    for line in lines:
        if line == "---" or EMPTY_FIELD_PATTERN.match(line.strip()):
            continue
        if not line and (not compact or not compact[-1]):
            continue
        compact.append(line)
    return "\n".join(compact).strip()


def _metadata_value(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(_metadata_value(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return resolve_wikilinks(str(value))


def compact_metadata(metadata: dict[str, Any]) -> str:
    values = []
    for key, value in metadata.items():
        if value is None or value is False or value == "" or value == [] or value == {}:
            continue
        if key == "importance" and str(value).casefold() == "normal":
            continue
        values.append(f"{key}={_metadata_value(value)}")
    return "; ".join(values)


def _title(path: Path, metadata: dict[str, Any], body: str) -> str:
    configured = str(metadata.get("title") or "").strip()
    if configured:
        return configured
    for line in body.splitlines():
        match = HEADING_PATTERN.match(line)
        if match:
            return match.group(2).strip()
    return path.stem


def render_note(relative: Path, metadata: dict[str, Any], body: str) -> Note:
    title = _title(relative, metadata, body)
    body = clean_body(body, title)
    parts = [f"## {title}", f"Source: {relative.as_posix()}"]
    metadata_line = compact_metadata(metadata)
    if metadata_line:
        parts.append(f"Meta: {metadata_line}")
    if body:
        parts.extend(["", body])
    rendered = "\n".join(parts).strip()
    group = relative.parent.as_posix() if relative.parent != Path(".") else "root"
    return Note(relative, group, title, len(body), rendered)


def collect_notes(root: Path) -> list[Note]:
    root = root.resolve()
    notes = []
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if any(part in EXCLUDE_FOLDERS for part in relative.parts):
            continue
        if path.name in EXCLUDE_FILES:
            continue
        metadata, body = extract_frontmatter(path.read_text(encoding="utf-8"))
        notes.append(render_note(relative, metadata, body))
    return notes


def _safe_name(value: str) -> str:
    value = INVALID_FILENAME.sub("_", value).strip(" ._")
    return re.sub(r"\s+", "_", value) or "root"


def _render_bundle(label: str, notes: list[Note]) -> str:
    body = "\n\n---\n\n".join(note.rendered for note in notes)
    return f"# {label}\n\n{body}\n"


def _category_bundles(short_notes: list[Note]) -> list[OutputSource]:
    grouped: dict[str, list[Note]] = defaultdict(list)
    for note in short_notes:
        grouped[note.group].append(note)

    outputs = []
    for group in sorted(grouped):
        parts: list[list[Note]] = []
        current: list[Note] = []
        current_size = 0
        for note in grouped[group]:
            note_size = len(note.rendered) + 7
            if current and current_size + note_size > MAX_CHARS_PER_MERGED_FILE:
                parts.append(current)
                current = []
                current_size = 0
            current.append(note)
            current_size += note_size
        if current:
            parts.append(current)

        for part_index, part in enumerate(parts, start=1):
            suffix = f"_part_{part_index:02d}" if len(parts) > 1 else ""
            filename = f"{_safe_name(group)}{suffix}.md"
            outputs.append(
                OutputSource(
                    filename,
                    _render_bundle(group, part),
                    "category_bundle",
                    tuple(part),
                )
            )
    return outputs


def _balanced_fallback(short_notes: list[Note], slots: int) -> list[OutputSource]:
    if slots <= 0:
        raise RuntimeError(
            "Standalone long notes use all 50 NotebookLM source slots; "
            "increase LONG_NOTE_CHARS or reduce the input set."
        )
    bin_count = min(slots, len(short_notes))
    bins: list[list[Note]] = [[] for _ in range(bin_count)]
    sizes = [0] * bin_count
    for note in sorted(short_notes, key=lambda item: len(item.rendered), reverse=True):
        target = min(range(bin_count), key=sizes.__getitem__)
        bins[target].append(note)
        sizes[target] += len(note.rendered)

    outputs = []
    for index, notes in enumerate(bins, start=1):
        notes.sort(key=lambda item: item.path.as_posix())
        outputs.append(
            OutputSource(
                f"mixed_bundle_{index:02d}.md",
                _render_bundle(f"Mixed knowledge bundle {index}", notes),
                "mixed_bundle",
                tuple(notes),
            )
        )
    return outputs


def build_outputs(notes: list[Note]) -> list[OutputSource]:
    long_notes = [note for note in notes if note.body_chars >= LONG_NOTE_CHARS]
    short_notes = [note for note in notes if note.body_chars < LONG_NOTE_CHARS]
    if len(long_notes) > NOTEBOOKLM_SOURCE_LIMIT:
        raise RuntimeError(
            f"{len(long_notes)} notes exceed the standalone threshold, more than "
            f"NotebookLM's {NOTEBOOKLM_SOURCE_LIMIT}-source limit."
        )

    standalone = []
    for note in long_notes:
        digest = hashlib.sha1(note.path.as_posix().encode("utf-8")).hexdigest()[:8]
        standalone.append(
            OutputSource(
                f"standalone_{_safe_name(note.path.stem)}_{digest}.md",
                f"# {note.title}\n\n{note.rendered}\n",
                "standalone",
                (note,),
            )
        )

    bundles = _category_bundles(short_notes)
    available = NOTEBOOKLM_SOURCE_LIMIT - len(standalone)
    if len(bundles) > available:
        bundles = _balanced_fallback(short_notes, available)

    outputs = [*standalone, *bundles]
    if len(outputs) > NOTEBOOKLM_SOURCE_LIMIT:
        raise RuntimeError("Output exceeds NotebookLM's 50-source limit.")
    return sorted(outputs, key=lambda output: output.filename)


def write_outputs(outputs: list[OutputSource]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_file in OUTPUT_DIR.glob("*.md"):
        old_file.unlink()

    manifest = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "source_limit": NOTEBOOKLM_SOURCE_LIMIT,
        "long_note_chars": LONG_NOTE_CHARS,
        "output_count": len(outputs),
        "outputs": [],
    }
    for output in outputs:
        path = OUTPUT_DIR / output.filename
        path.write_text(output.content, encoding="utf-8")
        manifest["outputs"].append(
            {
                "file": output.filename,
                "kind": output.kind,
                "note_count": len(output.notes),
                "characters": len(output.content),
                "sources": [note.path.as_posix() for note in output.notes],
            }
        )

    (OUTPUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build() -> None:
    notes = collect_notes(INPUT_DIR)
    outputs = build_outputs(notes)
    write_outputs(outputs)
    standalone = sum(output.kind == "standalone" for output in outputs)
    print(
        f"notes={len(notes)} outputs={len(outputs)}/{NOTEBOOKLM_SOURCE_LIMIT} "
        f"standalone={standalone} merged={len(outputs) - standalone}"
    )
    print(f"publish directory: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    build()
