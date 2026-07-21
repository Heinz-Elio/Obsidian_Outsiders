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