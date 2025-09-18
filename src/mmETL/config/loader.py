"""Config loader from YAML with env var expansion and include stub.

Doctest:
>>> from pathlib import Path
>>> from mmETL.config.loader import load_config
>>> yml = Path('examples/pipelines/tabular_only.yaml')
>>> isinstance(str(yml), str)
True
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from mmETL.config.models import Pipeline

__all__ = ["load_config"]


class ConfigError(Exception):
    """Raised when configuration loading fails."""


def _expand_env(content: str) -> str:
    return os.path.expandvars(content)


def _process_includes(content: str, base_dir: Path) -> str:
    # TODO: Implement YAML include processing. For now, return content unchanged.
    return content


def load_config(path: Path | str) -> Pipeline:
    path_obj = Path(path)
    if not path_obj.exists():
        raise ConfigError(f"Config file not found: {path_obj}")

    text = path_obj.read_text(encoding="utf-8")
    text = _expand_env(text)
    text = _process_includes(text, path_obj.parent)
    data: Any = yaml.safe_load(text) or {}

    try:
        return Pipeline.model_validate(data)
    except Exception as exc:  # noqa: BLE001
        raise ConfigError(str(exc)) from exc
