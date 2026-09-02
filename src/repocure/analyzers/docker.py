"""Docker configuration checks."""

from pathlib import Path

from ..models import Finding


def analyze(root: Path) -> list[Finding]:
    dockerfile = root / "Dockerfile"
    if not dockerfile.exists():
        return []
    text = dockerfile.read_text(encoding="utf-8", errors="ignore")
    findings: list[Finding] = []
    if ":latest" in text:
        findings.append(
            Finding(
                "DCK001",
                "Unpinned latest image",
                "The Dockerfile explicitly uses a mutable latest tag.",
                "medium",
                "docker",
                "Dockerfile",
                recommendation="Pin the base image to a stable version or digest.",
            )
        )
    if not (root / ".dockerignore").exists():
        findings.append(
            Finding(
                "DCK002",
                ".dockerignore is missing",
                "The build context may include unnecessary or sensitive files.",
                "low",
                "docker",
                recommendation="Add a .dockerignore file.",
            )
        )
    return findings
