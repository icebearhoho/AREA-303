"""Liveness + readiness probes. Always returns the standard envelope."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.config import settings
from app.core.responses import ApiResponse, PageMeta

router = APIRouter()


@router.get("/health", response_model=ApiResponse[dict])
async def health() -> ApiResponse[dict]:
    return ApiResponse[dict](
        success=True,
        data={"status": "ok", "version": settings.APP_NAME, "env": settings.APP_ENV},
        meta=PageMeta(),
        error=None,
    )


@router.get("/ready", response_model=ApiResponse[dict])
async def ready() -> ApiResponse[dict]:
    # Wire DB / Redis checks here later.
    return ApiResponse[dict](
        success=True,
        data={"ready": True},
        meta=PageMeta(),
        error=None,
    )
