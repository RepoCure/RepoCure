"""RepoCure configuration loading and validation."""

from __future__ import annotations

import sys
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

DEFAULT_EXCLUDES = (
    ".git/**",
    ".venv/**",
    "venv/**",
    "node_modules/**",
    "dist/**",
    "build/**",
    "**/__pycache__/**",
)


@dataclass(frozen=True, slots=True)
class Config:
    exclude: tuple[str, ...] = DEFAULT_EXCLUDES
    disabled_rules: frozenset[str] = frozenset()
    fail_under: int = 0
    max_file_size: int = 1_000_000
    max_files: int = 20_000

    def merged(
        self,
        *,
        exclude: list[str] | None = None,
        disabled_rules: list[str] | None = None,
        fail_under: int | None = None,
    ) -> Config:
        return replace(
            self,
            exclude=self.exclude + tuple(exclude or ()),
            disabled_rules=self.disabled_rules | frozenset(disabled_rules or ()),
            fail_under=self.fail_under if fail_under is None else fail_under,
        )


def load_config(root: Path, explicit: Path | None = None) -> Config:
    path = explicit or root / ".repocure.toml"
    if not path.exists():
        if explicit:
            raise ValueError(f"Configuration file not found: {path}")
        return Config()
    try:
        with path.open("rb") as handle:
            payload: dict[str, Any] = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ValueError(f"Invalid RepoCure configuration: {error}") from error
    values = payload.get("repocure", payload)
    allowed = {"exclude", "disabled_rules", "fail_under", "max_file_size", "max_files"}
    unknown = set(values) - allowed
    if unknown:
        raise ValueError(f"Unknown configuration option(s): {', '.join(sorted(unknown))}")
    config = Config(
        exclude=DEFAULT_EXCLUDES + tuple(_string_list(values.get("exclude", []), "exclude")),
        disabled_rules=frozenset(_string_list(values.get("disabled_rules", []), "disabled_rules")),
        fail_under=_integer(values.get("fail_under", 0), "fail_under", 0, 100),
        max_file_size=_integer(
            values.get("max_file_size", 1_000_000), "max_file_size", 1, 50_000_000
        ),
        max_files=_integer(values.get("max_files", 20_000), "max_files", 1, 200_000),
    )
    return config


def _string_list(value: object, name: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"Configuration option '{name}' must be a list of strings.")
    return value


def _integer(value: object, name: str, minimum: int, maximum: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not minimum <= value <= maximum:
        raise ValueError(f"Configuration option '{name}' must be between {minimum} and {maximum}.")
    return value


CONFIG_TEMPLATE = """# RepoCure project configuration
[repocure]
fail_under = 80
exclude = ["vendor/**", "generated/**"]
disabled_rules = []
max_file_size = 1000000
max_files = 20000
"""
