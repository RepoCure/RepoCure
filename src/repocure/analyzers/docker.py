"""Docker configuration checks."""

from pathlib import Path

from ..config import Config
from ..models import Finding
from ..utils import read_text


def analyze(root: Path, config: Config) -> list[Finding]:
    dockerfile = root / "Dockerfile"
    if not dockerfile.exists():
        return []
    text = read_text(dockerfile, root, config)
    if text is None:
        return []
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
    if not any(line.strip().upper().startswith("USER ") for line in text.splitlines()):
        findings.append(
            Finding(
                "DCK003",
                "Container may run as root",
                "No USER instruction was found in the Dockerfile.",
                "medium",
                "docker",
                "Dockerfile",
                recommendation="Create and switch to a non-root runtime user.",
            )
        )
    return findings
