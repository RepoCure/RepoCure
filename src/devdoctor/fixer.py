"""Safe fix planning for future automatic remediation."""

from .models import ScanReport


def planned_fixes(report: ScanReport) -> list[str]:
    return [item.recommendation for item in report.findings if item.recommendation]
