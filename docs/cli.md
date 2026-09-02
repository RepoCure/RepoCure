# CLI reference

`repocure scan [SOURCE]` scans a local directory or public HTTPS GitHub repository URL. Use `--format text|json|markdown|html|sarif`, `--output FILE`, `--fail-under SCORE`, or repeat `--analyzer NAME` to select checks.

```bash
repocure scan https://github.com/OWNER/REPOSITORY
```

Remote scans require Git. RepoCure uses a shallow clone, disables interactive credential prompts, scans locally, and deletes its temporary directory when finished. Run `repocure list-analyzers` to list built-in checks.
