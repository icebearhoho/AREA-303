"""#13 Emotion-Aware Flash Sale Optimizer — hesitation scoring.

Weights long dwell time, deep scrolling, repeat visits, and cart-abandon-
without-purchase into a single "interested but hesitating" score, then decides
whether to trigger a personalized, time-boxed discount.
"""

from __future__ import annotations

from app.schemas.flash_sale import FlashSaleRequest, FlashSaleResponse

HESITATION_THRESHOLD = 2.5


def analyze_hesitation(req: FlashSaleRequest) -> FlashSaleResponse:
    score = min(2.0, req.dwell_time_seconds / 60)          # up to 2 pts for 2+ min dwell
    score += (req.scroll_depth_pct / 100) * 1.0            # up to 1 pt for reading it all
    score += min(1.5, req.revisit_count * 0.5)             # up to 1.5 pts for repeat visits
    score += 1.5 if req.cart_opened_no_purchase else 0.0

    hesitating = score >= HESITATION_THRESHOLD
    trigger_now = hesitating and req.cart_opened_no_purchase
    discount = (15 if score >= 4 else 10) if trigger_now else (5 if hesitating else 0)

    if trigger_now:
        message = f"⏰ Ưu đãi riêng cho bạn: giảm {discount}% nếu hoàn tất đơn trong 10 phút tới!"
    elif hesitating:
        message = "Sản phẩm bạn đang xem còn số lượng giới hạn — đừng bỏ lỡ nhé!"
    else:
        message = "Chưa cần can thiệp — khách đang duyệt bình thường."

    return FlashSaleResponse(
        hesitating=hesitating, hesitation_score=round(score, 2), trigger_now=trigger_now,
        suggested_discount_pct=discount, message=message,
    )
