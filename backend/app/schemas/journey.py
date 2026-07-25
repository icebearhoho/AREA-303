"""Customer Journey Intelligence — Track 1, Đề 2.

Predicts a shopper's next action from the sequence of events in their current
session (view / cart / purchase / livestream), à la the brief's example
questions: will they buy or leave, what to recommend, what category they're
interested in. Not one of the original 17 ideas — added per the official
Track 1 brief.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.genai import ProductCard

EventType = Literal["view", "cart", "purchase", "livestream"]
Category = Literal["Thời trang", "Mỹ phẩm", "Phụ kiện"]


class JourneyEvent(BaseModel):
    type: EventType
    category: Category | None = None


class JourneyRequest(BaseModel):
    events: list[JourneyEvent] = Field(min_length=1, max_length=50)


class JourneyResponse(BaseModel):
    will_purchase: bool
    purchase_probability: float = Field(ge=0.0, le=1.0)
    top_category: Category | None
    category_breakdown: dict[str, int]
    recommended_products: list[ProductCard]
    reasoning: str
