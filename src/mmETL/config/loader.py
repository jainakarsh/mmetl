"""YAML loader with ${ENV} expansion and simple !include support.

Doctest:
>>> from pathlib import Path
>>> from mmETL.config.loader import load_yaml
>>> isinstance(load_yaml(Path('examples/pipelines/tabular_only.yaml')), dict)
True
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

__all__ = ["load_yaml"]


class LoaderError(Exception):
    """Raised when YAML loading fails."""


def _expand_env(text: str) -> str:
    return os.path.expandvars(text)


def _construct_include(loader: yaml.Loader, node: yaml.Node) -> Any:  # type: ignore[type-arg]
    rel_path = loader.construct_scalar(node)  # type: ignore[attr-defined]
    base_dir = Path(getattr(loader.stream, "name", ".")).parent  # type: ignore[attr-defined]
    include_path = (base_dir / rel_path).resolve()
    content = include_path.read_text(encoding="utf-8")
    return yaml.safe_load(_expand_env(content))


yaml.SafeLoader.add_constructor("!include", _construct_include)  # type: ignore[arg-type]


def load_yaml(path: Path | str) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise LoaderError(f"Config not found: {p}")
    text = p.read_text(encoding="utf-8")
    text = _expand_env(text)
    data = yaml.safe_load(text) or {}
    if not isinstance(data, dict):
        raise LoaderError("Root of YAML must be a mapping")
    return data
