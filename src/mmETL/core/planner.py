"""Planner: converts Pipeline to DAG by wiring task dependencies via inputs.

Doctest:
>>> from mmETL.config.schema import Pipeline, TaskSpec
>>> from mmETL.core.planner import plan_pipeline
>>> p = Pipeline(name='p', tasks=[
...   TaskSpec(id='a', op='noop', inputs=[]),
...   TaskSpec(id='b', op='noop', inputs=['a']),
... ], resources={})
>>> plan_pipeline(p).topological_sort()
['a', 'b']
"""
from __future__ import annotations

from mmETL.config.schema import Pipeline
from mmETL.core.dag import DAG

__all__ = ["plan_pipeline"]


def plan_pipeline(pipeline: Pipeline) -> DAG:
    dag = DAG()
    for task in pipeline.tasks:
        dag.add_node(task.id)
    # Simple rule: if a task lists another task id in inputs, add edge
    for task in pipeline.tasks:
        for inp in task.inputs:
            if any(t.id == inp for t in pipeline.tasks):
                dag.add_edge(inp, task.id)
    return dag
