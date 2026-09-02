from pathlib import Path

import pytest

from repocure.source import SourceError, is_github_url, project_source


@pytest.mark.parametrize(
    "url",
    ["https://github.com/RepoCure/RepoCure", "https://github.com/owner/repo.git"],
)
def test_accepts_repository_urls(url: str) -> None:
    assert is_github_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "http://github.com/owner/repo",
        "https://example.com/owner/repo",
        "https://github.com/owner",
        "https://user@github.com/owner/repo",
        "https://github.com/owner/repo?ref=main",
        "https://github.com/owner/repo#readme",
    ],
)
def test_rejects_unsafe_or_invalid_urls(url: str) -> None:
    assert not is_github_url(url)


def test_local_source(tmp_path: Path) -> None:
    with project_source(str(tmp_path)) as (path, label):
        assert path == tmp_path.resolve()
        assert label == str(tmp_path.resolve())


def test_rejects_non_github_remote() -> None:
    with (
        pytest.raises(SourceError, match="Only HTTPS GitHub"),
        project_source("https://example.com/owner/repo"),
    ):
        pass
