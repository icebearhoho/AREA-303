"""Shared GenAI utilities — LLM clients, RAG, caching, prompts.

Public surface (re-exported from :mod:`app.services.genai`):

* :class:`LlmClient` — async streaming chat interface
* :func:`get_llm_client` — factory keyed off settings.LLM_PROVIDER
* :func:`get_rag` — retrieval helper (Pinecone / FAISS / in-memory)
* :func:`llm_cache` — Redis-backed decorator w/ TTL

The :class:`MockLlmClient` is wired when ``DEMO_MODE=true`` or
``LLM_PROVIDER=mock``. This is the safety net the project plan requires:
demo mode must always succeed even with no API keys / no quota.
"""

from __future__ import annotations

from app.services.genai.base import (
    ChatChunk,
    LlmClient,
    LlmMessage,
    LlmResponse,
)
from app.services.genai.cache import llm_cache
from app.services.genai.factory import get_llm_client, get_rag
from app.services.genai.prompts import (
    CONTENT_GENERATOR_PROMPT,
    PERSONAL_SHOPPER_SYSTEM,
    RECSYS_REASONING_PROMPT,
    SELLER_COACH_SYSTEM,
)

__all__ = [
    "LlmClient",
    "LlmMessage",
    "LlmResponse",
    "ChatChunk",
    "get_llm_client",
    "get_rag",
    "llm_cache",
    "PERSONAL_SHOPPER_SYSTEM",
    "CONTENT_GENERATOR_PROMPT",
    "RECSYS_REASONING_PROMPT",
    "SELLER_COACH_SYSTEM",
]