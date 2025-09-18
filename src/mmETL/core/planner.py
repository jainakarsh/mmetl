"""Planner: converts Pipeline to DAG by wiring task dependencies via inputs/outputs.

Doctest:
>>> from mmETL.config.models import Pipeline, Task
>>> from mmETL.core.planner import plan_pipeline
>>> p = Pipeline(name="p", tasks=[
...   Task(id="a", uses="noop", outputs=["x"], config={}),
...   Task(id="b", uses="noop", inputs=["x"], config={}),
... ], resources={})
>>> dag = plan_pipeline(p)
>>> dag.topological_order()
['a', 'b']
"""
from __future__ import annotations

from typing import Dict, List

from mmETL.config.models import Pipeline, Task
from mmETL.core.dag import DAG

__all__ = ["plan_pipeline"]


def plan_pipeline(pipeline: Pipeline) -> DAG:
    produces: Dict[str, str] = {}
    dag = DAG()
    for task in pipeline.tasks:
        dag.add_node(task.id)
        for output in task.outputs:
            produces[output] = task.id
    for task in pipeline.tasks:
        for input_name in task.inputs:
            if input_name in produces:
                dag.add_edge(produces[input_name], task.id)
    return dag
