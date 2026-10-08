"""The insight theme on the base frame (servers/workbench/frame.py): only what differs from vanilla.

Two layouts (b11, 261007). Plan C (a Board whose board.md names its `prototype:`, or whose Jobs pair a
release and a data version, j0N_pN_<d>vM/): every level is drawn by insight_views.py from the folders
(insight_plan_c.py): the Board (s11), a Job (s12), a Task (s13). Today's layout (a register board in
insights/, or an Insight Block in tasks/ claimed by `workbench: insight`): the Block tab below, from the
old page's data, with b11's Map, the Reading row (Coverage · Tracks · Consistency · Findings) and Check's
gates as chips on each question row; its Jobs and Tasks stay the base's own.

The notes below describe today's layout.

An insight Board reads one dataset (Tools/designs/b11_theme_insight). b11 proposes (s11, 261007) a Job
per pair, Prototype version × data version; no Board has those Jobs on disk yet, so this theme fills
the Block tab from today's folders, with the old page's content (JL: carry over what exists) drawn in
the base's look only (JL 261007: no theme stylesheet): the frame's .topic folds, .wf-table, .q-row,
.chip, .st-ok / .st-warn, and the bj- work rows. b03 (s02-workbench-shared) placed the old Spaces:

    Description      Prototype · Dataset · Partitions      (was Scope › Dataset · Partitions, and Prototype)
    Idea Studio      vanilla: studio/ topics; the generated question map is a row (studio/)
    Audience Report  one view per partition, the old Insight Space: D · I · K · W sections, each
                     question a Question │ Work │ Report row (was Insight › <partition>)
    Work Details     the answering pages, one fold per folder (a partition, or a DIKW level)
    Runs             the task calls that answer the questions, with their status
    Delivery         Handoff: the person-signed Wisdom answers (was Delivery › Handoff)

Two snapshots, as the old page reads them: a register board in insights/ (insightboard.board_snapshot)
and an Insight Block (`workbench: insight`, instance_reader.legacy_snapshot). Check's gates have no
Space yet (b03 s02: proposed as chips on each row); the old page (/_board/insight-board) keeps them,
linked from the band. Read-only: nothing here writes; a run type only copies its prompt.
"""
from __future__ import annotations

from pathlib import Path

from live import insight_plan_c as PC
from live import insight_views as V
from live import insightboard as IB
from live.frame import Space, Theme, chain, esc, href, pop, table

LEVELS = (("D", "Data"), ("I", "Information"), ("K", "Knowledge"), ("W", "Wisdom"))
MARK = {"✅": "st-ok", "🟡": "st-warn"}


def _snap(block: Path, root: Path) -> dict:
    """The old page's snapshot of this Board: an Insight Block's, or a register board's."""
    from live.instance_reader import board_kind, legacy_snapshot
    if board_kind(block):
        return legacy_snapshot(block, root)
    return IB.board_snapshot(block, root, block.name)


def _kinds(snap: dict, *keys: str) -> tuple:
    """The old page's run cards of these Spaces, as Runs-panel kinds (label, prompt, skills)."""
    cards = IB._space_kinds(snap)
    return tuple({"label": k["label"], "prompt": k["prompt"],
                  "skills": [s.strip() for s in str(k.get("skill", "")).split("·") if s.strip()]}
                 for key in keys for k in cards.get(key, []))


def _mark(mark: str, text: str = "") -> str:
    cls = MARK.get(mark, "mut")
    return f'<span class={cls}>{esc(mark)}{(" " + esc(text)) if text else ""}</span>'


def _fold(title: str, meta: str, body: str, opened: bool = False) -> str:
    return (f'<details class=topic{" open" if opened else ""}><summary><b>{esc(title)}</b>'
            f'<span class=topic-meta>{esc(meta)}</span></summary>'
            f'<div style="padding:8px 14px">{body}</div></details>')


def _parts(snap: dict) -> list[dict]:
    """The partitions some question is asked on, in MT00's order."""
    return [p for p in snap["partitions"] if any(p["id"] in q["cells"] for q in snap["questions"])]


