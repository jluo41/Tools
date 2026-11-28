"""Build a Studio Type topic's right side from its elements.md: one requirement page per top button and left tab, and
the studio-views.json that lays the type out as its instances are (hai-studio A06: a type and its instances share
the top and the left; the type's right side is the requirement, an instance's the real thing).

    <host venv python> type_requirements.py examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure [--check]

Writes `<topic>/delivery/requirements/<view>--<tab>.html` and `<topic>/studio-views.json`. `--check` writes nothing and
exits 1 when a page or the views file is stale. A `## ` group whose entries carry `mark:` (rows of a real page) is not
a view: it only feeds the right-click cards.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

SPACE = next(p for p in Path(__file__).resolve().parents if (p / "plugins" / "haipipe-toolkit").is_dir())
sys.path.insert(0, str(SPACE / "plugins/haipipe-toolkit/servers/_host"))

CSS = """:root{--line:#e6e6e3;--muted:#6b6b66;--ink:#1d1d1b;--accent:#1f5fbf;--bg:#fff;--soft:#f4f4f2}
@media (prefers-color-scheme:dark){:root{--line:#3a3a37;--muted:#a3a39c;--ink:#ecece8;--accent:#8ab4ff;--bg:#1b1b19;--soft:#242422}}
body{margin:0;padding:14px 16px;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;max-width:760px}
h1{font-size:19px;margin:0 0 14px}h1 small{font-weight:400;color:var(--muted);font-size:13px;margin-right:6px}
dl{display:grid;grid-template-columns:72px minmax(0,1fr);gap:8px 12px;margin:0}
dt{font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding-top:3px}
dd{margin:0}ol{margin:0;padding-left:20px}li{margin:3px 0}
code{font-size:13px;background:var(--soft);padding:0 4px;border-radius:4px;overflow-wrap:anywhere}
dd{overflow-wrap:anywhere}
@media (max-width:400px){body dl{grid-template-columns:minmax(0,1fr);gap:2px 0}body dt{padding-top:10px}body dt:first-child{padding-top:0}}
.tree,.tree ul{list-style:none;padding:0;margin:0}.tree ul{margin:6px 0 8px 13px;padding-left:23px;border-left:1px solid var(--line)}
.tree li{position:relative;margin:4px 0;white-space:nowrap}.tree ul>li:before{content:'';position:absolute;left:-23px;top:13px;width:23px;border-top:1px solid var(--line)}
.tree summary{cursor:pointer;width:fit-content}.tree .leaf{padding-left:15px}.tree>li>details>summary{color:var(--root);font-weight:600}
.tree svg,.tree .ico{margin-right:5px}.tree small{margin-left:12px;color:var(--muted);font-size:11px;font-weight:400}
.tree{--root:#176353;--l-jg:#7048e8;--l-jn:#1971c2;--l-tg:#2b8a3e;--l-tn:#c2410c}
.lvl[data-level=job-group]{color:var(--l-jg);font-weight:600}.lvl[data-level=job-name]{color:var(--l-jn)}
.lvl[data-level=task-group]{color:var(--l-tg);font-weight:600}.lvl[data-level=task-name]{color:var(--l-tn)}
@media (prefers-color-scheme:dark){.tree{--root:#a4ddc4;--l-jg:#b197fc;--l-jn:#74c0fc;--l-tg:#8ce99a;--l-tn:#ffa94d}}
dd:has(>.tree){overflow-x:auto;overflow-wrap:normal;padding-bottom:4px}"""


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def words(text: str) -> str:
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(text))


LEVELS = {"Job group": "job-group", "Job name": "job-name", "Task group": "task-group", "Task name": "task-name"}


def tree(lines: list[str]) -> str:
    """The pattern to follow, drawn as an instance draws its tree (one look, so a type needs no separate example): the
    Files pane's folder drawing and file icons, ◇ for a level that is no folder or file, the connector lines, and for
    a row whose note names a level (Job group, Job name, Task group, Task name) that level's colour. Two spaces of
    indent are one level; `  # note` is a small word after the name, `  | words` the line's hover."""
    from live import ui_parts
    from live.file_icons import DEFAULT_ICON, FILE_ICONS, FILE_MARKS

    def row(text: str) -> str:
        text = text.partition("  | ")[0]
        name, _, note = text.partition("  # ")
        suffix = Path(name).suffix.lower()
        if name.endswith("/"):
            icon = ui_parts.FOLDER_ICON
        elif suffix in FILE_MARKS or suffix in FILE_ICONS:
            icon = FILE_MARKS.get(suffix) or f'<span class="ico">{FILE_ICONS[suffix]}</span>'
        else:
            icon = '<span class="ico">◇</span>'
        return icon + html.escape(name) + (f"<small>{html.escape(note.strip())}</small>" if note else "")

    def level_of(text: str) -> str:
        return LEVELS.get(text.partition("  | ")[0].partition("  # ")[2].strip(), "")

    def hover(text: str) -> str:
        why = text.partition("  | ")[2].strip()
        return f' title="{html.escape(why, quote=True)}"' if why else ""

    def level(i: int, depth: int) -> tuple[str, int]:
        out = ""
        while i < len(rows) and rows[i][0] == depth:
            kids, j = level(i + 1, depth + 1)
            text = row(rows[i][1])
            lvl = level_of(rows[i][1])
            why = hover(rows[i][1])
            out += (f'<li><details open><summary class="lvl" data-level="{lvl}"{why}>{text}</summary><ul>{kids}</ul></details></li>'
                    if kids else f'<li><span class="leaf lvl" data-level="{lvl}"{why}>{text}</span></li>')
            i = j
        return out, i

    rows = [((len(s) - len(s.lstrip(" "))) // 2, s.strip()) for s in lines]
    return f'<ul class="tree">{level(0, rows[0][0])[0]}</ul>' if rows else ""


def page(el: dict, example: str = '') -> str:
    rows = [("What", words(el.get("what", ""))), ("Why", words(el.get("why", "")))]
    if el.get("when"):
        rows.append(("When", words(el["when"])))
    if el.get("must"):
        rows.append(("Must show", "<ol>" + "".join(f"<li>{words(m)}</li>" for m in el["must"]) + "</ol>"))
    if el.get("pattern"):
        rows.append(("Pattern", tree(el["pattern"])))
    rows += [("From", words(el.get("from", ""))), ("Check", words(el.get("check", "")))]
    lead = f'<small>{html.escape(el["view"])} ›</small>' if el.get("tab") else ""
    body = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows if v)
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width,initial-scale=1"><title>{html.escape(el["name"])}</title><style>{CSS}</style></head>'
            f'<body><h1>{lead}{html.escape(el["name"])}</h1><dl>{body}</dl>{example}</body></html>\n')


def build(topic: Path) -> dict[Path, str]:
    """{file: its text} for the topic: every requirement page and the views file."""
    from host_paths import bootstrap
    bootstrap()
    from live.studio_types import elements_of
    els, out, views = elements_of(topic), {}, []
    if not els:
        raise ValueError(f"{topic.name} is no Studio Type: it has no elements.md")
    rel = topic.resolve().relative_to(SPACE).as_posix()
    for view in [e for e in els if e["tab"] is None]:
        tabs = [e for e in els if e["view"] == view["name"] and e["tab"] is not None]
        if any(e.get("mark") for e in tabs):                  # rows of a real page: right-click words only
            continue
        items = []
        for el in tabs or [view]:
            name = f'{slug(view["name"])}--{slug(el["name"])}.html' if tabs else f'{slug(view["name"])}.html'
            from requirement_examples import render
            out[topic / "delivery" / "requirements" / name] = page(el, render(topic, el, SPACE))
            items.append({"name": el["name"], "path": f"{rel}/delivery/requirements/{name}"})
        skills = [d.strip().strip("/") for d in view.get("skills", "").split(",") if d.strip()]
        if skills and not tabs:                              # the real skill files, not a card that says to list them
            items = [{"name": Path(d).name, "path": f"{d}/SKILL.md"} for d in skills if (SPACE / d / "SKILL.md").is_file()]
        views.append({"name": view["name"], "items": items})
    manifest = topic / "studio-views.json"
    data = json.loads(manifest.read_text()) if manifest.is_file() else {}
    data['views'] = views
    if data.get('check_type'):
        from check_views import build as check_build
        out.update(check_build(topic, data, SPACE))
    else:
        out[manifest] = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    return out


def main(argv: list[str]) -> int:
    check = "--check" in argv
    topic = (SPACE / next(a for a in argv if not a.startswith("--"))).resolve()
    files = build(topic)
    stale = [f for f, text in files.items() if not f.is_file() or f.read_text(encoding="utf-8") != text]
    extra = [f for f in (topic / "delivery" / "requirements").glob("*.html") if f not in files]
    if check:
        for f in stale + extra:
            print(f"❗ {f.relative_to(SPACE)}: stale")
        print(f"{'❗' if stale or extra else '✅'} {topic.name}: {len(files) - 1} requirement pages")
        return 1 if stale or extra else 0
    for f, text in files.items():
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")
    for f in extra:
        f.unlink()
    print(f"Built {len(files) - 1} requirement pages and studio-views.json for {topic.name}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
