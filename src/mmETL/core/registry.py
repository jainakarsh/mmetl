"""Registry for transforms using decorators.

Doctest:
>>> from mmETL.core.registry import register_transform, get_registered
>>> @register_transform('noop')
... def f(): pass
>>> 'noop' in get_registered()
True
"""
from __future__ import annotations

from typing import Any, Callable, Dict

__all__ = ["register_transform", "get_registered"]

_REGISTRY: Dict[str, Callable[..., Any]] = {}


class RegistryError(Exception):
    """Raised for registry-related errors."""


def register_transform(name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        if name in _REGISTRY:
            raise RegistryError(f"Duplicate transform: {name}")
        _REGISTRY[name] = fn
        return fn

    return deco


def get_registered() -> Dict[str, Callable[..., Any]]:
    return dict(_REGISTRY)
