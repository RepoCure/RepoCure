# DevDoctor

> Your project's personal doctor.

DevDoctor is a fast, dependency-free Python CLI that scans a software project, assigns a health score, and produces actionable findings.

## Features

- Security checks for likely secrets, private keys, unsafe `eval`, and shell execution.
- Dependency, documentation, tests, Git, Docker, and Python performance checks.
- Text, JSON, and Markdown reports.
- CI-friendly score thresholds and analyzer selection.
- Offline by default: source code never leaves your machine.

## Quick start

```bash
pip install -e .
devdoctor scan .
```

Generate a shareable report:

```bash
devdoctor scan . --format markdown --output REPORT.md
```

Fail CI when the score is below 80:

```bash
devdoctor scan . --fail-under 80
```

Run one analyzer:

```bash
devdoctor scan . --analyzer security
```

## Status

DevDoctor is currently an alpha MVP. Findings are signals that require developer review; they are not proof of a vulnerability.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security reports should follow [SECURITY.md](SECURITY.md).

## License

MIT

