# Architecture

The CLI resolves a local path or HTTPS GitHub source, loads a validated `Config`, and creates a `Scanner`. The scanner invokes deterministic analyzers that return immutable `Finding` objects. A `ScanReport` calculates health, severity, category, file-count, and timing metrics. Rich and file renderers present the same report model without mutating the scanned project.

Remote repositories are shallow-cloned to an isolated temporary directory with interactive Git authentication disabled. RepoCure does not import or execute scanned source code, does not follow symlinks, limits file sizes and counts, and removes the temporary directory after scanning.
