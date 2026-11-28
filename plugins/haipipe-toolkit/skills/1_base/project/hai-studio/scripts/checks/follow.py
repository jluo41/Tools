"""A topic's top buttons and left tabs are the ones its Studio Type lists (hai-studio type_follow.py)."""
from pathlib import Path

from checks.results import Result
from checks.freshness import owner, using_root


def check(topic: Path, data: dict, root: Path) -> list[Result]:
    if not data.get("check_type"):
        return []
    module = owner("type_follow")
    with using_root(module, root):
        bad, todo = module.problems(topic, root)
    if bad:
        return [Result("FAIL", "follows-type", topic / "studio-views.json", line) for line in bad]
    detail = "top buttons and left tabs are the type's"
    return [Result("PASS", "follows-type", topic, detail + (f"; {len(todo)} parts not filled in yet" if todo else ""))]
