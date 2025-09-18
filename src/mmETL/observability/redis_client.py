"""Redis client wrapper with no-op fallback if not configured.

Doctest:
>>> from mmETL.observability.redis_client import get_redis_client
>>> client = get_redis_client()
>>> client is None or hasattr(client, 'get')
True
"""
from __future__ import annotations

import os
from typing import Optional

try:  # optional import for environments without redis runtime
    import redis  # type: ignore
except Exception:  # noqa: BLE001
    redis = None  # type: ignore[assignment]

__all__ = ["get_redis_client"]


def get_redis_client() -> Optional["redis.Redis"]:
    url = os.getenv("REDIS_URL")
    if not url or redis is None:
        return None
    try:
        return redis.Redis.from_url(url)
    except Exception:  # noqa: BLE001
        return None
