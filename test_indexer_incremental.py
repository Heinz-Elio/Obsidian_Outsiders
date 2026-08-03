from pathlib import Path

from app.config import (
    ChunkConfig,
    Config,
    DatabaseConfig,
    EmbeddingConfig,
    RetrievalConfig,
    VaultConfig,
    WatcherConfig,
)
from app import indexer


class _FakeEmbedder:
    def __init__(self):
        self.embedded_texts = []

    def embed(self, texts):
        self.embedded_texts.extend(texts)
        return [[1.0, 0.0] for _ in texts]


class _FakeStore:
    sources = {}
    upsert_calls = 0
    reset_calls = 0
    exists = False

    def __init__(self, host, port, collection):
        self.collection = collection

    @classmethod
    def clear(cls):
        cls.sources = {}
        cls.upsert_calls = 0
        cls.reset_calls = 0
        cls.exists = False

    def collection_exists(self):
        return self.exists

    def reset_collection(self):
        type(self).sources = {}
        type(self).reset_calls += 1
        type(self).exists = False

    def delete_by_source_path(self, source_path):
        return len(type(self).sources.pop(source_path, []))

    def upsert(self, chunks, vectors):
        assert len(chunks) == len(vectors)
        type(self).upsert_calls += 1
        type(self).exists = True
        for chunk in chunks:
            type(self).sources.setdefault(chunk.source_path, []).append(chunk)


def _config(vault: Path, max_tokens: int = 500) -> Config:
    return Config(
        vault=VaultConfig(vault),
        embedding=EmbeddingConfig("fake", "fake-model"),
        chunking=ChunkConfig(max_tokens, 75),
        database=DatabaseConfig("localhost", 6333, "incremental_test"),
        retrieval=RetrievalConfig(5),
        watcher=WatcherConfig(True),
    )


def test_incremental_index_add_change_delete_and_skip(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    vault.mkdir()
    first = vault / "first.md"
    second = vault / "second.md"
    first.write_text("# First\nOriginal", encoding="utf-8")
    second.write_text("# Second\nOriginal", encoding="utf-8")

    config_holder = [_config(vault)]
    embedder = _FakeEmbedder()
    manifest = tmp_path / "manifest.json"
    _FakeStore.clear()
    monkeypatch.setattr(indexer, "load_config", lambda _path=None: config_holder[0])
    monkeypatch.setattr(indexer, "get_embedder", lambda *_args: embedder)
    monkeypatch.setattr(indexer, "VectorStore", _FakeStore)
    monkeypatch.setattr(indexer, "manifest_path", lambda _collection: manifest)

    documents, chunks = indexer.build_index()
    assert (documents, chunks) == (2, 2)
    assert len(embedder.embedded_texts) == 2
    assert _FakeStore.upsert_calls == 2

    documents, chunks = indexer.build_index()
    assert (documents, chunks) == (2, 0)
    assert len(embedder.embedded_texts) == 2
    assert _FakeStore.upsert_calls == 2

    first.write_text("# First\nChanged", encoding="utf-8")
    documents, chunks = indexer.build_index()
    assert (documents, chunks) == (2, 1)
    assert len(embedder.embedded_texts) == 3
    assert _FakeStore.upsert_calls == 3
    assert "Changed" in _FakeStore.sources["first.md"][0].text

    third = vault / "third.md"
    third.write_text("# Third\nNew", encoding="utf-8")
    documents, chunks = indexer.build_index()
    assert (documents, chunks) == (3, 1)
    assert set(_FakeStore.sources) == {"first.md", "second.md", "third.md"}

    second.unlink()
    documents, chunks = indexer.build_index()
    assert (documents, chunks) == (2, 0)
    assert set(_FakeStore.sources) == {"first.md", "third.md"}

    config_holder[0] = _config(vault, max_tokens=400)
    embedded_before = len(embedder.embedded_texts)
    documents, chunks = indexer.build_index()
    assert (documents, chunks) == (2, 2)
    assert len(embedder.embedded_texts) == embedded_before + 2
    assert _FakeStore.reset_calls == 2


def test_limit_documents_does_not_write_manifest_or_delete_sources(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "first.md").write_text("# First\nText", encoding="utf-8")
    (vault / "second.md").write_text("# Second\nText", encoding="utf-8")

    embedder = _FakeEmbedder()
    manifest = tmp_path / "manifest.json"
    _FakeStore.clear()
    _FakeStore.sources = {"unrelated.md": [object()]}
    _FakeStore.exists = True
    monkeypatch.setattr(indexer, "load_config", lambda _path=None: _config(vault))
    monkeypatch.setattr(indexer, "get_embedder", lambda *_args: embedder)
    monkeypatch.setattr(indexer, "VectorStore", _FakeStore)
    monkeypatch.setattr(indexer, "manifest_path", lambda _collection: manifest)

    documents, chunks = indexer.build_index(limit_documents=1)

    assert (documents, chunks) == (1, 1)
    assert "unrelated.md" in _FakeStore.sources
    assert not manifest.exists()
