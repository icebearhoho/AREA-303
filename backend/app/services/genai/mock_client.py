"""Demo-mode LLM client.

Returns pre-generated content and streams it token-by-token so the
frontend SSE consumer behaves identically to a real model.

This is the contract that lets ``scripts/prepare_demo_data.py`` (D2)
keep the dashboard working even when upstream LLMs are down or out
of quota.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from dataclasses import dataclass

from app.services.genai.base import ChatChunk, LlmClient, LlmMessage, LlmResponse


@dataclass(slots=True)
class _MockEntry:
    """Maps a query (substring match) to a canned reply."""

    match: str
    reply: str


# Demo replies keyed off query substring.  Ordered — first match wins.
_DEMO_REPLIES: list[_MockEntry] = [
    _MockEntry(
        match="sinh nhật",
        reply=(
            "Dựa trên câu hỏi của bạn, mình gợi ý 4 sản phẩm phù hợp:\n\n"
            "1. Túi tote canvas in họa tiết — Local Brand X (TikTok Shop, 4.7★)\n"
            "2. Son tint lì Bourjois Velvet 21 — Bourjois (Shopee, 4.5★)\n"
            "3. Mặt nạ ngủ Laneige — Laneige (Shopee, 4.8★)\n"
            "4. Áo thun oversize cotton — Local Brand Z (Shopee, 4.5★)\n\n"
            "Bạn muốn mình đi sâu hơn vào tiêu chí nào (giá, brand, rating)?"
        ),
    ),
    _MockEntry(
        match="son",
        reply=(
            "Với tiêu chí son cho bạn, mình lọc được 2 gợi ý nổi bật:\n\n"
            "1. Son tint lì Bourjois Velvet 21 — Bourjois (Shopee, 4.5★, 295k)\n"
            "2. Serum Vitamin C 15% NUDESTIX — NUDESTIX (Tiki, 4.4★, 720k)\n\n"
            "Son Bourjois Velvet là lựa chọn natural-fit, lâu trôi 8h."
        ),
    ),
    _MockEntry(
        match="skincare",
        reply=(
            "Cho skincare, mình đề xuất routine 3 bước:\n\n"
            "1. Serum Vitamin C 15% NUDESTIX — sáng da, giảm thâm\n"
            "2. Mặt nạ ngủ Laneige — cấp ẩm 8h\n"
            "3. Son tint Bourjois Velvet — finish velvet, không khô môi\n\n"
            "Da bạn da khô thì Laneige mask là bước quan trọng nhất."
        ),
    ),
]

DEFAULT_REPLY = (
    "Mình đang ở chế độ demo — không gọi Gemini/OpenAI thật.\n\n"
    "Với truy vấn của bạn, đây là 4 sản phẩm gợi ý từ catalog:\n\n"
    "1. Áo khoác denim unisex — Local Brand X (Shopee, 4.6★)\n"
    "2. Serum Vitamin C 15% — NUDESTIX (Tiki, 4.4★)\n"
    "3. Túi tote canvas — OEM (TikTok Shop, 4.7★)\n"
    "4. Son tint Bourjois Velvet 21 — Bourjois (Shopee, 4.5★)\n\n"
    "Hãy đặt câu hỏi cụ thể hơn (giá, brand, platform) để mình lọc sâu hơn."
)


def _resolve_reply(messages: list[LlmMessage]) -> str:
    """Pick a canned reply based on the last user message."""
    user_text = next(
        (m.content for m in reversed(messages) if m.role == "user"), ""
    ).lower()
    for entry in _DEMO_REPLIES:
        if entry.match in user_text:
            return entry.reply
    return DEFAULT_REPLY


class MockLlmClient(LlmClient):
    """Returns canned content. Streams it chunk-by-chunk with a small delay."""

    model = "mock-demo"

    def __init__(self, *, chunk_chars: int = 4, delay_ms: int = 14) -> None:
        self._chunk_chars = chunk_chars
        self._delay_ms = delay_ms

    async def chat(
        self,
        messages: list[LlmMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> LlmResponse:
        text = _resolve_reply(messages)
        if max_tokens is not None:
            # Rough char-budget proxy: 1 token ≈ 4 chars.
            text = text[: max_tokens * 4]
        return LlmResponse(
            content=text,
            model=self.model,
            usage={
                "prompt_tokens": sum(len(m.content) for m in messages) // 4,
                "completion_tokens": len(text) // 4,
                "total_tokens": (sum(len(m.content) for m in messages) + len(text)) // 4,
            },
        )

    async def stream(
        self,
        messages: list[LlmMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> AsyncIterator[ChatChunk]:
        text = _resolve_reply(messages)
        if max_tokens is not None:
            text = text[: max_tokens * 4]

        for i in range(0, len(text), self._chunk_chars):
            chunk = text[i : i + self._chunk_chars]
            await asyncio.sleep(self._delay_ms / 1000)
            yield ChatChunk(delta=chunk, finish_reason=None)

        yield ChatChunk(delta="", finish_reason="stop")