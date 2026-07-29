from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from app.model import Document


@dataclass(frozen=True)
class GraphEdge:
    source_path: str
    target_path: str
    relation: str


def _normalise_name(value: object) -> str:
    text = str(value or "").strip()
    if text.startswith("[[") and text.endswith("]]"):
        text = text[2:-2]
    text = text.split("|", 1)[0].split("#", 1)[0].strip()
    return text.replace("\\", "/").casefold()


def _values(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


class SourceGraph:
    """Resolve Obsidian entities and expose typed forward/backward relations."""

    def __init__(self, documents: Iterable[Document]):
        self.documents = list(documents)
        self.by_path = {document.path.as_posix(): document for document in self.documents}
        names: dict[str, set[str]] = defaultdict(set)
        for document in self.documents:
            path = document.path.as_posix()
            candidates = {
                path,
                Path(path).stem,
                document.title,
                *document.aliases,
                *document.entity_names,
                document.metadata.get("id", ""),
            }
            for candidate in candidates:
                name = _normalise_name(candidate)
                if name:
                    names[name].add(path)
        self.name_index = dict(names)
        self.edges: dict[str, list[GraphEdge]] = defaultdict(list)
        self.unresolved: list[dict[str, str]] = []
        self.ambiguous: list[dict[str, object]] = []
        self._build_edges()

    def resolve(self, target: str) -> str | None:
        name = _normalise_name(target)
        direct = target.replace("\\", "/").strip("/")
        if direct in self.by_path:
            return direct
        matches = self.name_index.get(name, set())
        return next(iter(matches)) if len(matches) == 1 else None

    def _add_reference(self, source: str, raw_target: str, relation: str) -> None:
        name = _normalise_name(raw_target)
        matches = self.name_index.get(name, set())
        if len(matches) == 1:
            target = next(iter(matches))
            if target != source:
                self.edges[source].append(GraphEdge(source, target, relation))
                self.edges[target].append(GraphEdge(target, source, f"backlink:{relation}"))
        elif len(matches) > 1:
            self.ambiguous.append(
                {"source_path": source, "target": raw_target, "matches": sorted(matches)}
            )
        elif name:
            self.unresolved.append(
                {"source_path": source, "target": raw_target, "relation": relation}
            )

    def _build_edges(self) -> None:
        relation_fields = {
            "involved": "involved",
            "character_involved": "involved",
            "prev": "event_prev",
            "next": "event_next",
            "location": "location",
        }
        for document in self.documents:
            source = document.path.as_posix()
            for target in document.links:
                self._add_reference(source, target, "wikilink")
            for field, relation in relation_fields.items():
                for target in _values(document.metadata.get(field)):
                    self._add_reference(source, target, relation)

    def related(
        self,
        source_or_entity: str,
        *,
        depth: int = 1,
        limit: int = 20,
    ) -> list[dict[str, str]]:
        source = self.resolve(source_or_entity)
        if source is None:
            return []
        seen = {source}
        queue = deque([(source, 0)])
        output = []
        while queue and len(output) < limit:
            current, level = queue.popleft()
            if level >= max(0, depth):
                continue
            for edge in self.edges.get(current, []):
                if edge.target_path in seen:
                    continue
                seen.add(edge.target_path)
                output.append(
                    {
                        "source_path": edge.target_path,
                        "relation": edge.relation,
                        "from_path": current,
                    }
                )
                queue.append((edge.target_path, level + 1))
                if len(output) >= limit:
                    break
        return output
