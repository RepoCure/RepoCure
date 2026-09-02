# Contributing

Thank you for helping improve RepoCure.

1. Fork the repository and create a focused branch.
2. Install development dependencies with `python -m pip install -e '.[dev]'`.
3. Add or update tests for every behavior change.
4. Run `ruff check .` and `pytest`.
5. Open a pull request describing the problem and solution.

New analyzers should be deterministic, offline by default, safe on untrusted source trees, and return actionable findings.

