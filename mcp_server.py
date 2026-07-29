from __future__ import annotations

import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from app.config import load_config
from app.context import assemble_evidence
from app.embedder import get_embedder
from app.graph import SourceGraph
from app.loader import load_documents
from app.retriever import HybridRetriever
from app.router import SCOPE_CATEGORIES, resolve_scope
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
documents = list(load_documents(config.vault.path))
graph = SourceGraph(documents)
retriever = HybridRetriever(documents, graph, store, embedder)
mcp = FastMCP("obsidian-rag")

@mcp.tool()
def search_knowledge(query: str, top_k: int | None = None) -> str:
    """Search the indexed vault and return source-cited passages."""
    limit = max(1, min(top_k or config.retrieval.top_k, 20))
    results = store.search(embedder.embed_one(query), limit)
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def query_knowledge(
    query: str,
    scope: str | None = None,
    entity: str | None = None,
    top_k: int | None = None,
) -> str:
    """Route a setting query to the most relevant category and return cited passages."""
    selected_scope = resolve_scope(query, scope)
    search_query = f"{entity} {query}".strip() if entity else query
    limit = max(1, min(top_k or config.retrieval.top_k, 20))
    results = store.search(
        embedder.embed_one(search_query),
        limit,
        category=SCOPE_CATEGORIES.get(selected_scope),
    )
    return json.dumps(
        {
            "scope_used": selected_scope or "all",
            "scope_requested": scope,
            "entity": entity,
            "results": results,
        },
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def retrieve_evidence(
    query: str,
    scope: str | None = None,
    entity: str | None = None,
    max_sources: int | None = None,
    token_budget: int | None = None,
) -> str:
    """Retrieve primary and related evidence with stable source citations."""
    selected_scope = resolve_scope(query, scope)
    source_limit = max(1, min(max_sources or 8, 20))
    budget = max(256, min(token_budget or 4000, 12000))
    results = retriever.retrieve(
        query,
        scope=selected_scope,
        entity=entity,
        limit=max(12, source_limit * 2),
    )
    bundle = assemble_evidence(
        results,
        store,
        token_budget=budget,
        max_sources=source_limit,
    )
    bundle.update(
        {
            "query": query,
            "entity": entity,
            "scope_used": selected_scope or "all",
            "scope_requested": scope,
        }
    )
    return json.dumps(bundle, ensure_ascii=False, indent=2)


@mcp.tool()
def get_related_sources(path: str, depth: int = 1) -> str:
    """Return typed wikilink, backlink, and event relations for one source."""
    resolved = graph.resolve(path)
    if resolved is None:
        return json.dumps(
            {"source_path": None, "error": "source or entity not uniquely resolved"},
            ensure_ascii=False,
            indent=2,
        )
    related = graph.related(resolved, depth=max(1, min(depth, 2)), limit=40)
    return json.dumps(
        {"source_path": resolved, "depth": depth, "related": related},
        ensure_ascii=False,
        indent=2,
    )


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
