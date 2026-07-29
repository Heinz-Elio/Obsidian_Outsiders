from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchAny,
    MatchText,
    MatchValue,
    PointIdsList,
    PointStruct,
    VectorParams,
)

from app.model import Chunk


class VectorStore:
    def __init__(self, host: str, port: int, collection: str):
        self.collection = collection
        self.client = QdrantClient(host=host, port=port)

    def ensure_collection(self, vector_size: int) -> None:
        if self.client.collection_exists(self.collection):
            return
        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    def upsert(self, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        if not chunks:
            return
        self.ensure_collection(len(vectors[0]))
        points = []
        for chunk, vector in zip(chunks, vectors):
            points.append(
                PointStruct(
                    id=str(uuid.UUID(hex=chunk.id[:32])),
                    vector=vector,
                    payload={
                        "chunk_id": chunk.id,
                        "source_path": chunk.source_path,
                        "title": chunk.title,
                        "heading": chunk.heading,
                        "text": chunk.text,
                        "chunk_index": chunk.chunk_index,
                        "tags": chunk.tags,
                        "modified": chunk.modified,
                        "category": chunk.category,
                        "metadata": chunk.metadata,
                        "source_id": chunk.source_id,
                        "aliases": chunk.aliases,
                        "links": chunk.links,
                        "relation_tags": chunk.relation_tags,
                    },
                )
            )
        self.client.upsert(collection_name=self.collection, points=points)

    def sync_sources(self, active_point_ids: set[str]) -> int:
        """Delete points no longer produced by the current full index build."""
        if not self.client.collection_exists(self.collection):
            return 0
        stale = []
        offset = None
        while True:
            records, offset = self.client.scroll(
                collection_name=self.collection,
                limit=256,
                offset=offset,
                with_payload=False,
                with_vectors=False,
            )
            stale.extend(str(record.id) for record in records if str(record.id) not in active_point_ids)
            if offset is None:
                break
        if stale:
            self.client.delete(
                collection_name=self.collection,
                points_selector=PointIdsList(points=stale),
                wait=True,
            )
        return len(stale)

    def search(
        self,
        vector: list[float],
        limit: int,
        *,
        category: str | None = None,
        source_prefix: str | None = None,
        source_paths: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        fallback_to_unfiltered: bool = True,
    ) -> list[dict[str, Any]]:
        query_filter = self._build_filter(category, source_prefix, metadata, source_paths)

        points = self._search_points(vector, limit, query_filter)
        if not points and query_filter is not None and fallback_to_unfiltered:
            points = self._search_points(vector, limit, None)

        return [
            {
                "score": point.score,
                **(point.payload or {}),
            }
            for point in points
        ]

    @staticmethod
    def _build_filter(
        category: str | None,
        source_prefix: str | None,
        metadata: dict[str, Any] | None,
        source_paths: list[str] | None = None,
    ) -> Filter | None:
        conditions = []
        if category:
            conditions.append(FieldCondition(key="category", match=MatchValue(value=category)))
        if source_prefix:
            conditions.append(
                FieldCondition(
                    key="source_path",
                    match=MatchText(text=source_prefix.replace("\\", "/").strip("/")),
                )
            )
        if source_paths:
            conditions.append(
                FieldCondition(
                    key="source_path",
                    match=MatchAny(any=source_paths),
                )
            )
        for key, value in (metadata or {}).items():
            if value is not None:
                conditions.append(
                    FieldCondition(
                        key=f"metadata.{key}",
                        match=MatchValue(value=value),
                    )
                )
        return Filter(must=conditions) if conditions else None

    def source_chunks(self, source_path: str) -> list[dict[str, Any]]:
        """Return all stored chunks for one source in document order."""
        records = []
        offset = None
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="source_path",
                    match=MatchValue(value=source_path),
                )
            ]
        )
        while True:
            batch, offset = self.client.scroll(
                collection_name=self.collection,
                scroll_filter=query_filter,
                limit=128,
                offset=offset,
                with_payload=True,
                with_vectors=False,
            )
            records.extend(
                {"id": str(record.id), **(record.payload or {})}
                for record in batch
            )
            if offset is None:
                break
        return sorted(records, key=lambda item: item.get("chunk_index", 0))

    def _search_points(self, vector: list[float], limit: int, query_filter: Filter | None):
        if hasattr(self.client, "query_points"):
            result = self.client.query_points(
                collection_name=self.collection,
                query=vector,
                limit=limit,
                with_payload=True,
                query_filter=query_filter,
            )
            return result.points
        else:
            return self.client.search(
                collection_name=self.collection,
                query_vector=vector,
                limit=limit,
                with_payload=True,
                query_filter=query_filter,
            )


def read_source(root: Path, relative_path: str) -> str:
    root = root.resolve()
    path = (root / relative_path).resolve()
    if root not in path.parents and path != root:
        raise ValueError("source path escapes the configured vault")
    return path.read_text(encoding="utf-8")
