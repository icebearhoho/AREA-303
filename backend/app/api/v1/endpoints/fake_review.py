"""#05 Fake Review — flag computer-generated / fabricated reviews (seller insight)."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.responses import ApiResponse, PageMeta
from app.schemas.insights import FakeReviewRequest
from app.services import insights

router = APIRouter()


@router.post("/", response_model=ApiResponse[dict])
async def detect(req: FakeReviewRequest) -> ApiResponse[dict]:
    data = await insights.detect_fake(req)
    return ApiResponse[dict](success=True, data=data.model_dump(), meta=PageMeta(), error=None)
