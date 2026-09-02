"""Built-in RepoCure analyzers."""

from .dependencies import analyze as dependencies
from .docker import analyze as docker
from .documentation import analyze as documentation
from .git import analyze as git
from .performance import analyze as performance
from .security import analyze as security
from .tests import analyze as tests

BUILTIN_ANALYZERS = {
    "security": security,
    "performance": performance,
    "dependencies": dependencies,
    "git": git,
    "docker": docker,
    "documentation": documentation,
    "tests": tests,
}
__all__ = ["BUILTIN_ANALYZERS"]
