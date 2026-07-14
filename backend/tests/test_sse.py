"""Tests for the SSE streaming helper."""

from __future__ import annotations

import json

import pytest

from app.core.sse import _heartbeat, _sse, stream_chunks
from app.services.genai.base import ChatChunk


def test_sse_data_frame_encodes_json():
    payload = {"delta": "hi", "finish_reason": None}
    raw = _sse(payload)
    assert raw.endswith(b"\n\n")
    assert raw.startswith(b"data: ")
    body = raw[len(b"data: ") : -2].decode()
    assert json.loads(body) == payload


def test_sse_string_passthrough():
    raw = _sse("hello")
    assert raw == b"data: hello\n\n"


def test_heartbeat_is_comment():
    assert _heartbeat().startswith(b":")


@pytest.mark.asyncio
async def test_stream_chunks_yields_events_then_done():
    async def gen():
        yield ChatChunk(delta="foo")
        yield ChatChunk(delta="bar", finish_reason="stop")

    body = stream_chunks(gen())
    frames: list[bytes] = []
    async for frame in body:
        frames.append(frame)
    done = json.loads(frames[-1].decode().split("data: ", 1)[1].rstrip("\n"))
    assert done["done"] is True