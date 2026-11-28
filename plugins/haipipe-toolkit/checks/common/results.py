"""Small, explicit results; a skipped or unsupported target is never a pass."""
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Result:
    status: str
    rule: str
    path: Path
    detail: str


def exit_code(results: list[Result]) -> int:
    if not results or any(r.status in {"ERROR", "UNCOVERED"} for r in results):
        return 2
    return int(any(r.status != "PASS" for r in results))


def display(result: Result, root: Path) -> str:
    try:
        path = result.path.relative_to(root)
    except ValueError:
        path = result.path
    return f"{result.status} [{result.rule}] {path}: {result.detail}"
