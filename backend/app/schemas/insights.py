"""Schemas for the seller-side insight features wired from the modeling layer.

#01 Review Sentiment and #05 Fake Review. The backend ships lightweight,
key-free heuristic scorers so the endpoints always respond in a demo; the
offline modeling layer (common/llm_client.py + review_sentiment/, fake_review/)
is the higher-accuracy LLM version evaluated separately.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


# --- #01 Review Sentiment -------------------------------------------------
class SentimentRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    rating: int | None = Field(default=None, ge=1, le=5)


class SentimentResponse(BaseModel):
    sentiment: Literal["positive", "neutral", "negative"]
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str


# --- #05 Fake Review ------------------------------------------------------
class FakeReviewRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    rating: int | None = Field(default=None, ge=1, le=5)
    category: str | None = None


class FakeReviewResponse(BaseModel):
    is_fake: bool
    confidence: float = Field(ge=0.0, le=1.0)
    signals: list[str]
    reason: str


# --- #02 Dynamic Pricing ---------------------------------------------------
class PricingRequest(BaseModel):
    product_name: str = Field(min_length=1, max_length=200)
    category: Literal["Thời trang", "Mỹ phẩm", "Phụ kiện"]
    current_price: int | None = Field(default=None, ge=0)


class PricingResponse(BaseModel):
    recommended_price: int
    low: int
    high: int
    category_median: int
    sample_size: int
    rationale: str


# --- #04 Churn Prediction ---------------------------------------------------
class ChurnRequest(BaseModel):
    recency_days: int = Field(ge=0, le=1000)
    frequency_orders: int = Field(ge=0, le=500)
    sessions_last_month: int = Field(ge=0, le=500)
    cart_abandon_rate: float = Field(ge=0.0, le=1.0)
    trend: Literal["declining", "stable", "growing"] = "stable"


class ChurnResponse(BaseModel):
    churn_risk: float = Field(ge=0.0, le=1.0)
    risk_band: Literal["low", "medium", "high"]
    drivers: list[str]
    retention_action: str
