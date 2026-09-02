"""Simple source-level performance signals."""

from __future__ import annotations

import ast
from pathlib import Path

from ..config import Config
from ..models import Finding
from ..utils import iter_files, relative


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.depth = 0
        self.lines: list[int] = []

    def visit_For(self, node: ast.For) -> None:
        self.depth += 1
        if self.depth >= 3:
            self.lines.append(node.lineno)
        self.generic_visit(node)
        self.depth -= 1

    visit_AsyncFor = visit_For


def analyze(root: Path, config: Config) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_files(root, {".py"}, config):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError, UnicodeError):
            continue
        visitor = Visitor()
        visitor.visit(tree)
        for line in visitor.lines:
            findings.append(
                Finding(
                    "PRF001",
                    "Deeply nested loop",
                    "Three or more nested loops may scale poorly.",
                    "low",
                    "performance",
                    relative(path, root),
                    line,
                    "Review the algorithmic complexity and consider indexing or vectorization.",
                )
            )
    return findings
