from __future__ import annotations

import argparse
import json
import sys

from app.embedder import FakeEmbedder, get_embedder
from app.indexer import build_index
from app.store import VectorStore
from app.config import load_config


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    parser = argparse.ArgumentParser(
        description="Small embedding smoke test (fake embeddings by default)."
    )
    parser.add_argument("--config", default="config.test.yaml")
    parser.add_argument("--limit-documents", type=int, default=5)
    parser.add_argument("--query", default="星降神臨")
    args = parser.parse_args()

    fake = FakeEmbedder()
    sample = fake.embed_one("small test 星降神臨")
    print(f"fake_embed_ok dims={len(sample)}")

    documents, chunks = build_index(
        args.config,
        limit_documents=args.limit_documents,
    )
    print(f"indexed documents={documents} chunks={chunks}")

    config = load_config(args.config)
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
    results = store.search(embedder.embed_one(args.query), config.retrieval.top_k)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"search_hits={len(results)}")


if __name__ == "__main__":
    main()
