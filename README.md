# RepoCure

> Diagnose your repository. Cure what matters.

RepoCure is a fast, local-first Python CLI that scans a software project, assigns a health score, and produces actionable findings without uploading source code.

## Features

- Security checks for likely secrets, private keys, unsafe `eval`, and shell execution.
- Dependency, documentation, tests, Git, Docker, and Python performance checks.
- Text, JSON, Markdown, standalone HTML, and SARIF reports.
- CI-friendly score thresholds and analyzer selection.
- Offline by default: source code never leaves your machine.

## Quick start

```bash
pip install repocure
repocure scan .
```

Generate a shareable report:

```bash
repocure scan . --format html --output repocure-report.html
```

Fail CI when the score is below 80:

```bash
repocure scan . --fail-under 80
```

Run one analyzer:

```bash
repocure scan . --analyzer security
```

## Status

RepoCure findings are review signals and may include false positives; they are not proof of a vulnerability.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security reports should follow [SECURITY.md](SECURITY.md).

## License

MIT
