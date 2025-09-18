"""Event emission stubs for runs and tasks."""
from __future__ import annotations

from mmETL.observability.metrics import get_redis

__all__ = ["emit"]


def emit(channel: str, payload: str) -> None:
    # TODO: implement structured events
    client = get_redis()
    client.set(f"event:{channel}", payload)
