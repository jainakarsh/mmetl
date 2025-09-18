"""Minimal DAG implementation for planning.

Doctest:
>>> from mmETL.core.dag import DAG
>>> g = DAG()
>>> g.add_node('a'); g.add_node('b'); g.add_edge('a','b')
>>> g.topological_order() in (["a","b"],)
True
"""
from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, Iterable, List, Set

__all__ = ["DAG"]


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

    def topological_order(self) -> List[str]:
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
            raise ValueError("Cycle detected in DAG")
        return order

    def nodes(self) -> Iterable[str]:
        return iter(self._nodes)
