"""#13 Emotion-Aware Flash Sale Optimizer.

Simplified as a "behaviour simulator" form (dwell time, scroll depth, revisit
count, cart-without-purchase) rather than live client-side event tracking —
consistent with how #04 Churn and #15 Regret are demoed. A production version
would feed this from real JS behavioural tracking on the product page.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class FlashSaleRequest(BaseModel):
    dwell_time_seconds: int = Field(ge=0, le=3600)
    scroll_depth_pct: int = Field(ge=0, le=100)
    revisit_count: int = Field(ge=0, le=20, default=0)
    cart_opened_no_purchase: bool = False
    price_vnd: int = Field(ge=0)


class FlashSaleResponse(BaseModel):
    hesitating: bool
    hesitation_score: float
    trigger_now: bool
    suggested_discount_pct: int
    message: str
