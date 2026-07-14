"""Dashboard KPIs — 4 cards on the home page. Skeleton with mock values."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.responses import ApiResponse, PageMeta

router = APIRouter()


@router.get("/summary", response_model=ApiResponse[dict])
async def summary() -> ApiResponse[dict]:
    """Return the 4 dashboard KPIs.

    Wire to real data sources once the registry + pipelines are in place.
    """
    data = {
        "kpis": [
            {"key": "ideas_total",      "value": 17,  "label": "Candidate ideas"},
            {"key": "datasets_usable",  "value": 12,  "label": "Usable datasets"},
            {"key": "models_planned",   "value": 17,  "label": "Models planned"},
            {"key": "platforms",        "value": 3,   "label": "Platforms (Shopee / Tiki / Lazada)"},
        ],
        "by_category": {
            "NLP": 4,
            "Time Series": 4,
            "Computer Vision": 2,
            "Generative AI": 4,
            "Behavioral AI": 3,
        },
    }
    return ApiResponse[dict](success=True, data=data, meta=PageMeta(), error=None)
