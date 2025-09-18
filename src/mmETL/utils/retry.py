"""Retry helper (simple)."""
from __future__ import annotations

import time
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

__all__ = ["retry"]


def retry(times: int = 3, delay: float = 0.1) -> Callable[[F], F]:  # type: ignore[override]
    def deco(fn: F) -> F:  # type: ignore[misc]
        def wrapped(*args: Any, **kwargs: Any):  # type: ignore[no-untyped-def]
            last: Exception | None = None
            for _ in range(times):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001
                    last = exc
                    time.sleep(delay)
            raise last  # type: ignore[misc]

        return wrapped  # type: ignore[return-value]

    return deco
