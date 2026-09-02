"""Core data models used by scanners and reporters."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
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

    @property
    def score(self) -> int:
        weights = {"critical": 30, "high": 15, "medium": 7, "low": 3, "info": 0}
        return max(0, 100 - sum(weights[item.severity] for item in self.findings))

    @property
    def status(self) -> str:
        return (
            "healthy" if self.score >= 80 else "needs-attention" if self.score >= 50 else "critical"
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "root": str(self.root),
            "score": self.score,
            "status": self.status,
            "analyzers": self.analyzers,
            "findings": [item.to_dict() for item in self.findings],
        }
