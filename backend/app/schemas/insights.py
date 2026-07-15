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
