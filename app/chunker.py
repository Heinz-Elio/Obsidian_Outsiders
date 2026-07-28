from __future__ import annotations

import hashlib
import re
from pathlib import Path

from app.model import Chunk, Document


SECTION = re.compile(r"(?m)^(#{1,6})\s+(.+?)\s*$")


def _chunk_text(text: str, size: int, overlap: int) -> list[str]:
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if not text:
        return []
    step = max(1, size - overlap)
    return [text[start:start + size] for start in range(0, len(text), step)]


def chunk_document(document: Document, max_tokens: int, overlap: int) -> list[Chunk]:
    """Split by headings first, then use a character window as a token proxy."""
    size = max(200, max_tokens * 4)
    overlap_size = min(size // 2, max(0, overlap * 4))
    sections: list[tuple[str, str]] = []
    matches = list(SECTION.finditer(document.text))

    if not matches:
        sections.append(("", document.text))
    else:
        if matches[0].start() > 0:
            sections.append(("", document.text[:matches[0].start()]))
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(document.text)
            sections.append((match.group(2), document.text[match.end():end]))

    chunks: list[Chunk] = []
    for heading, section_text in sections:
        prefix = f"{document.title}\n{heading}\n".strip()
        for part in _chunk_text(section_text, size, overlap_size):
            index = len(chunks)
            identity = f"{document.path.as_posix()}:{index}:{part}"
            chunk_id = hashlib.sha1(identity.encode("utf-8")).hexdigest()
            chunks.append(
                Chunk(
                    id=chunk_id,
                    source_path=document.path.as_posix(),
                    title=document.title,
                    heading=heading,
                    text=f"{prefix}\n{part}".strip(),
                    chunk_index=index,
                    tags=document.tags,
                    modified=document.modified,
                )
            )
    return chunks
