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

Scan any public GitHub repository directly:

```bash
repocure scan https://github.com/OWNER/REPOSITORY
```

RepoCure performs a shallow clone into a temporary directory, scans it locally, and removes the temporary copy automatically.

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

Scan GitHub and generate a shareable HTML report:

```bash
repocure scan https://github.com/OWNER/REPOSITORY --format html --output report.html
```

## Status

RepoCure findings are review signals and may include false positives; they are not proof of a vulnerability.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security reports should follow [SECURITY.md](SECURITY.md).

## License

MIT
