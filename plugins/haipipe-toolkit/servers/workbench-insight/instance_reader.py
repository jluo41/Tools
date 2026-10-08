"""Read an Insight Block for the Insight workbench (no UI of its own).

An Insight Block (haipipe-insight ref/block-contract.md) is a task Block: one Job per DIKW level
(j01_data … j04_wisdom), one Task per question (tNN_<name>/: question.md, scripts/, runs/<dataset>_
<partition>.sh, results/, reports/, the page). It is drawn by the SAME Insight workbench as every
InsightBoard: insightboard.render_insight_board, its Spaces, Insight › Questions one table per
partition with Logic · Work · Report, the Runs panels and the pop-outs. This module only READS the
Block and returns the snapshot shape insightboard.py already renders, for one dataset at a time
(board.md `datasets:`, the first unless one is named), so a partition stays the screen's unit:

    questions   one row per question, id `Q<L><N>` (I03 → QI3), its cells computed by
                haipipe-insight-check ref/check_block.py
    pages       the question's page in its task folder, plus the meta page the Dataset view reads
                (meta/meta.md, carried word for word from the board it was made from)
    work        one run per question × partition of the dataset (runs/<dataset>_<partition>.sh)
    notes       each question.md's short question, name, ask, why now, what would answer it,
                any other carried field, and its live needs

It also serves the two pop-outs the workbench opens: a run (its generated report first, its
receipt, its tables) and a file of the Block.
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

from host_paths import skill_dir

_REF = skill_dir("haipipe-insight") / "ref"
_CHECK = skill_dir("haipipe-insight-check") / "ref"
_LEVEL = {"D": "data", "I": "information", "K": "knowledge", "W": "wisdom"}
_STAGE = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}
_TEXT = {".md", ".csv", ".tsv", ".json", ".yaml", ".yml", ".py", ".sh", ".txt", ".lock"}
KINDS = ("insight-block",)


def _tools():
    """The contract's own readers: the Block checker and the runner's helpers."""
    for p in (str(_REF), str(_CHECK)):
        if p not in sys.path:
            sys.path.insert(0, p)
    return importlib.import_module("check_block"), importlib.import_module("run_question")


def _e(v) -> str:
    return html.escape("" if v is None else str(v), quote=True)


def board_kind(board: Path) -> str:
    """`insight-block` (a task Block with `workbench: insight`), or '' (a board made another way)."""
    path = Path(board) / "board.md"
    m = re.match(r"^---\n(.*?)\n---", path.read_text(encoding="utf-8") if path.is_file() else "", re.S)
    try:
        meta = (yaml.safe_load(m.group(1)) or {}) if m else {}
    except yaml.YAMLError:
        return ""
    return "insight-block" if meta.get("board-kind") == "task-block" and meta.get("workbench") == "insight" else ""


def datasets(board: Path) -> list[str]:
    """The Block's dataset names, in board.md order."""
    return list((_front(Path(board) / "board.md")[0].get("datasets") or {}).keys())


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


def run_url(board: Path, qfolder: Path, run: str, root: Path) -> str:
    rel = Path(qfolder).resolve().relative_to(Path(board).resolve()).as_posix()
    return (f"/_board/insight-run?board={quote(Path(board).name)}&task={quote(rel, safe='/')}"
            f"&call={quote(run)}")


def legacy_qid(qid: str) -> str:
    """I03 → QI3: the id shape the Insight workbench reads (its level, then its number)."""
    return f"Q{qid[0]}{int(qid[1:])}"


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
    return {"mark": m, "page": page_id, "note": note, "raw": f"{m} {page_id} {note}".strip()}


def _meta_page(board: Path, root: Path, rq, d01_done: bool, dataset: str) -> dict:
    """The meta page the Dataset view, the banner and gate GI0 read: the Block's carried meta page
    when it has one, else what D01 measured on this dataset's extract. A fact with no source is left
    out, never guessed."""
    carried = board / rq.META / "meta.md"
    if carried.is_file():
        text = carried.read_text(encoding="utf-8")
        return {"path": carried, "rel": f"{rq.META}/meta.md", "id": "MT00", "text": text,
                "title": _title(text, "The extract"), "state": "✅ measured by D01" if d01_done else "OPEN",
                "page_type": "meta", "identity_error": "", "register_level": "", "level": "", "partition": "",
                "receipt_field": "", "url": file_url(board, carried, root)}
    extract = (_front(board / "board.md")[0].get("datasets") or {}).get(dataset, "")
    lines = ["# The extract", "", f"{Path(extract).parent.as_posix()}/"]
    d01 = rq.task_folder(board, "D01")
    out = d01 / "results" / f"{dataset}_full" if d01 else None
    shape = json.loads((out / "extract_shape.json").read_text()) if out and (out / "extract_shape.json").is_file() else {}
    lines.append(f"{Path(extract).name}" + (f"   {shape['n_rows']:,} × {shape['n_columns']}" if shape else ""))
    return {"path": board / "board.md", "rel": "board.md", "id": "MT00", "text": "\n".join(lines) + "\n",
            "title": "The extract", "state": "✅ measured by D01" if d01_done else "OPEN", "page_type": "meta",
            "identity_error": "", "register_level": "", "level": "", "partition": "", "receipt_field": "",
            "url": file_url(board, board / "board.md", root)}


