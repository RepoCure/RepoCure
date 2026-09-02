"""Shared filesystem helpers."""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

IGNORED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
}


def iter_files(root: Path, suffixes: set[str] | None = None) -> Iterator[Path]:
    for current, directories, filenames in os.walk(root):
        directories[:] = sorted(item for item in directories if item not in IGNORED_DIRECTORIES)
        for filename in sorted(filenames):
            path = Path(current) / filename
            if suffixes is None or path.suffix.lower() in suffixes:
                yield path


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()
