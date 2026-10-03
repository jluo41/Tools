"""Read a Prototype and Instance board for the Insight workbench (no UI of its own).

A board made the Prototype way (haipipe-insight ref/prototype-contract.md) is drawn by
the SAME Insight workbench as every InsightBoard: insightboard.render_insight_board,
its four Spaces, Insight › Questions one table per partition with Logic · Work ·
Report, the Runs panels and the pop-outs. This module only READS the new layout and
returns the snapshot shape insightboard.py already renders:

    questions   one row per Prototype question, id `Q<L><N>` (I03 → QI3), its cells
                computed by haipipe-insight-check ref/check_instance.py
    pages       the question's page in its Instance folder, plus the meta page the
                Dataset view reads (the Prototype's 0-Meta/meta.md, carried word for
                word from the board it was made from; else 0-Meta/input.md and D01's results)
    work        one run per question × partition (runs/<partition>.sh)
    notes       each question file's short question, name, ask, why now, what would
                answer it, any other carried field, and its live needs

It also serves the two pop-outs the workbench opens: a run (receipt, generated
report, tables, as the existing run pop-out lays them out) and a file of the two boards.
"""

from __future__ import annotations

import html
import importlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

import yaml

from host_paths import SKILLS

_REF = SKILLS / "insight" / "haipipe-insight" / "ref"
_CHECK = SKILLS / "insight" / "haipipe-insight-check" / "ref"
_LEVEL = {"D": "data", "I": "information", "K": "knowledge", "W": "wisdom"}
_STAGE = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}
_TEXT = {".md", ".csv", ".tsv", ".json", ".yaml", ".yml", ".py", ".sh", ".txt", ".lock"}
KINDS = ("insight-instance", "insight-prototype")


def _tools():
    """The contract's own readers: the checker, the runner's helpers, the sync states."""
    for p in (str(_REF), str(_CHECK)):
        if p not in sys.path:
            sys.path.insert(0, p)
    return (importlib.import_module("check_instance"), importlib.import_module("run_question"),
            importlib.import_module("sync_instance"))


def _e(v) -> str:
    return html.escape("" if v is None else str(v), quote=True)


def board_kind(board: Path) -> str:
    """`insight-instance`, `insight-prototype`, or '' (a board made another way)."""
    path = Path(board) / "board.md"
    m = re.match(r"^---\n(.*?)\n---", path.read_text(encoding="utf-8") if path.is_file() else "", re.S)
    try:
        kind = (yaml.safe_load(m.group(1)) or {}).get("board-kind", "") if m else ""
    except yaml.YAMLError:
        return ""
    return kind if kind in KINDS else ""


def _front(path: Path) -> tuple[dict, str]:
    try:
        return _tools()[1].front(path)
    except Exception:  # noqa: BLE001 · a broken file reads as empty, never raised to the reader
        return {}, ""


def _title(text: str, fallback: str) -> str:
    m = re.search(r"(?m)^#\s+(.+?)\s*$", text) or re.search(r"(?m)^(.+)\n=+\s*$", text)
    return m.group(1).strip() if m else fallback


def _field(prose: str, label: str) -> str:
    m = re.search(rf"(?ms)^\*\*{re.escape(label)}\*\*:\s*(.+?)(?=\n\s*\n|\Z)", prose)
    return " ".join(m.group(1).split()) if m else ""


def file_url(board: Path, path: Path, root: Path) -> str:
    return (f"/_board/insight-board?board={quote(Path(board).name)}"
            f"&file={quote(Path(path).resolve().relative_to(Path(root).resolve()).as_posix())}")


def run_url(board: Path, qfolder: Path, partition: str, root: Path) -> str:
    rel = Path(qfolder).resolve().relative_to(Path(board).resolve()).as_posix()
    return (f"/_board/insight-run?board={quote(Path(board).name)}&task={quote(rel, safe='/')}"
            f"&call={quote(partition)}")


def legacy_qid(qid: str) -> str:
    """I03 → QI3: the id shape the Insight workbench reads (its level, then its number)."""
    return f"Q{qid[0]}{int(qid[1:])}"


