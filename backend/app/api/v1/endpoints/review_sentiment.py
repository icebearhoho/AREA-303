"""#01 Review Sentiment — classify a review's sentiment (seller insight)."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.responses import ApiResponse, PageMeta
from app.schemas.insights import SentimentRequest
from app.services import insights

router = APIRouter()


@router.post("/", response_model=ApiResponse[dict])
async def classify(req: SentimentRequest) -> ApiResponse[dict]:
    data = insights.analyze_sentiment(req)
    return ApiResponse[dict](success=True, data=data.model_dump(), meta=PageMeta(), error=None)
