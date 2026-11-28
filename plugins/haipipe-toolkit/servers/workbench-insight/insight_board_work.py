"""The Work column of an insight Board: which cells a page answers, the Runs and tickets behind a cell, what it
builds on, and the notes a question carries."""

from __future__ import annotations

import re
import traceback
from pathlib import Path
from urllib.parse import quote

from .insight_board_reader import (  # noqa: F401 · this module keeps answering these names
    FULL, CROSS, _QID, _read, _e, _page_link, _parse_cell, _yaml_flat, _parents, _inline)
from .insight_board_parts import _partition_name
from .insight_board_runtime import _tasks_root, _task_calls


# ─── which cells a page answers ─────────────────────────────────────────────

def page_cells(snap: dict, page: dict) -> list[tuple[str, str]]:
    """The register cells this page answers, as (question id, segment)."""
    out = []
    for row in snap["questions"]:
        for pid, cell in row["cells"].items():
            if cell.get("page") == page["id"]:
                out.append((row["id"], pid))
    return out


# ─── the workbench: four Spaces, one dataset (studio/insight-workbench-design.py) ─

# A refused or deferred cell, said in words: the head goes where a run would
# be, the reason under it.  Tokens from MT02/MT03's legends.
_REASONS = {
    "full-only": ("Answered on Full", "a property of the whole extract, the same in every segment"),
    "thin": ("Too few rows", "fewer than 300 rows per message in this segment"),
    "defer": ("Defers to Full", "asking whether to segment from inside a segment is circular"),
    "nomeas": ("No answer", "no field in the extract records it"),
    "nocon": ("No answer", "the experiment never varies it"),
    "noiden": ("No answer", "13 messages cannot separate it"),
}
# Scope, then Question Book, then Insight: the data, what is asked of it and by which code, then the
# answers; input, processing, output (the reader meets the data before the questions asked of it)
_SPACES = (("scope", "Scope"), ("prototype", "Question Book"), ("insight", "Insight"), ("check", "Check"), ("delivery", "Delivery"))
_ANSWERS = re.compile(r"(?m)^answers:\s*(.*)$")
_STAGE = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}


def _part_label(snap: dict, pid: str) -> str:
    """`full` -> `Full`, `youngmale` -> `Young male`, `cross` -> `Cross`."""
    if pid == FULL:
        return "Full"
    if pid == CROSS:
        return "Cross"
    name = _partition_name(snap, pid)
    return name[:1].upper() + name[1:] if name else pid


def _call_config(call: dict) -> Path | None:
    name = call.get("task_run") or call["call"]
    for path in (call["task_path"] / "configs" / f"{name}.yaml",
                 call["task_path"] / "scripts" / "config" / f"{name}.yaml"):
        if path.is_file():
            return path
    return None


def work_runs(snap: dict) -> list[dict]:
    """Every task call this board owns, with the questions it answers.

    A call belongs to this board because its config's `store:` is the board's
    store (one dataset, one workbench).  Its `answers:` line names the register
    questions its run answers; that line joins the Logic side to the Work side.
    Its segment is the MT00 row whose config it is.
    """
    if "work" in snap:
        return snap["work"]
    by_config = {row["config"]: row["id"] for row in snap["partitions"] if row.get("config")}
    # a run `rNN_<dataset>_<segment>` names its segment; the segment is the partition's MT00 name
    by_cut = {row["name"]: row["id"] for row in snap["partitions"]}
    out = []
    for call in _task_calls(snap):
        cfg = _call_config(call)
        hit = _ANSWERS.search(_read(cfg)) if cfg else None
        fields = _yaml_flat(_read(call["receipt"])) if call["ran"] else {}
        name = call.get("task_run") or call["call"]
        cut = "_".join(name.split("_")[2:]) if re.match(r"^r\d{2}_", name) else ""
        out.append({**call, "config": cfg, "partition": by_config.get(name) or by_cut.get(cut, ""),
                    "answers": _QID.findall(hit.group(1).split("#", 1)[0]) if hit else [],
                    "status": fields.get("status", "?") if call["ran"] else "not run"})
    snap["work"] = out
    return out


def page_tickets(snap: dict, page: dict | None) -> list[dict]:
    """The task runs one page rests on, read from its own runs/ tickets."""
    if not page:
        return []
    folder = page["path"].parent.name
    return [r for r in work_runs(snap) if r["source"] == "page-ticket" and r["page"] == folder]


