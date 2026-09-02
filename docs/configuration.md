# Configuration

RepoCure loads `.repocure.toml` from the scanned project root. Command-line options override file values.

```toml
[repocure]
fail_under = 80
exclude = ["vendor/**", "fixtures/**", "generated/**"]
disabled_rules = ["QLT002"]
max_file_size = 1000000
max_files = 20000
```

| Option | Purpose | Default |
|---|---|---|
| `fail_under` | Return exit code 1 below this score; 0 disables the gate | `0` |
| `exclude` | Additional glob patterns | `[]` |
| `disabled_rules` | Accepted or irrelevant rule IDs | `[]` |
| `max_file_size` | Maximum bytes read from one file | `1000000` |
| `max_files` | Maximum files considered per analyzer | `20000` |

Run `repocure init` to generate a safe starter configuration and `repocure rules` to inspect available rule IDs.

