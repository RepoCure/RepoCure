<p align="center"><img src="https://raw.githubusercontent.com/RepoCure/RepoCure/main/assets/banner.svg" alt="RepoCure — Diagnose your repository. Cure what matters." width="100%"></p>

<p align="center">
  <a href="https://pypi.org/project/repocure/"><img src="https://img.shields.io/pypi/v/repocure?color=2dd4bf" alt="PyPI version"></a>
  <a href="https://pypi.org/project/repocure/"><img src="https://img.shields.io/pypi/pyversions/repocure" alt="Python versions"></a>
  <a href="https://github.com/RepoCure/RepoCure/actions/workflows/tests.yml"><img src="https://github.com/RepoCure/RepoCure/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/RepoCure/RepoCure" alt="MIT license"></a>
</p>

RepoCure is a local-first repository health scanner for developers, maintainers, and CI pipelines. It turns security, quality, dependency, Docker, Git, documentation, testing, and CI signals into one clear score and actionable report.

```console
$ repocure scan https://github.com/OWNER/REPOSITORY
╭────────────────────────── RepoCure  92/100  healthy ──────────────────────────╮
│ Source: https://github.com/OWNER/REPOSITORY                                    │
│ Scanned 184 files in 241 ms · 1 finding                                        │
╰─────────────────────────────────────────────────────────────────────────────────╯
Severity   Rule     Finding                       Location
MEDIUM     SEC004   Shell execution enabled        tools/build.py:42
```

## Why RepoCure?

- **One command:** scan a local directory or public GitHub URL.
- **Local-first:** source code is analyzed on your machine and never sent to RepoCure.
- **CI-native:** stable exit codes, SARIF, JSON, Markdown, HTML, and a reusable GitHub Action.
- **Actionable:** every finding includes a rule, severity, location, and recommendation.
- **Configurable:** exclude generated code, disable accepted rules, and enforce a score threshold.
- **Safe by design:** HTTPS-only remote scans, shallow clones, file limits, no symlink traversal, and no code execution.

## Install

```bash
python -m pip install --upgrade repocure
```

Requires Python 3.10+ and Git for remote repository scans.

## Scan

```bash
# Current directory
repocure scan .

# Public GitHub repository
repocure scan https://github.com/OWNER/REPOSITORY

# Interactive standalone dashboard
repocure scan . --format html --output repocure-report.html

# GitHub Code Scanning / other SARIF consumers
repocure scan . --format sarif --output repocure.sarif

# Enforce quality in CI
repocure scan . --fail-under 80
```

## Configure

Create a starter configuration:

```bash
repocure init
```

`.repocure.toml`:

```toml
[repocure]
fail_under = 80
exclude = ["vendor/**", "generated/**"]
disabled_rules = ["QLT002"]
max_file_size = 1000000
max_files = 20000
```

CLI flags override configuration values:

```bash
repocure scan . --exclude "fixtures/**" --disable-rule QLT002
repocure rules
repocure list-analyzers
```

## GitHub Action

```yaml
name: Repository health
on: [push, pull_request]
permissions:
  contents: read
jobs:
  repocure:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: RepoCure/RepoCure@v2
        with:
          fail-under: "80"
```

See the [GitHub Action guide](docs/github-action.md) for SARIF integration.

## Reports

| Format | Best for |
|---|---|
| Rich terminal | Fast local feedback |
| HTML | Searchable, shareable offline dashboard |
| SARIF | GitHub Code Scanning and security platforms |
| JSON | Automation and integrations |
| Markdown | Pull requests and project artifacts |
| Text | Logs and minimal terminals |

## Built-in analyzers

`security` · `quality` · `dependencies` · `performance` · `docker` · `git` · `documentation` · `tests` · `ci`

RepoCure findings are review signals, not proof of a vulnerability. Review results in context before changing production code.

## Community

- [Documentation](docs/installation.md)
- [Roadmap](docs/roadmap.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Code of conduct](CODE_OF_CONDUCT.md)

Released under the [MIT License](LICENSE).