def _run_url(snap: dict, run: dict) -> str:
    if run.get("url"):                      # an Instance run (instance_reader)
        return run["url"]
    task = run["task_path"].resolve().relative_to(_tasks_root(snap).resolve()).as_posix()
    return (f"/_board/insight-run?board={quote(snap['board'].name)}"
            f"&task={quote(task, safe='/')}&call={quote(run['call'])}"
            + (f"&page={quote(run['page'])}" if run.get("page") else ""))


def _pop_url(snap: dict, page: dict) -> str:
    """A page opens as a document in the pop-out; there is no page-level workbench."""
    if page.get("url"):                     # an Instance page or spec (instance_reader)
        return page["url"]
    if snap["static"]:
        return _page_link(snap, page)
    return f"/_board/insight?board={quote(snap['board'].name)}&page={quote(page['id'])}"


def _answered_by(snap: dict) -> dict[str, list[str]]:
    """page id -> the register questions whose cell it settles."""
    out: dict[str, list[str]] = {}
    for q in snap["questions"]:
        for cell in q["cells"].values():
            if cell.get("page") and q["id"] not in out.setdefault(cell["page"], []):
                out[cell["page"]].append(q["id"])
    return out


def _builds_on(snap: dict, page: dict | None, qid: str, answered: dict) -> list[str]:
    """The lower questions this answer rests on: the questions its cited pages answer."""
    if not page:
        return []
    out = []
    for parent in _parents(page["text"]):
        for other in answered.get(parent, []):
            if other != qid and other not in out:
                out.append(other)
    return out


def _behind(snap: dict, page: dict | None, answered: dict) -> list[str]:
    """Every question below an answer, along all its citations (a K or W answer has
    no run of its own yet; the runs behind it are the runs of these questions)."""
    seen, out, frontier = set(), [], [page] if page else []
    while frontier:
        cur = frontier.pop(0)
        if cur["id"] in seen:
            continue
        seen.add(cur["id"])
        for parent in _parents(cur["text"]):
            out.extend(q for q in answered.get(parent, []) if q not in out)
            if parent in snap["by_id"]:
                frontier.append(snap["by_id"][parent])
    return out


def _numbers(qids: list[str]) -> str:
    """[QI7, QI8, QK2] -> `Information questions 7, 8 · Knowledge question 2`."""
    groups: dict[str, list[str]] = {}
    for qid in sorted(set(qids), key=lambda q: ("DIKW".index(q[1]), int(q[2:]))):
        groups.setdefault(qid[1], []).append(qid[2:])
    parts = []
    for lv in "DIKW":
        nums = groups.get(lv)
        if nums:
            parts.append(f'{_STAGE[lv]} question{"s" if len(nums) > 1 else ""} {", ".join(nums)}')
    return " · ".join(parts)


def _task_name(name: str) -> str:
    """`03_funnel_rates` -> `Funnel rates`."""
    words = re.sub(r"^[a-z]?\d+_", "", name).replace("_", " ")
    return words[:1].upper() + words[1:]


def _idname(name: str) -> str:
    """`j21_information_funnel` -> idtag `j21` + `information_funnel`."""
    head, _, tail = name.partition("_")
    return f'<span class=idtag>{_e(head)}</span>' + (f' {_e(tail)}' if tail else "")


def _run_note(run: dict) -> str:
    """`ok`, or `ok · 11 pages` when one task run stands behind several pages."""
    pages = run.get("n_pages", 1)
    return f'{run["status"]} · {pages} pages' if pages > 1 else run["status"]


def _run_lines(snap: dict, runs: list[dict]) -> str:
    """Block → Job → Task → Run, one level per line, each one step in (the Paper's
    B → J → T → R). A two-level legacy task folder has no Job line."""
    out, last_block, last_job = [], None, None
    runs = sorted(runs, key=lambda r: str(r["task_path"]))     # one Block, then one Job, at a time
    for task_path in dict.fromkeys(r["task_path"] for r in runs):
        group = [r for r in runs if r["task_path"] == task_path]
        block, job = group[0]["family"], group[0]["job"]
        if block != last_block:
            out.append(f'<div class=bj-b>{_idname(block)}</div>')
            last_block, last_job = block, None
        if job and job != last_job:
            out.append(f'<div class=bj-j>{_idname(job)}</div>')
            last_job = job
        lines = "".join(
            f'<a class="bj-run pop" href="{_e(_run_url(snap, r))}" data-pop="{_e(r["call"])}">'
            f'<span class=idtag>{_e(r["call"]).replace("_", "_<wbr>")}</span> <span class=mut>{_e(_run_note(r))}</span></a>'
            for r in group)
        out.append(f'<details class="bj-tr{" bj-flat" if not job else ""}"><summary class=bj-t>{_idname(task_path.name)} '
                   f'</summary>'
                   f'<div class=bj-runs>{lines}</div></details>')
    return "".join(out)


