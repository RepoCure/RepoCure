"""Console, JSON, and Markdown report rendering."""

from __future__ import annotations

import json
from html import escape

from .models import ScanReport


def render_text(report: ScanReport) -> str:
    lines = [
        f"RepoCure score: {report.score}/100 ({report.status})",
        f"Source: {report.source or report.root}",
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
        "# RepoCure Report",
        "",
        f"**Project health: {report.score}/100 — {report.status}**",
        "",
        f"Source: `{report.source or report.root}`",
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


def render_html(report: ScanReport) -> str:
    rows = (
        "".join(
            "<tr>"
            f"<td class='{escape(item.severity)}'>{escape(item.severity.upper())}</td>"
            f"<td>{escape(item.rule_id)}</td><td>{escape(item.title)}</td>"
            f"<td>{escape(item.path or '—')}{':' + str(item.line) if item.line else ''}</td>"
            f"<td>{escape(item.recommendation or 'Review the finding.')}</td></tr>"
            for item in report.findings
        )
        or "<tr><td colspan='5'>No findings. Great work!</td></tr>"
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RepoCure report</title><style>
body{{font:16px system-ui,sans-serif;max-width:1100px;margin:40px auto;padding:0 20px;color:#172033}}
.score{{font-size:3rem;font-weight:800;color:#2563eb}}table{{border-collapse:collapse;width:100%}}
th,td{{padding:12px;border-bottom:1px solid #dbe3ef;text-align:left;vertical-align:top}}
.critical,.high{{color:#b91c1c;font-weight:700}}.medium{{color:#a16207;font-weight:700}}.low{{color:#0369a1;font-weight:700}}
</style></head><body><h1>RepoCure Report</h1><div class="score">{report.score}/100</div>
<p>Source: <strong>{escape(report.source or str(report.root))}</strong></p>
<p>Status: <strong>{escape(report.status)}</strong> · Findings: {len(report.findings)}</p>
<table><thead><tr><th>Severity</th><th>Rule</th><th>Finding</th><th>Location</th><th>Recommendation</th></tr></thead>
<tbody>{rows}</tbody></table></body></html>\n"""


def render_sarif(report: ScanReport) -> str:
    levels = {
        "critical": "error",
        "high": "error",
        "medium": "warning",
        "low": "note",
        "info": "note",
    }
    rules: dict[str, dict[str, object]] = {}
    results: list[dict[str, object]] = []
    for item in report.findings:
        rules[item.rule_id] = {
            "id": item.rule_id,
            "name": item.title,
            "shortDescription": {"text": item.description},
            "help": {"text": item.recommendation or item.description},
        }
        result: dict[str, object] = {
            "ruleId": item.rule_id,
            "level": levels[item.severity],
            "message": {"text": item.title},
        }
        if item.path:
            result["locations"] = [
                {
                    "physicalLocation": {
                        "artifactLocation": {"uri": item.path},
                        "region": {"startLine": item.line or 1},
                    }
                }
            ]
        results.append(result)
    payload = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "RepoCure",
                        "version": "1.1.0",
                        "rules": list(rules.values()),
                    }
                },
                "results": results,
            }
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
