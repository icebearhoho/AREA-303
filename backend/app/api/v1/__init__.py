"""All v1 routers aggregated."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    content_generator,
    datasets,
    fake_review,
    health,
    ideas,
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
    segmentation.router, prefix="/segmentation", tags=["13-segmentation"]
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
