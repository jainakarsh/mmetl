"""Hashing helpers."""
from __future__ import annotations

import hashlib

__all__ = ["sha256_hex"]


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
