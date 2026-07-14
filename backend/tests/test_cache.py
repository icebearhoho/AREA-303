"""Tests for the LLM cache (Redis + in-process fallback)."""

from __future__ import annotations

import asyncio

import pytest

from app.services.genai.cache import _LOCAL_CACHE, invalidate_prefix, llm_cache


@pytest.mark.asyncio
async def test_cache_misses_then_hits_in_process():
    _LOCAL_CACHE.clear()
    calls = 0

    @llm_cache(prefix="t1", ttl=60)
    async def slow() -> dict:
        nonlocal calls
        calls += 1
        await asyncio.sleep(0)
        return {"v": calls}

    a = await slow()
    b = await slow()
    assert a == {"v": 1}
    assert b == {"v": 1}
    assert calls == 1


@pytest.mark.asyncio
async def test_invalidate_clears_prefix():
    _LOCAL_CACHE.clear()
    calls = 0

    @llm_cache(prefix="t2")
    async def f() -> int:
        nonlocal calls
        calls += 1
        return calls

    await f()
    assert calls == 1
    await invalidate_prefix("t2")
    await f()
    assert calls == 2


@pytest.mark.asyncio
async def test_cache_key_includes_args():
    _LOCAL_CACHE.clear()

    @llm_cache(prefix="t3")
    async def echo(x: int) -> int:
        return x * 10

    assert await echo(1) == 10
    assert await echo(2) == 20
    assert await echo(1) == 10  # cached