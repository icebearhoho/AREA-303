"""Shared test fixtures."""

import os

# Force test config BEFORE importing app modules.
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("JWT_SECRET", "test-secret")
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("REDIS_HOST", "localhost")

from app.main import app  # noqa: E402

__all__ = ["app"]