def legacy_snapshot(board: Path, root: Path, dataset: str = "") -> dict:
    """The snapshot insightboard.render_insight_board draws, read from an Insight Block for one dataset."""
    ci, rq = _tools()
    board, root = Path(board).resolve(), Path(root).resolve()
    names = datasets(board)
    ds = dataset if dataset in names else (names[0] if names else "")
    parts = _front(board / rq.META / "partitions.md")[0].get("partitions") or []
    problems, grid, check_notes = ci.run(board)
    strip = lambda run: run[len(ds) + 1:] if run.startswith(f"{ds}_") else None   # this dataset's runs, by partition
    grid = {qid: {strip(r): m for r, m in row.items() if strip(r)} for qid, row in grid.items()}
    pages, questions, work, notes, report_rows, rows_of, registers = [], [], [], {}, [], {}, {}
    for task in rq.question_folders(board):
        q, prose = _front(task / rq.QFILE)
        if not q or q.get("retired"):                   # a retired question is history: not on the board
            continue
        qid = rq.question_id(task)
        lid, letter = legacy_qid(qid), qid[0]
        job = task.parent
        lfile = level_file(job)
        reg = registers.setdefault(letter, {
            "path": lfile, "rel": job.name, "id": job.name,
            "text": lfile.read_text(encoding="utf-8") if lfile.is_file() else "",
            "title": f"{_STAGE[letter]} questions", "state": "OPEN", "page_type": "question",
            "identity_error": "", "register_level": _LEVEL[letter], "level": "", "partition": "", "receipt_field": "",
            "url": file_url(board, job, root)})
        page_md, page_id = task / f"{task.name}.md", ""
        if page_md.is_file():
            text = page_md.read_text(encoding="utf-8")
            marks = [m for m in grid.get(qid, {}).values() if m != "—"]
            page_id = qid
            pages.append({"path": page_md, "rel": page_md.relative_to(board).as_posix(), "id": qid, "text": text,
                          "title": _title(text, task.name),
                          "state": "✅ CHECK closed" if marks and all(m.startswith("✅") for m in marks) else "🟡 owed",
                          "page_type": _LEVEL[letter], "identity_error": "", "register_level": "", "level": _LEVEL[letter],
                          "partition": "", "receipt_field": "", "url": file_url(board, page_md, root)})
        cells = {p: _cell(m, page_id) for p, m in grid.get(qid, {}).items() if m != "—"}
        carried = (q.get("source") or {}).get("cells") or {}
        for p, m in grid.get(qid, {}).items():          # not asked here: the old board's refusal, as it read
            if m == "—" and str(carried.get(p, "")).startswith("🚫 "):
                reason = carried[p][2:].strip()
                cells[p] = {"mark": "🚫", "page": "", "note": reason, "raw": f"🚫 {reason}"}
        questions.append({"id": lid, "question": q.get("question") or q.get("ask", ""), "register": reg,
                          "cells": cells, "folder": task.name, "qid": qid})
        extra = {k: v for k, v in re.findall(r"(?m)^\*\*([^*]{2,60})\*\*:\s*(.+?)\s*$", prose)
                 if k not in ("Why", "Why now", "What would answer it")}
        notes[lid] = {"_reg": reg["id"], "name": q.get("name") or _title(prose, task.name), "ask": q.get("ask", ""),
                      "why": _field(prose, "Why now") or _field(prose, "Why"),
                      "answer": _field(prose, "What would answer it"),
                      "expect": next((v for k, v in extra.items() if "expect" in k.lower()), ""),
                      "needs": [(nid, n.get("kind", ""), n.get("what", "")) for nid, n in (q.get("needs") or {}).items()
                                if not n.get("retired")],
                      "agreed": str(q.get("agreed", "")), "spec": q}
        if not any(n.get("kind") == "compute" for n in rq.live_needs(q).values()):
            continue                                    # answered on its page alone: no run
        for part in rq.asked_partitions(q, parts):
            run = f"{ds}_{part}"
            rec_path = task / "results" / run / "runtime.yaml"
            rec = (yaml.safe_load(rec_path.read_text()) if rec_path.is_file() else {}) or {}
            status = rec.get("status", "not run")
            if rec.get("rows_after"):
                rows_of.setdefault(part, rec["rows_after"])
            url = run_url(board, task, run, root)
            work.append({"task_path": task, "family": job.name, "job": job.name, "task": task.name, "call": run,
                         "status": status, "page": task.name, "source": "page-ticket", "answers": [lid],
                         "partition": part, "run": run, "ticket": task / "runs" / f"{run}.sh", "receipt": rec_path,
                         "config": None, "ran": rec_path.is_file(), "task_run": run, "qid": qid, "url": url,
                         "receipt_data": rec})
            if (task / "reports" / run / "report.md").is_file():
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
    pages.insert(0, _meta_page(board, root, rq, d01_done, ds))
    by_id = {p["id"]: p for p in pages}
    for reg in registers.values():
        by_id.setdefault(reg["id"], reg)
    return {
        "layout": "instance", "current": True, "board": board, "root": root, "board_arg": board.name,
        "static": False, "relative": board.relative_to(root).as_posix(), "dataset": ds, "datasets": names,
        "title": board.name, "store": "", "store_path": None, "board_topic": "", "context": "",
        "pages": pages, "by_id": by_id, "partitions": partitions, "questions": questions,
        "question_ids": [q["id"] for q in questions],
        "registers": {lvl: [] for lvl in ("data", "information", "knowledge", "wisdom")},
        "runs": [], "events": [], "workflow_runtimes": [], "handoffs": [],
        "settled": sum(p["state"].startswith("✅") for p in pages),
        "work": work, "notes": notes, "report_rows": report_rows,
        "instance_problems": problems, "instance_notes": check_notes, "prototype": board,
    }