def instances_of(prototype: Path) -> list[Path]:
    prototype = Path(prototype).resolve()
    out = []
    for b in sorted(prototype.parent.glob("*/board.md")):
        meta = _front(b)[0]
        if meta.get("board-kind") == "insight-instance" and (b.parent / meta.get("prototype", "")).resolve() == prototype:
            out.append(b.parent)
    return out


def _cell(mark: str, page_id: str) -> dict:
    """A computed status as the cell the workbench reads: mark, page, note."""
    if not mark or mark == "—":
        return {"mark": "·", "page": "", "note": "", "raw": "·"}
    if mark.startswith("✅"):
        m, note = "✅", ""
    elif mark.startswith("🚫"):
        m, note = "🚫", mark[1:].replace("⚑", "").strip()
    elif mark.startswith("STALE"):
        m, note = "🟡", "stale: rerun the partition, then re-read"
    else:
        m, note = "🟡", ""
    if "⚑" in mark:
        note = (note + " · scripts differ from the Prototype").strip(" ·")
    return {"mark": m, "page": page_id, "note": note, "raw": f"{m} {page_id} {note}".strip()}


def _meta_page(board: Path, proto: Path, root: Path, rq, d01_done: bool) -> dict:
    """The meta page the Dataset view, the banner and gate GI0 read: the Prototype's carried
    meta page when it has one, else its input and what D01 measured on this extract. A fact
    with no source is left out, never guessed."""
    carried = proto / rq.META / "meta.md"
    if carried.is_file():
        text = carried.read_text(encoding="utf-8")
        return {"path": carried, "rel": "0-Meta/meta.md", "id": "MT00", "text": text,
                "title": _title(text, "The extract"), "state": "✅ measured by D01" if d01_done else "OPEN",
                "page_type": "meta", "identity_error": "", "rung": "", "level": "", "partition": "",
                "receipt_field": "", "url": file_url(board, carried, root)}
    meta = _front(board / "board.md")[0]
    inp, inp_text = _front(proto / rq.META / "input.md")
    extract = meta.get("extract", "")
    lines = ["# The extract", "", f"{Path(extract).parent.as_posix()}/"]
    d01 = next(iter(sorted((board / rq.RUNG_DIR["D"]).glob("D01-*/results/full"))), None)
    shape = {}
    if d01 and (d01 / "extract_shape.json").is_file():
        shape = json.loads((d01 / "extract_shape.json").read_text())
    lines.append(f"{Path(extract).name}" + (f"   {shape['n_rows']:,} × {shape['n_columns']}" if shape else ""))
    if inp.get("row"):
        lines += ["", f"One row is one {str(inp['row']).removeprefix('one ')}."]
    values = d01 / "column_values.csv" if d01 else None
    if values and values.is_file() and shape:
        import pandas as pd
        v = pd.read_csv(values).set_index("column")
        if "invitation_date" in v.index and pd.notna(v.loc["invitation_date", "value_min"]):
            lines += ["", f"Sent {v.loc['invitation_date', 'value_min']} to {v.loc['invitation_date', 'value_max']} · "
                          f"{shape['n_rows']:,} message rows"]
    return {"path": proto / rq.META / "input.md", "rel": "0-Meta/input.md", "id": "MT00",
            "text": "\n".join(lines) + "\n\n" + inp_text, "title": "The extract",
            "state": "✅ measured by D01" if d01_done else "OPEN", "page_type": "meta", "identity_error": "",
            "rung": "", "level": "", "partition": "", "receipt_field": "",
            "url": file_url(board, proto / rq.META / "input.md", root)}


