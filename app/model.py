from dataclasses import dataclass
from pathlib import Path


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