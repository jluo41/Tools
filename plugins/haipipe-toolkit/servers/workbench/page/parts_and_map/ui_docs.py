"""A theme Block's Docs view: one place per view and section of its example pages, where the person documents each
(JL 261115: "a new tab to put each view-section content here, and I can add the documentations").

It reads the Block's own view tables, `delivery/page-spec/block-views.md`, `job-views.md` and `task-views.md` (a row per page
type, a column per view, the view's sections in its cell), and shows for each type its views, and under each view its
sections. A section's documentation is one Markdown file:

    delivery/page-spec/docs/<level>/<view>/<section>.md      for example .../docs/block/idea/theory.md

The same section in the same view shares one file across types. A file not written yet shows its path, so the person
knows where to write. Viewing writes nothing.
"""
from __future__ import annotations

import re
from pathlib import Path

from live import frame
from live.focus_base import inside, markdown
from live.ui_parts import PB_CSS, PB_JS, _side_tabs
from live.page_spec import spec_dir

LEVELS = (("block", "Block pages"), ("job", "Job pages"), ("task", "Task pages"))
SKIP = {"category", "use cases"}
CSS = """<style>
.ud-view{margin:0 0 14px}.ud-view>h4{margin:0 0 6px;font-size:14px}
.ud-sec{border:1px solid var(--border,#e5e7eb);border-radius:6px;margin:0 0 6px;background:var(--paper,#fff)}
.ud-sec>summary{cursor:pointer;padding:6px 10px;font-weight:500;font-size:13.5px}
.ud-sec>summary .ud-path{font:400 11px ui-monospace,Menlo,monospace;color:var(--muted,#6b7280);margin-left:8px}
.ud-sec>.ud-body{padding:2px 12px 8px;font-size:13.5px}
.ud-sec.ud-none>summary{color:var(--muted,#6b7280);font-weight:400}
</style>"""


def slug(text: str) -> str:
    """A view's or section's file name: its words, lower case, joined by -, without emoji or marks."""
    words = re.sub(r"[^\w\s+-]", " ", re.sub(r"<[^>]+>", " ", text)).replace("+", " ").replace("_", " ")
    return "-".join(words.lower().split()) or "section"


def _cells(line: str) -> list:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table(source: Path) -> tuple:
    """(views, rows): the view names after Use Cases, and [(type name, {view: [sections]})] for each row."""
    lines = [ln for ln in source.read_text(encoding="utf-8", errors="replace").splitlines() if ln.lstrip().startswith("|")]
    if len(lines) < 3:
        return [], []
    head = _cells(lines[0])
    first = next((i for i, h in enumerate(head) if h.casefold() == "use cases"), 1) + 1
    type_col = 1 if len(head) > 1 else 0
    views = head[first:]
    rows = []
    for line in lines[2:]:
        cells = _cells(line)
        if len(cells) < len(head):
            continue
        secs = {}
        for view, cell in zip(views, cells[first:]):
            items = [s.strip() for s in re.split(r"<br\s*/?>", cell) if s.strip() and s.strip() not in ("—", "-")]
            if items:
                secs[view] = items
        if secs:
            rows.append((cells[type_col], secs))
    return views, rows


def _doc(folder: Path, root: Path, level: str, view: str, sec: str) -> str:
    path = spec_dir(folder) / "docs" / level / slug(view) / f"{slug(sec)}.md"
    rel = path.relative_to(folder).as_posix()
    if inside(path, root) and path.is_file():
        text = path.read_text(encoding="utf-8", errors="replace")
        text = re.sub(r"\A\s*#\s+.+\n", "", text)          # its own title repeats the section's name
        return (f'<details class="ud-sec"><summary>{frame.esc(sec)}</summary>'
                f'<div class="ud-body">{markdown(text, path.parent, root)}</div></details>')
    return (f'<details class="ud-sec ud-none"><summary>{frame.esc(sec)}<span class="ud-path">{frame.esc(rel)}</span>'
            f'</summary></details>')


def level_html(folder: Path, root: Path, level: str) -> str:
    """One level's types as side tabs; each type's views with their sections and documentation."""
    source = spec_dir(folder) / f"{level}-views.md"
    if not (inside(source, root) and source.is_file()):
        return ""
    views, rows = table(source)
    if not rows:
        return ""
    panels = []
    for _, secs in rows:
        panels.append("".join(f'<div class="ud-view"><h4>{frame.esc(re.sub(r"<[^>]+>", "", v))}</h4>'
                              + "".join(_doc(folder, root, level, v, s) for s in secs[v]) + '</div>'
                              for v in views if v in secs))
    return PB_CSS + _side_tabs(f"ud{level[0]}", [(re.sub(r"<[^>]+>", "", t), "") for t, _ in rows], panels) + PB_JS


