"""#10 Return/Refund Prediction — score an order's return risk (seller insight)."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.responses import ApiResponse, PageMeta
from app.schemas.insights import ReturnRequest
from app.services import insights

router = APIRouter()


@router.post("/", response_model=ApiResponse[dict])
async def score(req: ReturnRequest) -> ApiResponse[dict]:
    data = insights.score_return(req)
    return ApiResponse[dict](success=True, data=data.model_dump(), meta=PageMeta(), error=None)
