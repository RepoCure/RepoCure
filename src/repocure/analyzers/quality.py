"""Python maintainability and correctness checks."""

from __future__ import annotations

import ast
from pathlib import Path

from ..config import Config
from ..models import Finding
from ..utils import iter_files, relative


def analyze(root: Path, config: Config) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_files(root, {".py"}, config):
        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text)
        except SyntaxError as error:
            findings.append(
                Finding(
                    "QLT001",
                    "Python syntax error",
                    error.msg,
                    "high",
                    "quality",
                    relative(path, root),
                    error.lineno,
                    "Fix the syntax error before shipping or running this module.",
                )
            )
            continue
        except (OSError, UnicodeError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                findings.append(
                    Finding(
                        "QLT002",
                        "Broad exception handler",
                        "A bare except may hide cancellation, shutdown, or programming errors.",
                        "low",
                        "quality",
                        relative(path, root),
                        node.lineno,
                        "Catch the narrowest expected exception type.",
                    )
                )
    return findings