def has_docs(folder: Path) -> bool:
    return any((spec_dir(folder) / f"{k}-views.md").is_file() for k, _ in LEVELS)


def skill_html(folder: Path, root: Path) -> str:
    """Rules that are no part of a page (how the skills work): one file each under `delivery/page-spec/docs/skill/`, its topics inside."""
    base = spec_dir(folder) / "docs" / "skill"
    files = sorted(base.glob("*.md")) if inside(base, root) and base.is_dir() else []
    out = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        title = (re.match(r"\A\s*#\s+(.+)\n", text) or [None, path.stem])[1]
        body = markdown(re.sub(r"\A\s*#\s+.+\n", "", text), path.parent, root)
        out.append(f'<details class="ud-sec"><summary>{frame.esc(title)}</summary><div class="ud-body">{body}</div></details>')
    return "".join(out)


def view(folder: Path, root: Path, section) -> str:
    """The Docs view: a numbered section per level that has a view table, then the skill rules."""
    parts = [(name, html) for key, name in LEVELS if (html := level_html(folder, root, key))]
    if (skills := skill_html(folder, root)):
        parts.append(("Skill rules", skills))
    return CSS + "".join(section(n, name, body) for n, (name, body) in enumerate(parts, 1))


TOPIC = re.compile(r"(?m)^##\s+(.+?)\s*$")
TOPIC_CSS = """<style>
.ud-tp{border:1px solid var(--border,#e5e7eb);border-radius:8px;margin:0 0 8px;background:var(--paper,#fff)}
.ud-tp>summary{cursor:pointer;padding:8px 12px;font-weight:600;font-size:14px}
.ud-tp>.ud-body{padding:2px 14px 10px;font-size:13.5px}.ud-intro{font-size:13.5px;margin:0 0 10px}
.ud-intro code,.ud-tp code{font-size:12px}
</style>"""


def topic_groups(folder: Path, root: Path) -> list:
    """[(group name, its file, intro markdown, [(topic, body markdown)])]: every file under `delivery/page-spec/docs/`, in task, job,
    block, then skill order; a file is a topic group, each `## ` heading in it one topic (JL 261115: "could you put
    the topic groups here?")."""
    base = spec_dir(folder) / "docs"
    if not (inside(base, root) and base.is_dir()):
        return []
    rank = {"task": 0, "job": 1, "block": 2, "skill": 3}
    out = []
    for path in sorted(base.rglob("*.md"), key=lambda p: (rank.get(p.relative_to(base).parts[0], 9), str(p))):
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"\A\s*#\s+(.+?)\s*\n", text)
        name, text = (m.group(1), text[m.end():]) if m else (path.stem, text)
        heads = list(TOPIC.finditer(text))
        intro = text[:heads[0].start()] if heads else text
        topics = [(h.group(1).replace("Topic: ", ""), text[h.end():(heads[i + 1].start() if i + 1 < len(heads) else len(text))])
                  for i, h in enumerate(heads)]
        out.append((name, path, intro, topics))
    return out


def topics_html(folder: Path, root: Path) -> str:
    """The topic groups as left tabs, the open group's topics on the right, each a fold with its requests."""
    groups = topic_groups(folder, root)
    if not groups:
        return ""
    rel = lambda p: p.relative_to(folder).as_posix()
    where = {"plan": "Plan", "revise": "Draft Lab", "skill": "Skills"}
    label = lambda p: where.get(p.parent.name, p.parent.name.capitalize())
    items = [(f"{label(path)} ▸ {name}", "") for name, path, _, _ in groups]
    panels = []
    for name, path, intro, topics in groups:
        body = markdown(intro, path.parent, root) if intro.strip() else ""
        body += "".join(f'<details class="ud-tp"><summary>{frame.esc(t)}</summary><div class="ud-body">'
                        f'{markdown(b, path.parent, root)}</div></details>' for t, b in topics)
        panels.append(f'<div class=ud-intro><code>{frame.esc(rel(path))}</code></div>' + body)
    return TOPIC_CSS + PB_CSS + _side_tabs("udt", items, panels) + PB_JS
