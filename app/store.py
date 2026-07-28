from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

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
                        "source_path": chunk.source_path,
                        "title": chunk.title,
                        "heading": chunk.heading,
                        "text": chunk.text,
                        "chunk_index": chunk.chunk_index,
                        "tags": chunk.tags,
                        "modified": chunk.modified,
                    },
                )
            )
        self.client.upsert(collection_name=self.collection, points=points)

    def search(self, vector: list[float], limit: int) -> list[dict[str, Any]]:
        if hasattr(self.client, "query_points"):
            result = self.client.query_points(
                collection_name=self.collection,
                query=vector,
                limit=limit,
                with_payload=True,
            )
            points = result.points
        else:
            points = self.client.search(
                collection_name=self.collection,
                query_vector=vector,
                limit=limit,
                with_payload=True,
            )
        return [
            {
                "score": point.score,
                **(point.payload or {}),
            }
            for point in points
        ]


def read_source(root: Path, relative_path: str) -> str:
    root = root.resolve()
    path = (root / relative_path).resolve()
    if root not in path.parents and path != root:
        raise ValueError("source path escapes the configured vault")
    return path.read_text(encoding="utf-8")
