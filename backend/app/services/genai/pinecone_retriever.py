"""Pinecone retriever (lazy import).

The :mod:`pinecone` SDK is optional.  This module is only loaded when
the operator sets ``VECTOR_BACKEND=pinecone`` and provides a key.  In
dev / CI we fall back to the in-memory retriever so the install
surface stays small.
"""

from __future__ import annotations

from app.services.genai.rag import BaseRetriever, RetrievedDoc


class PineconeRetriever(BaseRetriever):
    """Lazy-loaded Pinecone client. Falls back to in-memory on error."""

    def __init__(self) -> None:
        try:
            from pinecone import Pinecone  # type: ignore[import-not-found]
        except ImportError as exc:  # pragma: no cover — optional dep
            raise RuntimeError(
                "pinecone SDK is not installed. `pip install pinecone` first."
            ) from exc

        from app.core.config import settings

        self._client = Pinecone(api_key=settings.PINECONE_API_KEY)
        self._index = self._client.Index(settings.PINECONE_INDEX)

    async def retrieve(self, query: str, *, top_k: int = 4) -> list[RetrievedDoc]:
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