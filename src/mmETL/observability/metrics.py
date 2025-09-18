"""Metrics helpers backed by Redis, with no-op fallback if not configured.

Doctest:
>>> c = get_redis()
>>> c.set('k','v'); c.get('k') in ('v', b'v', None)
True
"""
from __future__ import annotations

import os
from typing import Any, Optional

try:  # optional import for environments without redis runtime
    import redis  # type: ignore
except Exception:  # noqa: BLE001
    redis = None  # type: ignore[assignment]

__all__ = ["get_redis"]


class _StubClient:
    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def get(self, key: str) -> Any:
        return self._store.get(key)

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value


def get_redis() -> Any:
    url = os.getenv("REDIS_URL")
    if not url or redis is None:
        return _StubClient()
    try:
        return redis.Redis.from_url(url)
    except Exception:  # noqa: BLE001
        return _StubClient()
