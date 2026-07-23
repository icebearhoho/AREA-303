"""#14 AI Negotiation Bot cho B2B.

Rule-based (deterministic, key-free) counter-offer engine: no LLM call needed
for a demo — a real deployment would layer an LLM on top for natural-language
framing while keeping this price-logic as the guardrail.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class NegotiationRequest(BaseModel):
    product_name: str = Field(min_length=1, max_length=200)
    list_price_vnd: int = Field(ge=0)
    min_price_vnd: int = Field(ge=0)
    buyer_offer_vnd: int = Field(ge=0)
    round: int = Field(ge=1, le=10, default=1)


class NegotiationResponse(BaseModel):
    decision: Literal["accept", "counter", "reject"]
    counter_price_vnd: int | None
    message: str
    round: int
