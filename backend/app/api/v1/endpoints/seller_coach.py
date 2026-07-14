"""#17 Seller Coach — 5-step audit + 4-week roadmap."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.responses import ApiResponse, PageMeta
from app.schemas.genai import SellerCoachRequest
from app.services import seller_coach as service

router = APIRouter()


@router.post("/", response_model=ApiResponse[dict])
async def coach(req: SellerCoachRequest) -> ApiResponse[dict]:
    """Score a seller's audit + propose a roadmap."""
    data = await service.coach(req)
    return ApiResponse[dict](
        success=True,
        data=data.model_dump(),
        meta=PageMeta(),
        error=None,
    )