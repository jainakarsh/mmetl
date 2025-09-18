# mmETL

Minimal mmETL pipeline framework (MVP).

## Install (editable for dev)

```bash
pip install -e .[dev]
```

## CLI

```bash
mmetl --help
mmetl validate examples/pipelines/tabular_only.yaml
mmetl dry-run examples/pipelines/tabular_only.yaml
mmetl run examples/pipelines/tabular_only.yaml
mmetl status some-run-id
```

## File layout

- `src/mmETL/cli`: Typer CLI commands
- `src/mmETL/config`: Pydantic v2 models and YAML loader (env expand, include stub)
- `src/mmETL/core`: DAG, registry decorators, planner, executor stub
- `src/mmETL/observability`: Redis wrapper with safe fallback
- `src/mmETL/cache`: Fingerprint utilities
- `tests`: unit tests for CLI, schema, DAG, fingerprints
- `examples/pipelines`: example YAMLs

## Notes

- Heavy execution is stubbed. No network/DB calls by default.
- Redis is optional via `REDIS_URL`.
- TODO: Implement YAML includes, real adapters/transforms, scheduler/executor.
