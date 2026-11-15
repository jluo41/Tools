"""Studio > Runs: every Task's hard Runs and their status."""

from __future__ import annotations

import re
from pathlib import Path

from live.frame_base import _e, _empty_view


# ── Studio › Runs: every Task's hard Runs and their status, the fourth folding part (JL 261019) ───────────
_HARD_RUN = re.compile(r"^r\d{2,3}_")
_RUN_SKIP = {"history", "_old", "_archive", "results", "result", "node_modules"}
RUN_MARK = {"complete": "✅", "completed": "✅", "done": "✅", "failed": "❌", "error": "❌", "blocked": "🟧",
            "running": "▶️", "queued": "⏳", "queued_conditional": "⏳", "planned": "⬜", "not run": "⬜",
            "no receipt": "⬜"}


def _receipt(paths) -> tuple:
    """(status, when) from the first of these files that names a status: a finished Run its finish day; a running
    one when it started and its `progress:` line, when its runner writes one (JL 261019: "show the current run
    progress"); none of them, no receipt on this machine (it may have run elsewhere, so never "not run")."""
    for p in paths:
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        m = re.search(r"(?m)^status:\s*['\"]?([A-Za-z_ ]+?)['\"]?\s*$", text)
        if m and m.group(1).strip() not in ("null", "None", ""):
            status = m.group(1).strip()
            if status == "running":
                since = re.search(r"(?m)^started_at:\s*['\"]?\d{4}-(\d{2}-\d{2})[T ](\d{2}:\d{2})", text)
                done = re.search(r"(?m)^progress:\s*['\"]?([^'\"\n]+)", text)
                return status, " · ".join(x for x in (since and f"since {since.group(1)} {since.group(2)}",
                                                     done and done.group(1).strip()) if x)
            day = re.search(r"(?m)^finished_at:\s*['\"]?(\d{4}-\d{2}-\d{2})", text)
            return status, day.group(1) if day else ""
    return "no receipt", ""


def _run_status(run: Path) -> tuple:
    """(status, when) of one hard Run folder: its result's receipt first, else its card."""
    return _receipt((run / "result/runtime.yaml", run / "run.yaml"))


def hard_runs(block: Path) -> list:
    """[(job, task, run, status, day)] for every hard Run (runs/rNN_*) of every Task under the Block, in folder order;
    soft Runs (run-*) and history copies are left out. A Run is a folder, or in the older flat layout a ticket
    runs/rNN_*.sh with its receipt in the Task's results/rNN_*/ or the Job's results/<task>/rNN_*/ (Proj11 b01)."""
    out = []
    def walk(d: Path, job: str, depth: int) -> None:
        if depth > 6:
            return
        try:
            kids = sorted(p for p in d.iterdir() if p.is_dir() and p.name not in _RUN_SKIP and not p.name.startswith("."))
        except OSError:
            return
        for k in kids:
            if k.name == "runs":
                seen = set()
                for r in sorted(p for p in k.iterdir() if _HARD_RUN.match(p.name)):
                    name = r.name if r.is_dir() else r.stem if r.suffix == ".sh" else ""
                    if not name or name in seen:
                        continue
                    seen.add(name)
                    out.append((job, d.name, name, *(_run_status(r) if r.is_dir() else _receipt((
                        d / "results" / name / "runtime.yaml", d.parent / "results" / d.name / name / "runtime.yaml")))))
            elif re.match(r"^[jt]\d{2}", k.name) or depth == 0:
                walk(k, k.name if k.name[:1] == "j" and depth <= 1 else job, depth + 1)
    walk(block, "", 0)
    return out


def runs_tally(rows: list) -> str:
    """The marks of these Runs, counted: `✅12 ⏳4 ⬜35` (the Studio's Runs part and SPACE Home share it)."""
    return _tally(rows)


def run_cells(rows: list) -> str:
    """One Task's hard Runs as the cells of an aligned `rn-grid`: mark · Run · status · finish day (the Studio's
    Runs part and SPACE Home's Job rows share it)."""
    return "".join(f'<span class=rn-mark title="{_e(st)}">{RUN_MARK.get(st, "⬜")}</span><code>{_e(name)}</code>'
                   f'<span class=rn-st>{_e(st)}</span><span class=rn-day>{_e(day)}</span>' for _, _, name, st, day in rows)


