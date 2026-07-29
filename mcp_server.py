from __future__ import annotations

import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from app.config import load_config
from app.embedder import get_embedder
from app.loader import load_documents
from app.store import VectorStore, read_source


CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"
config = load_config(CONFIG_PATH)
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
mcp = FastMCP("obsidian-rag")


@mcp.tool()
def search_knowledge(query: str, top_k: int | None = None) -> str:
    """Search the indexed vault and return source-cited passages."""
    limit = max(1, min(top_k or config.retrieval.top_k, 20))
    results = store.search(embedder.embed_one(query), limit)
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def get_document(path: str) -> str:
    """Read one Markdown source by its relative vault path."""
    return read_source(config.vault.path, path)


@mcp.tool()
def list_sources(folder: str = "") -> str:
    """List indexed Markdown source paths, optionally below a folder."""
    prefix = folder.replace("\\", "/").strip("/")
    paths = []
    for document in load_documents(config.vault.path):
        relative = document.path.as_posix()
        if not prefix or relative == prefix or relative.startswith(prefix + "/"):
            paths.append(relative)
    return json.dumps(paths, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
