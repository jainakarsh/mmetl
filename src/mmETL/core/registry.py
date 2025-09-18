"""Registry for adapters and transforms using decorators.

Doctest:
>>> from mmETL.core.registry import adapter, transform, get_registered
>>> @adapter('noop')
... def a(): pass
>>> 'noop' in get_registered('adapter')
True
"""
from __future__ import annotations

from typing import Any, Callable, Dict

__all__ = ["adapter", "transform", "get_registered"]

_REGISTRIES: Dict[str, Dict[str, Callable[..., Any]]] = {
    "adapter": {},
    "transform": {},
}


class RegistryError(Exception):
    """Raised for registry-related errors."""


def _register(kind: str, name: str, fn: Callable[..., Any]) -> None:
    if name in _REGISTRIES[kind]:
        raise RegistryError(f"Duplicate {kind} registered: {name}")
    _REGISTRIES[kind][name] = fn


def adapter(name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        _register("adapter", name, fn)
        return fn

    return deco


def transform(name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        _register("transform", name, fn)
        return fn

    return deco


def get_registered(kind: str) -> Dict[str, Callable[..., Any]]:
    return dict(_REGISTRIES[kind])