def render_prototype(board: Path, root: Path) -> str:
    """Prototype › Meta: the Block's design, the questions and their code, laid out for the reader:
    four numbers, one table by level of questions, needs and scripts, the partitions, the shared
    settings, the design files. Read-only: a question changes only by a signed change."""
    ci, rq = _tools()
    board, root = Path(board).resolve(), Path(root).resolve()
    link = lambda path, label: (f'<a class=pop href="{_e(file_url(board, path, root))}" data-pop="{_e(label)}">'
                                f'{_e(label)}</a>' if path.exists() else f'<span class=mut>{_e(label)} · missing</span>')
    title = _title(_front(board / "board.md")[1], board.name)
    levels = {}
    for task in rq.question_folders(board):
        q = _front(task / rq.QFILE)[0]
        r = levels.setdefault(task.parent.name, {"live": 0, "retired": 0, "scripts": 0, "needs": 0})
        if q.get("retired"):
            r["retired"] += 1
            continue
        r["live"] += 1
        r["scripts"] += bool(list((task / "scripts").glob("*.py")))
        r["needs"] += sum(1 for n in (q.get("needs") or {}).values() if not (n or {}).get("retired"))
    total = lambda k: sum(r[k] for r in levels.values())
    tile = lambda n, label: f'<div class=ptile><b>{n}</b><span>{_e(label)}</span></div>'
    head = (f'<h2>Meta</h2><div class=pcard><div class=ptitle>{link(board / "board.md", board.name)}</div>'
            f'<div class=psub>{_e(title)}</div>'
            '<p class=lead>One task Block: one Job per level, one Task per question, holding its question, its one '
            'script, one run per dataset and partition, and its page.</p>'
            '<div class=ptiles>' + tile(total("live"), "live questions") + tile(total("needs"), "live needs")
            + tile(total("scripts"), "with a script") + tile(len(datasets(board)), "datasets") + '</div></div>')
    table = ('<h3>By level</h3><table><tr><th>Job</th><th class=num>Questions</th><th class=num>Needs</th>'
             '<th class=num>Scripts</th><th class=num>Retired</th></tr>'
             + "".join(f'<tr><td>{link(level_file(board / name), name)}</td><td class=num>{r["live"]}</td>'
                       f'<td class=num>{r["needs"]}</td><td class=num>{r["scripts"] or "—"}</td>'
                       f'<td class=num>{r["retired"] or "—"}</td></tr>' for name, r in sorted(levels.items()))
             + '</table><p class=mut>A question changes only by a signed change: the old one is retired, never edited.</p>')
    shared = sorted(board.glob("src/*.py")) + sorted(board.glob("j0[1-4]_*/src/*.py"))
    files = ('<h3>Design files</h3><table>'
             '<tr><th>Partitions and data</th><td>' + " · ".join(link(board / rq.META / n, n) for n in
                                                    ("meta.md", "partitions.md", "thresholds.yaml")) + '</td></tr>'
             '<tr><th>Level rules</th><td>' + " · ".join(link(f, f.parent.name) for f in sorted(level_file(j) for j in board.glob("j0[1-4]_*") if level_file(j).is_file()))
             + '</td></tr>'
             + (f'<tr><th>Shared code</th><td><details><summary>{len(shared)} modules two or more questions use</summary>'
                + "<br>".join(link(f, f.relative_to(board).as_posix()) for f in shared) + '</details></td></tr>' if shared else '')
             + '</table>')
    return head + table + _partitions_html(board) + _settings_html(board) + files


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
    """meta/partitions.md as a table: each partition and who it holds, in words."""
    rows = (_front(proto / "meta" / "partitions.md")[0].get("partitions") or [])
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
    """meta/thresholds.yaml as a table: one row per section, its values side by side."""
    path = proto / "meta" / "thresholds.yaml"
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return ''
    flat = lambda v: (", ".join(f"{k} {flat(x)}" for k, x in v.items()) if isinstance(v, dict)
                      else "not set" if v is None else str(v))
    body = "".join(f'<tr><td class=mono>{_e(k)}</td><td>{_e(flat(v))}</td></tr>' for k, v in data.items())
    return ('<h3>Shared settings</h3><table><tr><th>Section</th><th>Values</th></tr>' + body + '</table>'
            '<p class=mut>A question names a section here and never restates a value.</p>')