def _bindings(page: dict | None, qid: str) -> dict:
    """The page's answers.yaml entry for one question: need id -> binding
    (hai-insight ref/evidence-needs.md § 2).  Empty when the page binds none."""
    if not page:
        return {}
    path = page["path"].parent / "answers.yaml"
    if not path.is_file():
        return {}
    try:
        import yaml
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:  # noqa: BLE001 · an answers.yaml that cannot be read binds nothing; the server log names it
        traceback.print_exc()
        return {}
    entry = data.get(qid) if isinstance(data, dict) else None
    return entry if isinstance(entry, dict) else {}


_STEP_WORD = {"compute": "🧮 Compute", "cite": "📎 Reuse", "judge": "⚖️ Answer"}


def _step_label(n: int, eid: str, kind: str) -> str:
    """A need read as a numbered step, its E id only a tooltip (a row of E ids read as noise)."""
    return f'<b class=step title="{_e(eid)}">{n}. {_e(_STEP_WORD.get(kind, kind))}</b>'


def _needs_list(snap: dict, q: dict, binding: dict) -> str:
    """Each evidence need of the question with what the page binds to it."""
    rows = []
    for n, (eid, kind, text) in enumerate(question_notes(snap).get(q["id"], {}).get("needs") or [], 1):
        b = binding.get(eid)
        if b is None:
            where, cls = "not bound", " class=gap"
        elif b == "judge":
            where, cls = "made on the page", ""
        elif isinstance(b, dict) and "refused" in b:
            where, cls = f'refused · {_e(str(b["refused"]))}', ""
        elif isinstance(b, dict) and ("ticket" in b or "tickets" in b):
            where = " · ".join(_e(f) for f in b.get("files") or []) or "no files"
            cls = ""
        elif isinstance(b, dict) and "pages" in b:
            where, cls = "from page " + _e(", ".join(b["pages"])), ""
        else:
            where, cls = "from the cited question's page", ""
        rows.append(f'<li{cls}>{_step_label(n, eid, kind)} · {_inline(text)}'
                    f'<span class=wk-bind> → {where}</span></li>')
    return f'<ul class=wk-needs>{"".join(rows)}</ul>' if rows else ""


def _instance_binding(snap: dict, q: dict, pid: str) -> dict:
    """An Instance question's needs, bound the way answers.yaml binds them: a compute need to
    this partition's run and its spec files, a cite to the cited need, a judge to the page."""
    spec = question_notes(snap).get(q["id"], {}).get("spec") or {}
    rec = next((r["receipt_data"] for r in work_runs(snap) if r.get("qid") == q.get("qid") and r["partition"] == pid), {})
    out = {}
    for nid, n in (spec.get("needs") or {}).items():
        if n.get("kind") == "compute":
            out[nid] = ({"refused": rec.get("reason", "")} if rec.get("status") == "refused"
                        else {"ticket": pid, "files": list(n.get("output") or {})})
        elif n.get("kind") == "cite":
            out[nid] = {"pages": [str(n.get("from", ""))]}
        elif n.get("kind") == "judge":
            out[nid] = "judge"
    return out


