from mmETL.config.models import Pipeline, Task


def test_schema_happy_path() -> None:
    p = Pipeline(name="p", tasks=[Task(id="t1", uses="noop", inputs=[], outputs=[], config={})], resources={})
    assert p.name == "p"


def test_schema_error() -> None:
    try:
        Pipeline.model_validate({"name": "p"})
    except Exception:
        return
    raise AssertionError("Expected validation error")