def level_file(job: Path) -> Path:
    """A DIKW level Job's opening note: level.md."""
    return job / "level.md"


_LEVEL_LABEL = {"j01_data": "Data", "j02_information": "Information", "j03_knowledge": "Knowledge", "j04_wisdom": "Wisdom"}


def _prose(body: str, label: str) -> str:
    m = re.search(r"\*\*" + re.escape(label) + r"\*\*:\s*(.+?)(?:\n\s*\n|\Z)", body, re.S)
    return " ".join(m.group(1).split()) if m else ""


def _level_html(board: Path, root: Path, level_job: Path, n_parts: int) -> str:
    """One level's Job: its opening question, then one folding row per live question (id, name, the
    short question, partitions, script, agreed), then the retired ones folded."""
    ci, rq = _tools()
    link = lambda path, label: (f'<a class=pop href="{_e(file_url(board, path, root))}" data-pop="{_e(label)}">'
                                f'{_e(label)}</a>' if path.exists() else f'<span class=mut>{_e(label)}</span>')
    lfile = level_file(level_job)
    text = lfile.read_text(encoding="utf-8") if lfile.is_file() else ""
    opening = re.search(r"(?m)^## Opening\s*\n+(.+)", text)
    shared = sorted((level_job / "src").glob("*.py"))
    out = [f'<h2>{_e(_LEVEL_LABEL.get(level_job.name, level_job.name))}</h2>']
    if opening:
        out.append(f'<p class=pquote>{_e(opening.group(1).strip())}</p>')
    out.append('<p class=mut>' + link(lfile, lfile.name) + ': the opening, writing rule and law of this level'
               + (' · shared code: ' + " · ".join(link(f, f.name) for f in shared) if shared else '') + '</p>')
    live, retired = [], []
    for task in rq.question_folders(board):
        if task.parent != level_job:
            continue
        q, body = _front(task / rq.QFILE)
        (retired if q.get("retired") else live).append((task, q, body))
    for task, q, body in live:
        asked = (q.get("partitions") or {}).get("asked") or []
        if isinstance(asked, str):                       # `asked: all` names every partition
            asked = [asked]
        where = ("all partitions" if asked == ["all"] or (n_parts and len(asked) >= n_parts - 1 and "cross" not in asked)
                 else " · ".join(asked) or "not asked")
        scripts = sorted((task / "scripts").glob("*.py"))
        script = "✅ script" if scripts else (
            "📝 judged on its page" if level_job.name == "j04_wisdom" else "⬜ script not written")
        agreed = "✅ agreed" if str(q.get("agreed", "")).startswith("✅") else "⬜ not agreed"
        tags = "".join(f'<span class=chip>{_e(t)}</span>' for t in (where, script, agreed))
        parts = [f'<p><b>Ask</b>: {_e(q.get("ask", ""))}</p>']
        for label in ("Why now", "What would answer it"):
            t = _prose(body, label)
            if t:
                parts.append(f'<p><b>{label}</b>: {_e(t)}</p>')
        parts.append('<p class=mut>' + " · ".join([link(task / rq.QFILE, "question file")]
                                                  + [link(f, f.name) for f in scripts]) + '</p>')
        out.append(f'<details class=pq><summary><span class=pqid>{_e(q.get("id", ""))}</span>'
                   f'<span class=pqname>{_e(q.get("name", task.name))}</span>'
                   f'<span class=pqq>{_e(q.get("question", ""))}</span><span class=pqtags>{tags}</span></summary>'
                   f'<div class=pqbody>{"".join(parts)}</div></details>')
    if not live:
        out.append('<p class=note>No live question at this level yet.</p>')
    if retired:
        out.append(f'<details class=pretired><summary>Retired · {len(retired)}</summary><table>'
                   '<tr><th>Question</th><th>Replaced by</th><th>Why</th></tr>' + "".join(
                       f'<tr><td>{link(task / rq.QFILE, str(q.get("id", "")) + " " + str(q.get("name", "")))}</td>'
                       f'<td class=mono>{_e(", ".join(q.get("superseded_by") or []) or "—")}</td>'
                       f'<td>{_e(str(q.get("retired", "")))}</td></tr>' for task, q, _ in retired)
                   + '</table></details>')
    return "".join(out)


