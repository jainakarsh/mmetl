"""Pipeline fingerprint utilities.

Doctest:
>>> from mmETL.config.schema import Pipeline, TaskSpec
>>> from mmETL.cache.fingerprints import fingerprint_pipeline
>>> p = Pipeline(name='p', tasks=[TaskSpec(id='t', op='noop')], resources={})
>>> isinstance(fingerprint_pipeline(p), str)
True
"""
from __future__ import annotations

import json
import hashlib
from typing import Any

from mmETL.config.schema import Pipeline

__all__ = ["fingerprint_pipeline"]


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def fingerprint_pipeline(pipeline: Pipeline) -> str:
    serial = {
        "name": pipeline.name,
        "tasks": [
            {"id": t.id, "op": t.op, "inputs": list(t.inputs), "params": t.params}
            for t in pipeline.tasks
        ],
    }
    payload = _canonical(serial)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
