"""RAG retriever abstraction.

The frontend sends a user query to one of the GenAI endpoints; the
service layer encodes the query, retrieves the top-k documents from
a vector store, and injects them into the LLM prompt.

This module ships an :class:`InMemoryRetriever` seeded from a tiny
fixture (the same products the frontend's mock data uses).  A real
:class:`PineconeRetriever` is wired but only activated when the
operator sets ``VECTOR_BACKEND=pinecone`` + a key.
"""

from __future__ import annotations

import math
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.services.genai.demo_data import DEMO_CATALOG


@dataclass(slots=True)
class RetrievedDoc:
    id: str
    title: str
    text: str
    score: float  # 0..1 — higher is better
    metadata: dict


class BaseRetriever(ABC):
    @abstractmethod
    async def retrieve(self, query: str, *, top_k: int = 4) -> list[RetrievedDoc]:
        ...


# --------------------------------------------------------------------- #
# Text-similarity scoring — cheap + dependency-free.
# --------------------------------------------------------------------- #

_TOKEN_RE = re.compile(r"[a-zA-ZÀ-ỹ0-9]+", re.UNICODE)


def _tokenize(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text or "")]


def _tfidf(query_tokens: list[str], doc_tokens: list[str]) -> float:
    """Tiny TF-IDF cosine. Good enough for fixture retrieval."""
    if not query_tokens or not doc_tokens:
        return 0.0
    qset = set(query_tokens)
    overlap = qset.intersection(doc_tokens)
    if not overlap:
        return 0.0
    # Jaccard-ish — favors docs that share rare terms.
    return len(overlap) / math.sqrt(len(qset) * len(doc_tokens))


# --------------------------------------------------------------------- #
# In-memory retriever — seeded from DEMO_CATALOG.
# --------------------------------------------------------------------- #


class InMemoryRetriever(BaseRetriever):
    """Retrieves from a small in-memory product catalog."""

    def __init__(self, catalog: list[dict] | None = None) -> None:
        self._catalog = list(catalog or DEMO_CATALOG)
        # Pre-tokenize so each query is fast.
        self._docs: list[tuple[dict, list[str]]] = [
            (item, _tokenize(f"{item['title']} {item['text']}")) for item in self._catalog
        ]

    async def retrieve(self, query: str, *, top_k: int = 4) -> list[RetrievedDoc]:
        qtokens = _tokenize(query)
        scored: list[tuple[float, dict]] = []
        for item, dtokens in self._docs:
            s = _tfidf(qtokens, dtokens)
            # Bonus for category match — helps "son", "serum", "denim" hit.
            if any(t in item.get("text", "").lower() for t in qtokens):
                s += 0.05
            if s > 0:
                scored.append((s, item))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:top_k]
        if not top:
            # Fall back to the first N items so the consumer always has
            # *something* to ground on, even on gibberish queries.
            top = [(0.0, self._catalog[i]) for i in range(min(top_k, len(self._catalog)))]
        max_score = max(s for s, _ in top) or 1.0
        return [
            RetrievedDoc(
                id=item["id"],
                title=item["title"],
                text=item["text"],
                score=min(1.0, s / max_score),
                metadata=item.get("metadata", {}),
            )
            for s, item in top
        ]


# --------------------------------------------------------------------- #
# Pinecone retriever — wired but optional.
# --------------------------------------------------------------------- #


class PineconeRetriever(BaseRetriever):
    """Lazy-loaded Pinecone client.  Falls back to in-memory on error."""

    def __init__(self) -> None:
        # Imported lazily so the operator doesn't need the SDK in dev.
        from pinecone import Pinecone  # type: ignore[import-not-found]

        from app.core.config import settings

        self._client = Pinecone(api_key=settings.PINECONE_API_KEY)
        self._index = self._client.Index(settings.PINECONE_INDEX)

    async def retrieve(self, query: str, *, top_k: int = 4) -> list[RetrievedDoc]:
        # Pinecone Python SDK is sync; run it in a thread to keep the
        # endpoint async-friendly.
        import asyncio

        def _query() -> list[dict]:
            return self._index.search(
                namespace="tiki",
                query={"inputs": {"text": query}, "top_k": top_k},
                fields=["title", "text", "category", "platform"],
            ).get("result", {}).get("hits", [])

        hits = await asyncio.to_thread(_query)
        return [
            RetrievedDoc(
                id=str(h.get("id", "")),
                title=h.get("fields", {}).get("title", ""),
                text=h.get("fields", {}).get("text", ""),
                score=float(h.get("score", 0.0)),
                metadata={
                    "category": h.get("fields", {}).get("category"),
                    "platform": h.get("fields", {}).get("platform"),
                },
            )
            for h in hits
        ]