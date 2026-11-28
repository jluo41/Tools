"""Make a topic follow its Studio Type, for any type (hai-studio A06, A10; ref/studio-type.md).

    <host venv python> type_follow.py new <type> <topic>             start a topic from a type, named (`skills`)
    <host venv python> type_follow.py check <Block or topic> [...]   hold topics against the type each names
    <host venv python> type_follow.py follow <topic> [...]           build a topic as its type says, then check it

`new` writes the topic's studio-views.json with the type's own top buttons and left tabs, each still showing the
type's requirement page, and names the type (`check_type`). The topic then reads as its type does; every part is
replaced by the real thing, one at a time. It refuses a topic that already has a views file.

`follow` is the one command for "make this topic follow its type": it runs the builders the type names on its
`build:` line (hai-studio scripts, each given the topic), rebuilds the topic's Check view, then prints what `check`
prints. A builder that fails stops that topic.

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
import re
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
    from host_paths import bootstrap
    bootstrap()
    from live.studio_types import type_home
    type_topic = type_home(named, root)
    shape = shape_of(type_topic) if type_topic else []
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
    inside = (type_topic.relative_to(root).as_posix() if type_topic.is_relative_to(root) else "\0") + "/"
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
            if str(item.get("path", "")).startswith(inside) or "/delivery/requirements/" in str(item.get("path", "")):
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


def new(type_topic: Path, topic: Path, root: Path = SPACE) -> dict[Path, str]:
    """{file: text} of a new topic of the type: its views file with the type's own buttons and tabs, each showing
    its requirement, and the type named by its name. Where the type has pages of its own (the blueprint) they are
    shown; where only its elements.md is kept (the delivered copy) the requirement pages are written into the
    topic's own delivery/requirements/."""
    from host_paths import bootstrap
    bootstrap()
    from live.studio_types import elements_of, type_name
    out, own = {}, type_topic / "studio-views.json"
    if own.is_file() and type_topic.resolve().is_relative_to(root):
        views = [v for v in json.loads(own.read_text(encoding="utf-8")).get("views", []) if v.get("name") != "Check"]
    else:
        from type_requirements import page, slug
        els, views = elements_of(type_topic), []
        rel = topic.resolve().relative_to(root).as_posix()
        for view in shape_of(type_topic):
            items = []
            for el in [e for e in els if e["view"] == view["name"] and (e["tab"] is not None) == bool(view["tabs"])]:
                name = slug(view["name"]) + ("--" + slug(el["name"]) if view["tabs"] else "") + ".html"
                out[topic / "delivery/requirements" / name] = page(el)
                items.append({"name": el["name"], "path": f"{rel}/delivery/requirements/{name}"})
            views.append({"name": view["name"], "items": items})
    out[topic / "studio-views.json"] = json.dumps({"check_type": type_name(type_topic), "views": views},
                                                  indent=2, ensure_ascii=False) + "\n"
    return out


def builders_of(topic: Path, root: Path = SPACE) -> list[Path] | None:
    """The scripts the topic's type names on its `build:` line, in order; None when the topic names no type."""
    from host_paths import bootstrap
    bootstrap()
    from live.studio_types import elements_of, type_home
    try:
        named = json.loads((topic / "studio-views.json").read_text(encoding="utf-8")).get("check_type")
    except (OSError, ValueError):
        return None
    home = type_home(named, root)
    if home is None:
        return None
    line = next((e.get("build", "") for e in elements_of(home)), "")
    here = Path(__file__).resolve().parent                             # a type's own script first, then a shared one
    own = here.parent / "gallery" / re.sub(r"^s\d\d-studio-type-", "", home.name) / "scripts"
    return [own / n.strip() if (own / n.strip()).is_file() else here / n.strip() for n in line.split(",") if n.strip()]


def follow(topic: Path, root: Path = SPACE) -> int:
    """Build the topic as its type says, rebuild its Check view, report. 1 when a builder fails or a part is off."""
    import subprocess
    scripts = builders_of(topic, root)
    if scripts is None:
        print(f"— {topic.name}: names no type")
        return 1
    here = Path(__file__).resolve().parent
    for script in scripts:
        if not script.is_file() or not (script.parent == here or script.parent.parent.parent == here.parent / "gallery"):
            print(f"❗ {topic.name}: the type names a builder that is not a hai-studio script: {script.name}")
            return 1
        done = subprocess.run([sys.executable, str(script), topic.relative_to(root).as_posix()], capture_output=True, text=True)
        if done.returncode:
            print(f"❗ {topic.name}: {script.name} failed: {(done.stderr or done.stdout).strip().splitlines()[-1]}")
            return 1
    from check_views import build
    for path, text in build(topic, None, root).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    bad, open_ = problems(topic, root)
    for line in bad:
        print(f"❗ {topic.name}: {line}")
    for line in open_:
        print(f"⬜ {topic.name}: {line}")
    print(f"{'❗' if bad else '✅'} {topic.name}" + (f"  (built by {', '.join(s.name for s in scripts)})" if scripts else ""))
    return 1 if bad else 0


def topics_of(path: Path) -> list[Path]:
    if (path / "studio-views.json").is_file() or path.name[:1] == "s" and path.name[1:3].isdigit():
        return [path]
    return sorted(p for p in path.glob("s[0-9][0-9]-*") if p.is_dir())


def main(argv: list[str]) -> int:
    if len(argv) == 3 and argv[0] == "new":
        from host_paths import bootstrap
        bootstrap()
        from live.studio_types import type_home
        type_topic, topic = type_home(argv[1], SPACE), (SPACE / argv[2]).resolve()
        if type_topic is None or not topic.is_dir() or (topic / "studio-views.json").exists():
            print(f"❗ {topic.name}: " + (f"no Studio Type {argv[1]!r}" if type_topic is None else "no such topic folder"
                                          if not topic.is_dir() else "has a views file already"))
            return 1
        for path, text in new(type_topic, topic).items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        from check_views import build
        for path, text in build(topic, None, SPACE).items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        print(f"Wrote {topic.name}: the buttons and tabs of {type_topic.name}; each part still shows its requirement")
        return 0
    if len(argv) >= 2 and argv[0] == "follow":
        return max(follow((SPACE / a).resolve()) for a in argv[1:])
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
