from __future__ import annotations

import re
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import yaml

# =========================
# CONFIG
# =========================

INPUT_DIR = Path("./Setting")
OUTPUT_DIR = Path("./merged")

MERGE_NAME = "knowledge_base"

RESOLVE_WIKILINKS = True

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
    "00_總覽"
}

EXCLUDE_FILES = {
    "README.md",
}

# Optional: max size per merged file (soft split)
MAX_CHARS_PER_FILE = 300_000

# =========================
# PATTERNS
# =========================

WIKILINK_PATTERN = re.compile(r"\[\[([^\]|]+)(\|([^\]]+))?\]\]")
FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)

# =========================
# FRONTMATTER
# =========================

def extract_frontmatter(text: str):
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return {}, text

    raw_yaml = match.group(1)

    try:
        metadata = yaml.safe_load(raw_yaml) or {}
    except Exception:
        metadata = {}

    remaining = text[match.end():]
    return metadata, remaining


def format_metadata(metadata: dict) -> list[str]:
    if not metadata:
        return []

    out = ["## Metadata", ""]

    for k, v in metadata.items():
        if isinstance(v, list):
            v = ", ".join(map(str, v))
        elif isinstance(v, dict):
            v = str(v)

        out.append(f"- {k}: {v}")

    out.append("")
    return out

# =========================
# TEXT NORMALIZATION
# =========================

def resolve_wikilinks(text: str) -> str:
    def repl(m):
        return m.group(3) if m.group(3) else m.group(1)

    return WIKILINK_PATTERN.sub(repl, text)

# =========================
# FILE COLLECTION
# =========================

def collect_files_by_folder(root: Path) -> dict[str, list[Path]]:
    grouped = defaultdict(list)

    for path in root.rglob("*.md"):
        if any(part in EXCLUDE_FOLDERS for part in path.parts):
            continue
        if path.name in EXCLUDE_FILES:
            continue

        rel = path.relative_to(root)

        folder = str(rel.parent) if rel.parent != Path(".") else "root"

        grouped[folder].append(path)

    for k in grouped:
        grouped[k] = sorted(grouped[k])

    return dict(grouped)

# =========================
# VERSIONING
# =========================

def next_version(folder: Path, base: str) -> int:
    pattern = re.compile(rf"{re.escape(base)}_v(\d+)\.md")

    versions = []
    for f in folder.glob(f"{base}_v*.md"):
        m = pattern.match(f.name)
        if m:
            versions.append(int(m.group(1)))

    return max(versions, default=0) + 1

# =========================
# MERGE LOGIC
# =========================

def merge_group(group_name: str, files: list[Path]):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"{group_name.replace('\\', '_')}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.md"
    latest_file = OUTPUT_DIR / f"{group_name.replace('\\', '_')}_latest.md"

    lines = []

    lines.append(f"# {group_name}")
    lines.append("")
    lines.append(f"- Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"- Source count: {len(files)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    current_size = 0

    def flush_chunk():
        nonlocal lines, current_size
        current_size = 0

    for file in files:
        rel = file.relative_to(INPUT_DIR)
        text = file.read_text(encoding="utf-8")

        metadata, text = extract_frontmatter(text)

        if RESOLVE_WIKILINKS:
            text = resolve_wikilinks(text)

        block = []

        block.append(f"# Source: {rel}")
        block.extend(format_metadata(metadata))
        block.append("```text")
        block.append(str(rel))
        block.append("```")
        block.append("")
        block.append(text.strip())
        block.append("\n---\n")

        chunk = "\n".join(block)

        # soft split by size
        if current_size + len(chunk) > MAX_CHARS_PER_FILE:
            flush_chunk()

        lines.append(chunk)
        current_size += len(chunk)

    out_file.write_text("\n".join(lines), encoding="utf-8")
    shutil.copyfile(out_file, latest_file)

    print(f"[{group_name}] -> {out_file}")

# =========================
# MAIN
# =========================

def build():
    grouped = collect_files_by_folder(INPUT_DIR)

    for folder, files in grouped.items():
        merge_group(folder, files)


if __name__ == "__main__":
    build()