def legacy_snapshot(board: Path, root: Path) -> dict:
    """The snapshot insightboard.render_insight_board draws, read from a Prototype and its Instance."""
    ci, rq, sy = _tools()
    board, root = Path(board).resolve(), Path(root).resolve()
    meta = _front(board / "board.md")[0]
    proto = (board / meta.get("prototype", "")).resolve()
    parts = _front(proto / rq.META / "partitions.md")[0].get("partitions") or []
    problems, grid, check_notes = ci.run(board)
    pages, questions, work, notes, report_rows, rows_of, registers = [], [], [], {}, [], {}, {}
    for pq in rq.question_folders(proto):
        q, prose = _front(pq / f"{pq.name}.md")
        if not q or q.get("retired"):                   # a retired question is history: not on the board
            continue
        qid, lid, letter = pq.name[:3], legacy_qid(pq.name[:3]), pq.name[0]
        iq = board / pq.parent.name / pq.name
        rung_md = proto / pq.parent.name / "rung.md"
        reg = registers.setdefault(letter, {
            "path": proto / pq.parent.name / f"{pq.parent.name}-questions.md", "rel": pq.parent.name, "id": pq.parent.name,
            "text": rung_md.read_text(encoding="utf-8") if rung_md.is_file() else "",
            "title": f"{_STAGE[letter]} questions", "state": "OPEN", "page_type": "question",
            "identity_error": "", "rung": _LEVEL[letter], "level": "", "partition": "", "receipt_field": "",
            "url": file_url(board, proto / pq.parent.name, root)})
        page_md, page_id = iq / f"{iq.name}.md", ""
        if page_md.is_file():
            text = page_md.read_text(encoding="utf-8")
            marks = [m for m in grid.get(qid, {}).values() if m != "—"]
            page_id = qid
            pages.append({"path": page_md, "rel": page_md.relative_to(board).as_posix(), "id": qid, "text": text,
                          "title": _title(text, iq.name),
                          "state": "✅ CHECK closed" if marks and all(m.startswith("✅") for m in marks) else "🟡 owed",
                          "page_type": _LEVEL[letter], "identity_error": "", "rung": "", "level": _LEVEL[letter],
                          "partition": "", "receipt_field": "", "url": file_url(board, page_md, root)})
        cells = {p: _cell(m, page_id) for p, m in grid.get(qid, {}).items() if m != "—"}
        carried = (q.get("source") or {}).get("cells") or {}
        for p, m in grid.get(qid, {}).items():          # not asked here: the old board's refusal, as it read
            if m == "—" and str(carried.get(p, "")).startswith("🚫 "):
                reason = carried[p][2:].strip()
                cells[p] = {"mark": "🚫", "page": "", "note": reason, "raw": f"🚫 {reason}"}
        questions.append({"id": lid, "question": q.get("question") or q.get("ask", ""), "register": reg,
                          "cells": cells, "folder": pq.name, "qid": qid})
        extra = {k: v for k, v in re.findall(r"(?m)^\*\*([^*]{2,60})\*\*:\s*(.+?)\s*$", prose)
                 if k not in ("Why", "Why now", "What would answer it")}
        notes[lid] = {"_reg": reg["id"], "name": q.get("name") or _title(prose, pq.name), "ask": q.get("ask", ""),
                      "why": _field(prose, "Why now") or _field(prose, "Why"),
                      "answer": _field(prose, "What would answer it"),
                      "expect": next((v for k, v in extra.items() if "expect" in k.lower()), ""),
                      "needs": [(nid, n.get("kind", ""), n.get("what", "")) for nid, n in (q.get("needs") or {}).items()
                                if not n.get("retired")],
                      "agreed": str(q.get("agreed", "")), "spec": q}
        for part in rq.asked_partitions(q, parts):
            rec_path = iq / "results" / part / "runtime.yaml"
            rec = (yaml.safe_load(rec_path.read_text()) if rec_path.is_file() else {}) or {}
            status = rec.get("status", "not run")
            if rec.get("rows_after"):
                rows_of.setdefault(part, rec["rows_after"])
            url = run_url(board, iq, part, root)
            work.append({"task_path": iq, "family": pq.parent.name, "job": "", "task": pq.name, "call": part,
                         "status": status, "page": iq.name, "source": "page-ticket", "answers": [lid],
                         "partition": part, "ticket": iq / "runs" / f"{part}.sh", "receipt": rec_path,
                         "config": None, "ran": rec_path.is_file(), "task_run": part, "qid": qid, "url": url,
                         "receipt_data": rec})
            if (iq / "reports" / part / "report.md").is_file():
                report_rows.append({"name": f"{lid} · {part}", "status": status, "url": url, "keys": [f"{part}:{lid}"]})
    full_rows = rows_of.get("full")
    partitions = []
    for p in parts:
        where = " AND ".join(f'{c["column"]} {k} {v}' for c in (p.get("where") or []) for k, v in c.items()
                             if k != "column")
        n = rows_of.get(p["name"])
        partitions.append({"id": p["name"], "name": p["name"], "folder": "",
                           "pages": sum(1 for q in questions if q["cells"].get(p["name"], {}).get("page")),
                           "where": where, "rows": f"{n:,}" if n else "",
                           "share": f"{n / full_rows * 100:.2f}%" if n and full_rows else "", "config": ""})
    d01_done = str(grid.get("D01", {}).get("full", "")).startswith("✅")
    pages.insert(0, _meta_page(board, proto, root, rq, d01_done))
    by_id = {p["id"]: p for p in pages}
    for reg in registers.values():
        by_id.setdefault(reg["id"], reg)
    return {
        "layout": "instance", "current": True, "board": board, "root": root, "board_arg": board.name,
        "static": False, "relative": board.relative_to(root).as_posix(),
        "title": board.name, "store": "", "store_path": None, "board_topic": "", "context": "",
        "pages": pages, "by_id": by_id, "partitions": partitions, "questions": questions,
        "question_ids": [q["id"] for q in questions],
        "registers": {lvl: [] for lvl in ("data", "information", "knowledge", "wisdom")},
        "runs": [], "events": [], "workflow_runtimes": [], "handoffs": [],
        "settled": sum(p["state"].startswith("✅") for p in pages),
        "work": work, "notes": notes, "report_rows": report_rows,
        "instance_problems": problems, "instance_notes": check_notes, "prototype": proto,
    }



