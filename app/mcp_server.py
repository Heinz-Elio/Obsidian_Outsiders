from __future__ import annotations

import json
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, cast

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from mcp.server.fastmcp import FastMCP

from app.config import DEFAULT_CONFIG_PATH, Config, load_config
from app.context import assemble_evidence
from app.embedder import get_embedder
from app.graph import SourceGraph
from app.loader import load_documents
from app.model import Document
from app.retriever import HybridRetriever
from app.router import SCOPE_CATEGORIES, resolve_scope
from app.store import VectorStore, read_source


def _configure_stdio_logging() -> None:
    root = logging.getLogger()
    if not root.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
        root.addHandler(handler)
        root.setLevel(logging.WARNING)
    for name in ("httpx", "httpcore", "qdrant_client"):
        logging.getLogger(name).setLevel(logging.WARNING)


_configure_stdio_logging()


def _http_port_from_env() -> int:
    value = os.getenv("OBSIDIAN_RAG_PORT", "8000")
    try:
        port = int(value)
    except ValueError as exc:
        raise ValueError("OBSIDIAN_RAG_PORT must be an integer") from exc
    if not 1 <= port <= 65535:
        raise ValueError("OBSIDIAN_RAG_PORT must be between 1 and 65535")
    return port


@dataclass
class Runtime:
    config: Config
    embedder: object
    store: VectorStore
    documents: list[Document]
    graph: SourceGraph
    retriever: HybridRetriever


_runtime: Runtime | None = None
# One process, one transport. Cursor and Obsidian each spawn this module
# separately; both talk to the same Qdrant collection from config.yaml.
mcp = FastMCP(
    "obsidian-rag",
    host=os.getenv("OBSIDIAN_RAG_HOST", "127.0.0.1"),
    port=_http_port_from_env(),
    stateless_http=True,
)


def _transport_from_env() -> Literal["stdio", "sse", "streamable-http"]:
    value = os.getenv("OBSIDIAN_RAG_TRANSPORT", "stdio").strip().lower()
    aliases = {"http": "streamable-http", "streamable_http": "streamable-http"}
    value = aliases.get(value, value)
    if value not in {"stdio", "sse", "streamable-http"}:
        raise ValueError(
            "OBSIDIAN_RAG_TRANSPORT must be stdio, sse, or streamable-http"
        )
    return cast(Literal["stdio", "sse", "streamable-http"], value)


def _load_runtime() -> Runtime:
    global _runtime
    if _runtime is None:
        config = load_config(DEFAULT_CONFIG_PATH)
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
        _runtime = Runtime(
            config=config,
            embedder=embedder,
            store=store,
            documents=documents,
            graph=graph,
            retriever=HybridRetriever(documents, graph, store, embedder),
        )
    return _runtime


def _json_error(exc: Exception) -> str:
    return json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2)


@mcp.tool()
def search_knowledge(query: str, top_k: int | None = None) -> str:
    """Search the indexed vault and return source-cited passages."""
    try:
        runtime = _load_runtime()
        limit = max(1, min(top_k or runtime.config.retrieval.top_k, 20))
        results = runtime.store.search(runtime.embedder.embed_one(query), limit)
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as exc:
        return _json_error(exc)


@mcp.tool()
def query_knowledge(
    query: str,
    scope: str | None = None,
    entity: str | None = None,
    top_k: int | None = None,
) -> str:
    """Route a setting query to the most relevant category and return cited passages."""
    try:
        runtime = _load_runtime()
        selected_scope = resolve_scope(query, scope)
        search_query = f"{entity} {query}".strip() if entity else query
        limit = max(1, min(top_k or runtime.config.retrieval.top_k, 20))
        results = runtime.store.search(
            runtime.embedder.embed_one(search_query),
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
    except Exception as exc:
        return _json_error(exc)


@mcp.tool()
def retrieve_evidence(
    query: str,
    scope: str | None = None,
    entity: str | None = None,
    max_sources: int | None = None,
    token_budget: int | None = None,
) -> str:
    """Retrieve primary and related evidence with stable source citations."""
    try:
        runtime = _load_runtime()
        selected_scope = resolve_scope(query, scope)
        source_limit = max(1, min(max_sources or 8, 20))
        budget = max(256, min(token_budget or 4000, 12000))
        results = runtime.retriever.retrieve(
            query,
            scope=selected_scope,
            entity=entity,
            limit=max(12, source_limit * 2),
        )
        bundle = assemble_evidence(
            results,
            runtime.store,
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
    except Exception as exc:
        return _json_error(exc)


@mcp.tool()
def get_related_sources(path: str, depth: int = 1) -> str:
    """Return typed wikilink, backlink, and event relations for one source."""
    try:
        runtime = _load_runtime()
        resolved = runtime.graph.resolve(path)
        if resolved is None:
            return json.dumps(
                {"source_path": None, "error": "source or entity not uniquely resolved"},
                ensure_ascii=False,
                indent=2,
            )
        related = runtime.graph.related(resolved, depth=max(1, min(depth, 2)), limit=40)
        return json.dumps(
            {"source_path": resolved, "depth": depth, "related": related},
            ensure_ascii=False,
            indent=2,
        )
    except Exception as exc:
        return _json_error(exc)


@mcp.tool()
def get_document(path: str) -> str:
    """Read one Markdown source by its relative vault path."""
    try:
        return read_source(_load_runtime().config.vault.path, path)
    except Exception as exc:
        return _json_error(exc)


@mcp.tool()
def list_sources(folder: str = "") -> str:
    """List indexed Markdown source paths, optionally below a folder."""
    try:
        runtime = _load_runtime()
        prefix = folder.replace("\\", "/").strip("/")
        paths = []
        for document in runtime.documents:
            relative = document.path.as_posix()
            if not prefix or relative == prefix or relative.startswith(prefix + "/"):
                paths.append(relative)
        return json.dumps(paths, ensure_ascii=False, indent=2)
    except Exception as exc:
        return _json_error(exc)


if __name__ == "__main__":
    transport = _transport_from_env()
    print(f"obsidian-rag MCP transport={transport}", file=sys.stderr, flush=True)
    mcp.run(transport=transport)
