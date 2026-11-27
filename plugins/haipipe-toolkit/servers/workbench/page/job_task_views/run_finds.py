"""A work Job's Findings by type: what its Runs made, named in each Run's run.yaml `finds:` (b17 trace 261127/0045).

    finds:
      - file: result/ranges.csv     # relative to the Run folder
        kind: value                 # value · display · report
        name: Value ranges          # optional; else the Task's name
        from: [../../../t01_x/runs/run-check-01-name/result/example.csv]   # optional: the raw file(s) it was made from
        how: [read example.csv, min and max per number column]           # optional: how it was made

One fold per kind, 🔢 Values, 🖼️ Displays, 📄 Reports, laid out top-view-left-tab-right-content: a left tab per file of
each Task's newest Run that names one, the file on the right, its open dot opening the file itself; a fold with one
finding shows it full width. Under a finding, each raw file of `from:` with its own open dot and a mark (✅ the finding
is newer than it, ❗ it changed after the finding was made or is gone; the why is the hover), and `how:` as a "How this
is made" fold, as the paper theme's Values link back to their source Runs (workbench-paper board_evidence.source_status;
b17 trace 261127/1215). The file stays where the Run wrote it; Findings is an index, never a copy
(haipipe-run ref/receipts-and-inventory.md).
"""
from __future__ import annotations

import csv
import io
import json
import re
from pathlib import Path

import yaml

from live import frame
from live.focus_base import inside, markdown
from live.focus_plan_results import task_name
from live.ui_parts import _side_tabs, open_dot

KINDS = (("value", "🔢 Values", "find-values"), ("display", "🖼️ Displays", "find-displays"),
         ("report", "📄 Reports", "find-reports"))
PICTURES = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")


def _list(v) -> list:
    return [str(x).strip() for x in (v if isinstance(v, list) else [v] if v else []) if str(x).strip()]


def finds(run: Path) -> list:
    """[(file, kind, name, sources, steps)] a Run names under `finds:`, only the files on disk and the three kinds;
    sources are the `from:` paths resolved against the Run folder (on disk or not), steps the `how:` lines."""
    card = run / "run.yaml"
    try:
        data = yaml.safe_load(card.read_text(encoding="utf-8", errors="ignore")) if card.is_file() else {}
    except yaml.YAMLError:
        return []
    out = []
    for item in (data or {}).get("finds") or []:
        if not isinstance(item, dict):
            continue
        f, kind = run / str(item.get("file") or ""), str(item.get("kind") or "").strip()
        if item.get("file") and f.is_file() and kind in dict((k, t) for k, t, _ in KINDS):
            out.append((f, kind, str(item.get("name") or "").strip(),
                        [(run / x).resolve() for x in _list(item.get("from"))], _list(item.get("how"))))
    return out


def _newest(run: Path) -> str:
    """A Run's newest pass as MMDD (passes/pNN-MMDD), so the Run that ran last wins; '' when it has none."""
    days = [d.name.partition("-")[2] for d in (run / "passes").glob("p*") if d.is_dir()] if (run / "passes").is_dir() else []
    return max(days, default="")


def job_finds(job: Path, root: Path) -> dict:
    """{kind: [(task, file, name, sources, steps)]}: each Task's newest Run that names a finding, in the Job's Task order."""
    out: dict = {}
    for t in (t for t in frame.children(job, "Job") if inside(t, root)):
        runs = [r for r in (t / "runs").glob("*") if r.is_dir() and finds(r)] if (t / "runs").is_dir() else []
        if not runs:
            continue
        run = max(runs, key=lambda r: (_newest(r), r.name))
        for f, kind, name, src, how in finds(run):
            out.setdefault(kind, []).append((t, f, name, src, how))
    return out


def _table(rows: list, head: list) -> str:
    th = ''.join(f'<th>{frame.esc(str(h))}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{frame.esc(str(c))}</td>' for c in r) + '</tr>' for r in rows[:200])
    return f'<table class=fx-table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def _value(f: Path) -> str:
    """A table: a .csv, a list of rows in .json, or the paper's tables.json (tabs › tables › cols, rows › cells)."""
    text = f.read_text(encoding="utf-8", errors="ignore")
    if f.suffix.lower() == ".csv":
        rows = list(csv.reader(io.StringIO(text)))
        return _table(rows[1:], rows[0]) if rows else ''
    if f.suffix.lower() == ".json":
        try:
            data = json.loads(text)
        except ValueError:
            return f'<pre class=fx-pre>{frame.esc(text[:4000])}</pre>'
        if isinstance(data, list) and data and isinstance(data[0], dict):
            head = list(data[0])
            return _table([[r.get(h, '') for h in head] for r in data], head)
        if isinstance(data, dict) and data.get("tabs"):
            out = []
            for tab in data["tabs"]:
                for tb in tab.get("tables") or []:
                    rows = [[c.get("v", "") for c in r.get("cells") or []] for r in tb.get("rows") or []]
                    out.append((f'<h4 class=fx-h>{frame.esc(str(tab.get("title") or ""))}</h4>' if tab.get("title") else '')
                               + _table(rows, tb.get("cols") or []))
            return ''.join(out)
    return f'<pre class=fx-pre>{frame.esc(text[:4000])}</pre>'


