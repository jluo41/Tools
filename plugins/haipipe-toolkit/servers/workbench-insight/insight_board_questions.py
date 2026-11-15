"""The Report and Logic columns of an insight Board, and the Questions table that sets them beside the Work
column."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from .insight_board_reader import (  # noqa: F401 · this module keeps answering these names
    _TITLE, CROSS, _read, _e, _header, _parse_cell, _inline)
from .insight_board_parts import _slug, display_id
from .insight_board_work import (
    _REASONS, _STAGE, _part_label, _pop_url, _answered_by, _builds_on, _numbers, _step_label, _work_cell,
    question_notes)


# ─── the Report column: what an answer says, in a few lines ─────────────────

_STRENGTH = re.compile(r"\b(STRONG|MODERATE|WEAK)\b")


def _report_path(snap: dict, qid: str, pid: str) -> Path:
    """`reports/<segment>/<question>.md` on the board, e.g. reports/full/QI4.md."""
    row = next((p for p in snap["partitions"] if p["id"] == pid), None)
    return snap["board"] / "reports" / (row["name"] if row else pid) / f"{qid}.md"


def _sentences(text: str, n: int = 2) -> str:
    """The first n sentences, never segment inside one."""
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z`(])", text.strip())
    return " ".join(parts[:n])


def report(snap: dict, qid: str, pid: str) -> dict | None:
    """What one question's answer says on one segment.

    The answering page IS the report (a page folder is also a task
    folder, its .md says what its own results/ show).  A `reports/` file, from
    the brief report-file layout, is still read first when one exists.
    """
    if snap.get("layout") == "instance":
        return _run_report(snap, qid, pid)
    path = _report_path(snap, qid, pid)
    url = f"/_board/insight?board={quote(snap['board'].name)}&report={quote(pid + ':' + qid)}"
    if path.is_file():
        text = _read(path)
        head = _header(text)
        title = _TITLE.search(text)
        body = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()
                and not b.lstrip().startswith("#") and not re.match(r"^[a-z][a-z-]*:", b.strip())]
        return {"headline": title.group(1).strip() if title else qid, "text": _sentences(body[0]) if body else "",
                "strength": head.get("strength", ""), "limit": head.get("limit", ""), "url": url, "source": "report"}
    row = next((r for r in snap["questions"] if r["id"] == qid), None)
    page = snap["by_id"].get(((row or {}).get("cells", {}).get(pid) or {}).get("page", ""))
    if not page:
        return None
    # An old page's Opening says what the page does, not what was found, so it shows
    # only its headline.  A Page Face page (`folder-kind:` declared,
    # haipipe-insight ref/report.md § Shape) has an objective title and answers in
    # its Opening's first paragraph, so that answer is shown under the title.
    head = _header(page["text"])
    strength = _STRENGTH.search(page["state"])
    strength = head.get("strength") or (strength.group(1) if strength else "")
    text = ""
    if head.get("folder-kind"):
        opening = re.search(r"(?ms)^## Opening[ \t]*\n(.*?)(?=^\*\*|^## |\Z)", page["text"])
        if opening:
            first = opening.group(1).strip().split("\n\n")[0]
            text = _sentences(re.sub(r"\s*\[Q[DIKW]\d+\.E\d+\]", "", first), 3)
    return {"headline": page["title"], "text": text, "strength": strength,
            "limit": "", "url": _pop_url(snap, page), "source": "page", "page": page["id"]}


_LEAD = re.compile(r"(?m)^- (.+?)(?: \(`[^`]+`\))?\s*$")


def _run_report(snap: dict, qid: str, pid: str) -> dict | None:
    """A Question Book board's report: the run's generated reports/<segment>/report.md (the
    work generates the report; the page is the short answer that reads it). The cell shows its
    first lead line and opens the run; the question's page, when there is one, is named under it."""
    run = next((w for w in snap.get("work", []) if w.get("answers") == [qid] and w.get("partition") == pid), None)
    if not run:
        return None
    path = run["task_path"] / "reports" / run.get("run", pid) / "report.md"     # an Insight Block's run is <dataset>_<segment>
    if not path.is_file():
        return None
    text = _read(path)
    leads = [m.group(1) for m in _LEAD.finditer(text.split("\n## Power", 1)[0])]
    status = run.get("status", "")
    head = ("Run report" if status == "ok" else f"Run report · {status}")
    row = next((r for r in snap["questions"] if r["id"] == qid), None)
    page = snap["by_id"].get(((row or {}).get("cells", {}).get(pid) or {}).get("page", ""))
    return {"headline": head, "text": (leads[0][0].upper() + leads[0][1:] + ".") if leads else "",
            "strength": f"{len(leads) - 1} more in the report" if len(leads) > 1 else "", "limit": "", "url": run["url"],
            "source": "report", "page": page["id"] if page else "", "page_url": _pop_url(snap, page) if page else ""}


