"""CI/CD configuration checks."""

from __future__ import annotations

import re
from pathlib import Path

from ..config import Config
from ..models import Finding
from ..utils import read_text


def analyze(root: Path, config: Config) -> list[Finding]:
    workflow_dir = root / ".github" / "workflows"
    workflows = (
        list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
        if workflow_dir.is_dir()
        else []
    )
    if not workflows:
        return [
            Finding(
                "CIC001",
                "No CI workflow detected",
                "No GitHub Actions workflow was found.",
                "low",
                "ci",
                recommendation="Add automated linting and tests for pushes and pull requests.",
            )
        ]
    findings: list[Finding] = []
    for path in workflows:
        text = read_text(path, root, config)
        if text is None:
            continue
        match = re.search(r"(?m)^permissions:\s*write-all\s*$", text)
        if match:
            findings.append(
                Finding(
                    "CIC002",
                    "Overly broad workflow permissions",
                    "The workflow grants write access to every available scope.",
                    "high",
                    "ci",
                    path.relative_to(root).as_posix(),
                    text.count("\n", 0, match.start()) + 1,
                    "Grant only the job-level permissions that are required.",
                )
            )
    return findings
