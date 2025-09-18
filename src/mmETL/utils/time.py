"""Time helpers."""
from __future__ import annotations

import time as _time

__all__ = ["now_ms"]


def now_ms() -> int:
    return int(_time.time() * 1000)
