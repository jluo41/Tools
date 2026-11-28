"""Write a Skills topic's studio-views.json from its skills' own folders (hai-studio A08, ref/skills-topic.md):
one top button per skill; on the left the skill's whole top level under its real names: SKILL.md, CONSTITUTION.md,
ref/, scripts/, its other folders, then its loose files. A folder shows one fold per file (servers/workbench/studio/tabs/folder_folds.py).
A topic that has its own drawing gets a last button, Draw.

    <host venv python> skills_views.py <topic> [<topic> ...] [--check]
    <host venv python> skills_views.py <Block> [--check]            every Skills topic of the Block
    <host venv python> skills_views.py <topic> --skills <skill dir> [<skill dir> ...]    set or change its skills

A topic's skills are read from its own studio-views.json: each top button's first tab is the skill's SKILL.md.
Paths are from the SPACE root. `--check` writes nothing and exits 1 when a views file is stale: a skill gained or
lost a folder, a rules file or a loose file since it was written.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SPACE = next(p for p in Path(__file__).resolve().parents if (p / "plugins" / "haipipe-toolkit").is_dir())
sys.path.insert(0, str(SPACE / "plugins/haipipe-toolkit/servers/_host"))

OWN = ["SKILL.md", "CONSTITUTION.md"]        # the first two tabs, when the skill has them
FIRST = ("ref", "scripts")                   # the two folders every skill may have, before the others


def _files(folder: Path) -> list[str]:
    """The names of the files a fold would show in the folder, by the server's own rule."""
    from host_paths import bootstrap
    bootstrap()
    from live.folder_folds import files_of
    return [name for name, _ in files_of(folder, SPACE)]


def is_draw(view: dict) -> bool:
    """The topic's own drawing as a top button, after its skills."""
    first = (view.get("items") or [{}])[0]
    return view.get("name") == "Draw" and str(first.get("path", "")).endswith(".excalidraw")


def draw_view(topic: Path) -> list[dict]:
    """[the Draw view] when the topic has its own drawing, `<topic>/<topic>.excalidraw`; else []."""
    drawing = topic / f"{topic.name}.excalidraw"
    if not drawing.is_file():
        return []
    return [{"name": "Draw", "items": [{"name": "Draw", "path": drawing.resolve().relative_to(SPACE).as_posix()}]}]


def skills_of(topic: Path) -> list[str]:
    """The topic's skill folders, SPACE-relative, in button order; [] when it is no Skills topic."""
    try:
        data = json.loads((topic / "studio-views.json").read_text(encoding="utf-8"))
        views = data["views"]
    except (OSError, ValueError, KeyError, TypeError):
        return []
    out = []
    for view in views:
        if (view.get("name") == "Check" and data.get("check_type")) or is_draw(view):
            continue
        first = (view.get("items") or [{}])[0]
        path = first.get("path", "")
        if first.get("name") not in ("SKILL.md", "SKILL") or not path.endswith("/SKILL.md"):
            return []
        out.append(path[: -len("/SKILL.md")])
    return out


def items_of(skill: str) -> list[dict]:
    """The left tabs of one skill: its whole top level, each tab the file's or the folder's own name (a folder with
    its slash), in the fixed order: SKILL.md, CONSTITUTION.md, ref/, scripts/, the other folders, the loose files."""
    folder = SPACE / skill
    loose = _files(folder)
    items = [{"name": name, "path": f"{skill}/{name}"} for name in OWN if name in loose]
    rest = sorted(p.name for p in folder.iterdir()
                  if p.is_dir() and p.name not in FIRST and not p.name.startswith((".", "__")))
    for name in list(FIRST) + rest:
        if _files(folder / name):
            items.append({"name": name + "/", "folder": f"{skill}/{name}"})
        elif (folder / name).is_dir():          # a folder of folders (hai-draw's gallery/): one tab per inner folder
            items += [{"name": f"{name}/{sub.name}/", "folder": f"{skill}/{name}/{sub.name}"}
                      for sub in sorted((folder / name).iterdir(), key=lambda p: p.name)
                      if sub.is_dir() and not sub.name.startswith((".", "_")) and _files(sub)]
    items += [{"name": name, "path": f"{skill}/{name}"} for name in loose if name not in OWN]
    return items


def views_text(skills: list[str], topic: Path | None = None) -> str:
    views = [{"name": Path(skill).name, "items": items_of(skill)} for skill in skills]
    views += draw_view(topic) if topic else []
    return json.dumps({"views": views}, indent=2, ensure_ascii=False) + "\n"


def topics_of(path: Path) -> list[Path]:
    """The topic itself, or every Skills topic of a Block."""
    if (path / "studio-views.json").is_file():
        return [path]
    return [t for t in sorted(path.glob("s[0-9][0-9]-*/")) if skills_of(t)]


def main(argv: list[str]) -> int:
    check = "--check" in argv
    named = argv[argv.index("--skills") + 1:] if "--skills" in argv else []
    paths = [a for a in (argv[: argv.index("--skills")] if "--skills" in argv else argv) if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    bad = 0
    for topic in [t for p in paths for t in topics_of((SPACE / p).resolve()) or [(SPACE / p).resolve()]]:
        skills = [s.rstrip("/") for s in named] or skills_of(topic)
        missing = [s for s in skills if not (SPACE / s / "SKILL.md").is_file()]
        if not skills or missing:
            print(f"❗ {topic.name}: " + (f"no SKILL.md in {', '.join(missing)}" if missing else "names no skill (use --skills)"))
            bad += 1
            continue
        out = topic / "studio-views.json"
        data = json.loads(views_text(skills, topic))
        previous = json.loads(out.read_text()) if out.is_file() else {}
        data = dict(previous, views=data['views'])
        if data.get('check_type'):
            from check_views import build as check_build
            outputs = check_build(topic, data, SPACE)
        else:
            outputs = {out: json.dumps(data, indent=2, ensure_ascii=False) + "\n"}
        stale = [p for p, text in outputs.items() if not p.is_file() or p.read_text() != text]
        if check:
            print(f"{'❗' if stale else '✅'} {topic.name}: {len(skills)} skills" + (" (stale: run skills_views.py)" if stale else ""))
            bad += bool(stale)
        else:
            for p, text in outputs.items():
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(text, encoding='utf-8')
            # Validate the completed write; the checker calls pure builders, never this writer.
            plugin = Path(__file__).resolve().parents[5]
            if str(plugin) not in sys.path:
                sys.path.insert(0, str(plugin))
            from checks.run import check_targets
            from checks.common.results import display, exit_code
            results = check_targets([topic], SPACE)
            if exit_code(results):
                for result in results:
                    if result.status != 'PASS':
                        print(display(result, SPACE))
                bad += 1
                continue
            print(f"{'Wrote' if stale else 'Up to date:'} {topic.name}: {len(skills)} skills")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
