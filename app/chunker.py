from __future__ import annotations

import hashlib
import re
from pathlib import Path

from app.model import Chunk, Document


SECTION = re.compile(r"(?m)^\s{0,3}(#{1,6})\s+(.+?)\s*$")


def _normalise_text(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _chunk_text(text: str, size: int, overlap: int) -> list[str]:
    text = _normalise_text(text)
    if not text:
        return []
    if len(text) <= size:
        return [text]
    step = max(1, size - overlap)
    return [text[start:start + size] for start in range(0, len(text), step)]


def _make_chunk(document: Document, heading: str, part: str, index: int) -> Chunk:
    prefix = f"{document.title}\n{heading}".strip()
    identity = f"{document.path.as_posix()}:{heading}:{part}"
    return Chunk(
        id=hashlib.sha1(identity.encode("utf-8")).hexdigest(),
        source_path=document.path.as_posix(),
        title=document.title,
        heading=heading,
        text=f"{prefix}\n{part}".strip(),
        chunk_index=index,
        tags=document.tags,
        modified=document.modified,
        category=document.category,
        metadata=document.metadata,
        source_id=document.source_id,
        aliases=document.aliases,
        links=document.links,
        relation_tags=document.relation_tags,
    )


def chunk_document(document: Document, max_tokens: int, overlap: int) -> list[Chunk]:
    """Split by headings first, then use a character window as a token proxy."""
    size = max(200, max_tokens * 4)
    overlap_size = min(size // 2, max(0, overlap * 4))
    text = _normalise_text(document.text)
    if not text:
        return []
    if len(text) <= size:
        return [_make_chunk(document, "", text, 0)]

    sections: list[tuple[str, str]] = []
    matches = list(SECTION.finditer(text))

    if not matches:
        sections.append(("", text))
    else:
        if matches[0].start() > 0:
            sections.append(("", text[:matches[0].start()]))
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            sections.append((match.group(2), text[match.end():end]))

    chunks: list[Chunk] = []
    for heading, section_text in sections:
        section_text = _normalise_text(section_text)
        if not section_text:
            continue
        parts = (
            [section_text]
            if len(section_text) <= size
            else _chunk_text(section_text, size, overlap_size)
        )
        for part in parts:
            chunks.append(_make_chunk(document, heading, part, len(chunks)))
    return chunks
