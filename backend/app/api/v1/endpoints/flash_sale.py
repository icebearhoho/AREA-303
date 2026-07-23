"""#13 Emotion-Aware Flash Sale Optimizer."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.responses import ApiResponse, PageMeta
from app.schemas.flash_sale import FlashSaleRequest
from app.services import flash_sale as service

router = APIRouter()


@router.post("/", response_model=ApiResponse[dict])
async def analyze(req: FlashSaleRequest) -> ApiResponse[dict]:
    data = service.analyze_hesitation(req)
    return ApiResponse[dict](success=True, data=data.model_dump(), meta=PageMeta(), error=None)
