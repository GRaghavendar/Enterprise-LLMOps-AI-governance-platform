"""Small TF-IDF retriever implemented with the standard library."""

from __future__ import annotations

import math
from collections import Counter

from llmops_governance.schemas.evaluation import SourceChunk
from llmops_governance.utils import cosine_from_counts, tokenize


class TfidfRetriever:
    """A deterministic local retriever for offline demos and tests."""

    def __init__(self, chunks: list[SourceChunk]):
        self.chunks = chunks
        self._idf = self._compute_idf(chunks)
        self._chunk_vectors = [self._vectorize(chunk.text) for chunk in chunks]

    def retrieve(self, query: str, top_k: int = 3) -> list[SourceChunk]:
        query_vector = self._vectorize(query)
        scored: list[SourceChunk] = []
        for chunk, vector in zip(self.chunks, self._chunk_vectors):
            score = cosine_from_counts(query_vector, vector)
            scored.append(
                SourceChunk(
                    chunk_id=chunk.chunk_id,
                    source_document=chunk.source_document,
                    text=chunk.text,
                    similarity_score=round(score, 4),
                )
            )
        return sorted(scored, key=lambda item: item.similarity_score, reverse=True)[:top_k]

    def _compute_idf(self, chunks: list[SourceChunk]) -> dict[str, float]:
        document_count = max(len(chunks), 1)
        document_frequency: Counter[str] = Counter()
        for chunk in chunks:
            document_frequency.update(set(tokenize(chunk.text)))
        return {
            token: math.log((1 + document_count) / (1 + frequency)) + 1
            for token, frequency in document_frequency.items()
        }

    def _vectorize(self, text: str) -> dict[str, float]:
        counts = Counter(tokenize(text))
        if not counts:
            return {}
        max_count = max(counts.values())
        return {token: (count / max_count) * self._idf.get(token, 1.0) for token, count in counts.items()}

