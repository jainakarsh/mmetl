from mmETL.config.schema import Pipeline, TaskSpec


def test_schema_happy_path() -> None:
    p = Pipeline(name="p", tasks=[TaskSpec(id="t1", op="noop", inputs=[])], resources={})
    assert p.name == "p"


def test_schema_error() -> None:
    try:
        Pipeline.model_validate({"name": "p", "tasks": [{}]})
    except Exception:
        return
    raise AssertionError("Expected validation error")
