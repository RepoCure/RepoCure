"""Lightweight, offline security checks."""

from __future__ import annotations

import ast
import re
from pathlib import Path

from ..models import Finding
from ..utils import iter_files, relative

TEXT_PATTERNS = [
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
]
NON_PYTHON_PATTERNS = [
    ("SEC003", "Unsafe eval usage", re.compile(r"\beval\s*\("), "high"),
    ("SEC004", "Shell execution enabled", re.compile(r"shell\s*=\s*true", re.IGNORECASE), "medium"),
]


def _finding(rule_id: str, title: str, severity: str, path: Path, root: Path, line: int) -> Finding:
    return Finding(
        rule_id,
        title,
        "Potentially dangerous or sensitive code was detected.",
        severity,
        "security",
        relative(path, root),
        line,
        "Review the match and remove, replace, or protect it.",
    )


def _pattern_findings(text: str, path: Path, root: Path, patterns: list[tuple]) -> list[Finding]:
    findings: list[Finding] = []
    for rule_id, title, pattern, severity in patterns:
        findings.extend(
            _finding(rule_id, title, severity, path, root, text.count("\n", 0, match.start()) + 1)
            for match in pattern.finditer(text)
        )
    return findings


def _python_findings(text: str, path: Path, root: Path) -> list[Finding]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    findings: list[Finding] = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "eval"
        ):
            findings.append(
                _finding("SEC003", "Unsafe eval usage", "high", path, root, node.lineno)
            )
        if isinstance(node, ast.Call) and any(
            keyword.arg == "shell"
            and isinstance(keyword.value, ast.Constant)
            and keyword.value.value is True
            for keyword in node.keywords
        ):
            findings.append(
                _finding("SEC004", "Shell execution enabled", "medium", path, root, node.lineno)
            )
    return findings


def analyze(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    suffixes = {".py", ".js", ".ts", ".env", ".yml", ".yaml", ".json", ".toml"}
    for path in iter_files(root, suffixes):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        findings.extend(_pattern_findings(text, path, root, TEXT_PATTERNS))
        extra = (
            _python_findings(text, path, root)
            if path.suffix == ".py"
            else _pattern_findings(text, path, root, NON_PYTHON_PATTERNS)
        )
        findings.extend(extra)
    return findings
