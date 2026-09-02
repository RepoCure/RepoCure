# Architecture

The CLI creates a `Scanner`, which invokes registered analyzers. Each analyzer returns immutable `Finding` objects. A `ScanReport` calculates the health score, and renderers serialize the result without mutating the scanned project.

