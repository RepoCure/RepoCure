from pathlib import Path

from devdoctor.models import Finding, ScanReport
from devdoctor.report import render_json, render_markdown, render_text


def test_all_renderers_include_score() -> None:
    report = ScanReport(Path("."), [Finding("X001", "Example", "Details", "low", "test")], ["test"])
    assert "97/100" in render_text(report)
    assert '"score": 97' in render_json(report)
    assert "97/100" in render_markdown(report)
