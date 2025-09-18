"""mmETL Typer CLI (validate, dry_run, run, status).

Doctest:
>>> from typer.testing import CliRunner
>>> from mmETL.cli.main import app
>>> CliRunner().invoke(app, ["--help"]).exit_code == 0
True
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from mmETL.config.loader import load_yaml
from mmETL.config.resolver import resolve_pipeline
from mmETL.core.executor import Executor
from mmETL.core.planner import plan_pipeline
from mmETL.observability.metrics import get_redis

__all__ = ["app"]

app = typer.Typer(add_completion=False, help="mmETL pipeline CLI")
_console = Console()


@app.command()
def validate(config: Path) -> None:
    """Validate a pipeline YAML config and print name on success."""
    try:
        data = load_yaml(config)
        pipeline = resolve_pipeline(data)
        _console.print(f"OK: {pipeline.name}")
    except Exception as exc:  # noqa: BLE001 - surfaced to CLI
        typer.secho(f"Invalid config: {exc}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command()
def dry_run(config: Path) -> None:
    """Compile DAG and print topological order."""
    try:
        data = load_yaml(config)
        pipeline = resolve_pipeline(data)
        dag = plan_pipeline(pipeline)
        order = dag.topological_sort()
        table = Table(title="Execution Order")
        table.add_column("#", justify="right")
        table.add_column("Task")
        for idx, node in enumerate(order, start=1):
            table.add_row(str(idx), node)
        _console.print(table)
    except Exception as exc:  # noqa: BLE001
        typer.secho(f"Failed to plan: {exc}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command()
def run(config: Path, run_id: Optional[str] = typer.Option(None, "--run-id", help="Run id")) -> None:
    """Plan and echo the execution (stub)."""
    data = load_yaml(config)
    pipeline = resolve_pipeline(data)
    dag = plan_pipeline(pipeline)
    executor = Executor()
    executor.plan_and_echo(dag, run_id=run_id)


@app.command()
def status(run_id: str) -> None:
    """Fetch run status from Redis (or no-op stub)."""
    client = get_redis()
    key = f"mmetl:run:{run_id}:status"
    value = client.get(key)
    _console.print(value if isinstance(value, str) else (value.decode() if value else "unknown"))
