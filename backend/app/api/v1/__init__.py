"""All v1 routers aggregated."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, datasets, health, ideas, kpis, users

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(ideas.router, prefix="/ideas", tags=["ideas"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(kpis.router, prefix="/kpis", tags=["kpis"])
