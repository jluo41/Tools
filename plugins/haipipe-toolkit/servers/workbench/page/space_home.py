"""The SPACE page's Home view: the front door of one SPACE (or one folder of Projects).

It answers "which Project do I open, and what waits on me?" in three parts, each hidden when empty:
A. Waiting on you, the questions every Project below asks the person (its waiting collection Runs);
B. Projects, one row per Project under its folder, with its one line and its buttons;
C. This week, the Blocks whose pages changed in the last seven days, newest first;
D. Constitution, the rules feedback made (space_constitution, haistack).
What one Project found, decided or planned is its own page's (project_page); this page never lists Blocks' work.
"""
from __future__ import annotations

import datetime as dt
import os
import time
from pathlib import Path

from live import frame
from live.focus_base import inside, kids, one_line, page_level, page_url, read_face
from live.focus_interactions import page_interactions
from live.focus_reports import blocks_under
from live.focus_tree import status_html
from live.focus_styles_bands import BAND_CSS, band_sec
from live.space_constitution import constitution_html

RECENT_DAYS = 7
RECENT_MAX = 8
WAIT_SHOWN = 5
SKIP = {"runs", "_archive", "_old", "delivery", "node_modules", "__pycache__", "assets"}

CSS = """<style>

.sh-list{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.sh-list li{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline;padding:8px 12px;border:1px solid var(--line);
  border-radius:var(--radius-surface,8px);background:var(--card)}
.sh-list li:hover{border-color:var(--accent)}
.sh-list a.sh-name{font-weight:600;color:var(--fg);text-decoration:none}.sh-list a.sh-name:hover{color:var(--accent)}
.sh-where{color:var(--mut);font:12px/1.5 ui-monospace,Menlo,monospace;overflow-wrap:anywhere}
.sh-line{flex-basis:100%;color:var(--mut);font-size:13px}
.sh-day{color:var(--mut);font:12px/1.5 ui-monospace,Menlo,monospace}
.sh-wait li{border-color:#f0a040}
.band-sec .kid-pic.none{display:none}
.sh-more{margin-top:6px}.sh-more>summary{cursor:pointer;color:var(--accent);font-size:13px}.sh-more>.sh-list{margin-top:6px}
</style>"""


def _where(page: Path, root: Path) -> str:
    """A page's place from its Project down: `Project-X / work / b01_topic`."""
    parts = page.relative_to(root).parts
    start = next((i for i, p in enumerate(parts) if p.startswith("Project-")), 0)
    return " / ".join(parts[start:])


KEEP = 60                                      # seconds a SPACE-wide scan is reused
_RECENT_CACHE: dict = {}                       # folder -> (time, list)
_WAIT_CACHE: dict = {}                         # folder -> (time, rows): Home's section and the page tray share one walk


# where a collection Run can sit below a Project: on the Project, a Theme, a Block, a Job or a Task
COLLECT_DEPTHS = ("runs", "*/runs", "*/*/runs", "*/*/j*/runs", "*/*/j*/t*/runs")


def collect_pages(folder: Path) -> list:
    """The pages below a SPACE or folder of Projects that hold a collection Run (`runs/rNN_collect_*`), found by fixed-
    depth globs from each Project: building every page of a big SPACE (thousands) only to find a few took seconds."""
    projects = [q for g in kids(folder) for q in (kids(g) if page_level(g) == "Folder" else [g])] \
        if page_level(folder) == "SPACE" else kids(folder)
    pages = set()
    for project in projects:
        for depth in COLLECT_DEPTHS:
            for run in project.glob(depth + "/r[0-9]*_collect_*"):
                if run.is_dir():
                    pages.add(run.parent.parent)
    return sorted(pages)


def waiting_rows(folder: Path, root: Path) -> list:
    """Every waiting collection Run at this SPACE or folder of Projects and every page below it, read once per render
    (kept KEEP seconds, so the 🙋 tray and the Waiting section never walk the SPACE twice)."""
    hit = _WAIT_CACHE.get(str(folder))
    if hit and time.monotonic() - hit[0] < KEEP:
        return hit[1]
    rows = []
    for page in collect_pages(folder):
        try:
            rows += [r for r in page_interactions(page, root) if r.get("state") == "waiting"]
        except Exception:                      # one bad record never hides the rest
            continue
    _WAIT_CACHE[str(folder)] = (time.monotonic(), rows)
    return rows


