"""Reuse the Studio Type placeholder rule, including its current scope."""
from pathlib import Path

from checks.common.paths import owner
from checks.common.results import Result


def check(topic: Path) -> list[Result]:
    module = owner("placeholder_check")
    bad = {(path, name) for path, name in module.names(topic) if module.SLOT.fullmatch(name)}
    if bad:
        return [Result("FAIL", "placeholders", path, f"write the slot as 〈{name}〉")
                for path, name in sorted(bad)]
    return [Result("PASS", "placeholders", topic, "no bare numbered type slots")]