def _report_cell(snap: dict, q: dict, pid: str) -> str:
    cell = q["cells"].get(pid, _parse_cell("·"))
    if cell["mark"] == "·":
        return '<p class=wk-none>Not asked on this segment</p>'
    page = snap["by_id"].get(cell.get("page", ""))
    if cell["mark"] == "🚫" and not page:
        head, why = _REASONS.get(cell["note"], ("No answer", cell["note"]))
        return f'<p class=rp-text><b>{_e(head)}</b> · {_e(why)}</p>'
    rep = report(snap, q["id"], pid)
    if rep is None:
        return '<p class=wk-none>No report yet</p>'
    word = ("Defers to Full" if "defers" in cell["note"] else
            "Partly answered" if cell["mark"] == "🟡" else
            "No answer" if cell["mark"] == "🚫" else "")
    tags = " · ".join(x for x in (rep["strength"], rep["limit"]) if x)
    return ('<p class=rp-label><span class=kind>Report</span>'
            + (f' <span class=mut>{_e(word)}</span>' if word else "") + '</p>'
            f'<p class=rp-title><a class=pop href="{_e(rep["url"])}" data-pop="{_e(rep["headline"])}">{_e(rep["headline"])}</a></p>'
            + (f'<p class=rp-text>{_inline(rep["text"])}</p>' if rep["text"] else "")
            + (f'<p class=rp-tags>{_e(tags)}</p>' if tags else "")
            + (f'<p class=rp-tags>page {_e(display_id(rep["page"], {p["id"]: p["name"] for p in snap["partitions"]}))}</p>'
               if rep["source"] == "page" else "")
            + (f'<p class=rp-tags>answer: <a class=pop href="{_e(rep["page_url"])}" data-pop="{_e(rep["page"])}">'
               f'page {_e(rep["page"])}</a></p>' if rep.get("page_url") else ""))


def _logic_cell(snap: dict, q: dict, cell: dict, base: list[str]) -> str:
    """Question N · its short name, the ask, then (folded) why it matters, what
    would answer it and what was expected: rich enough to read, closed by default."""
    note = question_notes(snap).get(q["id"], {})
    short = q["question"][:1].upper() + q["question"][1:]      # the Queue row: short, plain
    rows = [(label, note.get(key, "")) for label, key in
            (("The ask", "ask"), ("Why it matters", "why"), ("What would answer it", "answer"), ("Expected", "expect"))]
    rows = [(label, text) for label, text in rows if text]
    needs = note.get("needs") or []
    need_dd = ("".join(f'<li>{_step_label(n, e, kind)} · {_inline(text)}</li>' for n, (e, kind, text) in enumerate(needs, 1))
               if needs else "")
    more = ('<details class=q-more><summary>More</summary><dl>'
            + "".join(f'<dt>{_e(label)}</dt><dd>{_inline(text[:1].upper() + text[1:])}</dd>' for label, text in rows)
            + (f'<dt>How it is answered <span class=mut>{"agreed" if note.get("agreed", "").startswith("✅") else "not agreed"}</span></dt>'
               f'<dd><ul class=q-needs>{need_dd}</ul></dd>' if needs else "")
            + '</dl></details>') if rows or needs else ""
    # the mark sits right after its label: the status belongs to the question
    return (f'<div class=q-top><span class=kind>Question {_e(q["id"][2:])}</span>'
            f'<span class=mark>{_e(cell["mark"] if cell["mark"] != "·" else "")}</span></div>'
            f'{("<div class=q-title><b class=q-name>" + _e(note["name"]) + "</b></div>") if note.get("name") else ""}'
            f'<div class=q-text>{_inline(short)}</div>'
            f'{("<div class=q-sub>builds on " + _e(_numbers(base)) + "</div>") if base else ""}{more}')


