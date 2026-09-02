"""Command-line interface for RepoCure."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .analyzers import BUILTIN_ANALYZERS
from .report import render_html, render_json, render_markdown, render_sarif, render_text
from .scanner import Scanner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repocure", description="Diagnose the health of a software project."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list-analyzers", help="list available analyzers")
    scan = commands.add_parser("scan", help="scan a project")
    scan.add_argument("path", nargs="?", default=".")
    scan.add_argument(
        "--format", choices=("text", "json", "markdown", "html", "sarif"), default="text"
    )
    scan.add_argument("--output", type=Path)
    scan.add_argument("--fail-under", type=int, choices=range(101))
    scan.add_argument("--analyzer", action="append", dest="analyzers")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "list-analyzers":
        print("\n".join(BUILTIN_ANALYZERS))
        return 0
    try:
        report = Scanner(args.path, args.analyzers).scan()
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    renderers = {
        "text": render_text,
        "json": render_json,
        "markdown": render_markdown,
        "html": render_html,
        "sarif": render_sarif,
    }
    output = renderers[args.format](report)
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return int(args.fail_under is not None and report.score < args.fail_under)


if __name__ == "__main__":
    raise SystemExit(main())
