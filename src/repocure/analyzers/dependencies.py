"""Dependency hygiene checks."""

from pathlib import Path

from ..models import Finding


def analyze(root: Path) -> list[Finding]:
    manifests = [
        "pyproject.toml",
        "requirements.txt",
        "package.json",
        "Cargo.toml",
        "go.mod",
        "pom.xml",
    ]
    if any((root / name).exists() for name in manifests):
        return []
    return [
        Finding(
            "DEP001",
            "No dependency manifest found",
            "RepoCure could not identify a supported dependency manifest.",
            "low",
            "dependencies",
            recommendation="Add the dependency manifest used by the project.",
        )
    ]
