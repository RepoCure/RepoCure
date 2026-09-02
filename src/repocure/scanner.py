"""Project scan orchestration."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from time import perf_counter

from .analyzers import BUILTIN_ANALYZERS
from .config import Config
from .models import Finding, ScanReport
from .utils import iter_files


class Scanner:
    def __init__(
        self,
        root: str | Path,
        analyzers: Iterable[str] | None = None,
        source: str | None = None,
        config: Config | None = None,
    ) -> None:
        self.root = Path(root).expanduser().resolve()
        self.analyzer_names = list(analyzers or BUILTIN_ANALYZERS)
        self.source = source
        self.config = config or Config()

    def scan(self) -> ScanReport:
        if not self.root.is_dir():
            raise ValueError(f"Project path is not a directory: {self.root}")
        unknown = set(self.analyzer_names) - set(BUILTIN_ANALYZERS)
        if unknown:
            raise ValueError(f"Unknown analyzer(s): {', '.join(sorted(unknown))}")
        started = perf_counter()
        files_scanned = sum(1 for _ in iter_files(self.root, config=self.config))
        findings: list[Finding] = []
        for name in self.analyzer_names:
            findings.extend(BUILTIN_ANALYZERS[name](self.root, self.config))
        findings = [item for item in findings if item.rule_id not in self.config.disabled_rules]
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        findings.sort(key=lambda item: (order[item.severity], item.rule_id, item.path or ""))
        duration_ms = round((perf_counter() - started) * 1000)
        return ScanReport(
            self.root, findings, self.analyzer_names.copy(), self.source, files_scanned, duration_ms
        )