def _display(f: Path, root: Path) -> str:
    url = frame._file_url(f, root)
    if f.suffix.lower() in PICTURES:
        return f'<img class=fx-img src="{frame.esc(url)}" alt="{frame.esc(f.name)}" loading="lazy">'
    return f'<iframe class=fx-frame src="{frame.esc(url)}" title="{frame.esc(f.name)}" loading="lazy"></iframe>'


def _report(f: Path, root: Path) -> str:
    if f.suffix.lower() in (".html", ".htm", ".pdf"):
        return (f'<iframe class=fx-frame src="{frame.esc(frame._file_url(f, root))}" title="{frame.esc(f.name)}" '
                f'loading="lazy"></iframe>')
    text = f.read_text(encoding="utf-8", errors="ignore")
    return markdown(text, f.parent, root) if f.suffix.lower() == ".md" else f'<pre class=fx-pre>{frame.esc(text[:8000])}</pre>'


def _source(f: Path, src: Path, root: Path) -> str:
    """One raw file under a finding: its name with its open dot, ✅ when the finding is newer, ❗ when not or gone."""
    if not inside(src, root):
        return ''
    try:
        rel = src.relative_to(root).as_posix()
    except ValueError:
        return ''
    if not src.exists():
        mark, why = '❗', f'{rel} is gone'
    elif src.stat().st_mtime > f.stat().st_mtime:
        mark, why = '❗', f'{src.name} changed after {f.name} was made; run it again'
    else:
        mark, why = '✅', f'{f.name} was made after {src.name} last changed'
    line = (f'<div class=fx-src><span class=fx-mark title="{frame.esc(why)}">{mark}</span> '
            f'<span title="{frame.esc(rel)}">{frame.esc(src.name)}</span></div>')
    return open_dot(line, frame._file_url(src, root), src.name, pop=src.name) if src.exists() else line


def _origin(f: Path, src: list, how: list, kind: str, root: Path) -> str:
    """The raw files a finding was made from, then how it was made; nothing when the Run names neither."""
    lines = ''.join(_source(f, s, root) for s in src)
    what = {'value': 'table', 'display': 'display', 'report': 'report'}[kind]
    steps = (f'<details class=fx-how><summary>How this {what} is made</summary><ol>'
             + ''.join(f'<li>{frame.esc(h)}</li>' for h in how) + '</ol></details>') if how else ''
    return f'<div class=fx-origin>{lines}{steps}</div>' if lines or steps else ''


def sections(job: Path, root: Path) -> list:
    """[(title, word, html, waits, None, id)]: one fold per kind a Run names, for `numbered`, Values first."""
    found = job_finds(job, root)
    out = []
    for kind, title, sid in KINDS:
        rows = found.get(kind) or []
        if not rows:
            continue
        per_task = {}
        for t, *_ in rows:
            per_task[t] = per_task.get(t, 0) + 1
        items, panels = [], []
        for t, f, name, src, how in rows:
            label = name or task_name(t) + (f' · {f.name}' if per_task[t] > 1 else '')
            body = _value(f) if kind == "value" else _display(f, root) if kind == "display" else _report(f, root)
            rel = f.relative_to(t).as_posix()
            items.append((label, ''))
            panels.append(open_dot(f'<div class=fx-body title="{frame.esc(t.name + "/" + rel)}">{body}</div>',
                                   frame._file_url(f, root), rel, pop=f'{t.name} · {f.name}')
                          + _origin(f, src, how, kind, root))
        eid = 'fx' + kind[0] + re.sub(r'\W', '', job.name)
        body = panels[0] if len(panels) == 1 else _side_tabs(eid, items, panels)   # one thing: full width, no left tab
        out.append((title, '', FX_CSS + body, '', None, sid))
    return out


FX_CSS = """<style>
.fx-table{border-collapse:collapse;font-size:13px;width:100%}.fx-table th,.fx-table td{border-bottom:1px solid var(--line);padding:5px 8px;text-align:left}
.fx-table th{color:var(--muted);font-weight:500}.fx-h{margin:4px 0 6px;font-size:13px}
.fx-img{max-width:100%;display:block;margin:auto}.fx-frame{width:100%;height:420px;border:1px solid var(--line);border-radius:6px;background:#fff}
.fx-pre{white-space:pre-wrap;font-size:12.5px;margin:0}
.fx-origin{margin-top:8px;font-size:12.5px;color:var(--muted)}.fx-src{padding:3px 24px 3px 0}.fx-mark{cursor:help}
.fx-how{margin-top:4px}.fx-how summary{cursor:pointer}.fx-how ol{margin:4px 0 0 18px;padding:0}
</style>"""