def prototype_views(board: Path, root: Path) -> list[tuple[str, str, str]]:
    """The Prototype Space (JL 261003): Meta, then one View per level's Job. Returns [(key, label, html)]."""
    board, root = Path(board).resolve(), Path(root).resolve()
    views = [("meta", "Meta", render_prototype(board, root))]
    n_parts = len(_front(board / "meta" / "partitions.md")[0].get("partitions") or [])
    for level_job in sorted(board.glob("j0[1-4]_*")):
        if level_job.is_dir():
            label = _LEVEL_LABEL.get(level_job.name, level_job.name)
            views.append((label.lower(), label, _level_html(board, root, level_job, n_parts)))
    return views


def _allowed(board: Path) -> list[Path]:
    return [Path(board).resolve()]


def render_run(board: Path, root: Path, task: str, partition: str) -> str:
    """One run (`partition` is the run stem, <dataset>_<partition>) as the workbench's run pop-out
    lays a run out: where it is, its links, its generated report first, its receipt, its tables."""
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
            f' · answers {_e(legacy_qid(_tools()[1].question_id(qf)))}</p>', f'<div class=links>{"".join(links)}</div>']
    receipt = res / "runtime.yaml"
    docs = sorted(rep.glob("*.md")) if rep.is_dir() else []
    if docs:                                    # the run's report first: the point, its figures, its tables
        body.append(f'<h2>Report</h2>' + "".join(
            f'<div class=doc>{_md_view(f.read_text(encoding="utf-8"), base=raw(f).rsplit("/", 1)[0] + "/")}</div>'
            for f in docs))
    body.append(f'<details><summary><b>Receipt</b></summary><pre>{_e(receipt.read_text()[:4000])}</pre></details>'
                if receipt.is_file() else '<p class=mut>Not run yet: no receipt.</p>')
    files = sorted(f for f in res.rglob("*") if f.is_file()
                   and not (docs and f.parent == res and f.name.startswith("fig_"))) if res.is_dir() else []
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
    """One file (or folder) of the Block, as a document in the pop-out."""
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
    if path.suffix.lower() == ".md" and path.stem == path.parent.name and re.search(r"(?m)^## Opening\b", text):
        # a question's answering Page: the shared Page reader, the web delivery's own document
        from .page_reader import page_document
        raw = "/" + quote(path.relative_to(root).as_posix(), safe="/")
        return 200, page_document(path, root, f'<a href="{_e(raw)}" target=_blank rel=noopener>Source ↗</a>')
    head = f'<h1>{_e(path.name)}</h1><p class="where mut"><code>{_e(path.relative_to(root).as_posix())}</code></p>'
    if path.suffix.lower() in (".csv", ".tsv"):
        body = _csv_view(path)
    elif path.suffix.lower() == ".md":
        m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
        body = (f"<pre>{_e(m.group(1))}</pre>" + _md_view(m.group(2))) if m else _md_view(text)
    else:
        body = f"<pre>{_e(text[:200_000])}</pre>"
    return 200, _RESULT_PAGE.format(title=_e(path.name), body=head + body)
