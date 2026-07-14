"""User endpoints skeleton."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.responses import ApiResponse, PageMeta

router = APIRouter()


@router.get("/", response_model=ApiResponse[list[dict]])
async def list_users() -> ApiResponse[list[dict]]:
    return ApiResponse[list[dict]](
        success=True, data=[], meta=PageMeta(page=1, page_size=20, total=0), error=None
    )
