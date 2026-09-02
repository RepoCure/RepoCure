import json
from pathlib import Path

from repocure.cli import main


def test_cli_writes_json_report(tmp_path: Path) -> None:
    output = tmp_path / "report.json"
    assert main(["scan", str(tmp_path), "--format", "json", "--output", str(output)]) == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert 0 <= payload["score"] <= 100


def test_fail_under_returns_failure(tmp_path: Path) -> None:
    assert main(["scan", str(tmp_path), "--fail-under", "100"]) == 1


def test_list_analyzers(capsys) -> None:
    assert main(["list-analyzers"]) == 0
    assert "security" in capsys.readouterr().out
