from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from app.config import PROJECT_ROOT, Config


INDEX_SCHEMA_VERSION = 1


def manifest_path(collection: str) -> Path:
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", collection).strip("._") or "default"
    return PROJECT_ROOT / "qdrant_storage" / f"index_manifest_{safe_name}.json"


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def index_signature(config: Config) -> dict[str, Any]:
    return {
        "schema_version": INDEX_SCHEMA_VERSION,
        "embedding": {
            "provider": config.embedding.provider,
            "model": config.embedding.model,
        },
        "chunking": {
            "max_tokens": config.chunking.max_tokens,
            "overlap": config.chunking.overlap,
        },
    }


def empty_manifest(config: Config) -> dict[str, Any]:
    return {
        **index_signature(config),
        "sources": {},
    }


def load_manifest(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def is_compatible(manifest: dict[str, Any], config: Config) -> bool:
    expected = index_signature(config)
    return all(manifest.get(key) == value for key, value in expected.items())


def save_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)
