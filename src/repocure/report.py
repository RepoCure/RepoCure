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
            f"<tr data-severity='{escape(item.severity)}' data-search='{escape((item.rule_id + ' ' + item.title + ' ' + (item.path or '')).lower())}'>"
            f"<td><span class='pill {escape(item.severity)}'>{escape(item.severity.upper())}</span></td>"
            f"<td>{escape(item.rule_id)}</td><td>{escape(item.title)}</td>"
            f"<td>{escape(item.path or '—')}{':' + str(item.line) if item.line else ''}</td>"
            f"<td>{escape(item.recommendation or 'Review the finding.')}</td></tr>"
            for item in report.findings
        )
        or "<tr><td colspan='5'>No findings. Great work!</td></tr>"
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RepoCure · Repository Health Report</title><style>
:root{{--bg:#08111f;--card:#111d30;--line:#26364f;--text:#e8eef8;--muted:#8fa3bf;--brand:#5eead4;--blue:#60a5fa}}
*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at 15% 0,#152a46 0,var(--bg) 42%);color:var(--text);font:14px Inter,ui-sans-serif,system-ui,sans-serif}}
main{{max-width:1240px;margin:auto;padding:48px 24px 80px}}header{{display:flex;justify-content:space-between;gap:24px;align-items:flex-end;margin-bottom:28px}}
.brand{{font-size:13px;letter-spacing:.18em;text-transform:uppercase;color:var(--brand);font-weight:800}}h1{{font-size:clamp(30px,5vw,56px);margin:8px 0 4px;letter-spacing:-.04em}}.source{{color:var(--muted);word-break:break-all}}
.score{{font-size:58px;font-weight:900;letter-spacing:-.06em;color:var(--brand)}}.score small{{font-size:18px;color:var(--muted);letter-spacing:0}}
.grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:24px 0}}.card{{background:linear-gradient(145deg,#15243a,var(--card));border:1px solid var(--line);border-radius:16px;padding:18px}}
.card b{{display:block;font-size:26px;margin-top:6px}}.label{{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.08em}}
.toolbar{{display:flex;flex-wrap:wrap;gap:10px;margin:28px 0 14px}}input,button{{border:1px solid var(--line);border-radius:10px;background:#0c1728;color:var(--text);padding:10px 13px}}
input{{flex:1;min-width:220px}}button{{cursor:pointer}}button.active{{border-color:var(--brand);color:var(--brand)}}
.table-wrap{{overflow:auto;background:var(--card);border:1px solid var(--line);border-radius:16px}}table{{border-collapse:collapse;width:100%;min-width:900px}}th,td{{padding:14px 16px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}th{{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.08em}}
.pill{{display:inline-block;border-radius:99px;padding:4px 8px;font-size:11px;font-weight:800}}.critical,.high{{color:#fecaca;background:#7f1d1d}}.medium{{color:#fde68a;background:#713f12}}.low{{color:#bae6fd;background:#075985}}.info{{color:#cbd5e1;background:#334155}}
footer{{color:var(--muted);margin-top:18px}}@media(max-width:800px){{header{{display:block}}.grid{{grid-template-columns:repeat(2,1fr)}}}}
</style></head><body><main><header><div><div class="brand">RepoCure v2</div><h1>Repository health</h1><div class="source">{escape(report.source or str(report.root))}</div></div><div class="score">{report.score}<small>/100</small></div></header>
<section class="grid"><div class="card"><span class="label">Status</span><b>{escape(report.status)}</b></div><div class="card"><span class="label">Files</span><b>{report.files_scanned:,}</b></div><div class="card"><span class="label">Findings</span><b>{len(report.findings)}</b></div><div class="card"><span class="label">High risk</span><b>{report.severity_counts["critical"] + report.severity_counts["high"]}</b></div><div class="card"><span class="label">Duration</span><b>{report.duration_ms:,} ms</b></div></section>
<div class="toolbar"><input id="search" placeholder="Search rule, finding, or file…" aria-label="Search findings"><button class="active" data-filter="all">All</button><button data-filter="critical">Critical</button><button data-filter="high">High</button><button data-filter="medium">Medium</button><button data-filter="low">Low</button></div>
<div class="table-wrap"><table><thead><tr><th>Severity</th><th>Rule</th><th>Finding</th><th>Location</th><th>Recommendation</th></tr></thead><tbody>{rows}</tbody></table></div>
<footer>Generated {escape(report.generated_at)} · Offline report · No source code was uploaded</footer></main>
<script>const rows=[...document.querySelectorAll('tbody tr')],search=document.querySelector('#search'),buttons=[...document.querySelectorAll('button[data-filter]')];let filter='all';function apply(){{const q=search.value.toLowerCase();rows.forEach(r=>r.hidden=!((filter==='all'||r.dataset.severity===filter)&&(r.dataset.search||'').includes(q)))}}search.addEventListener('input',apply);buttons.forEach(b=>b.addEventListener('click',()=>{{filter=b.dataset.filter;buttons.forEach(x=>x.classList.toggle('active',x===b));apply()}}));</script></body></html>\n"""


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
                        "version": "2.0.0",
                        "rules": list(rules.values()),
                    }
                },
                "results": results,
            }
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
