"""Executor stub that only echoes the plan.

Doctest:
>>> from mmETL.core.dag import DAG
>>> from mmETL.core.executor import Executor
>>> e = Executor(); g = DAG(); g.add_node('a')
>>> e.plan_and_echo(g, run_id='r1') is None
True
"""
from __future__ import annotations

from typing import Optional

from rich.console import Console

from mmETL.core.dag import DAG

__all__ = ["Executor"]


class Executor:
    def __init__(self) -> None:
        self._console = Console()

    def plan_and_echo(self, dag: DAG, run_id: Optional[str] = None) -> None:
        run_label = run_id or "unknown"
        self._console.print(f"[bold]Plan (stub)[/bold] run_id={run_label}")
        for idx, node in enumerate(dag.topological_sort(), start=1):
            self._console.print(f"  {idx}. {node}")
