"""All v1 routers aggregated."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    churn,
    content_generator,
    datasets,
    dynamic_pricing,
    fake_review,
    health,
    ideas,
    journey,
    kpis,
    personal_shopper,
    recsys,
    review_sentiment,
    segmentation,
    seller_coach,
    users,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(ideas.router, prefix="/ideas", tags=["ideas"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(kpis.router, prefix="/kpis", tags=["kpis"])
api_router.include_router(
    personal_shopper.router,
    prefix="/personal-shopper",
    tags=["03-personal-shopper"],
)
api_router.include_router(
    content_generator.router,
    prefix="/content-generator",
    tags=["09-content-generator"],
)
api_router.include_router(recsys.router, prefix="/recsys", tags=["11-recsys"])
api_router.include_router(
    # NOTE: "Customer Segmentation" is a bonus feature (from customer_segmentation/
    # offline modeling) and is NOT official idea #13 in the AREA303_17_Ideas brief
    # (#13 there is "Emotion-Aware Flash Sale Optimizer" — see frontend/lib/nav.ts
    # slug "emotion-sale"). Tagged without a number to avoid confusion.
    segmentation.router, prefix="/segmentation", tags=["bonus-customer-segmentation"]
)
api_router.include_router(
    seller_coach.router, prefix="/seller-coach", tags=["17-seller-coach"]
)
api_router.include_router(
    review_sentiment.router, prefix="/review-sentiment", tags=["01-review-sentiment"]
)
api_router.include_router(
    fake_review.router, prefix="/fake-review", tags=["05-fake-review"]
)
api_router.include_router(
    dynamic_pricing.router, prefix="/dynamic-pricing", tags=["02-dynamic-pricing"]
)
api_router.include_router(churn.router, prefix="/churn", tags=["04-churn"])
api_router.include_router(
    # Track 1, Đề 2 — not one of the original 17 ideas.
    journey.router, prefix="/journey", tags=["bonus-customer-journey"]
)
