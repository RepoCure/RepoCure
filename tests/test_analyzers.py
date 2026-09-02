from pathlib import Path

from repocure.scanner import Scanner


def scan_rule(tmp_path: Path, analyzer: str) -> set[str]:
    return {item.rule_id for item in Scanner(tmp_path, [analyzer]).scan().findings}


def test_quality_detects_syntax_error(tmp_path: Path) -> None:
    (tmp_path / "broken.py").write_text("def broken(:\n", encoding="utf-8")
    assert "QLT001" in scan_rule(tmp_path, "quality")


def test_security_detects_unsafe_deserialization(tmp_path: Path) -> None:
    (tmp_path / "unsafe.py").write_text("import pickle\npickle.loads(data)\n", encoding="utf-8")
    assert "SEC005" in scan_rule(tmp_path, "security")


def test_dependencies_detect_unpinned_requirement(tmp_path: Path) -> None:
    (tmp_path / "requirements.txt").write_text("requests\n", encoding="utf-8")
    assert "DEP002" in scan_rule(tmp_path, "dependencies")


def test_ci_detects_write_all(tmp_path: Path) -> None:
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "ci.yml").write_text("permissions: write-all\n", encoding="utf-8")
    assert "CIC002" in scan_rule(tmp_path, "ci")
