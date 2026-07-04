"""Shared FastAPI dependencies."""

from __future__ import annotations

from collections.abc import AsyncIterator

from fastapi import Depends, Header
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedError
from app.core.security import decode_access_token
from app.db.redis import get_redis
from app.db.session import get_db  # re-export


async def get_db_dep() -> AsyncIterator[AsyncSession]:  # alias for clarity
    async for s in get_db():
        yield s


async def get_redis_dep() -> Redis:
    return get_redis()


async def get_current_user(
    authorization: str | None = Header(default=None),
) -> dict:
    """Decode the Bearer JWT and return the claims. Replace with DB lookup later."""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise UnauthorizedError("Missing bearer token.")
    token = authorization.split(" ", 1)[1]
    return decode_access_token(token)


__all__ = ["get_db", "get_redis", "get_current_user"]
