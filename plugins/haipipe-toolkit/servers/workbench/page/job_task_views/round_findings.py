"""A work Job's round findings: what its Tasks' rounds found (b17 trace 261126/1145_job_findings).

Laid out top-view-left-tab-right-content, as the Tasks band is grouped: a numbered fold per Task group (the face's
`bands:` line, `t0N Task Group 1`), in it a left tab per Task that has a round (its name, its newest round's state),
and on the right that round: its title and when, what it found (its pass.md Summary), what it changed, and the
round itself to open in the page's viewer. A Task with no round yet has nothing found and no tab.
"""
from __future__ import annotations

import re
from pathlib import Path

from live import frame
from live.focus_base import inside
from live.focus_jobs import band_names
from live.focus_plan_results import round_rows, task_name
from live.state_marks import WORDS
from live.ui_parts import _side_tabs, open_dot, state_mark


def _section(text: str, name: str) -> str:
    return (re.search(rf"(?ms)^## {name}\s*\n(.*?)(?=^## |\Z)", text) or [None, ""])[1].strip()


def _panel(task: Path, mark: str, title: str, small: str, where: Path, root: Path) -> str:
    """The newest round of a Task: what it found, what it changed, and the round to open."""
    md = where / "pass.md"
    text = md.read_text(encoding="utf-8", errors="ignore") if md.is_file() else ""
    found, changed = _section(text, "Summary"), _section(text, "Changed")
    changed = [c.strip("-* `") for c in changed.splitlines() if c.strip() and c.strip() not in ("<nothing>", "-")]
    run = where.parent.parent.name
    body = (f'<div class=rf-head>{state_mark(mark)}<b>{frame.esc(title)}</b><small>{frame.esc(small)} · {frame.esc(run)}</small></div>'
            + (f'<p class=pb-big>{frame.esc(found)}</p>' if found else '')
            + (f'<ul class=rf-changed>' + ''.join(f'<li><code>{frame.esc(c)}</code></li>' for c in changed[:12]) + '</ul>'
               if changed else ''))
    # the round itself opens from the dot on the top-right corner, never an "Open ↗" word (AGENTS.md › UI design)
    return open_dot(body, frame._file_url(md, root), "pass.md", pop=task.name + " · " + title) if md.is_file() else body


def _word(mark: str) -> str:
    """A tab's state word, from its round's mark (the Files pane's words: waits for you, running, done)."""
    from live.focus_plan_results import row_key
    return WORDS.get(row_key(mark), "")


def sections(job: Path, root: Path) -> list:
    """[(title, word, body, waits)]: one numbered section per Task group with a found round, for `numbered`."""
    tasks = [t for t in frame.children(job, "Job") if inside(t, root)]
    named = band_names(frame.face(job)) if frame.face(job) else {}
    groups = {}
    for t in tasks:
        rounds = [r for r in round_rows(t) if r[4] == "round"]
        if not rounds:
            continue
        rounds.sort(key=lambda r: r[5].name.partition("-")[2], reverse=True)     # the newest round of any Run
        d = re.match(r"t(\d)\d", t.name)
        groups.setdefault(d.group(1) if named and d else "", []).append((t, rounds[0]))
    out = []
    for d, rows in groups.items():
        title = named.get(d, "").strip() or "Tasks"
        eid = "rf" + re.sub(r"\W", "", job.name) + (d or "x")
        items = [(task_name(t), _word(r[0])) for t, r in rows]
        panels = [_panel(t, r[0], r[1], r[2], r[5], root) for t, r in rows]
        waits = any(w == WORDS.get("you") for _, w in items)
        word = WORDS.get("you", "waits for you") if waits else ""
        out.append(("📌 " + title, word, ROUND_CSS + _side_tabs(eid, items, panels), ""))
    return out


ROUND_CSS = """<style>
.rf-head{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:0 0 8px}.rf-head small{color:var(--muted)}
.rf-changed{margin:6px 0 0;padding-left:18px;font-size:13px}
</style>"""
