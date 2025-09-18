"""Environment helpers."""
from __future__ import annotations

import os

__all__ = ["getenv"]


def getenv(key: str, default: str | None = None) -> str | None:
    return os.getenv(key, default)
