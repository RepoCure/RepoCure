from pathlib import Path

from repocure.models import Finding, ScanReport
from repocure.report import render_html, render_json, render_markdown, render_sarif, render_text


def test_all_renderers_include_score() -> None:
    report = ScanReport(Path("."), [Finding("X001", "Example", "Details", "low", "test")], ["test"])
    assert "97/100" in render_text(report)
    assert '"score": 97' in render_json(report)
    assert "97/100" in render_markdown(report)
    assert "97/100" in render_html(report)
    assert '"version": "2.1.0"' in render_sarif(report)
