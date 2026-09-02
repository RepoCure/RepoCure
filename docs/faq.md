# FAQ

## Does RepoCure upload my code?

No. Analysis runs locally. A GitHub URL requires network access only to clone that repository; RepoCure does not send the cloned source anywhere else.

## Is every security finding a vulnerability?

No. Findings are review signals and may include false positives.

## Can I suppress an accepted finding?

Yes. Add its stable ID to `disabled_rules` in `.repocure.toml`.

## Can RepoCure scan private repositories?

Scan a private repository after cloning it locally. Remote URL mode deliberately disables interactive credentials.
