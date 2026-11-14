"""What the paper Board's evidence Jobs say about one Section: each printed value of this Section in the value Job's
ledger (j02_evidence_value, result/ledger.csv) and each citation in the citation Job's (j03_evidence_cite,
result/citations.csv), newest Run per Task.

A Section never runs evidence itself; the Board's evidence Jobs do, and the Section reads their verdict (JL 261113,
on a Section's own "Runs of this step": "do we need this? how do you think this to the block level evidence???").
Read-only.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

from live.frame import esc

STATUS_CLASS = {"match": "ok", "verified": "ok", "mismatch": "bad", "differs": "bad", "missing": "bad",
                "no anchor": "mut", "owed": "wait"}

CHECK_CSS = ("<style>.bc-row{display:grid;grid-template-columns:60px 1fr auto auto;gap:4px 12px;align-items:baseline;"
             "padding:5px 0;border-top:1px solid var(--line);font-size:13.5px}.bc-row .s{color:var(--muted);font-size:12px}"
             ".bc-st{font-size:12px;font-weight:600;border-radius:9px;padding:0 7px;border:1px solid var(--line)}"
             ".bc-st.ok{color:#2f9e44;border-color:#b2f2bb}.bc-st.bad{color:#e03131;border-color:#ffc9c9}"
             ".bc-st.wait{color:#e67700;border-color:#ffd8a8}.bc-st.mut{color:var(--muted)}"
             ".bc-row a{font-size:12px}.bc-h{margin:10px 0 2px;font-size:12.5px;font-weight:600;color:var(--muted)}"
             "@media(max-width:600px){.bc-row{grid-template-columns:44px 1fr}}</style>")


def _board(folder: Path) -> Path | None:
    from live.address_links import paper_board_of
    return paper_board_of(folder)


def _newest(task: Path, name: str) -> Path | None:
    """The newest Run's result file of a Board evidence Task."""
    found = sorted(task.glob(f"runs/r[0-9]*/result/{name}"))
    return found[-1] if found else None


def _read(path: Path) -> list:
    try:
        with path.open(encoding="utf-8", newline="") as fh:
            return list(csv.DictReader(fh))
    except (OSError, csv.Error):
        return []


def _num(s: str) -> int:
    m = re.search(r"\d+", s or "")
    return int(m.group(0)) if m else 0


def value_checks(folder: Path) -> list:
    """[(sentence, printed, value, status, label, Task)] for this Section, from every value Task's newest ledger."""
    board = _board(folder)
    out = []
    for task in sorted(board.glob("j*_evidence_value/t[0-9]*_*")) if board else []:
        ledger = _newest(task, "ledger.csv")
        for r in _read(ledger) if ledger else []:
            if (r.get("section") or "").strip() == folder.name:
                out.append(((r.get("sentence") or "").strip(), (r.get("printed") or "").strip(),
                            (r.get("value") or "").strip(), (r.get("status") or "").strip().lower(),
                            (r.get("label") or r.get("key") or "").strip(), task))
    return sorted(out, key=lambda x: _num(x[0]))


def cite_checks(folder: Path) -> list:
    """[(sentences, key, status, Task)] for this Section, from every citation Task's newest citations.csv."""
    board = _board(folder)
    out = []
    for task in sorted(board.glob("j*_evidence_cite/t[0-9]*_*")) if board else []:
        table = _newest(task, "citations.csv")
        for r in _read(table) if table else []:
            m = re.search(rf"{re.escape(folder.name)}\s+((?:S\d+[a-z]?(?:,\s*)?)+)", r.get("cited_in") or "")
            if m:
                out.append((m.group(1).strip(" ,"), (r.get("key") or "").strip(),
                            (r.get("status") or "").strip().lower(), task))
    return sorted(out, key=lambda x: _num(x[0]))


def _task_link(task: Path, root: Path) -> str:
    from live.address_links import href
    job = task.parent
    label = f"{job.name.split('_')[0]}.{task.name.split('_')[0]}"
    return f'<a href="{esc(href(task, root))}" data-pop="{esc(task.name)}" title="{esc(task.name)}">{esc(label)}</a>'


def checks_html(folder: Path, root: Path) -> tuple:
    """(html, word) of "Checked at the Board" for a Section: its printed values, then its citations."""
    values, cites = value_checks(folder), cite_checks(folder)
    if not values and not cites:
        return "", ""
    pill = lambda st: f'<span class="bc-st {STATUS_CLASS.get(st, "mut")}">{esc(st or "not read")}</span>'
    html = CHECK_CSS
    if values:
        html += '<p class=bc-h>Printed values · the value Job</p>' + "".join(
            f'<div class=bc-row><span class=s>{esc(s)}</span><span>{esc(printed or "not printed")}'
            + (f' <span class=s>· {esc(label)}</span>' if label else "") + f'</span>{pill(st)}{_task_link(task, root)}</div>'
            for s, printed, value, st, label, task in values)
    if cites:
        html += '<p class=bc-h>Citations · the citation Job</p>' + "".join(
            f'<div class=bc-row><span class=s>{esc(s)}</span><span><code>{esc(key)}</code></span>{pill(st)}'
            f'{_task_link(task, root)}</div>' for s, key, st, task in cites)
    return html, ""                              # each row's pill shows its state; no "N differ" / "all match" tally