def render_prototype(board: Path, root: Path) -> str:
    """Scope › Prototype: the design this Instance reads its extract through (JL 261002: Scope is the
    board's own data to understand, and the Prototype is part of it). Laid out for the reader
    (JL 261003: "not well designed"): what the Prototype is with four numbers; one table by rung of
    questions, needs, scripts and this board's copies; only the copies that need action; the design
    files last. Read-only: a question changes by a signed change, a script by sync_instance.py."""
    ci, rq, sy = _tools()
    board, root = Path(board).resolve(), Path(root).resolve()
    meta = _front(board / "board.md")[0]
    proto = (board / meta.get("prototype", "")).resolve()
    if not (proto / "board.md").is_file():
        return '<p class=note>This board does not name a Prototype in its <code>board.md</code>.</p>'
    link = lambda path, label: (f'<a class=pop href="{_e(file_url(board, path, root))}" data-pop="{_e(label)}">'
                                f'{_e(label)}</a>' if path.exists() else f'<span class=mut>{_e(label)} · missing</span>')
    title = _title(_front(proto / "board.md")[1], proto.name)

    # the questions by rung, and this board's script copies by rung
    rungs = {}
    for pq in rq.question_folders(proto):
        q = _front(pq / f"{pq.name}.md")[0]
        r = rungs.setdefault(pq.parent.name, {"live": 0, "retired": 0, "scripts": 0, "needs": 0, "copies": {}})
        if q.get("retired"):
            r["retired"] += 1
            continue
        r["live"] += 1
        r["scripts"] += bool(list((pq / "scripts").glob("*.py")))
        r["needs"] += sum(1 for n in (q.get("needs") or {}).values() if not (n or {}).get("retired"))
    rows = sy.status(board)
    for iq, _, st, _ in rows:
        c = rungs.setdefault(iq.parent.name, {"live": 0, "retired": 0, "scripts": 0, "needs": 0, "copies": {}})["copies"]
        c[st] = c.get(st, 0) + 1
    total = lambda k: sum(r[k] for r in rungs.values())
    in_sync = sum(1 for *_, st, _ in rows if st == "in sync")

    tile = lambda n, label: f'<div class=ptile><b>{n}</b><span>{_e(label)}</span></div>'
    head = (f'<h2>Meta</h2><div class=pcard><div class=ptitle>{link(proto / "board.md", proto.name)}</div>'
            f'<div class=psub>{_e(title)}</div>'
            '<p class=lead>The design this board reads its extract through: the partitions, the questions and their '
            'scripts, and no data. This board holds one run per partition and one page per question.</p>'
            '<div class=ptiles>' + tile(total("live"), "live questions") + tile(total("needs"), "live needs")
            + tile(total("scripts"), "with a script")
            + tile(f'{in_sync}/{len(rows)}' if rows else "—", "copies in sync") + '</div></div>')

    state_mark = {"in sync": "✅", "new in prototype": "⬇️", "prototype changed": "🔄",
                  "instance changed": "✏️", "both changed": "❗"}
    def copies(c):
        if not c:
            return '<span class=mut>—</span>'
        return " · ".join(f'{state_mark.get(st, "")} {n} {_e(st)}' for st, n in sorted(c.items(), key=lambda kv: kv[0] != "in sync"))
    table = ('<h3>By rung</h3><table><tr><th>Rung</th><th class=num>Questions</th><th class=num>Needs</th>'
             '<th class=num>Scripts</th><th>This board\'s copies</th><th class=num>Retired</th></tr>'
             + "".join(f'<tr><td>{link(proto / name / "rung.md", name)}</td><td class=num>{r["live"]}</td>'
                       f'<td class=num>{r["needs"]}</td><td class=num>{r["scripts"] or "—"}</td>'
                       f'<td>{copies(r["copies"])}</td><td class=num>{r["retired"] or "—"}</td></tr>'
                       for name, r in sorted(rungs.items()))
             + '</table><p class=mut>A question changes only by a signed change: the old one is retired, never edited.</p>')

    # only the copies that need something, grouped by what they need
    act = {"new in prototype": "In the Prototype, not copied here yet",
           "prototype changed": "Changed in the Prototype since the copy",
           "instance changed": "Changed here; a different agent reviews it",
           "both changed": "Changed in both; merge by hand"}
    groups = {}
    for iq, name, st, rev in rows:
        if st in act:
            groups.setdefault(st, []).append((iq, name, rev))
    if groups:
        todo = '<h3>Needs action</h3>'
        for st, items in groups.items():
            chips = "".join(f'<span class=chip title="{_e(name)}{" · reviewed" if rev else ""}">'
                            f'{link(proto / iq.parent.name / iq.name / f"{iq.name}.md", iq.name.split("-")[0])}</span>'
                            for iq, name, rev in items)
            todo += (f'<div class=pact><div><b>{state_mark[st]} {len(items)} · {_e(act[st])}</b></div>'
                     f'<div class=pchips>{chips}</div></div>')
        todo += '<p class=mut>Settle a copy with <code>sync_instance.py</code> (haipipe-insight): --diff, --pull, --reviewed.</p>'
    elif rows:
        todo = '<p class=note>✅ Every script copy matches the Prototype.</p>'
    else:
        todo = '<p class=note>No question has scripts yet.</p>'

    shared = sorted(proto.glob("src/*.py")) + sorted(proto.glob("[1-4]-*/src/*.py"))
    files = ('<h3>Design files</h3><table>'
             '<tr><th>Partitions and data</th><td>' + " · ".join(link(proto / rq.META / n, n) for n in
                                                    ("meta.md", "partitions.md", "thresholds.yaml")) + '</td></tr>'
             '<tr><th>Rung rules</th><td>' + " · ".join(link(f, f.parent.name) for f in sorted(proto.glob("[1-4]-*/rung.md")))
             + '</td></tr>'
             + (f'<tr><th>Shared code</th><td><details><summary>{len(shared)} modules two or more questions use</summary>'
                + "<br>".join(link(f, f.relative_to(proto).as_posix()) for f in shared) + '</details></td></tr>' if shared else '')
             + '</table>')
    return head + table + todo + _partitions_html(proto) + _settings_html(proto) + files


