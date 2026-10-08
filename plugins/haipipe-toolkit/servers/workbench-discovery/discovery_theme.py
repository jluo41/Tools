"""The discovery theme on the base frame (servers/workbench/frame.py): only what differs from vanilla.

A Discovery Block climbs Block → Job (an inquiry) → Task (a typed Task Page, its Paper Runs in runs/ and
results/) with the ladder's own jNN_ / tNN_ names. Each Space carries over what the old Discovery page
(discovery_views.py, /_board/discovery-board) shows, read through the same snapshot (discoveryboard.py),
drawn in the base's look only (JL 261007: no theme stylesheet): wf-table, the folding .topic row, .q-row,
.chip, .st-ok / .st-warn.

    Block  Description: Block · Resources | Audience Report: Questions · Reports
           | Work Details: Papers · Tasks · Citations | Runs: All · Blocked | Delivery: Reports · BibTeX
    Job    Audience Report: the Questions its Tasks serve | Work Details: its Tasks | Runs: its Tasks' Runs
    Task   Audience Report: Synthesis | Work Details: Papers · Notes | Runs: its Paper Runs

Idea Studio reads as vanilla (studio/ topics). A discovery Task is a Discovery Task Page, not a Page
workbench Page: its own views are its papers and synthesis, so it does not use page_task_spaces. Run
types come from the family's Workbench Table (skills/…/workbench-discovery/ref/workbench-table.md) and
only copy their prompt. Read-only: nothing here writes.
"""
from __future__ import annotations

from pathlib import Path

from live.discoveryboard import block_snapshot
from live.discovery_views import table_rows
from live.frame import Space, Theme, chain, esc, pop, rel, table

ORDER = {"failed": 0, "blocked": 1, "missing": 2, "running": 3, "waiting": 4, "planned": 5, "complete": 6}
BAD = ("blocked", "failed", "missing")
# the old page's (Space, View) -> the frame's Space, for the Workbench Table's run types
SPACE_OF = {("Scope", "Block"): "Description", ("Scope", "Resources"): "Description",
            ("Scope", "Questions"): "Audience Report", ("Work", "Questions"): "Audience Report",
            ("Check", "Reports"): "Audience Report", ("Scope", "RoadMap Draw"): "Idea Studio",
            ("Work", "Papers"): "Work Details", ("Work", "Tasks"): "Work Details",
            ("Check", "Citations"): "Work Details", ("Check", "Runs"): "Runs",
            ("Delivery", "Reports"): "Delivery", ("Delivery", "BibTeX"): "Delivery"}


def _kinds(space: str, views=None) -> tuple:
    """The Workbench Table's run types for one frame Space (optionally only some old Views)."""
    out = []
    for r in table_rows():
        where = SPACE_OF.get((r["Space"], r["View"]))
        if where != space or r["Run type"] in ("", "none") or (views and r["View"] not in views):
            continue
        signs = f' The person signs {r["Person signs"]}.' if r.get("Person signs") not in ("", "none", None) else ""
        out.append({"label": r["Run type"], "skills": [r["Skill"]] if r["Skill"] not in ("", "none") else [],
                    "prompt": f'Run with {r["Agent"]}: {r["Run type"]} in the Discovery folder {{folder}} '
                              f'({r["Space"]} › {r["View"]}), following {r["Skill"]}.{signs}'})
    return tuple(out)


def _pick(sub: str, options: tuple) -> str:
    return sub if sub in options else options[0]


def _st(status: str) -> str:
    cls = "st-ok" if status == "complete" else "st-warn" if status in BAD or status in ("waiting", "planned") else "mut"
    return f'<span class={cls}>{esc(status)}</span>'


def _empty(text: str) -> str:
    return f'<p class=mut>{esc(text)}</p>'


def _fold(title: str, meta: str = "", body: str = "", opened: bool = False) -> str:
    return (f'<details class=topic{" open" if opened else ""}><summary><b>{esc(title)}</b>'
            f'<span class=topic-meta>{meta}</span></summary><div style="padding:8px 14px">{body}</div></details>')


