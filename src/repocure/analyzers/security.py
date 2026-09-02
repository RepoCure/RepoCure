"""Lightweight, offline security checks."""

from __future__ import annotations

import re
from pathlib import Path

from ..models import Finding
from ..utils import iter_files, relative

PATTERNS = [
    (
        "SEC001",
        "Possible private key",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "critical",
    ),
    (
        "SEC002",
        "Possible hard-coded secret",
        re.compile(r"(?i)(?:api[_-]?key|secret|password|token)\s*=\s*['\"][^'\"\n]{8,}['\"]"),
        "high",
    ),
    ("SEC003", "Unsafe eval usage", re.compile(r"\beval\s*\("), "high"),
    ("SEC004", "Shell execution enabled", re.compile(r"shell\s*=\s*True"), "medium"),
]


def analyze(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_files(root, {".py", ".js", ".ts", ".env", ".yml", ".yaml", ".json", ".toml"}):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for rule_id, title, pattern, severity in PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(
                    Finding(
                        rule_id,
                        title,
                        "Potentially dangerous or sensitive code was detected.",
                        severity,
                        "security",
                        relative(path, root),
                        line,
                        "Review the match and remove, replace, or protect it.",
                    )
                )
    return findings
