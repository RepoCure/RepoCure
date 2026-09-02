"""Project scan orchestration."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from .analyzers import BUILTIN_ANALYZERS
from .models import Finding, ScanReport


class Scanner:
    def __init__(self, root: str | Path, analyzers: Iterable[str] | None = None) -> None:
        self.root = Path(root).expanduser().resolve()
        self.analyzer_names = list(analyzers or BUILTIN_ANALYZERS)

    def scan(self) -> ScanReport:
        if not self.root.is_dir():
            raise ValueError(f"Project path is not a directory: {self.root}")
        unknown = set(self.analyzer_names) - set(BUILTIN_ANALYZERS)
        if unknown:
            raise ValueError(f"Unknown analyzer(s): {', '.join(sorted(unknown))}")
        findings: list[Finding] = []
        for name in self.analyzer_names:
            findings.extend(BUILTIN_ANALYZERS[name](self.root))
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        findings.sort(key=lambda item: (order[item.severity], item.rule_id, item.path or ""))
        return ScanReport(self.root, findings, self.analyzer_names.copy())
