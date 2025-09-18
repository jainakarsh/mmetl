"""Heartbeat stub for future scheduling integration.

Doctest:
>>> from mmETL.observability.heartbeat import beat
>>> beat('r1') is None
True
"""
from __future__ import annotations

from mmETL.observability.metrics import get_redis

__all__ = ["beat"]


def beat(run_id: str) -> None:
    # TODO: emit heartbeat timestamp
    client = get_redis()
    client.set(f"mmetl:run:{run_id}:heartbeat", "alive")