def _where_text(rule: dict) -> str:
    """One filter condition in words: {column: age, lte: 35} -> `age ≤ 35`."""
    ops = {"eq": "=", "ne": "≠", "lt": "<", "lte": "≤", "gt": ">", "gte": "≥", "in": "in"}
    col = rule.get("column", "?")
    for k, sym in ops.items():
        if k in rule:
            v = rule[k]
            v = int(v) if isinstance(v, float) and v.is_integer() else v
            return f"{col} {sym} {v}"
    return col


def _partitions_html(proto: Path) -> str:
    """0-Meta/partitions.md as a table: each partition and who it holds, in words."""
    rows = (_front(proto / "0-Meta" / "partitions.md")[0].get("partitions") or [])
    if not rows:
        return ''
    body = "".join(
        f'<tr><td class=mono>{_e(r.get("name", ""))}</td><td>'
        + (_e("every row") if not r.get("where") and not r.get("of") else
           _e("compares " + ", ".join(r["of"])) if r.get("of") else
           _e(" · ".join(_where_text(w) for w in r["where"]))) + '</td></tr>' for r in rows)
    return ('<h3>Partitions</h3><table><tr><th>Partition</th><th>Who it holds</th></tr>' + body +
            '</table><p class=mut>Row counts for this board are in Scope › Partitions.</p>')


