"""Resolve local project paths and public GitHub repository URLs."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlparse

GITHUB_PATH = re.compile(r"^/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?/?$")


class SourceError(ValueError):
    """Raised when a scan source cannot be safely resolved."""


def is_github_url(value: str) -> bool:
    parsed = urlparse(value)
    return (
        parsed.scheme == "https"
        and parsed.netloc.lower() == "github.com"
        and not parsed.params
        and not parsed.query
        and not parsed.fragment
        and bool(GITHUB_PATH.fullmatch(parsed.path))
    )


@contextmanager
def project_source(value: str) -> Iterator[tuple[Path, str]]:
    """Yield a local project directory and its user-facing source label."""
    if not value.startswith(("http://", "https://")):
        path = Path(value).expanduser().resolve()
        if not path.is_dir():
            raise SourceError(f"Project path is not a directory: {path}")
        yield path, str(path)
        return

    if not is_github_url(value):
        raise SourceError("Only HTTPS GitHub repository URLs are supported for remote scans.")
    if shutil.which("git") is None:
        raise SourceError("Git is required to scan a GitHub repository URL.")

    clone_url = value.rstrip("/")
    temporary = tempfile.TemporaryDirectory(prefix="repocure-")
    destination = Path(temporary.name) / "repository"
    environment = os.environ.copy()
    environment.update({"GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_NOSYSTEM": "1"})
    command = [
        "git",
        "-c",
        "protocol.file.allow=never",
        "clone",
        "--quiet",
        "--depth",
        "1",
        "--single-branch",
        "--no-tags",
        "--filter=blob:none",
        clone_url,
        str(destination),
    ]
    try:
        subprocess.run(
            command, check=True, timeout=120, env=environment, capture_output=True, text=True
        )
        yield destination, clone_url
    except subprocess.TimeoutExpired as error:
        raise SourceError("GitHub clone timed out after 120 seconds.") from error
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or "Git clone failed.").strip().splitlines()[-1]
        raise SourceError(f"Could not clone the GitHub repository: {detail}") from error
    finally:
        temporary.cleanup()
