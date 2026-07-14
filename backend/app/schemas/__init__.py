"""Pydantic request/response schemas. Add one file per feature."""

from app.schemas.genai import (
    AuditStep,
    ContentGeneratorRequest,
    ContentGeneratorResponse,
    ContentVariant,
    Platform,
    ProductCard,
    Recommendation,
    RecsysRequest,
    RecsysResponse,
    RoadmapWeek,
    SellerCoachRequest,
    SellerCoachResponse,
    ShopperProductsResponse,
    ShopperRequest,
)
from app.schemas.responses import HealthResponse, IdeaOut, KpiSummary

__all__ = [
    "AuditStep",
    "ContentGeneratorRequest",
    "ContentGeneratorResponse",
    "ContentVariant",
    "HealthResponse",
    "IdeaOut",
    "KpiSummary",
    "Platform",
    "ProductCard",
    "Recommendation",
    "RecsysRequest",
    "RecsysResponse",
    "RoadmapWeek",
    "SellerCoachRequest",
    "SellerCoachResponse",
    "ShopperProductsResponse",
    "ShopperRequest",
]