def _settings_html(proto: Path) -> str:
    """0-Meta/thresholds.yaml as a table: one row per section, its values side by side."""
    path = proto / "0-Meta" / "thresholds.yaml"
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return ''
    flat = lambda v: (", ".join(f"{k} {flat(x)}" for k, x in v.items()) if isinstance(v, dict)
                      else "not set" if v is None else str(v))
    body = "".join(f'<tr><td class=mono>{_e(k)}</td><td>{_e(flat(v))}</td></tr>' for k, v in data.items())
    return ('<h3>Shared settings</h3><table><tr><th>Section</th><th>Values</th></tr>' + body + '</table>'
            '<p class=mut>A question names a section here and never restates a value.</p>')


_RUNG_LABEL = {"1-Data": "Data", "2-Information": "Information", "3-Knowledge": "Knowledge", "4-Wisdom": "Wisdom"}


def _prose(body: str, label: str) -> str:
    m = re.search(r"\*\*" + re.escape(label) + r"\*\*:\s*(.+?)(?:\n\s*\n|\Z)", body, re.S)
    return " ".join(m.group(1).split()) if m else ""


def _rung_html(board: Path, root: Path, proto: Path, rung: Path, states: dict, n_parts: int) -> str:
    """One rung of the Prototype: its opening question, then one folding row per live question
    (id, name, the short question, partitions, script, agreed), then the retired ones folded."""
    ci, rq, sy = _tools()
    link = lambda path, label: (f'<a class=pop href="{_e(file_url(board, path, root))}" data-pop="{_e(label)}">'
                                f'{_e(label)}</a>' if path.exists() else f'<span class=mut>{_e(label)}</span>')
    text = (rung / "rung.md").read_text(encoding="utf-8") if (rung / "rung.md").is_file() else ""
    opening = re.search(r"(?m)^## Opening\s*\n+(.+)", text)
    shared = sorted((rung / "src").glob("*.py"))
    out = [f'<h2>{_e(_RUNG_LABEL.get(rung.name, rung.name))}</h2>']
    if opening:
        out.append(f'<p class=pquote>{_e(opening.group(1).strip())}</p>')
    out.append('<p class=mut>' + link(rung / "rung.md", "rung.md") + ': the opening, writing rule and law of this rung'
               + (' · shared code: ' + " · ".join(link(f, f.name) for f in shared) if shared else '') + '</p>')
    live, retired = [], []
    for pq in rq.question_folders(proto):
        if pq.parent != rung:
            continue
        q, body = _front(pq / f"{pq.name}.md")
        (retired if q.get("retired") else live).append((pq, q, body))
    mark = {"in sync": "✅ script in sync", "new in prototype": "⬇️ not copied here",
            "prototype changed": "🔄 update waiting", "instance changed": "✏️ changed here", "both changed": "❗ both changed"}
    for pq, q, body in live:
        asked = (q.get("partitions") or {}).get("asked") or []
        if isinstance(asked, str):                       # `asked: all` names every partition
            asked = [asked]
        where = ("all partitions" if asked == ["all"] or (n_parts and len(asked) >= n_parts - 1 and "cross" not in asked)
                 else " · ".join(asked) or "not asked")
        scripts = sorted((pq / "scripts").glob("*.py"))
        st = states.get(pq.name)
        script = (mark.get(st, st) if st else "⬜ script not written") if scripts else (
            "📝 judged on its page" if rung.name.startswith("4-") else "⬜ script not written")
        agreed = "✅ agreed" if str(q.get("agreed", "")).startswith("✅") else "⬜ not agreed"
        tags = "".join(f'<span class=chip>{_e(t)}</span>' for t in (where, script, agreed))
        parts = [f'<p><b>Ask</b>: {_e(q.get("ask", ""))}</p>']
        for label in ("Why now", "What would answer it"):
            t = _prose(body, label)
            if t:
                parts.append(f'<p><b>{label}</b>: {_e(t)}</p>')
        parts.append('<p class=mut>' + " · ".join([link(pq / f"{pq.name}.md", "question file")]
                                                  + [link(f, f.name) for f in scripts]) + '</p>')
        out.append(f'<details class=pq><summary><span class=pqid>{_e(q.get("id", pq.name[:3]))}</span>'
                   f'<span class=pqname>{_e(q.get("name", pq.name))}</span>'
                   f'<span class=pqq>{_e(q.get("question", ""))}</span><span class=pqtags>{tags}</span></summary>'
                   f'<div class=pqbody>{"".join(parts)}</div></details>')
    if not live:
        out.append('<p class=note>No live question on this rung yet.</p>')
    if retired:
        out.append(f'<details class=pretired><summary>Retired · {len(retired)}</summary><table>'
                   '<tr><th>Question</th><th>Replaced by</th><th>Why</th></tr>' + "".join(
                       f'<tr><td>{link(pq / f"{pq.name}.md", str(q.get("id", "")) + " " + str(q.get("name", "")))}</td>'
                       f'<td class=mono>{_e(", ".join(q.get("superseded_by") or []) or "—")}</td>'
                       f'<td>{_e(str(q.get("retired", "")))}</td></tr>' for pq, q, _ in retired)
                   + '</table></details>')
    return "".join(out)


