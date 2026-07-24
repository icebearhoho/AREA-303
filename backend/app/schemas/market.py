"""Track 2, Đề 3 — Market Intelligence.

Compare a competitor's product/price against our internal catalog and
recommend a competitive, margin-safe response. Numeric decisions (price floor,
recommended price, margin) are deterministic; the strategic narrative is LLM.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Category = Literal["Thời trang", "Mỹ phẩm", "Phụ kiện"]


class MarketRequest(BaseModel):
    our_product: str = Field(min_length=1, max_length=200)
    category: Category
    our_price_vnd: int = Field(ge=1000, le=100_000_000)
    our_cost_vnd: int = Field(ge=0, le=100_000_000)
    competitor_name: str = Field(min_length=1, max_length=200)
    competitor_price_vnd: int = Field(ge=1000, le=100_000_000)
    competitor_discount_pct: float = Field(default=0.0, ge=0.0, le=90.0)
    min_margin_pct: float = Field(default=15.0, ge=0.0, le=90.0)


class MarketResponse(BaseModel):
    position: Literal["cheaper", "parity", "pricier"]
    recommended_action: Literal["hold", "match_price", "undercut", "differentiate"]
    recommended_price_vnd: int
    price_floor_vnd: int
    margin_pct_at_recommended: float
    competitor_effective_price_vnd: int
    reasoning: str
