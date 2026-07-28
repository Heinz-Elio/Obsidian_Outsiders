from __future__ import annotations

import re
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
        links = [match.group(2) or match.group(1) for match in WIKILINK.finditer(body)]

        yield Document(
            path=relative,
            title=str(metadata.get("title") or _title(path, body)),
            text=_clean_links(body).strip(),
            tags=sorted(set(tags)),
            aliases=_as_list(metadata.get("aliases")),
            links=links,
            headings=headings,
            modified=path.stat().st_mtime,
        )
