"""Test-suite discovery checks."""

from pathlib import Path

from ..models import Finding


def analyze(root: Path) -> list[Finding]:
    candidates = [root / "tests", root / "test", root / "spec"]
    has_tests = any(
        path.is_dir()
        and any(item.is_file() and item.name != ".gitkeep" for item in path.rglob("*"))
        for path in candidates
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
