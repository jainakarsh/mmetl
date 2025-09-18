from mmETL.cache.fingerprint import stable_fingerprint


def test_stable_fingerprint_deterministic() -> None:
    a = stable_fingerprint({"a": 1, "b": [1, 2, 3]})
    b = stable_fingerprint({"b": [1, 2, 3], "a": 1})
    assert a == b


def test_stable_fingerprint_changes() -> None:
    a = stable_fingerprint({"x": 1})
    b = stable_fingerprint({"x": 2})
    assert a != b
