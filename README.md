# mmETL

**Minimal multimodal ETL framework (MVP)**

mmETL lets you define config-driven pipelines across tabular, graph, vector, and document modalities, with reproducible runs, pushdown to best-of-breed engines, and built-in status/metrics.

This repo is an MVP scaffold: functional CLI, schema + DAG planner, stubs for caching/observability, and tests.

## Installation (Dev Mode)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
```

## CLI Usage

```bash
mmetl --help
mmetl validate examples/pipelines/tabular_only.yaml
mmetl dry-run examples/pipelines/tabular_only.yaml
mmetl run examples/pipelines/tabular_only.yaml
mmetl status some-run-id
```



## Package Overview

### 📦 CLI Package

**Purpose:** The public face of mmETL. Turns a pipeline YAML into concrete actions: validate configs, compile DAGs, echo execution plans, and fetch run status. Keeps UX and pretty output but delegates logic to config and core.

**Architecture:** Presentation/entry layer. Only layer end-users touch (`mmetl` or `python -m mmETL`).

**Scripts:**
- `cli/main.py` — Typer app with commands validate, dry_run, run, status
- `__main__.py` — Enables `python -m mmETL`
- `cli/__init__.py` — Package marker

---

### ⚙️ Config Package

**Purpose:** Source-of-truth for pipeline structure. Loads YAML, expands `${ENV}`, supports `!include`, and validates to strong Pydantic models. Centralizes parsing/validation.

**Architecture:** Parsing & validation layer: converts untrusted text into a typed Pipeline.

**Scripts:**
- `schema.py` — Pipeline, TaskSpec models
- `loader.py` — YAML loader with env expansion + include
- `resolver.py` — Validates/normalizes raw dict → Pipeline
- `__init__.py` — Re-exports entry points

---

### 🧠 Core Package

**Purpose:** Minimal planning and (stub) execution engine. Builds DAGs, detects cycles, provides a stub executor, and manages transform registry.

**Architecture:** Domain/engine layer: config → executable plan, independent of IO.

**Scripts:**
- `dag.py` — DAG + CycleError; topological_sort()
- `planner.py` — Convert Pipeline → DAG
- `executor.py` — Echo plan stub
- `registry.py` — Transform registry (@register_transform)
- `__init__.py` — Re-exports

---

### 📊 Observability Package

**Purpose:** Lightweight metrics/status plumbing with Redis stub fallback. Exposes hooks for status, heartbeats, events—usable in dev without Redis.

**Architecture:** Cross-cutting ops layer: CLI/executors call it, but no business logic.

**Scripts:**
- `metrics.py` — get_redis(): Redis client or stub
- `heartbeat.py` — Stubbed run heartbeat
- `events.py` — Stubbed structured events
- `__init__.py` — Re-exports

---

### 💾 Cache Package

**Purpose:** Idempotency primitives: fingerprints, watermarks, and a stub store. Keeps caching isolated from planning/execution.

**Architecture:** Cross-cutting infra: used by executors/transforms to skip work safely.

**Scripts:**
- `fingerprints.py` — fingerprint_pipeline(Pipeline) -> str
- `watermarks.py` — Stubs for get/set_watermark
- `store.py` — Placeholder cache store API
- `__init__.py` — Re-exports

---

### 🛠️ Utils Package

**Purpose:** Reusable helpers (hashing, env, time, retry) with no external deps. Keeps business code clean and avoids circulars.

**Architecture:** Support library: shared across config/core/observability.

**Scripts:**
- `hashing.py` — sha256_hex
- `env.py` — Env var wrapper
- `time.py` — now_ms()
- `retry.py` — @retry(times, delay) decorator
- `__init__.py` — Package marker

---

## Examples & Tests

**Purpose:** Examples demonstrate YAML schema; tests encode acceptance criteria (CLI help/validate, DAG ordering/cycles, fingerprint determinism).

**Scripts:**
- `examples/pipelines/tabular_only.yaml` — Minimal 2-task pipeline
- `tests/unit/test_cli.py` — CLI smoke tests
- `tests/unit/test_dag.py` — DAG cycle detection
- `tests/unit/test_fingerprints.py` — Fingerprint determinism

---

## Roadmap

- [ ] Implement real transforms/adapters
- [ ] Flesh out caching (watermarks, store)
- [ ] Add cross-modality primitives
- [ ] Extend executor with pushdown (DuckDB, Neo4j, etc)
- [ ] Improve observability (structured events, lineage)

---

## Reading Order Guide

Here's a suggested order to explore the codebase so you understand the trajectory and flow:

| Step | Module / File | What to Read / Focus On | Why It Matters |
|------|---------------|-------------------------|----------------|
| 1 | `examples/pipelines/tabular_only.yaml` | YAML shape: tasks, dependencies, params | Baseline for what valid config looks like |
| 2 | `src/mmETL/config/schema.py` & `loader.py` | Model structure + how YAML becomes typed objects | Ensures future schema changes stay consistent |
| 3 | `src/mmETL/core/planner.py` & `dag.py` | How task dependencies map → graph, cycle detection, ordering | Core deterministic behavior of pipelines |
| 4 | `src/mmETL/cli/main.py` | How commands (validate, dry-run, run, status) invoke config & core | Entry points users interact with |
| 5 | `src/mmETL/cache/fingerprints.py` | How pipeline signature is computed | Key for idempotency & skipping work |
| 6 | `src/mmETL/observability/metrics.py` | Redis vs stub behavior for status/telemetry | Critical for monitoring & status reporting |
| 7 | `tests/unit/*` | Especially DAG + fingerprint tests | Verify acceptance criteria and invariants |
