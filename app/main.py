"""Backward-compatible FastAPI entry point.

The canonical application now lives in :mod:`api.main`. Importing the shared app
prevents model-loading drift and keeps legacy deployment commands operational.
"""

from api.main import app

__all__ = ["app"]
