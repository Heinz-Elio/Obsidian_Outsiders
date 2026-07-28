from __future__ import annotations

from collections.abc import Sequence

import ollama


class OllamaEmbedder:
    def __init__(self, model: str):
        self.model = model

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []
        response = ollama.embed(model=self.model, input=list(texts))
        embeddings = response["embeddings"] if isinstance(response, dict) else response.embeddings
        return [list(vector) for vector in embeddings]

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]
