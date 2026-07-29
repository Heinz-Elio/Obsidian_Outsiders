from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from app.model import Document


SECTION = re.compile(r"(?m)^(#{1,6})\s+(.+?)\s*$")


def find_document(documents: Iterable[Document], target: str) -> Document | None:
    """Resolve a path, title, id, stem, alias, or entity name."""
    needle = target.strip().replace("\\", "/").casefold()
    documents = list(documents)
    title_matches = []
    partial_matches = []
    for document in documents:
        primary_candidates = {
            document.path.as_posix().casefold(),
            document.title.casefold(),
            document.path.stem.casefold(),
            document.metadata.get("id", "").casefold()
            if isinstance(document.metadata.get("id"), str)
            else "",
        }
        if needle in primary_candidates:
            return document
        if needle and (
            needle in document.title.casefold()
            or needle in document.path.stem.casefold()
        ):
            title_matches.append(document)
    if len(title_matches) == 1:
        return title_matches[0]

    for document in documents:
        candidates = {name.casefold() for name in document.entity_names}
        if needle in candidates:
            return document
        if any(needle and needle in candidate for candidate in candidates):
            partial_matches.append(document)
    if len(partial_matches) == 1:
        return partial_matches[0]
    return None


def document_sections(document: Document, headings: list[str] | None = None) -> list[dict]:
    wanted = {heading.casefold() for heading in headings or []}
    matches = list(SECTION.finditer(document.text))
    sections = []
    boundaries = [(0, matches[0].start())] if matches else [(0, len(document.text))]
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(document.text)
        boundaries.append((match.end(), end))

    if not matches:
        selected = [(0, "", document.text)]
    else:
        selected = []
        if matches[0].start() > 0:
            selected.append((0, "", document.text[:matches[0].start()]))
        for index, match in enumerate(matches):
            heading = match.group(2).strip()
            if wanted and heading.casefold() not in wanted:
                continue
            selected.append((index, heading, document.text[match.end():boundaries[index + 1][1]]))

    for index, heading, text in selected:
        if text.strip():
            start = document.text[: document.text.find(text)].count("\n") + 1
            sections.append(
                {
                    "section_index": index,
                    "heading": heading,
                    "start_line": start,
                    "end_line": start + text.count("\n"),
                    "text": text.strip(),
                }
            )
    return sections


def related_documents(
    document: Document,
    documents: Iterable[Document],
    relation_types: list[str] | None = None,
) -> list[dict]:
    wanted = set(relation_types or [])
    output = []
    names = {
        name.casefold()
        for name in [document.title, document.path.stem, *document.aliases, *document.links]
    }
    for candidate in documents:
        if candidate.source_id == document.source_id:
            continue
        candidate_names = {
            str(name).casefold()
            for name in [
                candidate.title,
                candidate.path.stem,
                *candidate.aliases,
                candidate.metadata.get("name_en", ""),
            ]
        }
        linked = bool(
            names.intersection(candidate_names)
            or candidate.title.casefold() in names
        )
        relations = sorted(set(document.relation_tags).intersection(wanted or document.relation_tags))
        if linked or relations:
            output.append(
                {
                    "source_path": candidate.path.as_posix(),
                    "title": candidate.title,
                    "category": candidate.category,
                    "relation_tags": relations,
                    "entity_names": candidate.entity_names,
                }
            )
    return output


def classify_question(question: str) -> str:
    if any(token in question for token in ("為什麼", "為何", "原因", "如何導致")):
        return "因果未知"
    if any(token in question for token in ("將會", "之後", "未來", "會否", "會不會")):
        return "未來未知"
    return "過去未知"
