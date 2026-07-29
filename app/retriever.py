from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable

from app.graph import SourceGraph
from app.model import Document
from app.router import SCOPE_CATEGORIES
from app.store import VectorStore


def _text(value: object) -> str:
    return str(value or "").strip().casefold()


class HybridRetriever:
    """Combine entity matching, semantic search, and one-hop source relations."""

    def __init__(
        self,
        documents: Iterable[Document],
        graph: SourceGraph,
        store: VectorStore,
        embedder,
    ):
        self.documents = list(documents)
        self.by_path = {document.path.as_posix(): document for document in self.documents}
        self.graph = graph
        self.store = store
        self.embedder = embedder

    def _lexical_sources(self, query: str, entity: str | None) -> dict[str, float]:
        query_text = _text(query)
        requested = _text(entity)
        matches = {}
        for document in self.documents:
            names = {
                _text(document.title),
                _text(document.path.stem),
                *(_text(name) for name in document.entity_names),
                _text(document.metadata.get("id")),
            }
            names.discard("")
            score = 0.0
            if requested and requested in names:
                score = 1.0
            elif requested and any(requested in name or name in requested for name in names):
                score = 0.9
            elif any(len(name) >= 2 and name in query_text for name in names):
                score = 0.85
            if score:
                matches[document.path.as_posix()] = score
        return matches

    def retrieve(
        self,
        query: str,
        *,
        scope: str | None = None,
        entity: str | None = None,
        limit: int = 16,
        graph_limit: int = 12,
        per_source: int = 2,
    ) -> list[dict[str, Any]]:
        vector = self.embedder.embed_one(f"{entity or ''} {query}".strip())
        category = SCOPE_CATEGORIES.get(scope)
        lexical = self._lexical_sources(query, entity)
        semantic = self.store.search(
            vector,
            max(12, limit * 2),
            fallback_to_unfiltered=True,
        )
        lexical_chunks = []
        for path in lexical:
            lexical_chunks.extend(
                self.store.search(
                    vector,
                    1,
                    source_paths=[path],
                    fallback_to_unfiltered=False,
                )
            )

        seed_paths = list(lexical)
        for result in semantic:
            path = result.get("source_path")
            if path and path not in seed_paths:
                seed_paths.append(path)
            if len(seed_paths) >= 6:
                break

        relations: dict[str, list[str]] = defaultdict(list)
        for seed in seed_paths:
            per_seed_limit = graph_limit if seed in lexical else 4
            for item in self.graph.related(seed, depth=1, limit=per_seed_limit):
                reason = f"{item['relation']} from {item['from_path']}"
                if reason not in relations[item["source_path"]]:
                    relations[item["source_path"]].append(reason)

        related_paths = [path for path in relations if path not in seed_paths][: graph_limit * 2]
        related = []
        for path in related_paths:
            related.extend(
                self.store.search(
                    vector,
                    1,
                    source_paths=[path],
                    fallback_to_unfiltered=False,
                )
            )

        candidates: dict[tuple[str, str], dict[str, Any]] = {}
        for result in [*lexical_chunks, *semantic, *related]:
            path = str(result.get("source_path", ""))
            chunk_key = str(result.get("chunk_id") or result.get("chunk_index", ""))
            if not path:
                continue
            semantic_score = max(0.0, float(result.get("score", 0.0)))
            lexical_score = lexical.get(path, 0.0)
            graph_score = 0.25 if path in relations else 0.0
            category_score = (
                0.1
                if category and result.get("category") == category
                else 0.0
            )
            rank_score = semantic_score + lexical_score + graph_score + category_score
            item = {
                **result,
                "rank_score": round(rank_score, 6),
                "retrieval_kind": "primary" if path in seed_paths else "related",
                "relation_reason": relations.get(path, []),
                "lexical_score": lexical_score,
            }
            key = (path, chunk_key)
            if key not in candidates or item["rank_score"] > candidates[key]["rank_score"]:
                candidates[key] = item

        ranked = sorted(
            candidates.values(),
            key=lambda item: (
                item["retrieval_kind"] == "primary",
                item["rank_score"],
            ),
            reverse=True,
        )
        counts: dict[str, int] = defaultdict(int)
        output = []
        for item in ranked:
            path = item["source_path"]
            if counts[path] >= max(1, per_source):
                continue
            counts[path] += 1
            output.append(item)
            if len(output) >= max(1, limit):
                break
        return output
