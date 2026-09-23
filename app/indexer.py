from __future__ import annotations

import argparse
from pathlib import Path

from app.chunker import chunk_document
from app.config import load_config
from app.embedder import get_embedder
from app.loader import load_document, source_paths
from app.manifest import (
    empty_manifest,
    is_compatible,
    load_manifest,
    manifest_path,
    save_manifest,
    source_hash,
)
from app.store import VectorStore
from app.outline_converter import OUTPUT_SUBDIR, convert_workbook, write_documents


def _refresh_outline_sources(vault: Path) -> None:
    source = vault / "大綱及行動.xlsx"
    if not source.exists():
        return

    output = vault / OUTPUT_SUBDIR
    documents = convert_workbook(source)
    unchanged = write_documents(documents, output)
    status = "unchanged" if unchanged else "updated"
    print(f"{status} generated outline sources={len(documents)}")


def _upsert_chunks(store, embedder, chunks) -> None:
    batch_size = 16
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        store.upsert(batch, embedder.embed([chunk.text for chunk in batch]))


def build_index(
    config_path: str | None = None,
    *,
    limit_documents: int | None = None,
    full: bool = False,
) -> tuple[int, int]:
    config = load_config(config_path)
    _refresh_outline_sources(config.vault.path)
    paths = list(source_paths(config.vault.path))
    if limit_documents is not None:
        paths = paths[: max(0, limit_documents)]

    store = VectorStore(
        config.database.host,
        config.database.port,
        config.database.collection,
    )

    if limit_documents is not None:
        embedder = get_embedder(
            config.embedding.provider,
            config.embedding.model,
            config.embedding.num_gpu,
        )
        chunks = []
        for path in paths:
            chunks.extend(
                chunk_document(
                    load_document(config.vault.path, path),
                    config.chunking.max_tokens,
                    config.chunking.overlap,
                )
            )
        _upsert_chunks(store, embedder, chunks)
        return len(paths), len(chunks)

    state_path = manifest_path(config.database.collection)
    manifest = load_manifest(state_path)
    manifest_sources = manifest.get("sources") if manifest else None
    needs_full_rebuild = (
        full
        or manifest is None
        or not isinstance(manifest_sources, dict)
        or not is_compatible(manifest, config)
        or not store.collection_exists()
    )
    if needs_full_rebuild:
        store.reset_collection()
        manifest = empty_manifest(config)
        manifest_sources = manifest["sources"]
        print("performing full index rebuild")

    current: dict[str, tuple[Path, str]] = {}
    for path in paths:
        relative = path.relative_to(config.vault.path).as_posix()
        current[relative] = (path, source_hash(path))

    deleted_paths = sorted(set(manifest_sources) - set(current))
    changed_paths = [
        relative
        for relative, (_, digest) in current.items()
        if manifest_sources.get(relative, {}).get("content_hash") != digest
    ]

    for relative in deleted_paths:
        deleted = store.delete_by_source_path(relative)
        manifest_sources.pop(relative, None)
        print(f"removed source={relative} chunks={deleted}")

    embedder = None
    indexed_chunks = 0
    for position, relative in enumerate(changed_paths, start=1):
        path, digest = current[relative]
        document = load_document(config.vault.path, path)
        chunks = chunk_document(
            document,
            config.chunking.max_tokens,
            config.chunking.overlap,
        )
        if chunks and embedder is None:
            embedder = get_embedder(
                config.embedding.provider,
                config.embedding.model,
                config.embedding.num_gpu,
            )
        vectors = embedder.embed([chunk.text for chunk in chunks]) if chunks else []
        deleted = store.delete_by_source_path(relative)
        if chunks:
            store.upsert(chunks, vectors)
        manifest_sources[relative] = {
            "source_id": document.source_id,
            "content_hash": digest,
            "chunk_ids": [chunk.id for chunk in chunks],
        }
        indexed_chunks += len(chunks)
        print(
            f"indexed source {position}/{len(changed_paths)}={relative} "
            f"chunks={len(chunks)} replaced={deleted}"
        )

    save_manifest(state_path, manifest)
    print(
        f"scan complete sources={len(paths)} changed={len(changed_paths)} "
        f"deleted={len(deleted_paths)} unchanged={len(paths) - len(changed_paths)}"
    )
    return len(paths), indexed_chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Index the Obsidian vault into Qdrant.")
    parser.add_argument("--config", default=None)
    parser.add_argument(
        "--limit-documents",
        type=int,
        default=None,
        help="Index only the first N documents (useful for smoke tests).",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Discard the existing collection and rebuild every source.",
    )
    args = parser.parse_args()
    documents, chunks = build_index(
        args.config,
        limit_documents=args.limit_documents,
        full=args.full,
    )
    print(f"scanned {documents} documents and indexed {chunks} chunks")


if __name__ == "__main__":
    main()
