"""Server-Sent Events (SSE) helpers.

Wire format reference: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events

Each event frame is:

    data: <payload>\\n\\n

Heartbeats are SSE comments (lines starting with ``:``) — clients
ignore them but intermediaries (proxies, load balancers) keep the
connection open.

The :class:`SseResponse` is a :class:`StreamingResponse` subclass
that:

* sends the correct ``Content-Type: text/event-stream`` + ``Cache-Control`` headers
* emits a periodic heartbeat comment so connections survive idle proxies
* cleans up the underlying LLM client when the client disconnects
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from typing import Any

from starlette.responses import StreamingResponse

from app.core.config import settings
from app.services.genai.base import ChatChunk


def _sse(data: Any) -> bytes:
    """Encode a payload as an SSE ``data:`` frame."""
    if not isinstance(data, str):
        data = json.dumps(data, ensure_ascii=False, default=str)
    return f"data: {data}\n\n".encode()


def _heartbeat() -> bytes:
    return b": ping\n\n"


async def stream_chunks(
    chunks: AsyncIterator[ChatChunk],
    *,
    heartbeat_seconds: float | None = None,
    on_done: dict | None = None,
) -> AsyncIterator[bytes]:
    """Wrap an LLM chunk stream into SSE-encoded bytes.

    Each :class:`ChatChunk` becomes one SSE event with payload
    ``{"delta": "...", "finish_reason": null|"stop"|...}``.
    The final frame (after ``finish_reason`` is set) is ``{"done": true, ...}``.

    Returns an async iterator — iterate it directly, do not ``await`` it.
    """

    interval = heartbeat_seconds if heartbeat_seconds is not None else settings.SSE_HEARTBEAT_SECONDS

    last_payload: dict | None = None
    try:
        while True:
            # Race the next chunk against the heartbeat timer.
            next_chunk_task = asyncio.create_task(anext(chunks, None))
            hb_task = asyncio.create_task(asyncio.sleep(interval))
            done, _ = await asyncio.wait(
                {next_chunk_task, hb_task}, return_when=asyncio.FIRST_COMPLETED
            )

            if next_chunk_task in done:
                hb_task.cancel()
                chunk = next_chunk_task.result()
                if chunk is None:
                    break
                payload = {
                    "delta": chunk.delta,
                    "finish_reason": chunk.finish_reason,
                }
                last_payload = payload
                yield _sse(payload)
                if chunk.finish_reason:
                    break
            else:
                next_chunk_task.cancel()
                yield _heartbeat()
    finally:
        yield _sse(
            {
                "done": True,
                "last": last_payload,
                "meta": on_done or {},
            }
        )


class SseResponse(StreamingResponse):
    """StreamingResponse preconfigured for SSE."""

    def __init__(self, body: AsyncIterator[bytes]) -> None:
        super().__init__(
            body,
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache, no-transform",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )