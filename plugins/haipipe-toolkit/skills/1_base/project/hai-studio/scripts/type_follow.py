"""Make a topic follow its Studio Type, for any type (hai-studio A06, A10; ref/studio-type.md).

    <host venv python> type_follow.py new <type topic> <topic>       start a topic from a type
    <host venv python> type_follow.py check <Block or topic> [...]   hold topics against the type each names

`new` writes the topic's studio-views.json with the type's own top buttons and left tabs, each still showing the
type's requirement page, and names the type (`check_type`). The topic then reads as its type does; every part is
replaced by the real thing, one at a time. It refuses a topic that already has a views file.

`check` reads only the type's `elements.md` and the topic's views file, so a type written tomorrow is checked with no
new code. It reports, per topic:

    no top button X            the type lists X (and gives it no `when:`), the topic lacks it
    top button X is not in the type
    X: no left tab Y           the same, one level down
    X: left tab Y is not in the type
    X is out of order

and, as ⬜ lines that do not fail (the topic follows its type, a part is not done):

    X › Y still shows the requirement     a part started by `new` and not replaced yet
    X: a name in 〈 〉          a name the topic has not settled

A name the type writes in 〈 〉 is a slot: zero or more real names stand there. A part with a `when:` line may be
absent. The managed Check button is never held against the type. Exit 1 on any ❗.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SPACE = next(p for p in Path(__file__).resolve().parents if (p / "plugins" / "haipipe-toolkit").is_dir())
sys.path.insert(0, str(SPACE / "plugins/haipipe-toolkit/servers/_host"))
sys.path.insert(0, str(Path(__file__).resolve().parent))


def _slot(name: str) -> bool:
    return "〈" in name


def shape_of(type_topic: Path) -> list[dict]:
    """The type's top buttons, each with its left tabs: [{name, slot, optional, tabs: [{name, slot, optional}]}].
    A group whose entries carry `mark:` names rows of a real page, not a view, and is left out."""
    from host_paths import bootstrap
    bootstrap()
    from live.studio_types import elements_of
    els, out = elements_of(type_topic), []
    for view in [e for e in els if e["tab"] is None]:
        tabs = [e for e in els if e["view"] == view["name"] and e["tab"] is not None]
        if any(e.get("mark") for e in tabs):
            continue
        out.append({"name": view["name"], "slot": _slot(view["name"]), "optional": bool(view.get("when")),
                    "tabs": [{"name": t["name"], "slot": _slot(t["name"]), "optional": bool(t.get("when"))} for t in tabs]})
    return out


def _ordered(names: list[str], order: list[str]) -> bool:
    seen = [order.index(n) for n in names if n in order]
    return seen == sorted(seen)


def problems(topic: Path, root: Path = SPACE) -> tuple[list[str], list[str]] | None:
    """(what keeps the topic from following the type it names, what it has not filled in yet); None when it names
    no type. The first list empty means it follows."""
    try:
        data = json.loads((topic / "studio-views.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    named = data.get("check_type")
    if not named:
        return None
    type_topic = (root / named).resolve()
    shape = shape_of(type_topic)
    if not shape:
        return [f"its type {Path(named).name} has no elements.md to follow"], []
    if type_topic == topic.resolve():
        return [], []
    todo = []
    views = [v for v in data.get("views", []) if v.get("name") != "Check"]
    names = [v["name"] for v in views]
    fixed = {s["name"]: s for s in shape if not s["slot"]}
    slots = [s for s in shape if s["slot"]]
    out = [f"no top button {n}" for n, s in fixed.items() if n not in names and not s["optional"]]
    if not _ordered(names, [s["name"] for s in shape if not s["slot"]]):
        out.append("its top buttons are out of the type's order")
    inside = type_topic.relative_to(root).as_posix() + "/"
    for view in views:
        name = view["name"]
        kind = fixed.get(name) or (slots[0] if slots else None)
        if kind is None:
            out.append(f"top button {name} is not in the type")
            continue
        if _slot(name):
            todo.append(f"{name}: a name in 〈 〉, not settled")
        items = [i for i in view.get("items", []) if isinstance(i, dict)]
        tabs = [i.get("name", "") for i in items]
        for item in items:
            if str(item.get("path", "")).startswith(inside):
                todo.append(f"{name} › {item.get('name')} still shows the requirement")
            elif _slot(item.get("name", "")):
                todo.append(f"{name}: left tab {item.get('name')} is a name in 〈 〉, not settled")
        if not kind["tabs"]:
            continue
        own = {t["name"]: t for t in kind["tabs"] if not t["slot"]}
        out += [f"{name}: no left tab {n}" for n, t in own.items() if n not in tabs and not t["optional"]]
        if not any(t["slot"] for t in kind["tabs"]):
            out += [f"{name}: left tab {n} is not in the type" for n in tabs if n not in own]
        if not _ordered(tabs, [t["name"] for t in kind["tabs"] if not t["slot"]]):
            out.append(f"{name}: its left tabs are out of the type's order")
    return out, todo


def new(type_topic: Path, topic: Path, root: Path = SPACE) -> str:
    """The views file of a new topic of the type: the type's own buttons and tabs, each showing its requirement."""
    data = json.loads((type_topic / "studio-views.json").read_text(encoding="utf-8"))
    views = [v for v in data.get("views", []) if v.get("name") != "Check"]
    return json.dumps({"check_type": type_topic.resolve().relative_to(root).as_posix(), "views": views},
                      indent=2, ensure_ascii=False) + "\n"


def topics_of(path: Path) -> list[Path]:
    if (path / "studio-views.json").is_file() or path.name[:1] == "s" and path.name[1:3].isdigit():
        return [path]
    return sorted(p for p in path.glob("s[0-9][0-9]-*") if p.is_dir())


def main(argv: list[str]) -> int:
    if len(argv) == 3 and argv[0] == "new":
        type_topic, topic = (SPACE / argv[1]).resolve(), (SPACE / argv[2]).resolve()
        out = topic / "studio-views.json"
        if out.exists() or not topic.is_dir() or not (type_topic / "studio-views.json").is_file():
            print(f"❗ {topic.name}: " + ("has a views file already" if out.exists() else "no such topic folder"
                                          if not topic.is_dir() else f"{type_topic.name} has no views file"))
            return 1
        out.write_text(new(type_topic, topic), encoding="utf-8")
        from check_views import build
        for path, text in build(topic, None, SPACE).items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        print(f"Wrote {topic.name}: the buttons and tabs of {type_topic.name}; each part still shows its requirement")
        return 0
    if len(argv) < 2 or argv[0] != "check":
        print(__doc__)
        return 2
    bad = 0
    for topic in [t for a in argv[1:] for t in topics_of((SPACE / a).resolve())]:
        found = problems(topic)
        if found is None:
            print(f"— {topic.name}: names no type")
            continue
        for line in found[0]:
            print(f"❗ {topic.name}: {line}")
        for line in found[1]:
            print(f"⬜ {topic.name}: {line}")
        print(f"{'❗' if found[0] else '✅'} {topic.name}")
        bad += bool(found[0])
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
