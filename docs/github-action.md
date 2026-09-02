# GitHub Action

RepoCure can enforce repository health on every pull request.

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

To publish findings in GitHub Code Scanning, generate SARIF and upload it with `github/codeql-action/upload-sarif@v4`. Public repositories support third-party SARIF uploads.

