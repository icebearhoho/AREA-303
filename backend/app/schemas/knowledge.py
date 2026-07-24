"""Track 2, Đề 1 — Product Knowledge (causal sales explanation).

Explains *why* a product's sales moved by attributing the change across the
commerce entities that drive it (price, promotion, stock, traffic, competitor
activity). Driver attribution is deterministic; the explanation is LLM.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Category = Literal["Thời trang", "Mỹ phẩm", "Phụ kiện"]


class ProductKnowledgeRequest(BaseModel):
    product: str = Field(min_length=1, max_length=200)
    category: Category
    sales_prev: int = Field(ge=0, le=1_000_000_000)
    sales_curr: int = Field(ge=0, le=1_000_000_000)
    price_change_pct: float = Field(default=0.0, ge=-90.0, le=500.0)
    promotion_active: bool = False
    competitor_promo: bool = False
    stock_status: Literal["ok", "low", "out"] = "ok"
    traffic_change_pct: float = Field(default=0.0, ge=-100.0, le=1000.0)


class Driver(BaseModel):
    factor: str
    direction: Literal["up", "down"]
    impact: Literal["low", "medium", "high"]


class ProductKnowledgeResponse(BaseModel):
    sales_change_pct: float
    direction: Literal["up", "down", "flat"]
    drivers: list[Driver]
    promotion_effectiveness: str
    explanation: str
