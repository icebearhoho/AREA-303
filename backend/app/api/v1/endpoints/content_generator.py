"""#09 Content Generator — 3 platform variants."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.responses import ApiResponse, PageMeta
from app.schemas.genai import ContentGeneratorRequest
from app.services import content_generator as service

router = APIRouter()


@router.post("/", response_model=ApiResponse[dict])
async def generate(req: ContentGeneratorRequest) -> ApiResponse[dict]:
    """Generate 1-3 platform variants of a product description."""
    data = await service.generate(req)
    return ApiResponse[dict](
        success=True,
        data=data.model_dump(),
        meta=PageMeta(),
        error=None,
    )