# ── Description ────────────────────────────────────────────────────────────────────────────────
def _prototype(snap: dict) -> str:
    """The questions, by level: what is asked and on which cuts (the Prototype's release, or the
    register board's MT01-MT04)."""
    notes, parts = IB.question_notes(snap), _parts(snap)
    out = []
    for lv, name in LEVELS:
        qs = [q for q in snap["questions"] if q["id"][1] == lv]
        if not qs:
            continue
        rows = [(f'<b>{esc(q["id"][2:])}</b>', esc(notes.get(q["id"], {}).get("name", "")), esc(q["question"]),
                 " ".join(_mark(q["cells"][p["id"]]["mark"], IB._part_label(snap, p["id"]))
                          for p in parts if p["id"] in q["cells"]))
                for q in qs]
        out.append(_fold(f"{name} questions", str(len(qs)), table(("#", "name", "the ask", "asked on"), rows),
                         opened=not out))
    return "".join(out) or '<p class=mut>No question registered on this Board yet.</p>'


def _dataset(snap: dict) -> str:
    return table(("fact", "value"), [(esc(k), v) for k, v in IB._input_facts(snap)])


def _partitions(snap: dict) -> str:
    rows = [(f'<b>{esc(IB._part_label(snap, r["id"]))}</b>',
             f'<code>{esc(r["where"] or ("no rows of its own" if r["id"] == IB.CROSS else "—"))}</code>',
             esc(r["rows"] or "—"), esc(r["share"] or "—"),
             esc((r.get("config") or "—") + (".yaml" if r.get("config") else ""))) for r in snap["partitions"]]
    return ('<p class=mut>Cuts of this one extract. A cut is one config per task, never a second dataset.</p>'
            + table(("partition", "where", "rows", "share", "config"), rows))


def _map(snap: dict) -> str:
    """b11 s11's Map on today's layout: one implicit release (today's questions) × its datasets; a Job
    per pair comes with plan C, so each cell is today's runs on that dataset."""
    datasets = list(snap.get("datasets") or []) or ["the extract"]
    runs = IB.work_runs(snap)
    cells = [f'<span class=st-ok>{len(runs)} run{"" if len(runs) == 1 else "s"} today</span>' for _ in datasets]
    return ('<p class=mut>The two clocks crossed: Prototype releases as rows, data versions as columns. This Board '
            'is today\'s layout: one set of questions, not yet versioned, so one row; a Job per pair comes with '
            'plan C (b11 s00).</p>' + table(["release \\ data"] + datasets, [["<b>today</b>"] + cells]))


DESCRIPTION = (("Map", _map), ("Prototype", _prototype), ("Dataset", _dataset), ("Partitions", _partitions))
READINGS = ("Coverage", "Tracks", "Consistency", "Findings")


# ── Audience Report: a view per partition, Question │ Work │ Report ─────────────────────────────
def _cell_runs(snap: dict, q: dict, pid: str, answered: dict) -> list[dict] | None:
    """The task runs behind one question on one partition, as the old Work column finds them;
    None when the question is not asked there."""
    cell = q["cells"].get(pid, IB._parse_cell("·"))
    page = snap["by_id"].get(cell.get("page", ""))
    if cell["mark"] == "·":
        return None
    work = IB.work_runs(snap)
    if snap.get("layout") == "instance":
        return [r for r in work if r.get("qid") == q.get("qid") and r["partition"] == pid]
    binding = IB._bindings(page, q["id"])
    if binding:
        bound = {t for b in binding.values() if isinstance(b, dict)
                 for t in ([b["ticket"]] if b.get("ticket") else []) + list(b.get("tickets") or [])}
        return [r for r in IB.page_tickets(snap, page) if r["call"] in bound]
    own = IB.page_tickets(snap, page) or [
        r for r in work if q["id"] in r["answers"] and (pid == IB.CROSS or r["partition"] == pid)]
    if own or not page or q["id"][1] not in "KW":
        return own
    lower = IB._behind(snap, page, answered)               # a K or W answer rests on the runs of what it cites
    return [r for r in work if set(r["answers"]) & set(lower) and (pid == IB.CROSS or r["partition"] == pid)]


