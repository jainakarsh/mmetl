"""Cache store stub (to be implemented later)."""
from __future__ import annotations

__all__ = ["CacheStore"]


class CacheStore:
    """Placeholder cache store API."""

    # TODO: implement backing store
    def get(self, key: str) -> str | None:  # pragma: no cover - stub
        return None

    def set(self, key: str, value: str) -> None:  # pragma: no cover - stub
        return None
