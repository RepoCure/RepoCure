"""Shared filesystem helpers."""

from __future__ import annotations

import os
from collections.abc import Iterator
from fnmatch import fnmatch
from pathlib import Path

from .config import Config

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


def iter_files(
    root: Path, suffixes: set[str] | None = None, config: Config | None = None
) -> Iterator[Path]:
    config = config or Config()
    yielded = 0
    for current, directories, filenames in os.walk(root):
        base = Path(current)
        directories[:] = sorted(
            item
            for item in directories
            if item not in IGNORED_DIRECTORIES
            and not _excluded((base / item).relative_to(root).as_posix() + "/", config.exclude)
        )
        for filename in sorted(filenames):
            path = base / filename
            rel = path.relative_to(root).as_posix()
            if path.is_symlink() or _excluded(rel, config.exclude):
                continue
            try:
                allowed_size = path.stat().st_size <= config.max_file_size
            except OSError:
                continue
            if allowed_size and (suffixes is None or path.suffix.lower() in suffixes):
                yield path
                yielded += 1
                if yielded >= config.max_files:
                    return


def _excluded(path: str, patterns: tuple[str, ...]) -> bool:
    normalized = path.removeprefix("./")
    return any(
        fnmatch(normalized, pattern)
        or (pattern.endswith("/**") and fnmatch(normalized.rstrip("/"), pattern[:-3]))
        for pattern in patterns
    )


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def read_text(path: Path, root: Path, config: Config) -> str | None:
    """Read a repository file only when it is safe and within configured limits."""
    try:
        rel = relative(path, root)
        if (
            path.is_symlink()
            or _excluded(rel, config.exclude)
            or path.stat().st_size > config.max_file_size
        ):
            return None
        return path.read_text(encoding="utf-8", errors="ignore")
    except (OSError, ValueError):
        return None