def _report(snap: dict, q: dict, pid: str) -> str:
    cell = q["cells"].get(pid, IB._parse_cell("·"))
    if cell["mark"] == "·":
        return '<p class=mut>Not asked on this cut</p>'
    page = snap["by_id"].get(cell.get("page", ""))
    if cell["mark"] == "🚫" and not page:
        head, why = IB._REASONS.get(cell["note"], ("No answer", cell["note"]))
        return f'<p class=rp-text><b>{esc(head)}</b> · {esc(why)}</p>'
    rep = IB.report(snap, q["id"], pid)
    if rep is None:
        return '<p class=mut>No report yet</p>'
    word = ("Defers to Full" if "defers" in cell["note"] else "Partly answered" if cell["mark"] == "🟡"
            else "No answer" if cell["mark"] == "🚫" else "")
    tags = " · ".join(x for x in (rep["strength"], rep["limit"], word) if x)
    return (f'<p class=rp-title>{pop(rep["url"], rep["headline"], rep["headline"])}</p>'
            + (f'<p class=rp-text>{IB._inline(rep["text"])}</p>' if rep["text"] else "")
            + (f'<p class=rp-tags>{esc(tags)}</p>' if tags else ""))


def _gate_chips(snap: dict, qid: str, pid: str, cell: dict) -> str:
    """Check's gates as chips on the question's row (b03 s02, b11 Q03): each gate this question needs,
    its state; the skipped ones (below its DIKW level) are left out."""
    if cell.get("mark", "·") == "·":
        return ""
    try:
        gates = IB._cell_view(snap, qid, pid)["gates"]
    except Exception:
        return ""
    cls = {"passed": "st-ok", "held": "st-warn", "refused": "st-warn"}
    chips = " ".join(f'<span class="chip {cls.get(g["state"], "mut")}" title="{esc(g["name"])} · {esc(g["note"])}">'
                     f'{esc(IB._gate_label(g["key"]))} {esc(g["state"])}</span>'
                     for g in gates if g["state"] != "skipped")
    return f'<p class=gate-chips>{chips}</p>' if chips else ""


def _coverage(snap: dict, pid: str) -> str:
    """Coverage on today's layout: what was asked and answered on this cut, by DIKW level."""
    out = []
    for lv, name in LEVELS:
        qs = [q for q in snap["questions"] if q["id"][1] == lv]
        if not qs:
            continue
        rows = [(f'<b>{esc(q["id"][2:])}</b>', esc(q["question"]),
                 _mark(q["cells"].get(pid, IB._parse_cell("·"))["mark"])) for q in qs]
        out.append(_fold(f"{name} questions", str(len(qs)), table(("#", "question", "on this cut"), rows), opened=True))
    return "".join(out) or '<p class=mut>No question registered on this Board yet.</p>'


def _one_job(snap: dict, pid: str) -> str:
    return ('<p class=mut>This Board is today\'s layout: its answers are one implicit Job (one set of questions on '
            'one extract), so there is nothing to track or compare yet; tracks and consistency come with plan C\'s '
            'Jobs (b11 s00, s11).</p>')