# ── the views, each from the old page's data ───────────────────────────────────────────────────
def _block(snap: dict) -> str:
    t = snap["totals"]
    jobs = "<br>".join(f'<span class=chip>{esc(j["name"])}</span> {esc(j["title"])} '
                       f'<span class=mut>· {len(j["tasks"])} Tasks · {sum(len(x["papers"]) for x in j["tasks"])} papers</span>'
                       for j in snap["jobs"]) or '<span class=mut>no Jobs yet</span>'
    rows = [("state", esc(snap["state"] or "Not recorded.")), ("spine", esc(snap["spine"] or "Not recorded.")),
            ("close condition", esc(snap["close"] or "Not recorded.")), ("jobs", jobs),
            ("reading", esc(f'{t["papers"]} papers · {t["complete"]} Runs complete · {t["blocked"]} blocked · '
                            f'{t["needs_person"]} to verify · {t["bib"]} BibTeX entries'))]
    return table(("", ""), rows)


def _resources(snap: dict) -> str:
    folds = "".join(_fold(r["title"], esc(", ".join(r["questions"]) or "Block reference"),
                          f'<p>{esc(r["contribution"])}</p><p class=mut>{esc(r["notes"] or "No notes yet.")}</p>'
                          + (f'<p><a href="{esc(r["url"])}" target=_blank rel=noopener>Open source ↗</a></p>' if r["url"] else ""))
                    for r in snap["resources"])
    return folds or _empty("No related resources yet.")


def _paper_table(papers: list, show_task: bool = True) -> str:
    if not papers:
        return _empty("No papers here.")
    rows = []
    for p in papers:
        source = (f'<a href="{esc(p["subject_url"])}" target=_blank rel=noopener>{esc(p["subject_kind"] or "source")} ↗</a>'
                  if p["subject_url"] else esc(p["subject_kind"]))
        title = pop(p["card_url"], p["run"], p["title"]) if p["card_url"] else esc(p["title"])
        readout = f'<div class=mut>{esc(p["readout"][:220])}</div>' if p["readout"] else ""
        verify = f'<span class={"st-warn" if p["needs_person"] else "st-ok"}>{esc(p["verification"])}</span>'
        row = ([f'<span class=chip>{esc(p["job"][:3])} {esc(p["task_id"][-3:])}</span>'] if show_task else []) + \
              [f'<span class=chip>{esc(p["id"])}</span>', title + readout, source, esc(p["reading_depth"]), verify, _st(p["status"])]
        rows.append(row)
    heads = (("Task",) if show_task else ()) + ("Run", "Paper", "Source", "Read", "Verified", "Status")
    return table(heads, rows)


def _papers(snap: dict) -> str:
    parts = [f'<h2>{esc(job["id"])} {esc(task["name"])} · {esc(task["title"])} '
             f'<span class=mut>{len(task["papers"])} papers</span></h2>' + _paper_table(task["papers"], False)
             for job in snap["jobs"] for task in job["tasks"] if task["papers"]]
    t = snap["totals"]
    return (f'<p class=mut>{t["papers"]} papers in {t["tasks"]} Tasks; click a paper for its Result card.</p>'
            + ("".join(parts) or _empty("No Paper Runs yet. Find papers from this Space's Runs panel.")))


def _tasks(tasks: list) -> str:
    rows = [(f'<span class=chip>{esc(t["job"][:3])}</span>',
             (pop(t["page_url"] or t["source_url"], t["name"], t["name"]) if (t["page_url"] or t["source_url"]) else esc(t["name"]))
             + f'<br><b>{esc(t["title"])}</b>',
             esc(t["discovery_type"]), esc(f'{t["complete"]}/{t["total"]}'),
             esc(sum(p["needs_person"] for p in t["papers"])),
             " ".join(pop(s["url"], s["name"]) for s in t["synthesis"]) or '<span class=mut>none yet</span>',
             esc("; ".join(t["issues"][:2]) or "none")) for t in tasks]
    return table(("Job", "Task", "Type", "Runs complete", "To verify", "Synthesis", "Findings"), rows) if rows else \
        _empty("No Task Pages yet.")


def _citations(snap: dict) -> str:
    todo = [p for p in snap["papers"] if p["needs_person"]]
    return f'<p class=mut>{len(todo)} of {len(snap["papers"])} papers need a person.</p>' + _paper_table(todo)


