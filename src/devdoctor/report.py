"""Console, JSON, and Markdown report rendering."""

from __future__ import annotations

import json

from .models import ScanReport


def render_text(report: ScanReport) -> str:
    lines = [
        f"DevDoctor score: {report.score}/100 ({report.status})",
        f"Findings: {len(report.findings)}",
    ]
    for item in report.findings:
        location = f" [{item.path}{':' + str(item.line) if item.line else ''}]" if item.path else ""
        lines.append(f"- {item.severity.upper():8} {item.rule_id}: {item.title}{location}")
    return "\n".join(lines) + "\n"


def render_json(report: ScanReport) -> str:
    return json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n"


def render_markdown(report: ScanReport) -> str:
    lines = [
        "# DevDoctor Report",
        "",
        f"**Project health: {report.score}/100 — {report.status}**",
        "",
        "## Findings",
        "",
    ]
    if not report.findings:
        lines.append("No findings. Great work!")
    for item in report.findings:
        location = (
            f" (`{item.path}`" + (f":{item.line}" if item.line else "") + ")" if item.path else ""
        )
        lines.extend(
            [f"### {item.severity.upper()} — {item.title}{location}", "", item.description, ""]
        )
        if item.recommendation:
            lines.extend([f"Recommendation: {item.recommendation}", ""])
    return "\n".join(lines).rstrip() + "\n"