def _audience(snap: dict, pid: str) -> str:
    notes, answered = IB.question_notes(snap), IB._answered_by(snap)
    row = next((p for p in snap["partitions"] if p["id"] == pid), {})
    size = f'{row["rows"]} rows' if row.get("rows") else ("compares the cuts" if pid == IB.CROSS else "")
    head = ('<div class="q-row q-head-row"><div>Question · the logic</div><div>Work · the runs</div>'
            '<div>Report · what it says</div></div>')
    out = [f'<p class=mut>{esc(IB._part_label(snap, pid))}{(" · " + esc(size)) if size else ""}</p>']
    for lv, name in LEVELS:
        qs = [q for q in snap["questions"] if q["id"][1] == lv
              and (pid != IB.CROSS or q["cells"].get(IB.CROSS, {}).get("mark", "·") != "·")]
        if not qs:
            continue
        rows = []
        for q in qs:
            cell = q["cells"].get(pid, IB._parse_cell("·"))
            note = notes.get(q["id"], {})
            runs = _cell_runs(snap, q, pid, answered)
            work = ('<span class=mut>—</span>' if runs is None else
                    IB._run_lines(snap, runs) if runs else '<span class=mut>No run names it under answers: yet</span>')
            logic = (f'<p class=q-head><span class=kind>{esc(name)} question {esc(q["id"][2:])}</span> '
                     f'{_mark(cell["mark"]) if cell["mark"] != "·" else ""}</p>'
                     + (f'<p><b>{esc(note["name"])}</b></p>' if note.get("name") else "")
                     + f'<p class=mut>{esc(q["question"])}</p>' + _gate_chips(snap, q["id"], pid, cell))
            rows.append(f'<div class=q-row id="question-{esc(q["id"])}"><div class=q-l>{logic}</div>'
                        f'<div class=q-w>{work}</div><div class=q-r>{_report(snap, q, pid)}</div></div>')
        out.append(_fold(f"{name} questions", str(len(qs)), head + "".join(rows), opened=True))
    return "".join(out) if len(out) > 1 else out[0] + '<p class=mut>No question is asked on this cut.</p>'


# ── Work Details, Runs, Delivery ─────────────────────────────────────────────────────────────────
def _pages(snap: dict, block: Path) -> str:
    """The answering pages, one fold per folder under the Board (a partition, or a DIKW level)."""
    groups: dict[str, list[dict]] = {}
    for p in snap["pages"]:
        path = Path(p["path"])
        try:
            top = path.resolve().relative_to(block.resolve()).parts[0]
        except (ValueError, IndexError):
            top = ""
        groups.setdefault(top if top != path.name else "", []).append(p)
    out = []
    for top, pages in sorted(groups.items()):
        rows = [(pop(IB._pop_url(snap, p), p["title"], p["id"] + " ↗"), esc(p["title"]),
                 _mark(p["state"][:1], p["state"][1:].strip()) if p["state"] else '<span class=mut>—</span>')
                for p in sorted(pages, key=lambda p: p["id"])]
        out.append(_fold(top or "the Board's own", f"{len(pages)} pages", table(("page", "title", "state"), rows),
                         opened=not out))
    return "".join(out) or '<p class=mut>No answering page yet.</p>'


def _runs(snap: dict) -> str:
    rows = [(esc(IB._task_name(Path(r["task_path"]).name)), pop(IB._run_url(snap, r), r["call"], r["call"] + " ↗"),
             esc(IB._part_label(snap, r["partition"]) if r["partition"] else "—"), esc(" · ".join(r["answers"]) or "—"),
             f'<span class={"st-ok" if r["status"] in ("ok", "complete", "completed", "done") else "mut"}>{esc(r["status"])}</span>')
            for r in IB.work_runs(snap)]
    return ('<p class=mut>The task calls that answer this Board\'s questions; a call names them under answers:.</p>'
            + table(("task", "run", "partition", "answers", "status"), rows))


def _delivery(snap: dict) -> str:
    rows = [(pop(IB._pop_url(snap, h["record"]), h["title"], h["title"]), f'<code>{esc(h["serves"])}</code>',
             f'<span class={"st-ok" if h["bindable"] else "st-warn"}>{esc(h["eligibility"])}</span> · '
             f'{esc(h["eligibility_reason"])}') for h in snap["handoffs"]]
    ready = sum(h["bindable"] for h in snap["handoffs"])
    return (f'<p class=mut>{ready} signed Wisdom answer{"" if ready == 1 else "s"} ready for design. Only a signed, '
            'current handoff leaves this Board.</p>'
            + (table(("Wisdom answer", "serves", "current eligibility"), rows) if rows else
               '<p class=mut>No Wisdom answer is ready to leave this Board yet.</p>'))


