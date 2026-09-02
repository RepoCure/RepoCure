"""Command-line interface for RepoCure."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .analyzers import BUILTIN_ANALYZERS
from .config import CONFIG_TEMPLATE, load_config
from .report import render_html, render_json, render_markdown, render_sarif, render_text
from .rules import RULES
from .scanner import Scanner
from .source import SourceError, project_source
from .ui import print_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repocure", description="Diagnose the health of a software project."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list-analyzers", help="list available analyzers")
    commands.add_parser("rules", help="list every built-in rule")
    init = commands.add_parser("init", help="create a .repocure.toml configuration")
    init.add_argument("path", nargs="?", default=".")
    init.add_argument("--force", action="store_true")
    scan = commands.add_parser("scan", help="scan a project")
    scan.add_argument("source", nargs="?", default=".", help="local path or HTTPS GitHub URL")
    scan.add_argument(
        "--format", choices=("text", "json", "markdown", "html", "sarif"), default="text"
    )
    scan.add_argument("--output", type=Path)
    scan.add_argument("--fail-under", type=int, choices=range(101))
    scan.add_argument("--analyzer", action="append", dest="analyzers")
    scan.add_argument("--exclude", action="append", default=[], help="additional glob to exclude")
    scan.add_argument("--disable-rule", action="append", default=[], help="rule ID to suppress")
    scan.add_argument("--config", type=Path, help="path to a TOML configuration file")
    scan.add_argument("--no-color", action="store_true", help="disable colors in terminal output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "list-analyzers":
        print("\n".join(BUILTIN_ANALYZERS))
        return 0
    if args.command == "rules":
        for rule in RULES:
            print(f"{rule.rule_id}\t{rule.severity}\t{rule.category}\t{rule.title}")
        return 0
    if args.command == "init":
        destination = Path(args.path).expanduser().resolve() / ".repocure.toml"
        if destination.exists() and not args.force:
            print(f"error: Configuration already exists: {destination}", file=sys.stderr)
            return 2
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(CONFIG_TEMPLATE, encoding="utf-8")
        print(f"Created {destination}")
        return 0
    try:
        with project_source(args.source) as (path, label):
            explicit = args.config.expanduser().resolve() if args.config else None
            config = load_config(path, explicit).merged(
                exclude=args.exclude, disabled_rules=args.disable_rule, fail_under=args.fail_under
            )
            report = Scanner(path, args.analyzers, source=label, config=config).scan()
    except (ValueError, SourceError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    renderers = {
        "text": render_text,
        "json": render_json,
        "markdown": render_markdown,
        "html": render_html,
        "sarif": render_sarif,
    }
    if args.format == "text" and not args.output and sys.stdout.isatty():
        print_report(report, no_color=args.no_color)
    else:
        output = renderers[args.format](report)
        if args.output:
            args.output.write_text(output, encoding="utf-8")
        else:
            print(output, end="")
    return int(config.fail_under > 0 and report.score < config.fail_under)


if __name__ == "__main__":
    raise SystemExit(main())
