"""Public rule catalog."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Rule:
    rule_id: str
    category: str
    severity: str
    title: str


RULES = (
    Rule("SEC001", "security", "critical", "Possible private key"),
    Rule("SEC002", "security", "high", "Possible hard-coded secret"),
    Rule("SEC003", "security", "high", "Unsafe eval usage"),
    Rule("SEC004", "security", "medium", "Shell execution enabled"),
    Rule("SEC005", "security", "high", "Unsafe deserialization"),
    Rule("SEC006", "security", "medium", "Weak cryptographic hash"),
    Rule("PRF001", "performance", "low", "Deeply nested loop"),
    Rule("DEP001", "dependencies", "low", "No dependency manifest"),
    Rule("DEP002", "dependencies", "medium", "Unpinned Python dependency"),
    Rule("DCK001", "docker", "medium", "Unpinned latest image"),
    Rule("DCK002", "docker", "low", "Missing .dockerignore"),
    Rule("DCK003", "docker", "medium", "Container runs as root"),
    Rule("DOC001", "documentation", "low", "Missing README"),
    Rule("DOC002", "documentation", "low", "Missing license"),
    Rule("DOC003", "documentation", "low", "Missing contributing guide"),
    Rule("GIT001", "git", "medium", "Missing .gitignore"),
    Rule("GIT002", "git", "high", "Environment file present"),
    Rule("TST001", "tests", "medium", "No tests detected"),
    Rule("QLT001", "quality", "high", "Python syntax error"),
    Rule("QLT002", "quality", "low", "Broad exception handler"),
    Rule("CIC001", "ci", "low", "No CI workflow detected"),
    Rule("CIC002", "ci", "high", "Overly broad workflow permissions"),
)