def spaces(level, folder, root, sub):
    folder, root = Path(folder).resolve(), Path(root).resolve()
    block = chain(folder, root).get("Block")
    if block is not None and PC.is_plan_c(block):     # b11's plan C: Board · Job · Task from the folders
        def link(space, s, target=None):
            return href(Path(target) if target else folder, root, THEME, space, s)
        view = {"Block": V.board_spaces, "Job": V.job_spaces, "Task": V.task_spaces}.get(level)
        return view(folder, root, sub, link) if view else {}
    if level != "Block" or not (folder / "board.md").is_file():
        return {}                                   # today's layout: a Job or Task is the base's own
    snap = _snap(folder, root)
    desc = {name: fn for name, fn in DESCRIPTION}
    d_open = sub if sub in desc else DESCRIPTION[0][0]
    labels = {IB._part_label(snap, p["id"]): p["id"] for p in _parts(snap)}
    full = next((lab for lab, pid in labels.items() if pid == IB.FULL), next(iter(labels), ""))
    a_part, _, a_read = (sub or "").partition("/")
    a_open = a_part if a_part in labels else full
    a_read = a_read if a_read in READINGS else "Findings"   # today's rows are this Board's findings
    reading = (V.second_row(lambda space, s: href(folder, root, THEME, space, s), "Audience Report", a_open,
                            READINGS, a_read, "Reading") if a_open else "")
    body = ({"Coverage": _coverage, "Tracks": _one_job, "Consistency": _one_job, "Findings": _audience}[a_read](
        snap, labels[a_open]) if a_open else '<p class=mut>No register question on this Board yet.</p>')
    return {
        "Description": Space(html=desc[d_open](snap), subspaces=tuple(desc), open=d_open,
                             run_types=_kinds(snap, "scope", "prototype")),
        "Audience Report": Space(html=reading + body, subspaces=tuple(labels), open=a_open,
                                 run_types=_kinds(snap, "insight")[2:]),
        "Work Details": Space(html=_pages(snap, folder)),
        "Runs": Space(html=_runs(snap), run_types=_kinds(snap, "insight")[:2] + _kinds(snap, "check")),
        "Delivery": Space(html=_delivery(snap), run_types=_kinds(snap, "delivery")),
    }


def claims(block):
    """An Insight Board wherever it sits: an Insight Block kept in tasks/ says `workbench: insight` in
    its board.md, or Home opens it as an Insight Board (home.board_workbench_route)."""
    from live.home import board_workbench_route
    return board_workbench_route(block) == "insight-board"


# today's layout's buttons (the old page's run cards), named by the Run each makes (haipipe-run ref/run-types-by-space.md
# rule 6, b11 s21's names); a hard Run keeps its rNN_ name. Plan C's are named in insight_views.RUNS.
RUN_NAMES = {"Prepare extract": "run-add-version-<d>vM", "Ask": "run-ask-<L><NN>", "Carry a board over": "run-carry-<board>",
             "Register a cut": "run-set-cuts-p<N>", "Review the questions": "run-review-questions-p<N>",
             "Plan the evidence": "run-plan-evidence-<L><NN>", "Write the script": "run-write-script-<L><NN>",
             "Review the script": "run-review-script-<L><NN>", "Draw the question map": "run-map-questions",
             "Report": "run-write-<tNN>", "Pool or split": "run-pool-<tNN>", "Data runs": "rNN_<partition>",
             "Information runs": "rNN_<partition>", "Mechanical check": "run-check-alignment-<tNN>",
             "Answer review": "run-check-<tNN>", "Handoff draft": "run-draft-handoff"}

THEME = Theme(name="insight", label="Insight", icon="🔎", guide="insight", spaces=spaces, claims=claims,
              run_names=RUN_NAMES)
