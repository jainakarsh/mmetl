"""mmETL command line interface.

Provides user-facing commands: validate, dry-run, run, status.

Doctest:
>>> from pathlib import Path
>>> isinstance(Path('.').name, str)
True
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from mmETL.config.loader import load_config
from mmETL.core.executor import Executor
from mmETL.core.planner import plan_pipeline
from mmETL.observability.redis_client import get_redis_client

__all__ = ["app", "main"]

app = typer.Typer(add_completion=False, help="mmETL pipeline CLI")
console = Console()


@app.command()
def validate(config: Path) -> None:
    """Validate a pipeline YAML config.

    Exits 0 on valid, non-zero on invalid.
    """
    try:
        _ = load_config(config)
        console.print("Config valid.")
    except Exception as exc:  # noqa: BLE001 - surfaced to CLI
        typer.secho(f"Invalid config: {exc}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command("dry-run")
def dry_run(config: Path) -> None:
    """Parse config and print a human-readable plan (topological order)."""
    try:
        pipeline = load_config(config)
        dag = plan_pipeline(pipeline)
        order = dag.topological_order()
        console.print("Execution order:")
        for idx, node in enumerate(order, start=1):
            console.print(f"  {idx}. {node}")
    except Exception as exc:  # noqa: BLE001
        typer.secho(f"Failed to plan: {exc}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command()
def run(config: Path, run_id: Optional[str] = typer.Option(None, help="Run identifier")) -> None:
    """Execute a pipeline. Heavy execution is stubbed; just logs the plan."""
    try:
        pipeline = load_config(config)
        dag = plan_pipeline(pipeline)
        executor = Executor()
        executor.execute(dag, run_id=run_id)
        console.print("Run submitted (stub).")
    except Exception as exc:  # noqa: BLE001
        typer.secho(f"Run failed: {exc}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command()
def status(run_id: str) -> None:
    """Fetch run status from Redis (or no-op stub)."""
    client = get_redis_client()
    if client is None:
        console.print("Redis not configured. Status unavailable.")
        raise typer.Exit(code=0)

    key = f"mmetl:run:{run_id}:status"
    value = client.get(key)
    console.print(value.decode() if value else "unknown")


def main() -> None:
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
