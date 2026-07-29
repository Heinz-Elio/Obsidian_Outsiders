from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Document:
    path: Path
    title: str
    text: str
    tags: list[str]
    aliases: list[str]
    links: list[str]
    headings: list[str]
    modified: float
    category: str
    metadata: dict[str, Any]
    source_id: str
    entity_names: list[str]
    relation_tags: list[str]


@dataclass
class Chunk:
    id: str
    source_path: str
    title: str
    heading: str
    text: str
    chunk_index: int
    tags: list[str]
    modified: float
    category: str
    metadata: dict[str, Any]
    source_id: str
    aliases: list[str]
    links: list[str]
    relation_tags: list[str]