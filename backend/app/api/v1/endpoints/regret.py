"""#15 Post-purchase Regret Predictor — score a purchase's regret risk (seller insight)."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.responses import ApiResponse, PageMeta
from app.schemas.insights import RegretRequest
from app.services import insights

router = APIRouter()


@router.post("/", response_model=ApiResponse[dict])
async def score(req: RegretRequest) -> ApiResponse[dict]:
    data = insights.score_regret(req)
    return ApiResponse[dict](success=True, data=data.model_dump(), meta=PageMeta(), error=None)
