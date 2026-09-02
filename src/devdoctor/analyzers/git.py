"""Git repository hygiene checks."""

from pathlib import Path

from ..models import Finding


def analyze(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not (root / ".gitignore").is_file():
        findings.append(
            Finding(
                "GIT001",
                ".gitignore is missing",
                "Generated files and secrets may be committed accidentally.",
                "medium",
                "git",
                recommendation="Add a .gitignore appropriate for the project stack.",
            )
        )
    if (root / ".env").is_file():
        findings.append(
            Finding(
                "GIT002",
                ".env exists in the project",
                "Confirm that the environment file is ignored and not committed.",
                "high",
                "git",
                ".env",
                recommendation="Keep secrets out of Git and provide .env.example instead.",
            )
        )
    return findings
