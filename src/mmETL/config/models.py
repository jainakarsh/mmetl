"""Configuration models for mmETL.

Doctest:
>>> from mmETL.config.models import Pipeline, Task, Resource
>>> p = Pipeline(name="p", tasks=[Task(id="t1", uses="noop", inputs=[], outputs=[], config={})], resources={})
>>> isinstance(p.name, str)
True
"""
from __future__ import annotations

from typing import Dict, List, Mapping, Optional

from pydantic import BaseModel, Field

__all__ = ["Resource", "Task", "Pipeline"]


class Resource(BaseModel):
    name: str
    type: str
    config: Mapping[str, object] = Field(default_factory=dict)


class Task(BaseModel):
    id: str
    uses: str
    inputs: List[str] = Field(default_factory=list)
    outputs: List[str] = Field(default_factory=list)
    config: Mapping[str, object] = Field(default_factory=dict)
    resource: Optional[str] = None


class Pipeline(BaseModel):
    name: str
    tasks: List[Task]
    resources: Dict[str, Resource] = Field(default_factory=dict)
