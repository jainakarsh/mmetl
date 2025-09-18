"""Schema models for mmETL configuration.

Doctest:
>>> from mmETL.config.schema import Pipeline, TaskSpec
>>> Pipeline(name='p', tasks=[TaskSpec(id='t', op='noop')], resources={}).name
'p'
"""
from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field

__all__ = ["TaskSpec", "Pipeline"]


class TaskSpec(BaseModel):
    id: str
    op: str
    inputs: List[str] = Field(default_factory=list)
    params: Dict[str, Any] = Field(default_factory=dict)


class Pipeline(BaseModel):
    name: str
    tasks: List[TaskSpec]
    resources: Dict[str, Any] = Field(default_factory=dict)
