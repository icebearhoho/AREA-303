"""LLM client interface — every provider (Gemini / OpenAI / mock) implements this."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass, field


@dataclass(slots=True)
class LlmMessage:
    role: str  # "system" | "user" | "assistant"
    content: str


@dataclass(slots=True)
class LlmResponse:
    """Single non-streamed completion."""

    content: str
    model: str
    usage: dict[str, int] = field(default_factory=dict)
    raw: dict | None = None


@dataclass(slots=True)
class ChatChunk:
    """One token (or a few) streamed from the model."""

    delta: str
    finish_reason: str | None = None


class LlmClient(ABC):
    """Streaming-first async chat client.

    Implementations MUST emit ``ChatChunk.delta`` chunks as they arrive
    and finish with a final chunk whose ``finish_reason`` is set to a
    non-None value (``"stop"``, ``"length"``, etc.).
    """

    model: str

    @abstractmethod
    async def chat(
        self,
        messages: list[LlmMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> LlmResponse:
        """Single-shot completion."""

    @abstractmethod
    def stream(
        self,
        messages: list[LlmMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> AsyncIterator[ChatChunk]:
        """Async iterator of :class:`ChatChunk`.

        The caller is expected to iterate the entire stream and treat the
        final ``finish_reason`` as the end-of-stream marker.
        """
        raise NotImplementedError

    async def aclose(self) -> None:
        """Optional cleanup hook (e.g. close httpx client)."""
        return None