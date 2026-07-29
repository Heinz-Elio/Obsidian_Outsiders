from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable

from app.store import VectorStore


def _token_estimate(text: str) -> int:
    return max(1, (len(text) + 3) // 4)


def _citation(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_path": item.get("source_path"),
        "title": item.get("title"),
        "heading": item.get("heading"),
        "chunk_id": item.get("chunk_id"),
        "chunk_index": item.get("chunk_index"),
    }


def assemble_evidence(
    results: Iterable[dict[str, Any]],
    store: VectorStore,
    *,
    token_budget: int = 4000,
    max_sources: int = 8,
) -> dict[str, Any]:
    """Pack ranked chunks into a cited, source-diverse evidence bundle."""
    budget = max(256, token_budget)
    source_limit = max(1, max_sources)
    used_tokens = 0
    top_rank = 0.0
    has_exact_match = False
    used_sources: set[str] = set()
    used_chunks: set[tuple[str, object]] = set()
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for result in results:
        path = str(result.get("source_path", ""))
        if not path:
            continue
        if path not in used_sources and len(used_sources) >= source_limit:
            continue
        key = (path, result.get("chunk_id") or result.get("chunk_index"))
        if key in used_chunks:
            continue
        text = str(result.get("text", "")).strip()
        cost = _token_estimate(text)
        if used_tokens + cost > budget:
            continue
        kind = "primary" if result.get("retrieval_kind") == "primary" else "related"
        top_rank = max(top_rank, float(result.get("rank_score", result.get("score", 0.0))))
        has_exact_match = has_exact_match or float(result.get("lexical_score", 0.0)) > 0
        evidence = {
            "text": text,
            "citation": _citation(result),
            "rank_score": result.get("rank_score", result.get("score")),
            "relation_reason": result.get("relation_reason", []),
        }
        groups[kind].append(evidence)
        used_chunks.add(key)
        used_sources.add(path)
        used_tokens += cost

        index = result.get("chunk_index")
        heading = result.get("heading")
        if not isinstance(index, int):
            continue
        for neighbor in store.source_chunks(path):
            neighbor_index = neighbor.get("chunk_index")
            if neighbor_index not in (index - 1, index + 1):
                continue
            if heading and neighbor.get("heading") != heading:
                continue
            neighbor_key = (
                path,
                neighbor.get("chunk_id") or neighbor_index,
            )
            neighbor_text = str(neighbor.get("text", "")).strip()
            neighbor_cost = _token_estimate(neighbor_text)
            if neighbor_key in used_chunks or used_tokens + neighbor_cost > budget:
                continue
            groups[kind].append(
                {
                    "text": neighbor_text,
                    "citation": _citation(neighbor),
                    "rank_score": result.get("rank_score", result.get("score")),
                    "relation_reason": ["adjacent chunk"],
                }
            )
            used_chunks.add(neighbor_key)
            used_tokens += neighbor_cost

    if has_exact_match:
        confidence = "high"
    elif top_rank >= 0.5:
        confidence = "medium"
    else:
        confidence = "low"
    return {
        "primary": groups["primary"],
        "related": groups["related"],
        "sources_used": sorted(used_sources),
        "estimated_tokens": used_tokens,
        "token_budget": budget,
        "grounding_confidence": confidence,
        "answerability": "uncertain" if confidence == "low" else "supported",
    }