def waiting(folder: Path, root: Path) -> tuple[str, int]:
    """A. Every waiting question below this SPACE, each opening its page's Interactions view: (the list, how many)."""
    rows = waiting_rows(folder, root)
    items = [
        f'<li><a class="sh-name" href="{frame.esc(page_url(r["page"], root, "interactions"))}">'
        f'🙋 {frame.esc(r.get("title") or r.get("run") or "")}</a>'
        f'<span class="sh-where">{frame.esc(_where(r["page"], root))}</span></li>'
        for r in rows if r.get("page") is not None and inside(r["page"], root)]
    if not items:
        return "", 0
    more = (f'<details class="sh-more"><summary>More</summary><ul class="sh-list sh-wait">{"".join(items[WAIT_SHOWN:])}'
            '</ul></details>' if len(items) > WAIT_SHOWN else "")   # the first few stay in view, so Projects do too
    return f'<ul class="sh-list sh-wait">{"".join(items[:WAIT_SHOWN])}</ul>{more}', len(items)


def _newest(block: Path) -> float:
    """The newest change to a Block's own pages (.md faces and notes), its Runs' output left out."""
    newest = 0.0
    for dirpath, dirs, files in os.walk(block):
        dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
        for f in files:
            if f.endswith(".md"):
                try:
                    newest = max(newest, os.stat(os.path.join(dirpath, f)).st_mtime)
                except OSError:
                    pass
    return newest


def recent(folder: Path, root: Path, today: dt.date | None = None) -> str:
    """C. The Blocks changed in the last RECENT_DAYS days, newest first, at most RECENT_MAX."""
    hit = _RECENT_CACHE.get(str(folder))
    if hit and today is None and time.monotonic() - hit[0] < KEEP:   # a walk of every Block's pages: seconds on a big
        return hit[1]                                                  # SPACE, so kept a minute
    out = _recent(folder, root, today)
    if today is None:
        _RECENT_CACHE[str(folder)] = (time.monotonic(), out)
    return out


def _recent(folder: Path, root: Path, today: dt.date | None = None) -> str:
    since = dt.datetime.combine((today or dt.date.today()) - dt.timedelta(days=RECENT_DAYS), dt.time()).timestamp()
    changed = sorted(((t, b) for b in blocks_under(folder) if inside(b, root) and b.is_dir()
                      for t in [_newest(b)] if t >= since), key=lambda tb: tb[0], reverse=True)[:RECENT_MAX]
    items = []
    for t, block in changed:
        line = one_line(read_face(block, root).get("goal") or "")
        day = dt.datetime.fromtimestamp(t).strftime("%a %d %b")
        items.append(f'<li><span class="sh-day">{day}</span>'
                     f'<a class="sh-name" href="{frame.esc(page_url(block, root))}">{frame.esc(block.name)}</a>'
                     f'<span class="sh-where">{frame.esc(_where(block.parent, root))}</span>'
                     + (f'<span class="sh-line">{frame.esc(line)}</span>' if line else '') + '</li>')
    return f'<ul class="sh-list">{"".join(items)}</ul>' if items else ""


def space_home(folder: Path, root: Path) -> str:
    """The Home view of a SPACE or a folder of Projects: numbered open sections, as every page's, each hidden when
    empty: 🙋 Waiting on you (its bar carries the orange 🙋 N), 📁 Projects, 🕒 This week."""
    level = page_level(folder)
    wait, n = waiting(folder, root)
    secs = [("🙋 Waiting on you", f"{n} waiting for you", wait), ("📁 Projects", "", status_html(folder, root, level, [])),
            ("🕒 This week", "", recent(folder, root)), ("📜 Constitution", "", constitution_html(root))]
    return CSS + BAND_CSS + "".join(band_sec(i, title, word, body, opened=True, src="ix" if word else "")
                                    for i, (title, word, body) in enumerate([s for s in secs if s[2]], 1))
