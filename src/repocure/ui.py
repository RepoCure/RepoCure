"""Professional terminal rendering powered by Rich."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .models import ScanReport

COLORS = {
    "critical": "bold white on red",
    "high": "bold red",
    "medium": "bold yellow",
    "low": "cyan",
    "info": "dim",
}


def print_report(report: ScanReport, *, no_color: bool = False) -> None:
    console = Console(no_color=no_color)
    score_color = "green" if report.score >= 80 else "yellow" if report.score >= 50 else "red"
    heading = Text.assemble(
        ("RepoCure  ", "bold bright_blue"),
        (f"{report.score}/100", f"bold {score_color}"),
        (f"  {report.status}", "dim"),
    )
    summary = f"Source: {report.source or report.root}\nScanned {report.files_scanned:,} files in {report.duration_ms:,} ms · {len(report.findings)} findings"
    console.print(Panel(summary, title=heading, border_style=score_color, padding=(1, 2)))
    if not report.findings:
        console.print("[bold green]✓ No findings. Your repository looks healthy.[/]")
        return
    table = Table(show_header=True, header_style="bold", box=None, pad_edge=False)
    table.add_column("Severity", width=10)
    table.add_column("Rule", width=8)
    table.add_column("Finding", ratio=2)
    table.add_column("Location", ratio=2)
    for item in report.findings:
        location = (item.path or "—") + (f":{item.line}" if item.line else "")
        table.add_row(
            Text(item.severity.upper(), style=COLORS[item.severity]),
            item.rule_id,
            item.title,
            location,
        )
    console.print(table)
    console.print(
        "\n[dim]Run with --format html for an interactive report or --format sarif for GitHub Code Scanning.[/]"
    )