def runs_list(rows: list) -> str:
    """Hard Runs as card rows like the Jobs rows (JL 261019, on the bare lists: "they are not in the good format"):
    one folded card per Job, its Task and Run counts and tally on the right; opened, each Task a heading and its
    Runs an aligned table: mark · Run · status · finish day."""
    jobs: dict = {}
    for r in rows:
        jobs.setdefault(r[0] or "(no Job)", {}).setdefault(r[1], []).append(r)
    cards = []
    for job, tasks in jobs.items():
        body = []
        for task, rs in tasks.items():
            # each Run shows its own mark on its line; no count or tally on the page (AGENTS.md Page words, JL 261113)
            body.append(f'<div class=rn-task><b>{_e(task)}</b></div><div class=rn-grid>{run_cells(rs)}</div>')
        cards.append(f'<details class=rn-card><summary><b>{_e(job)}</b></summary>'
                     f'<div class=rn-body>{"".join(body)}</div></details>')
    return f'<div class=rn-rows>{"".join(cards)}</div>'


RUN_LEGEND = "✅ complete · ❌ failed · 🟧 blocked · ▶️ running, since when · ⏳ queued · ⬜ not run or no receipt here"
RUN_CSS = (".rn-rows{display:grid;gap:6px}.rn-card{border:1px solid var(--line);border-radius:10px;background:var(--bg);overflow:hidden}"
           ".rn-card>summary{display:flex;gap:10px;align-items:baseline;cursor:pointer;padding:8px 12px;list-style:none}"
           ".rn-card>summary::-webkit-details-marker{display:none}.rn-card>summary::before{content:'▸';color:var(--mut)}"
           ".rn-card[open]>summary::before{content:'▾'}.rn-card[open]>summary{border-bottom:1px solid var(--line)}"
           ".rn-card>summary>b{font-size:15px;overflow-wrap:anywhere}.rn-meta{color:var(--mut);font-size:13px}"
           ".rn-tally{margin-left:auto;font:12px/1.4 ui-monospace,Menlo,monospace;white-space:nowrap}"
           ".rn-body{padding:6px 12px 10px 30px}.rn-task{display:flex;gap:10px;align-items:baseline;margin:8px 0 4px}"
           ".rn-task>b{font-size:14px}.rn-grid{display:grid;grid-template-columns:22px minmax(0,1fr) 150px minmax(96px,auto);"
           "column-gap:12px;row-gap:3px;align-items:baseline;margin-left:4px}.rn-grid code{font:13px ui-monospace,Menlo,monospace;"
           "overflow-wrap:anywhere}.rn-st,.rn-day{color:var(--mut);font-size:12px}.rn-day{text-align:right}"
           ".rn-legend{color:var(--mut);font-size:12px;margin:6px 0 0}")


def _tally(rows: list) -> str:
    from collections import Counter
    c = Counter(RUN_MARK.get(r[3], "⬜") for r in rows)
    return " ".join(f"{m}{c[m]}" for m in ("✅", "❌", "🟧", "▶️", "⏳", "⬜") if c[m])


def studio_runs(block: Path, root: Path, theme=None) -> str:
    """The Studio's Runs, under Delivery (JL 261019: "list another one to show the Hard Run, for each task, and just
    show their status"): each Job, each of its Tasks, each hard Run with its mark, status and finish day. Read from
    the Runs' receipts; nothing is written. No tally: each Run carries its own mark (JL 261113)."""
    rows = hard_runs(block)
    meta = ""                                            # no tally on the page (JL 261113); each Run carries its mark
    if not rows:
        body = _empty_view("No hard Run yet: a Task's executable Runs (runs/rNN_*) list here with their status.")
    else:
        body = runs_list(rows) + f'<p class=rn-legend>{RUN_LEGEND}; read from each Run\'s result/runtime.yaml, else its run.yaml</p>'
    return (f'<details class=studio-related id=studio-runs><summary><b>Runs</b>'
            f'<span class=related-meta>{_e(meta)}</span></summary><div class=related-in>{body}</div></details>')
