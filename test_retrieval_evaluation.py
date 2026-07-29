import json
from pathlib import Path

from app.config import load_config
from app.context import assemble_evidence
from app.embedder import get_embedder
from app.graph import SourceGraph
from app.indexer import build_index
from app.loader import load_documents
from app.retriever import HybridRetriever
from app.store import VectorStore


def _retriever() -> HybridRetriever:
    config = load_config("config.test.yaml")
    documents = list(load_documents(config.vault.path))
    return HybridRetriever(
        documents,
        SourceGraph(documents),
        VectorStore(
            config.database.host,
            config.database.port,
            config.database.collection,
        ),
        get_embedder(
            config.embedding.provider,
            config.embedding.model,
            config.embedding.num_gpu,
        ),
    )


def test_cross_source_retrieval_recall():
    build_index("config.test.yaml")
    retriever = _retriever()
    cases = json.loads(
        Path("retrieval_eval_cases.json").read_text(encoding="utf-8")
    )
    for case in cases:
        results = retriever.retrieve(
            case["query"],
            entity=case.get("entity"),
            limit=24,
        )
        actual = {result["source_path"] for result in results}
        expected = set(case["expected_sources"])
        recall = len(actual.intersection(expected)) / len(expected)
        assert recall >= case["minimum_recall"], (
            case["name"],
            recall,
            sorted(expected - actual),
        )
        bundle = assemble_evidence(
            results,
            retriever.store,
            token_budget=3000,
            max_sources=8,
        )
        evidence = bundle["primary"] + bundle["related"]
        assert evidence
        assert bundle["estimated_tokens"] <= bundle["token_budget"]
        assert all(item["citation"]["chunk_id"] for item in evidence)


def test_graph_relations_include_event_sequence():
    config = load_config()
    graph = SourceGraph(load_documents(config.vault.path))
    related = graph.related("海都事件", depth=1, limit=40)
    assert any(
        item["source_path"].endswith("埃爾確解封.md")
        and item["relation"] == "event_prev"
        for item in related
    )
