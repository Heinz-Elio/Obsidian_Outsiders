from __future__ import annotations

import argparse
from pathlib import Path

from app.chunker import chunk_document
from app.config import load_config
from app.embedder import get_embedder
from app.loader import load_documents
from app.store import VectorStore


def build_index(
    config_path: str | None = None,
    *,
    limit_documents: int | None = None,
) -> tuple[int, int]:
    config = load_config(config_path)
    documents = list(load_documents(config.vault.path))
    if limit_documents is not None:
        documents = documents[: max(0, limit_documents)]
    chunks = []
    for document in documents:
        chunks.extend(
            chunk_document(
                document,
                config.chunking.max_tokens,
                config.chunking.overlap,
            )
        )

    embedder = get_embedder(
        config.embedding.provider,
        config.embedding.model,
        config.embedding.num_gpu,
    )
    store = VectorStore(
        config.database.host,
        config.database.port,
        config.database.collection,
    )
    batch_size = 16
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        store.upsert(batch, embedder.embed([chunk.text for chunk in batch]))
        print(f"indexed {min(start + batch_size, len(chunks))}/{len(chunks)} chunks")
    return len(documents), len(chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Index the Obsidian vault into Qdrant.")
    parser.add_argument("--config", default=None)
    parser.add_argument(
        "--limit-documents",
        type=int,
        default=None,
        help="Index only the first N documents (useful for smoke tests).",
    )
    args = parser.parse_args()
    documents, chunks = build_index(
        args.config,
        limit_documents=args.limit_documents,
    )
    print(f"indexed {documents} documents and {chunks} chunks")


if __name__ == "__main__":
    main()
