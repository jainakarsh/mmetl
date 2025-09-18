from pathlib import Path

from typer.testing import CliRunner

from mmETL.cli.main import app

runner = CliRunner()


def test_cli_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "validate" in result.stdout


def test_validate_ok(tmp_path: Path) -> None:
    (tmp_path / "p.yaml").write_text(
        """
name: p
resources: {}
tasks:
  - id: a
    op: noop
  - id: b
    op: noop
    inputs: [a]
        """,
        encoding="utf-8",
    )
    result = runner.invoke(app, ["validate", str(tmp_path / "p.yaml")])
    assert result.exit_code == 0


def test_validate_fail(tmp_path: Path) -> None:
    (tmp_path / "p.yaml").write_text("{}", encoding="utf-8")
    result = runner.invoke(app, ["validate", str(tmp_path / "p.yaml")])
    assert result.exit_code != 0
