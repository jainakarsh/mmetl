"""Fingerprint utilities for caching.

Doctest:
>>> from mmETL.cache.fingerprint import stable_fingerprint
>>> stable_fingerprint({"a":1}) == stable_fingerprint({"a":1})
True
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

__all__ = ["stable_fingerprint"]


def _default(obj: Any) -> Any:
    if isinstance(obj, set):
        return sorted(obj)
    raise TypeError(f"Unserializable object: {type(obj)}")


def stable_fingerprint(data: Any) -> str:
    payload = json.dumps(data, default=_default, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
