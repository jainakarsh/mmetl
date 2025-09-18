from mmETL.core.dag import DAG, CycleError


def test_topological_order_simple() -> None:
    g = DAG()
    g.add_edge("a", "b")
    assert g.topological_sort() == ["a", "b"]


def test_topological_order_cycle() -> None:
    g = DAG()
    g.add_edge("a", "b")
    g.add_edge("b", "a")
    try:
        g.topological_sort()
    except CycleError:
        return
    raise AssertionError("Expected cycle detection")
