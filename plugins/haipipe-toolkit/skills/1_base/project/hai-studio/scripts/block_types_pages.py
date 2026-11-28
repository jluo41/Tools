"""Build a Block Structure instance's Job types and Task types views from its types.md: one page per type (what it is
for, what it must hold, the real Jobs or Tasks of that type in the example Block), and the two views in the topic's
studio-views.json, after Structure (b17 s71: the class lists the slots, an instance its real types).

    python3 block_types_pages.py examples/Project-Ladder/blueprint/b17_theme_work/s01-work-ladder [--check]

`--check` writes nothing and exits 1 when a page or the views are stale.
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from block_types_check import SPACE, field, read_types  # noqa: E402
from type_requirements import CSS, slug, words  # noqa: E402

VIEWS = {"Job types": ("Job group type", "Job type"), "Task types": ("Task group type", "Task type")}


def members(block: Path, level: str, kind: str) -> list[Path]:
    """The example Block's Jobs (or Tasks) that name this type."""
    if level == "Job type":
        return [j for j in sorted(block.glob("j[0-9]*_*/")) if field(j / f"{j.name}.md", "job-type") == kind]
    if level == "Task type":
        return [t for t in sorted(block.glob("j[0-9]*_*/t[0-9]*_*/")) if field(t / f"{t.name}.md", "task-type") == kind]
    return []


def agreed(about: dict) -> bool:
    return about.get("agreed", "yes").strip().lower() != "no"


def shown(kind: str, about: dict) -> str:
    """A type not agreed yet is written in 〈 〉 (AGENTS.md "Page words")."""
    return kind if agreed(about) else f"〈{kind}〉"


def page(level: str, kind: str, about: dict, real: list[Path]) -> str:
    rows = [("For", words(about.get("for", ""))), ("Holds", words(about.get("holds", "")))]
    if not agreed(about):
        rows.append(("Open", "Read from the example Block; not yet agreed as a type of every Block of this kind."))
    if real:
        links = "".join(f'<li><a target="_top" href="/_board/workbench?path={quote(p.relative_to(SPACE).as_posix())}&amp;layout=focus">'
                        f'{html.escape(p.name)}</a></li>' for p in real)
        rows.append(("In the example", f"<ul>{links}</ul>"))
    body = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows if v)
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width,initial-scale=1"><title>{html.escape(shown(kind, about))}</title><style>{CSS}'
            f'ul{{margin:0;padding-left:18px}}a{{color:var(--accent)}}</style></head>'
            f'<body><h1><small>{html.escape(level)} ›</small>{html.escape(shown(kind, about))}</h1><dl>{body}</dl></body></html>\n')


def build(topic: Path) -> dict[Path, str]:
    example, types = read_types(topic / "types.md")
    block, rel, out, views = SPACE / example, topic.resolve().relative_to(SPACE).as_posix(), {}, []
    for view, levels in VIEWS.items():
        items = []
        for level in levels:
            for kind, about in types.get(level, {}).items():
                name = f"{slug(level)}--{slug(kind)}.html"
                out[topic / "delivery" / "types" / name] = page(level, kind, about, members(block, level, kind))
                items.append({"name": shown(kind, about), "path": f"{rel}/delivery/types/{name}"})
        views.append({"name": view, "items": items})
    manifest = topic / "studio-views.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    kept = [v for v in data["views"] if v["name"] not in VIEWS]
    at = next((i + 1 for i, v in enumerate(kept) if v["name"] == "Structure"), 0)
    data["views"] = kept[:at] + views + kept[at:]
    out[manifest] = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    return out


def main(argv: list[str]) -> int:
    check = "--check" in argv
    topic = (SPACE / next(a for a in argv if not a.startswith("--"))).resolve()
    files = build(topic)
    stale = [f for f, text in files.items() if not f.is_file() or f.read_text(encoding="utf-8") != text]
    if check:
        for f in stale:
            print(f"❗ {f.relative_to(SPACE)}: stale")
        print(f"{'❗' if stale else '✅'} {topic.name}: {len(files) - 1} type pages")
        return 1 if stale else 0
    for f, text in files.items():
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")
    print(f"Built {len(files) - 1} type pages and the two views for {topic.name}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
