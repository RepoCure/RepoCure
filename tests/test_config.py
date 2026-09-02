from pathlib import Path

import pytest

from repocure.config import Config, load_config
from repocure.scanner import Scanner


def test_loads_project_config(tmp_path: Path) -> None:
    (tmp_path / ".repocure.toml").write_text(
        '[repocure]\nfail_under = 85\nexclude = ["fixtures/**"]\ndisabled_rules = ["TST001"]\n',
        encoding="utf-8",
    )
    config = load_config(tmp_path)
    assert config.fail_under == 85
    assert "fixtures/**" in config.exclude
    assert config.disabled_rules == {"TST001"}


def test_rejects_unknown_config_option(tmp_path: Path) -> None:
    (tmp_path / ".repocure.toml").write_text("[repocure]\nsurprise = true\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Unknown configuration"):
        load_config(tmp_path)


def test_disabled_rule_is_removed(tmp_path: Path) -> None:
    report = Scanner(
        tmp_path, ["tests"], config=Config(disabled_rules=frozenset({"TST001"}))
    ).scan()
    assert report.findings == []


def test_excluded_source_is_not_analyzed(tmp_path: Path) -> None:
    generated = tmp_path / "generated"
    generated.mkdir()
    (generated / "broken.py").write_text("this is invalid python !", encoding="utf-8")
    report = Scanner(tmp_path, ["quality"], config=Config(exclude=("generated/**",))).scan()
    assert report.findings == []