def _questions_table(snap: dict, pid: str, sel: str, answered: dict) -> str:
    """One partition's table: Logic (the questions asked at each level), Work (the
    runs that answer them), Report (what each answer says).  Every audience table lists
    the same questions in the same order; only the work and the marks change.
    Cross owns no rows, so it lists only the questions that compare the segments."""
    groups = []
    open_level = sel.split(":")[-1][1:2] if ":" in sel else ""
    for lv in "DIKW":
        rows = [q for q in snap["questions"] if q["id"][1] == lv
                and (pid != CROSS or q["cells"].get(CROSS, {}).get("mark", "·") != "·")]
        if not rows:
            continue
        body = []
        for q in rows:
            cell = q["cells"].get(pid, _parse_cell("·"))
            page = snap["by_id"].get(cell.get("page", ""))
            key = f"{pid}:{q['id']}"
            base = _builds_on(snap, page, q["id"], answered)
            muted = " dim" if cell["mark"] in {"·", "🚫"} and not page else ""
            body.append(
                f'<div class="hl-row{muted}{" on" if key == sel else ""}" data-key="{_e(key)}" '
                f'data-label="{_e(_STAGE[lv])} question {_e(q["id"][2:])} · {_e(_part_label(snap, pid))}" data-q="{_e(q["id"])}">'
                f'<div class=hl-l>{_logic_cell(snap, q, cell, base)}</div>'
                f'<div class=hl-r>{_work_cell(snap, q, pid, answered)}</div>'
                f'<div class=hl-p>{_report_cell(snap, q, pid)}</div></div>')
        reg = rows[0]["register"]
        source = (f'<a class="pop lvl-src" href="{_e(_pop_url(snap, reg))}" data-pop="{_e(reg["title"])}">'
                  f'{_e(reg["id"])} · {_e(_slug(reg))} ↗</a>')
        groups.append(f'<details class=lvl{" open" if lv == open_level else ""}><summary>{_e(_STAGE[lv])} questions '
                      f'<span class=mut>{len(rows)}</span>{source}</summary>{"".join(body)}</details>')
    row = next((p for p in snap["partitions"] if p["id"] == pid), {})
    size = f' · {row["rows"]} rows' if row.get("rows") else (" · compares the segments" if pid == CROSS else "")
    return (f'<div class=hl data-part="{_e(pid)}"><h2>{_e(_part_label(snap, pid))}{_e(size)}</h2>'
            '<div class=hl-head><span>Logic · the question</span><span>Work · the runs</span><span>Report · what it says</span></div>'
            + "".join(groups) + '</div>')


def _render_questions(snap: dict, pid: str, sel: str) -> str:
    parts = [p["id"] for p in snap["partitions"]
             if any(p["id"] in q["cells"] for q in snap["questions"])]
    if not parts:
        return '<p class=note>No register question on this board yet. Ask one in Scope › Questions.</p>'
    pid = pid if pid in parts else parts[0]
    answered = _answered_by(snap)
    chips = "".join(f'<button type=button class="part{" on" if p == pid else ""}" data-part="{_e(p)}">{_e(_part_label(snap, p))}</button>'
                    for p in parts)
    tables = "".join(_questions_table(snap, p, sel if sel.startswith(p + ":") else "", answered) for p in parts)
    return f'<div class=parts>{chips}</div><div class=hls data-on="{_e(pid)}">{tables}</div>'
