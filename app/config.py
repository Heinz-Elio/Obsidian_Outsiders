from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass
class VaultConfig:
    path: Path

@dataclass
class EmbeddingConfig:
    provider: str
    model: str

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


def load_config(path="config.yaml") -> Config:

    with open(path, encoding="utf8") as f:
        raw = yaml.safe_load(f)

    return Config(vault=VaultConfig(Path(raw["vault"]["path"])),
                    embedding=EmbeddingConfig(raw["embedding"]["provider"],
                                              raw["embedding"]["model"],),
                    chunking=ChunkConfig(raw["chunking"]["max_tokens"],
                                         raw["chunking"]["overlap"],),
                    database=DatabaseConfig(raw["database"]["host"],
                                            raw["database"]["port"],
                                            raw["database"]["collection"],),
                    retrieval=RetrievalConfig(raw["retrieval"]["top_k"]),
                    watcher=WatcherConfig(raw["watcher"]["recursive"]),
    )