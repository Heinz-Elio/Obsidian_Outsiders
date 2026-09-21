from __future__ import annotations

import re
import hashlib
from pathlib import Path
from typing import Iterable

import yaml

from app.model import Document


FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
H1 = re.compile(r"^\s{0,3}#\s+(.+?)\s*#*\s*$", re.MULTILINE)
TAG = re.compile(r"(?<!\w)#([\w-]+)")
# "- [[target]] #relation #other" lines used in the 關係 section of notes.
TYPED_RELATION = re.compile(
    r"^\s*-\s*\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]\s*((?:#[\w-]+\s*)+)$",
    re.MULTILINE,
)
ALIAS_SPLIT = re.compile(r"\s*[|｜/／,，、]\s*")

# Intermediate NotebookLM exports produced by scripts/mw_converter.py.
EXCLUDED_SUFFIXES = (".mw.md",)

EXCLUDED_DIRS = {
    ".git",
    ".obsidian",
    ".smart-env",
    ".idea",
    ".venv",
    ".cursor-usage",
    "copilot",
    "Excalidraw",
    "merged",
    "Templates",
}


def _category(relative: Path) -> str:
    """Return the stable setting category encoded by a folder name."""
    for part in relative.parts:
        if "_" in part and part[:2].isdigit():
            return part[3:] or part
    return "uncategorized"


def _metadata(raw: dict) -> dict:
    """Keep frontmatter values safe and useful as vector-store payloads."""
    allowed = {
        "type",
        "importance",
        "entity_type",
        "alive",
        "ranger",
        "military",
        "process_srune",
        "have_combat_eq",
        "name_en",
        "id",
        "involved",
        "character_involved",
        "prev",
        "next",
        "location",
        "timeline",
        "sub_type",
        "source_file",
        "source_sheet",
        "operation",
        "generated",
    }
    return {key: value for key, value in raw.items() if key in allowed}


def _relation_values(metadata: dict) -> list[str]:
    keys = ("involved", "character_involved", "prev", "next", "location")
    values = []
    for key in keys:
        values.extend(_as_list(metadata.get(key)))
    return sorted(set(values))


def _source_id(relative: Path) -> str:
    return hashlib.sha1(relative.as_posix().casefold().encode("utf-8")).hexdigest()


def _frontmatter(text: str) -> tuple[dict, str]:
    match = FRONTMATTER.match(text)
    if not match:
        return {}, text
    return yaml.safe_load(match.group(1)) or {}, text[match.end():]


def _as_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if item is not None and str(item).strip()]
    return [str(value)]


def _title(path: Path, text: str) -> str:
    match = HEADING.search(text)
    return match.group(1) if match else path.stem


def _body_aliases(text: str) -> list[str]:
    """Read the reading/romanisation line placed directly under the H1 heading.

    Notes write e.g. ``ななみ　にこら | Nanami Nikola`` on the first non-empty
    line after ``# 七海尼歌娜``. Anything that looks like markup is ignored.
    """
    match = H1.search(text)
    if not match:
        return []
    rest = text[match.end():].lstrip("\n").split("\n", 1)[0].strip()
    if not rest or len(rest) > 80 or rest[0] in "#-|*>[!`":
        return []
    aliases = []
    for part in ALIAS_SPLIT.split(rest):
        part = part.strip()
        if part and part not in aliases:
            aliases.append(part)
    return aliases


def _typed_relations(text: str) -> list[tuple[str, str]]:
    relations: list[tuple[str, str]] = []
    for match in TYPED_RELATION.finditer(text):
        target = match.group(1).strip()
        if not target:
            continue
        for tag in TAG.findall(match.group(2)):
            pair = (target, tag.casefold())
            if pair not in relations:
                relations.append(pair)
    return relations


def _clean_links(text: str) -> str:
    return WIKILINK.sub(lambda match: match.group(2) or match.group(1), text)


def source_paths(root: Path) -> Iterable[Path]:
    """Yield source Markdown paths while excluding generated/plugin state."""
    root = root.resolve()
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if path.name.lower().endswith(EXCLUDED_SUFFIXES):
            continue
        yield path


def load_document(root: Path, path: Path) -> Document:
    """Parse one Markdown source below the configured vault root."""
    root = root.resolve()
    path = path.resolve() if path.is_absolute() else (root / path).resolve()
    if root not in path.parents:
        raise ValueError("source path escapes the configured vault")
    relative = path.relative_to(root)

    raw = path.read_text(encoding="utf-8")
    metadata, body = _frontmatter(raw)
    headings = HEADING.findall(body)
    tags = _as_list(metadata.get("tags"))
    tags.extend(TAG.findall(body))
    links = [match.group(1).strip() for match in WIKILINK.finditer(body)]
    aliases = _as_list(metadata.get("aliases"))
    title = str(metadata.get("title") or _title(path, body))
    for alias in _body_aliases(body):
        if alias != title and alias not in aliases:
            aliases.append(alias)
    relations = _typed_relations(body)
    relation_tags = _relation_values(metadata)
    entity_names = sorted(
        {
            path.stem,
            title,
            str(metadata.get("name_en") or ""),
            *aliases,
        }
        - {""}
    )

    return Document(
        path=relative,
        title=title,
        text=_clean_links(body).strip(),
        tags=sorted(set(tags)),
        aliases=aliases,
        links=links,
        headings=headings,
        modified=path.stat().st_mtime,
        category=_category(relative),
        metadata=_metadata(metadata),
        source_id=_source_id(relative),
        entity_names=entity_names,
        relation_tags=relation_tags,
        relations=relations,
    )


def load_documents(root: Path) -> Iterable[Document]:
    """Yield parsed Markdown documents from the configured vault."""
    for path in source_paths(root):
        yield load_document(root, path)
