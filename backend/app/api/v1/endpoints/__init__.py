"""Per-feature routers. New feature? Add a new file here and wire it in
``app/api/v1/__init__.py``.
"""

from app.api.v1.endpoints import auth, datasets, health, ideas, kpis, users

__all__ = ["auth", "datasets", "health", "ideas", "kpis", "users"]
