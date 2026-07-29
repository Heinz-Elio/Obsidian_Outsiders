from __future__ import annotations

import hashlib
import math
import re
from collections.abc import Sequence


TOKEN = re.compile(r"[\w\u4e00-\u9fff]+", re.UNICODE)


class OllamaEmbedder:
    def __init__(self, model: str, num_gpu: int | None = None):
        self.model = model
        self.num_gpu = num_gpu

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []
        import ollama

        kwargs: dict = {"model": self.model, "input": list(texts)}
        if self.num_gpu is not None:
            kwargs["options"] = {"num_gpu": self.num_gpu}
        response = ollama.embed(**kwargs)
        embeddings = response["embeddings"] if isinstance(response, dict) else response.embeddings
        return [list(vector) for vector in embeddings]

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]


class FakeEmbedder:
    """Deterministic bag-of-tokens embeddings for local smoke tests without Ollama."""

    def __init__(self, dims: int = 768):
        self.dims = dims

    def _vector(self, text: str) -> list[float]:
        values = [0.0] * self.dims
        tokens = TOKEN.findall(text.lower())
        if not tokens:
            tokens = ["empty"]
        for token in tokens:
            digest = hashlib.sha1(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "little") % self.dims
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            values[index] += sign
        norm = math.sqrt(sum(value * value for value in values)) or 1.0
        return [value / norm for value in values]

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._vector(text) for text in texts]

    def embed_one(self, text: str) -> list[float]:
        return self._vector(text)


def get_embedder(provider: str, model: str, num_gpu: int | None = None):
    provider = (provider or "ollama").lower()
    if provider == "fake":
        return FakeEmbedder()
    if provider == "ollama":
        return OllamaEmbedder(model, num_gpu=num_gpu)
    raise ValueError(f"unsupported embedding provider: {provider}")
