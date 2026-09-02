from pathlib import Path

import pytest

from repocure.scanner import Scanner


def test_clean_minimal_project_scores_100(tmp_path: Path) -> None:
    for name in ("README.md", "LICENSE", "CONTRIBUTING.md", ".gitignore", "pyproject.toml"):
        (tmp_path / name).write_text("ok", encoding="utf-8")
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_sample.py").write_text("def test_ok(): assert True", encoding="utf-8")
    report = Scanner(tmp_path).scan()
    assert report.score == 100
    assert report.status == "healthy"


def test_security_finds_eval(tmp_path: Path) -> None:
    source = tmp_path / "app.py"
    source.write_text("eval(user_input)\n", encoding="utf-8")
    report = Scanner(tmp_path, ["security"]).scan()
    assert report.findings[0].rule_id == "SEC003"
    assert report.findings[0].line == 1


def test_unknown_analyzer_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Unknown analyzer"):
        Scanner(tmp_path, ["missing"]).scan()
