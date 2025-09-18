"""Minimal DAG implementation for planning.

Doctest:
>>> from mmETL.core.dag import DAG
>>> g = DAG(); g.add_edge('a','b')
>>> g.topological_sort()
['a', 'b']
"""
from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, Iterable, List, Set

__all__ = ["DAG", "CycleError"]


class CycleError(Exception):
    """Raised when a cycle is detected in the DAG."""


class DAG:
    def __init__(self) -> None:
        self._nodes: Set[str] = set()
        self._edges_out: Dict[str, Set[str]] = defaultdict(set)
        self._edges_in: Dict[str, Set[str]] = defaultdict(set)

    def add_node(self, node: str) -> None:
        self._nodes.add(node)

    def add_edge(self, src: str, dst: str) -> None:
        self.add_node(src)
        self.add_node(dst)
        self._edges_out[src].add(dst)
        self._edges_in[dst].add(src)

    def topological_sort(self) -> List[str]:
        indegree: Dict[str, int] = {n: len(self._edges_in[n]) for n in self._nodes}
        queue: deque[str] = deque([n for n, d in indegree.items() if d == 0])
        order: List[str] = []
        while queue:
            n = queue.popleft()
            order.append(n)
            for m in list(self._edges_out[n]):
                indegree[m] -= 1
                if indegree[m] == 0:
                    queue.append(m)
        if len(order) != len(self._nodes):
            raise CycleError("Cycle detected in DAG")
        return order

    def nodes(self) -> Iterable[str]:
        return iter(self._nodes)
