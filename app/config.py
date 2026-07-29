from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config.yaml"


@dataclass
class VaultConfig:
    path: Path


@dataclass
class EmbeddingConfig:
    provider: str
    model: str
    num_gpu: int | None = None


@dataclass
class ChunkConfig:
    max_tokens: int
    overlap: int


@dataclass
class DatabaseConfig:
    host: str
    port: int
    collection: str


@dataclass
class RetrievalConfig:
    top_k: int


@dataclass
class WatcherConfig:
    recursive: bool


@dataclass
class Config:
    vault: VaultConfig
    embedding: EmbeddingConfig
    chunking: ChunkConfig
    database: DatabaseConfig
    retrieval: RetrievalConfig
    watcher: WatcherConfig


def resolve_config_path(path: str | Path | None = None) -> Path:
    """Resolve config.yaml against cwd first, then the project root."""
    if path is None:
        return DEFAULT_CONFIG_PATH

    config_path = Path(path)
    if config_path.is_absolute():
        return config_path.resolve()

    cwd_candidate = (Path.cwd() / config_path).resolve()
    if cwd_candidate.exists():
        return cwd_candidate

    return (PROJECT_ROOT / config_path).resolve()


def load_config(path: str | Path | None = None) -> Config:
    config_path = resolve_config_path(path)
    with config_path.open(encoding="utf8") as f:
        raw = yaml.safe_load(f)

    vault = raw.get("vault", {})
    vault_path = vault.get("path", raw.get("vault_path", "."))
    vault_path = Path(vault_path)
    if not vault_path.is_absolute():
        vault_path = (config_path.parent / vault_path).resolve()

    return Config(
        vault=VaultConfig(vault_path),
        embedding=EmbeddingConfig(
            raw["embedding"]["provider"],
            raw["embedding"]["model"],
            raw["embedding"].get("num_gpu"),
        ),
        chunking=ChunkConfig(
            raw["chunking"]["max_tokens"],
            raw["chunking"]["overlap"],
        ),
        database=DatabaseConfig(
            raw["database"]["host"],
            raw["database"]["port"],
            raw["database"]["collection"],
        ),
        retrieval=RetrievalConfig(raw["retrieval"]["top_k"]),
        watcher=WatcherConfig(raw["watcher"]["recursive"]),
    )
