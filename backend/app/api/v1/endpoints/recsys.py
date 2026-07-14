"""#11 Recsys — recommendations endpoint."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.responses import ApiResponse, PageMeta
from app.schemas.genai import RecsysRequest
from app.services import recsys as service

router = APIRouter()


@router.post("/", response_model=ApiResponse[dict])
async def recommend(req: RecsysRequest) -> ApiResponse[dict]:
    """Return ranked recommendations with per-item reasoning."""
    data = await service.recommend(req)
    return ApiResponse[dict](
        success=True,
        data=data.model_dump(),
        meta=PageMeta(),
        error=None,
    )