def prototype_views(board: Path, root: Path) -> list[tuple[str, str, str]]:
    """The Prototype Space (JL 261003: "give the Prototype a SPACE ... Meta, D, I, K, W as the
    views"): Meta, then one View per rung. Returns [(key, label, html)]."""
    ci, rq, sy = _tools()
    board, root = Path(board).resolve(), Path(root).resolve()
    proto = (board / (_front(board / "board.md")[0].get("prototype") or "")).resolve()
    views = [("meta", "Meta", render_prototype(board, root))]
    if not (proto / "board.md").is_file():
        return views
    states = {}
    for iq, _, st, _ in sy.status(board):
        prev = states.get(iq.name)
        states[iq.name] = st if prev in (None, "in sync") else prev     # the worst state of a question's scripts
    n_parts = len(_front(proto / "0-Meta" / "partitions.md")[0].get("partitions") or [])
    for rung in sorted(proto.glob("[1-4]-*")):
        if rung.is_dir():
            label = _RUNG_LABEL.get(rung.name, rung.name)
            views.append((label.lower(), label, _rung_html(board, root, proto, rung, states, n_parts)))
    return views


def _allowed(board: Path) -> list[Path]:
    board = Path(board).resolve()
    out = [board]
    if board_kind(board) == "insight-instance":
        out.append((board / (_front(board / "board.md")[0].get("prototype") or "")).resolve())
    return out


