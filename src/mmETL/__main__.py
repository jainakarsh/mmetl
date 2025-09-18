"""Module entry point to launch the CLI via `python -m mmETL`."""
from __future__ import annotations

from mmETL.cli.main import app


def main() -> None:
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