def _questions(questions: list) -> str:
    if not questions:
        return _empty("No Questions registered yet. Ask one from this Space's Runs panel.")
    out = ['<div class="q-row q-head-row"><div>Logic · the question</div><div>Work · the Tasks and their papers</div>'
           '<div>Report · what it says</div></div>']
    for q in questions:
        logic = (f'<p class=q-head><span class=kind>{esc(q["id"])}</span> <b>{esc(q["title"])}</b></p>'
                 + (f'<p>{esc(q["question"])}</p>' if q["question"] != q["title"] else "")
                 + (f'<p class=mut>{esc(q["hypothesis"])}</p>' if q.get("hypothesis") else ""))
        work = "<br>".join(f'{pop(w["task"]["page_url"] or w["task"]["source_url"], w["task"]["name"], w["task"]["name"])} '
                           f'<span class=mut>{len(w["task"]["papers"])} papers · {w["task"]["complete"]}/{w["task"]["total"]} Runs</span>'
                           for w in q["work"]) or '<span class=mut>No Task linked yet.</span>'
        r = q["report"]
        report = ((f'<p class=rp-title>{pop(r["url"] or r["source_url"], r["title"] or r["path"])}</p>'
                   + (f'<p class=rp-text>{esc(r["answer"])}</p>' if r["answer"] else "")
                   + f'<p class=rp-tags>{esc(r["status"])}</p>') if r["present"] else '<p class=mut>No report yet</p>')
        out.append(f'<div class=q-row id="question-{esc(q["id"])}"><div class=q-l>{logic}</div>'
                   f'<div class=q-w>{work}</div><div class=q-r>{report}</div></div>')
    return "".join(out)


def _reports(questions: list) -> str:
    folds = []
    for q in questions:
        r = q["report"]
        body = (f'<p>{esc(r["answer"] or "No answer yet.")}</p>'
                f'<p><b>Next:</b> {esc(r["next"] or "Record the next action in the Report.")}</p>'
                + "".join(f'<p class=st-warn>{esc(i)}</p>' for i in q["issues"] + r["issues"])
                + (f'<p>{pop(r["url"], "the report", "Open the report ↗")}</p>' if r["url"] else ""))
        folds.append(_fold(f'{q["id"]} · {q["title"]}', esc(r["status"]), body))
    return "".join(folds) or _empty("No Questions registered yet.")


def _runs(runs: list, only_bad: bool = False) -> str:
    rows = sorted((r for r in runs if not only_bad or r["status"] in BAD), key=lambda r: ORDER.get(r["status"], 9))
    return table(("Task", "Run", "Status", "Why"),
                 [(f'<span class=chip>{esc(r["job"][:3])} {esc(r["task_id"][-3:])}</span>',
                   pop(r["result_url"], r["name"], r["name"]) if r.get("result_url") else esc(r["name"]),
                   _st(r["status"]), esc(r["failure"] or "; ".join(r["issues"][:1]))) for r in rows]) if rows else \
        _empty("No blocked or failed Runs." if only_bad else "No Runs yet.")


def _delivery_reports(snap: dict) -> str:
    out = []
    for q in snap["questions"]:
        r = q["report"]
        if r["present"] and r["status"] == "answered":
            body = "".join(f'<p>{esc(p)}</p>' for p in r.get("opening", [])) + (
                ('<h2>Answer</h2>' + "".join(f'<p>{esc(p)}</p>' for p in r["answer_text"])) if r.get("answer_text") else "")
            out.append(_fold(r["title"] or r["path"], esc(q["id"]), body + f'<p>{pop(r["url"], "the report", "Open ↗")}</p>'))
    return "".join(out) or _empty("No Question is answered yet.")


def _bib(papers: list) -> str:
    entries = [p for p in papers if p["bib"]]
    if not entries:
        return _empty("No Run has written a .bib yet.")
    files = " · ".join(pop(p["bib_url"], p["run"] + ".bib") for p in entries)
    text = "\n\n".join(p["bib"].strip() for p in entries)
    return (f'<p class=mut>{len(entries)} entries from {len(papers)} papers.</p><p>{files}</p>'
            f'<pre class=space-source>{esc(text)}</pre>')


def _synthesis(task: dict, folder: Path, root: Path) -> str:
    folds = []
    for s in task["synthesis"]:
        path = folder / s["name"]
        text = path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""
        folds.append(_fold(s["name"], pop(s["url"], s["name"], "open ↗") if s["url"] else "",
                           f'<pre class=space-source>{esc(text)}</pre>', opened=len(task["synthesis"]) == 1))
    return "".join(folds) or _empty("No synthesis yet (summary.md, verdict.md or landscape.md). "
                                    "Synthesize the Task from Work Details.")