def _work_cell(snap: dict, q: dict, pid: str, answered: dict) -> str:
    """The Work column of one question in one segment.  When the answering page
    binds the question's evidence needs (answers.yaml), each need is listed with
    what answers it, and only the runs those needs are bound to are shown.
    Otherwise: the page's tickets, or for a Knowledge or Wisdom answer with no run
    of its own, the runs behind the pages it cites.  The Report column says what
    the answer is."""
    cell = q["cells"].get(pid, _parse_cell("·"))
    page = snap["by_id"].get(cell.get("page", ""))
    if cell["mark"] == "·" or (cell["mark"] == "🚫" and not page and snap.get("layout") != "instance"):
        return '<p class=wk-none>—</p>'
    if snap.get("layout") == "instance":
        runs = [r for r in work_runs(snap) if r.get("qid") == q.get("qid") and r["partition"] == pid]
        if cell["mark"] == "🚫" and not runs:                # not asked here: no run, as a refused cell reads
            return '<p class=wk-none>—</p>'
        binding = _instance_binding(snap, q, pid)
        return (f'<details class=wk open><summary><span class=kind>Task Work</span></summary>'
                f'{_needs_list(snap, q, binding)}'
                + (f'<div class=bj>{_run_lines(snap, runs)}</div>' if runs else "")
                + '</details>')
    work = work_runs(snap)
    binding = _bindings(page, q["id"])
    if binding:
        bound = {t for b in binding.values() if isinstance(b, dict)
                 for t in ([b["ticket"]] if b.get("ticket") else []) + list(b.get("tickets") or [])}
        runs = [r for r in page_tickets(snap, page) if r["call"] in bound]
        return (f'<details class=wk open><summary><span class=kind>Task Work</span></summary>'
                f'{_needs_list(snap, q, binding)}'
                + (f'<div class=bj>{_run_lines(snap, runs)}</div>' if runs else "")
                + '</details>')
    own = page_tickets(snap, page) or [
        r for r in work if q["id"] in r["answers"] and (pid == CROSS or r["partition"] == pid)]
    lv = q["id"][1]
    if own:
        names = list(dict.fromkeys(_task_name(r["task_path"].name) for r in own))
        return (f'<details class=wk open><summary><span class=kind>Task Work</span></summary>'
                f'<p class=wk-title><b>{_e(" · ".join(names))}</b></p>'
                f'<div class=bj>{_run_lines(snap, own)}</div></details>')
    if page and lv in "KW":
        lower = _behind(snap, page, answered)
        behind, seen = [], {}
        for r in work:
            if set(r["answers"]) & set(lower) and (pid == CROSS or r["partition"] == pid):
                key = (r["task_path"], r.get("task_run") or r["call"])
                if key in seen:
                    seen[key]["n_pages"] += 1
                else:
                    seen[key] = {**r, "n_pages": 1}
                    behind.append(seen[key])
        if behind:
            return (f'<details class=wk open><summary><span class=kind>Task Work</span></summary>'
                    f'<div class=bj>{_run_lines(snap, behind)}</div></details>')
    return '<p class=wk-none>No run names it under <code>answers:</code> yet</p>'


_DIVISION = re.compile(r"(?m)^#{3,4}\s+\d+\s+·\s+(Q[DIKW]\d+)\s+·\s+(.+?)\s*$")
_FIELD = re.compile(r"(?m)^\*\*([^*]{2,60})\*\*:\s*(.+?)\s*$")
# an evidence need under "What would answer it" (hai-insight ref/evidence-needs.md)
_NEED = re.compile(r"(?m)^- (E\d+) · (compute|cite|judge) · (.+?)\s*$")


def question_notes(snap: dict) -> dict[str, dict]:
    """question id -> its register division: short name, the ask, why it matters,
    what would answer it, and an expected answer when the register records one.
    Each MT01-MT04 register writes one `#### N · QI2 · Variant Performance`
    division per question; a question without one keeps only its Queue row."""
    if "notes" in snap:
        return snap["notes"]
    out = {}
    for q in snap["questions"]:
        reg = q["register"]
        if reg["id"] in {n.get("_reg") for n in out.values()}:
            continue
        heads = list(_DIVISION.finditer(reg["text"]))
        for i, m in enumerate(heads):
            body = reg["text"][m.end():heads[i + 1].start() if i + 1 < len(heads) else len(reg["text"])]
            body = re.split(r"(?m)^#{1,3}\s", body)[0]
            fields = {k.strip().lower(): v for k, v in _FIELD.findall(body)}
            out[m.group(1)] = {"_reg": reg["id"], "name": m.group(2),
                               "ask": fields.get("the ask", ""), "why": fields.get("why now", ""),
                               "answer": fields.get("what would answer it", ""),
                               "expect": next((v for k, v in fields.items() if "expect" in k), ""),
                               "needs": [(e, kind, rest.split(" · ")[0]) for e, kind, rest in _NEED.findall(body)
                                         if "retired:" not in rest],
                               "agreed": fields.get("needs agreed", "")}
    snap["notes"] = out
    return out
