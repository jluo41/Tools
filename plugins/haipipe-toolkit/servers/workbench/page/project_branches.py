"""A Project's Timeline as a transit map: one line per Block, its dated records as stations, newest on top.

The idea and the column rule are borrowed from Trace Canvas (github.com/CallSymmetryEcho/trace-canvas, MIT, its
renderGit): each record is one row; each Block is one coloured line running from its newest to its oldest record;
columns are reused the way `git log --graph` reuses them, so a Block whose records have ended gives its column to a
later one. The records are this workbench's own, read from disk by focus_studio.timeline_events (git changes,
finished Runs, work sessions, log notes); nothing is kept in a second store. A question waiting on the person sits
on top of its Block's line, joined to it by a dashed line, like a live tip (one per Block).
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from live import frame
from live.focus_base import inside, page_url
from live.focus_interactions import interactions
from live.focus_reports import blocks_under
from live.focus_studio import timeline_events
from live.focus_styles_bands import BAND_CSS, band_sec

GIT_MAX = 300                     # commits read for the whole page
GIT_DAYS = 120                    # and no older than this
_GIT_CACHE: dict = {}             # (folder, HEAD) -> git log text
ROWS_MAX = 80                     # the newest records drawn; older ones stay in each Block's own Timeline
ROW, PADX, LW = 34, 14, 22        # row height, left padding, column width (px)
COLORS = ("#0072CE", "#E4002B", "#00A651", "#F28C28", "#8E3A96", "#00A0B0", "#B5651D", "#5B6B7F")
GLYPH = {"run": "run", "pass": "pass", "log": "log", "commit": "commit", "wait": "wait"}
KIND = {"commit": "change", "run": "Run", "pass": "work session", "log": "note", "wait": "waits on you"}


def _station(kind: str, x: float, y: float, color: str) -> str:
    """◆ a finished Run, □ a work session, • a log note, ○ a change, a filled orange dot a waiting question."""
    if kind == "run":
        return f'<path d="M{x} {y-7}L{x+7} {y}L{x} {y+7}L{x-7} {y}Z" fill="{color}" stroke="var(--card,#fff)" stroke-width="2"/>'
    if kind == "pass":
        return f'<rect x="{x-5.5}" y="{y-5.5}" width="11" height="11" rx="2" fill="var(--card,#fff)" stroke="{color}" stroke-width="2.5"/>'
    if kind == "log":
        return f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"/>'
    if kind == "wait":
        return f'<circle cx="{x}" cy="{y}" r="7" fill="#F28C28" stroke="var(--card,#fff)" stroke-width="2.5"/>'
    return f'<circle cx="{x}" cy="{y}" r="5.5" fill="var(--card,#fff)" stroke="{color}" stroke-width="2.5"/>'


def git_rows(folder: Path, blocks: list) -> list:
    """The git changes of every Block from one `git log` of the whole page (one per Block was seconds slower):
    each commit lands on each Block whose files it touched. Kept per (folder, HEAD), so only a new commit reads again."""
    try:
        head = subprocess.run(["git", "-C", str(folder), "rev-parse", "--show-toplevel", "HEAD"], capture_output=True,
                              text=True, timeout=5).stdout.split()
        if len(head) != 2:
            return []
        top, key = Path(head[0]), (str(folder), head[1])
        if key not in _GIT_CACHE:
            # only the Blocks' own folders, without rename detection: a whole-tree log took seconds on a big repo
            specs = [b.resolve().relative_to(folder.resolve()).as_posix() for b in blocks
                     if folder.resolve() in b.resolve().parents]
            out = subprocess.run(["git", "-C", str(folder), "log", f"-{GIT_MAX}", f"--since={GIT_DAYS}.days",
                                  "--no-renames", "--format=%x01%cs%x09%s", "--name-only", "--", *specs],
                                 capture_output=True, text=True, timeout=10) if specs else None
            _GIT_CACHE[key] = out.stdout if out is not None and out.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return []
    text = _GIT_CACHE[key]
    if not text or not top.is_dir():
        return []
    prefix = {b: b.resolve().relative_to(top.resolve()).as_posix() + "/" for b in blocks
              if top.resolve() in b.resolve().parents}
    rows = []
    for entry in text.split("\x01")[1:]:
        head, _, files = entry.partition("\n")
        day, _, words = head.partition("\t")
        for block, pre in prefix.items():
            if any(f.startswith(pre) for f in files.splitlines()):
                rows.append((day, "commit", words, "", block))
    return rows


def records(folder: Path, root: Path) -> tuple[list, list, int]:
    """(lines, rows, waiting): the Blocks that have records, the rows newest first, and how many questions wait. A row is
    (day, kind, words, where, block); waiting questions come first, with no day."""
    blocks = [b for b in blocks_under(folder) if inside(b, root) and b.is_dir()]
    rows, waiting, n_wait = git_rows(folder, blocks), [], 0
    for block in blocks:
        for day, kind, words, where in timeline_events(block, root, git=False):
            rows.append((day, kind, words, where, block))
        try:
            for r in interactions(block, root):
                if r.get("state") == "waiting":
                    n_wait += 1
                    if any(w[4] == block for w in waiting):
                        continue                   # one tip per Block: the page's 🙋 tray lists them all
                    page = r.get("page") or block
                    where = "" if page == block else " · ".join(page.relative_to(block).parts)
                    waiting.append(("", "wait", r.get("title") or r.get("run") or "", where, block, page))
        except Exception:                      # one bad record never hides the map
            pass
    rows.sort(key=lambda r: r[0], reverse=True)
    rows = waiting + rows[:ROWS_MAX]
    order = []                                 # lines in the order they first appear from the top
    for r in rows:
        if r[4] not in order:
            order.append(r[4])
    return order, rows, n_wait


def columns(order: list, rows: list) -> dict:
    """Each Block's column: the first column free over its rows, reused once the line above it has ended."""
    span = {}
    for i, r in enumerate(rows):
        lo, hi = span.get(r[4], (i, i))
        span[r[4]] = (min(lo, i), max(hi, i))
    taken, lane = [], {}
    for block in order:
        lo, hi = span[block]
        k = next((k for k, used in enumerate(taken) if all(u_hi + 1 < lo or hi + 1 < u_lo for u_lo, u_hi in used)), -1)
        if k < 0:
            k = len(taken)
            taken.append([])
        taken[k].append((lo, hi))
        lane[block] = k
    return lane, span


