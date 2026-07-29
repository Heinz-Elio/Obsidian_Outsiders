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
TAG = re.compile(r"(?<!\w)#([\w-]+)")

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
        return [str(item) for item in value]
    return [str(value)]


def _title(path: Path, text: str) -> str:
    match = HEADING.search(text)
    return match.group(1) if match else path.stem


def _clean_links(text: str) -> str:
    return WIKILINK.sub(lambda match: match.group(2) or match.group(1), text)


def load_documents(root: Path) -> Iterable[Document]:
    """Yield source Markdown files while excluding generated/plugin state."""
    root = root.resolve()
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue

        raw = path.read_text(encoding="utf-8")
        metadata, body = _frontmatter(raw)
        headings = HEADING.findall(body)
        tags = _as_list(metadata.get("tags"))
        tags.extend(TAG.findall(body))
        links = [match.group(1).strip() for match in WIKILINK.finditer(body)]
        aliases = _as_list(metadata.get("aliases"))
        relation_tags = _relation_values(metadata)
        entity_names = sorted(
            {
                path.stem,
                str(metadata.get("title") or _title(path, body)),
                str(metadata.get("name_en") or ""),
                *aliases,
            }
            - {""}
        )

        yield Document(
            path=relative,
            title=str(metadata.get("title") or _title(path, body)),
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
        )
