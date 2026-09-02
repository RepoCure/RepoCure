"""Documentation completeness checks."""

from pathlib import Path

from ..models import Finding


def analyze(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    checks = [
        (
            "README.md",
            "DOC001",
            "README is missing",
            "Add a README with purpose, installation, and usage.",
        ),
        ("LICENSE", "DOC002", "License is missing", "Choose and add an open-source license."),
        (
            "CONTRIBUTING.md",
            "DOC003",
            "Contributing guide is missing",
            "Document how contributors can participate.",
        ),
    ]
    for filename, rule_id, title, recommendation in checks:
        if not (root / filename).is_file():
            findings.append(
                Finding(
                    rule_id,
                    title,
                    f"{filename} was not found at the project root.",
                    "low",
                    "documentation",
                    recommendation=recommendation,
                )
            )
    return findings
