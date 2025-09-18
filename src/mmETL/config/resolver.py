"""Resolver: validates raw dict into Pipeline model.

Doctest:
>>> from mmETL.config.resolver import resolve_pipeline
>>> p = resolve_pipeline({
...   'name': 'p',
...   'tasks': [{'id': 't', 'op': 'noop'}],
...   'resources': {}
... })
>>> p.name
'p'
"""
from __future__ import annotations

from typing import Any, Dict

from mmETL.config.schema import Pipeline

__all__ = ["resolve_pipeline"]


def resolve_pipeline(data: Dict[str, Any]) -> Pipeline:
    # TODO: add defaults/normalization as needed
    return Pipeline.model_validate(data)