def _notes(folder: Path, root: Path) -> str:
    skip = {folder.name + ".md", "summary.md", "verdict.md", "landscape.md"}
    files = [p for p in sorted(folder.glob("*.md")) if p.name not in skip]
    return "".join(_fold(p.name, esc(rel(p, root)), f'<pre class=space-source>{esc(p.read_text(encoding="utf-8", errors="replace"))}</pre>')
                   for p in files) or _empty("No notes beside the Task Page.")


# ── the theme ──────────────────────────────────────────────────────────────────────────────────
def _snap(folder: Path, root: Path) -> dict | None:
    block = chain(folder, root).get("Block")
    try:
        return block_snapshot(block, root) if block else None
    except (ValueError, OSError):                   # not a Discovery Block: the vanilla frame
        return None


def spaces(level, folder, root, sub):
    folder, root = Path(folder).resolve(), Path(root).resolve()
    snap = _snap(folder, root)
    if snap is None:
        return {}
    if level == "Block":
        d = _pick(sub, ("Block", "Resources"))
        a = _pick(sub, ("Questions", "Reports"))
        w = _pick(sub, ("Papers", "Tasks", "Citations"))
        r = _pick(sub, ("All", "Blocked"))
        v = _pick(sub, ("Reports", "BibTeX"))
        return {
            "Description": Space(html=_block(snap) if d == "Block" else _resources(snap), subspaces=("Block", "Resources"),
                                 open=d, run_types=_kinds("Description")),
            "Audience Report": Space(html=_questions(snap["questions"]) if a == "Questions" else _reports(snap["questions"]),
                                     subspaces=("Questions", "Reports"), open=a, run_types=_kinds("Audience Report")),
            "Work Details": Space(html={"Papers": lambda: _papers(snap), "Tasks": lambda: _tasks(snap["tasks"]),
                                        "Citations": lambda: _citations(snap)}[w](),
                                  subspaces=("Papers", "Tasks", "Citations"), open=w, run_types=_kinds("Work Details")),
            "Runs": Space(html=_runs(snap["runs"], r == "Blocked"), subspaces=("All", "Blocked"), open=r,
                          run_types=_kinds("Runs")),
            "Delivery": Space(html=_delivery_reports(snap) if v == "Reports" else _bib(snap["papers"]),
                              subspaces=("Reports", "BibTeX"), open=v)}
    if level == "Job":
        job = next((j for j in snap["jobs"] if j["name"] == folder.name), None)
        if job is None:
            return {}
        ids = {t["id"] for t in job["tasks"]}
        questions = [q for q in snap["questions"] if any(w["task"]["id"] in ids for w in q["work"])]
        runs = [r for r in snap["runs"] if r["job"] == job["name"]]
        return {"Audience Report": Space(html=_questions(questions), run_types=_kinds("Audience Report", ("Questions",))),
                "Work Details": Space(html=_tasks(job["tasks"]), run_types=_kinds("Work Details", ("Tasks",))),
                "Runs": Space(html=_runs(runs), run_types=_kinds("Runs"))}
    if level == "Task":
        task = next((t for t in snap["tasks"] if t["name"] == folder.name and t["job"] == folder.parent.name), None)
        if task is None:
            return {}
        w = _pick(sub, ("Papers", "Notes"))
        runs = [r for r in snap["runs"] if r["task_id"] == task["id"] and r["job"] == task["job"]]
        return {"Audience Report": Space(html=_synthesis(task, folder, root), subspaces=("Synthesis",), open="Synthesis",
                                         run_types=_kinds("Work Details", ("Tasks",))),
                "Work Details": Space(html=_paper_table(task["papers"], False) if w == "Papers" else _notes(folder, root),
                                      subspaces=("Papers", "Notes"), open=w, run_types=_kinds("Work Details", ("Papers",))),
                "Runs": Space(html=_runs(runs), run_types=_kinds("Runs"))}
    return {}


# each button's Run (haipipe-run rule 6); reading a paper is a hard Run with its own name
RUN_NAMES = {"Add a resource": "run-add-resource-<slug>", "Ask a Question": "run-ask-<qNN>",
             "Review the questions": "run-review-questions", "Write the report": "run-report-<qNN>",
             "Check a report": "run-check-<qNN>", "Find papers": "run-find-papers-<tNN>",
             "Read a paper": "rNN_<author><year>_<subject>", "Synthesize a Task": "run-synthesize-<tNN>",
             "Verify a citation": "run-verify-citation-<slug>", "Review a Run": "run-review-<run>"}

THEME = Theme(name="discovery", label="Discovery", icon="🔭", guide="discovery", spaces=spaces, run_names=RUN_NAMES)
