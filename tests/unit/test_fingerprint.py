from mmETL.cache.fingerprints import fingerprint_pipeline
from mmETL.config.schema import Pipeline, TaskSpec


def test_fingerprint_deterministic() -> None:
    p1 = Pipeline(name="p", tasks=[TaskSpec(id="t", op="noop", inputs=[], params={})], resources={})
    p2 = Pipeline(name="p", tasks=[TaskSpec(id="t", op="noop", inputs=[], params={})], resources={})
    assert fingerprint_pipeline(p1) == fingerprint_pipeline(p2)


essentially_different = Pipeline(name="p", tasks=[TaskSpec(id="t", op="noop", inputs=[], params={"x": 1})], resources={})

def test_fingerprint_changes() -> None:
    p1 = Pipeline(name="p", tasks=[TaskSpec(id="t", op="noop", inputs=[], params={"x": 1})], resources={})
    p2 = Pipeline(name="p", tasks=[TaskSpec(id="t", op="noop", inputs=[], params={"x": 2})], resources={})
    assert fingerprint_pipeline(p1) != fingerprint_pipeline(p2)
