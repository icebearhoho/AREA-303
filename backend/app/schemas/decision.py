"""Track 2, Đề 5 — E-commerce Decision Intelligence.

Learn from a log of past operating decisions (price / promo / ad / inventory)
and their measured outcomes, then recommend an action for the current
situation. Selection of the best past decision + ad-timing is deterministic;
the recommendation narrative is LLM.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Category = Literal["Thời trang", "Mỹ phẩm", "Phụ kiện"]
DecisionKind = Literal["price", "promo", "ad", "inventory"]
Metric = Literal["ROAS", "sales_lift_pct", "margin_pct", "sell_through_pct"]


class PastDecision(BaseModel):
    kind: DecisionKind
    description: str = Field(min_length=1, max_length=300)
    metric: Metric
    value: float = Field(ge=-1000.0, le=100_000.0)
    month: int | None = Field(default=None, ge=1, le=12)


class DecisionRequest(BaseModel):
    situation: str = Field(min_length=1, max_length=500)
    category: Category
    decisions: list[PastDecision] = Field(min_length=1, max_length=200)


class BestDecision(BaseModel):
    kind: DecisionKind
    description: str
    metric: Metric
    value: float


class DecisionResponse(BaseModel):
    best_decision: BestDecision
    best_ad_month: int | None
    recommended_action: str
    reasoning: str
