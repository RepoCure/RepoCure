"""Test-suite discovery checks."""

from pathlib import Path

from ..config import Config
from ..models import Finding
from ..utils import iter_files, relative


def analyze(root: Path, config: Config) -> list[Finding]:
    test_directories = {"tests", "test", "spec"}
    has_tests = any(
        relative(path, root).split("/", 1)[0] in test_directories and path.name != ".gitkeep"
        for path in iter_files(root, config=config)
    )
    if has_tests:
        return []
    return [
        Finding(
            "TST001",
            "No tests detected",
            "No populated conventional test directory was found.",
            "medium",
            "tests",
            recommendation="Add automated tests under tests/ and run them in CI.",
        )
    ]