CSS = """<style>
.br-legend{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}
.br-chip{display:inline-flex;align-items:center;gap:6px;padding:2px 9px 2px 6px;border:1px solid var(--line);
  border-radius:999px;font-size:12.5px;color:var(--fg);text-decoration:none;background:var(--card)}
.br-chip i{width:9px;height:9px;border-radius:50%%;border:3px solid var(--c)}.br-chip:hover{border-color:var(--accent)}
.br-keys{display:flex;flex-wrap:wrap;gap:4px 14px;margin:0 0 12px;color:var(--mut);font-size:12px}
.br-map{position:relative;overflow:hidden}.br-svg{position:absolute;top:0;left:0;overflow:visible}
.br-row{display:flex;align-items:center;gap:8px;height:%(row)dpx;white-space:nowrap;overflow:hidden;border-bottom:1px solid var(--line)}
.br-row:last-child{border-bottom:0}.br-day{flex:none;width:76px;color:var(--mut);font:12px ui-monospace,Menlo,monospace}
.br-words{flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;color:var(--fg);font-size:13.5px}
.br-where{color:var(--mut);font-size:12px}.br-pill{flex:none;max-width:34%%;overflow:hidden;text-overflow:ellipsis;
  padding:1px 8px;border-radius:999px;border:1px solid var(--c);color:var(--fg);font-size:11.5px;text-decoration:none}
.br-wait .br-words{font-weight:600}.br-wait .br-day{color:#F28C28}
@media (max-width:680px){.br-pill{display:none}.br-day{width:58px}}
</style>""" % {"row": ROW}


def branches_html(folder: Path, root: Path) -> str:
    """The transit map of a Project (or any page above its Blocks)."""
    order, rows, n_wait = records(folder, root)
    if not rows:
        return '<p class="mut">Nothing dated below this page yet.</p>'
    lane, span = columns(order, rows)
    color = {b: COLORS[i % len(COLORS)] for i, b in enumerate(order)}
    ncol = max(lane.values()) + 1
    x = lambda k: PADX + k * LW
    y = lambda i: i * ROW + ROW / 2
    gw = PADX * 2 + (ncol - 1) * LW
    svg = []
    for block in order:                                   # the lines first, the stations over them
        lo, hi = span[block]
        tips = [i for i, r in enumerate(rows) if r[4] == block and r[1] == "wait"]
        first = min((i for i, r in enumerate(rows) if r[4] == block and r[1] != "wait"), default=None)
        cx = x(lane[block])
        if first is not None and hi > first:
            svg.append(f'<line x1="{cx}" y1="{y(first)}" x2="{cx}" y2="{y(hi)}" stroke="{color[block]}" stroke-width="3" '
                       f'stroke-linecap="round"><title>{frame.esc(block.name)}</title></line>')
        if tips:
            end = y(first) if first is not None else y(max(tips))
            svg.append(f'<line x1="{cx}" y1="{y(min(tips))}" x2="{cx}" y2="{end}" stroke="{color[block]}" '
                       'stroke-width="2" stroke-dasharray="3 4"/>')
    for i, r in enumerate(rows):
        svg.append(_station(r[1], x(lane[r[4]]), y(i), color[r[4]]))
    lines = []
    for i, r in enumerate(rows):
        day, kind, words, where, block = r[:5]
        href = page_url(r[5], root, "interactions") if kind == "wait" else page_url(block, root, "timeline")
        lines.append(
            f'<div class="br-row{" br-wait" if kind == "wait" else ""}" style="padding-left:{gw + 6}px" '
            f'title="{frame.esc(KIND.get(kind, kind))}: {frame.esc(words)}">'
            f'<span class="br-day">{"🙋" if kind == "wait" else frame.esc(day[5:] if len(day) == 10 else day)}</span>'
            f'<a class="br-words" href="{frame.esc(href)}">{frame.esc(words)}'
            + (f' <span class="br-where">· {frame.esc(where)}</span>' if where else '') + '</a>'
            f'<a class="br-pill" style="--c:{color[block]}" href="{frame.esc(page_url(block, root))}">'
            f'{frame.esc(block.name)}</a></div>')
    legend = "".join(f'<a class="br-chip" style="--c:{color[b]}" href="{frame.esc(page_url(b, root))}"><i></i>'
                     f'{frame.esc(b.name)}</a>' for b in order)
    keys = ('<p class="br-keys"><span>◆ Run finished</span><span>□ work session</span><span>○ change</span>'
            '<span>• note</span><span style="color:#F28C28">● waits on you</span></p>')
    body = (f'<nav class="br-legend" aria-label="Blocks">{legend}</nav>' + keys
            + f'<div class="br-map"><svg class="br-svg" width="{gw}" height="{len(rows) * ROW}" aria-hidden="true">'
            + "".join(svg) + '</svg>' + "".join(lines) + '</div>')
    word = f"{n_wait} waiting for you" if n_wait else ""     # the bar's orange 🙋 N (ui_parts.word_span)
    return CSS + BAND_CSS + band_sec(1, "🚇 Timeline", word, body, opened=True, src="ix")
