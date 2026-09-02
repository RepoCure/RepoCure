"""Core data models used by scanners and reporters."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

Severity = Literal["critical", "high", "medium", "low", "info"]


@dataclass(frozen=True, slots=True)
class Finding:
    rule_id: str
    title: str
    description: str
    severity: Severity
    category: str
    path: str | None = None
    line: int | None = None
    recommendation: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class ScanReport:
    root: Path
    findings: list[Finding] = field(default_factory=list)
    analyzers: list[str] = field(default_factory=list)
    source: str | None = None
    files_scanned: int = 0
    duration_ms: int = 0
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def score(self) -> int:
        weights = {"critical": 30, "high": 15, "medium": 7, "low": 3, "info": 0}
        return max(0, 100 - sum(weights[item.severity] for item in self.findings))

    @property
    def status(self) -> str:
        return (
            "healthy" if self.score >= 80 else "needs-attention" if self.score >= 50 else "critical"
        )

    @property
    def severity_counts(self) -> dict[str, int]:
        counts = Counter(item.severity for item in self.findings)
        return {name: counts.get(name, 0) for name in ("critical", "high", "medium", "low", "info")}

    @property
    def category_counts(self) -> dict[str, int]:
        return dict(sorted(Counter(item.category for item in self.findings).items()))

    def to_dict(self) -> dict[str, object]:
        return {
            "source": self.source or str(self.root),
            "score": self.score,
            "status": self.status,
            "generated_at": self.generated_at,
            "duration_ms": self.duration_ms,
            "files_scanned": self.files_scanned,
            "severity_counts": self.severity_counts,
            "category_counts": self.category_counts,
            "analyzers": self.analyzers,
            "findings": [item.to_dict() for item in self.findings],
        }