def render_run(board: Path, root: Path, task: str, partition: str) -> str:
    """One partition run as the workbench's run pop-out lays a run out: where it is, its
    links, its receipt, its summaries (the generated report), its tables, its other files."""
    from .paper import _RESULT_PAGE, _csv_view, _md_view
    board, root = Path(board).resolve(), Path(root).resolve()
    qf = (board / task).resolve()
    if not qf.is_relative_to(board) or not (qf / "runs" / f"{partition}.sh").is_file():
        raise FileNotFoundError(f"{task} · {partition}")
    res, rep = qf / "results" / partition, qf / "reports" / partition
    raw = lambda f: "/" + quote(f.resolve().relative_to(root).as_posix(), safe="/")
    links = [f'<a href="{_e(raw(f))}" target=_blank rel=noopener>{label} ↗</a>'
             for f, label in ((qf / "runs" / f"{partition}.sh", "Run script"),
                              *[(s, "Script") for s in sorted((qf / "scripts").glob("*.py"))]) if f.is_file()]
    body = [f'<h1>{_e(partition)}</h1><p class="where mut"><code>{_e(res.relative_to(root).as_posix())}</code>'
            f' · answers {_e(legacy_qid(qf.name[:3]))}</p>', f'<div class=links>{"".join(links)}</div>']
    receipt = res / "runtime.yaml"
    body.append(f'<h2>Receipt</h2><pre>{_e(receipt.read_text()[:4000])}</pre>' if receipt.is_file()
                else '<p class=mut>Not run yet: no receipt.</p>')
    docs = sorted(rep.glob("*.md")) if rep.is_dir() else []
    if docs:
        body.append(f'<h2>Summaries · {len(docs)}</h2>' + "".join(
            f'<div class=doc><h3>{_e(f.name)}</h3>{_md_view(f.read_text(encoding="utf-8"))}</div>' for f in docs))
    files = sorted(f for f in res.rglob("*") if f.is_file()) if res.is_dir() else []
    tabs = [f for f in files if f.suffix.lower() in (".csv", ".tsv")]
    for f in tabs:
        if f is tabs[0]:
            body.append(f'<h2>Tables · {len(tabs)}</h2>')
        body.append(f'<h3>{_e(f.name)}</h3>{_csv_view(f)}')
    rest = [f for f in files if f not in tabs and f != receipt]
    if rest:
        body.append(f'<h2>Other files · {len(rest)}</h2><ul class=files>' + "".join(
            f'<li><a href="{_e(raw(f))}" target=_blank rel=noopener>{_e(f.relative_to(res).as_posix())}</a></li>'
            for f in rest) + '</ul>')
    return _RESULT_PAGE.format(title=_e(partition), body="\n".join(body))


def render_file(board: Path, root: Path, rel: str) -> tuple[int, str]:
    """One file (or folder) of the Instance or its Prototype, as a document in the pop-out."""
    from .paper import _RESULT_PAGE, _csv_view, _md_view
    root, board = Path(root).resolve(), Path(board).resolve()
    try:
        path = (root / rel).resolve()
    except (OSError, RuntimeError):
        return 404, "<p>No such file.</p>"
    if not any(path == a or path.is_relative_to(a) for a in _allowed(board)) or \
            any(p.startswith(".") for p in path.relative_to(root).parts):
        return 404, "<p>This file is not part of the board.</p>"
    if path.is_dir():
        items = "".join(f'<li><a href="{_e(file_url(board, f, root))}">{_e(f.name)}{"/" if f.is_dir() else ""}</a></li>'
                        for f in sorted(path.iterdir()) if not f.name.startswith("."))
        return 200, _RESULT_PAGE.format(title=_e(path.name), body=f"<h1>{_e(path.name)}/</h1><ul class=files>{items}</ul>")
    if not path.is_file() or path.suffix.lower() not in _TEXT:
        return 404, "<p>Only text files open here.</p>"
    text = path.read_text(encoding="utf-8", errors="replace")
    head = f'<h1>{_e(path.name)}</h1><p class="where mut"><code>{_e(path.relative_to(root).as_posix())}</code></p>'
    if path.suffix.lower() in (".csv", ".tsv"):
        body = _csv_view(path)
    elif path.suffix.lower() == ".md":
        m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
        body = (f"<pre>{_e(m.group(1))}</pre>" + _md_view(m.group(2))) if m else _md_view(text)
    else:
        body = f"<pre>{_e(text[:200_000])}</pre>"
    return 200, _RESULT_PAGE.format(title=_e(path.name), body=head + body)
