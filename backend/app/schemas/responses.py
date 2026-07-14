"""Shared response schemas. Per-feature schemas live next to their feature."""

from __future__ import annotations

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str
    env: str


class IdeaOut(BaseModel):
    id: int
    slug: str
    category: str


class KpiSummary(BaseModel):
    kpis: list[dict]
    by_category: dict[str, int]
