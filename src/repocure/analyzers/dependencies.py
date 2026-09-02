"""Dependency hygiene checks."""

from pathlib import Path

from ..config import Config
from ..models import Finding
from ..utils import read_text


def analyze(root: Path, config: Config) -> list[Finding]:
    manifests = [
        "pyproject.toml",
        "requirements.txt",
        "package.json",
        "Cargo.toml",
        "go.mod",
        "pom.xml",
    ]
    findings: list[Finding] = []
    if not any((root / name).exists() for name in manifests):
        findings.append(
            Finding(
                "DEP001",
                "No dependency manifest found",
                "RepoCure could not identify a supported dependency manifest.",
                "low",
                "dependencies",
                recommendation="Add the dependency manifest used by the project.",
            )
        )
    requirements = root / "requirements.txt"
    if requirements.is_file():
        contents = read_text(requirements, root, config)
        for number, raw in enumerate((contents or "").splitlines(), 1):
            line = raw.strip()
            if (
                line
                and not line.startswith(("#", "-", "http"))
                and not any(operator in line for operator in ("==", "~=", ">=", "<=", " @ "))
            ):
                findings.append(
                    Finding(
                        "DEP002",
                        "Unpinned Python dependency",
                        f"Dependency '{line}' has no version constraint.",
                        "medium",
                        "dependencies",
                        "requirements.txt",
                        number,
                        "Add a compatible or exact version constraint.",
                    )
                )
    return findings
