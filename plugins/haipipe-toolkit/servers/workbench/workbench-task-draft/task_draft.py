"""The draft Task's screen: what a Task whose face says `task-type: draft` shows in the frame's Spaces.

One Task type, one folder (b32 s41-D15, JL 261016: "I want to put the UI assets related to this workbench-task-xxx
to this folder ... we can have many other types of the task types later"). Everything a draft Task shows lives in
servers/workbench/workbench-task-draft/: this layout, the Page views it embeds (outline.py, evidence.py, runs.py,
delivery.py, ...), their assets/ and the standalone reader/. Its manual is skills/1_base/workbench/workbench-task-draft/.

The frame finds this file by its name: every `workbench-task-<type>/task_<type>.py` (in servers/workbench/ for a type every
theme uses, or in servers/workbench-<theme>/ for a theme's own) names TASK_TYPE and gives spaces(folder, root, sub).
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from urllib.parse import urlencode

from live.draft_steps import CHIPS, STEPS, current, delivery_cards, facts, states, step_view
from live.frame import LEVEL_SKILL, ROUTE, RUN_ANY, Space, _e, _link, _rel, chain, face, question_rows

TASK_TYPE = "draft"

# A Task's Page views (this folder), each once a route and a page of its own, shown in place as
# a subspace of the Space it belongs to (JL 261007: "why not merge them into the base"):
# {Space: ((subspace, view), ...)}; the view is served by this route, `?view=<view>&path=<face>`.
PAGE_VIEWS = {"Description": (("Folder", "folder"),),
              "Audience Report": (("Draft", "draft"),),
              "Work Details": (("Evidence", "evidence"), ("Value", "value")),
              "Runs": (("Page Runs", "runs"),),
              "Delivery": (("Lanes", "delivery"),)}


# what each Page view reads, for the Disk box (this folder: each module's docstring)
PAGE_VIEW_DISK = {"folder": (("./", "every lane of the Page folder, and how old each is"),),
                  "draft": (("{face}", "the Page: its Content divisions, aims and states"),
                            ("draft/", "the plan versions, Scratch and Revise")),
                  "evidence": (("runs/*/passes/*/result.yaml", "one card per Evidence Result, by type (older Pages: results/*/)"),),
                  "value": (("evidence/probe/*/card.md", "## Values: the numbers a probe card holds"),
                            ("{face}", "the sentences that cite PP<NN>.v<n>")),
                  "runs": (("runs/", "the Page's Runs: planned, registered, done"),),
                  "delivery": (("delivery/", "one segment per lane: latex · word · slide · render"),)}


def page_view(view: str, md: Path, root: Path) -> str:
    """One Page view, in place: the page its route draws, framed."""
    src = ROUTE + "?" + urlencode({"view": view, "path": _rel(md, root)})
    return (f'<iframe class=page-view src="{_e(src)}&amp;embed=1" loading=lazy title="{_e(view)}"></iframe>'
            f'<p class=mut>{_link(src, "open on its own ↗")}</p>')


def with_page_views(out: dict, level: str, folder: Path, root: Path, sub: str, first: dict) -> dict:
    """Add a Task's Page views to its Spaces: each Space's own content becomes its first subspace
    (named in `first`), the views follow; the open one is drawn."""
    md = face(folder)
    if level != "Task" or not md or md.name == "board.md":
        return out
    for space, views in PAGE_VIEWS.items():
        v = out.get(space, Space())
        own = v.subspaces or (first[space],)
        views = tuple((n, view) for n, view in views if n not in own)   # a theme's own view of that name wins
        names = tuple(n for n, _ in views)
        opened = sub if sub in names else (v.open or own[0])
        html_ = next((page_view(view, md, root) for n, view in views if n == sub), v.html)
        disk = next((tuple((d.replace("{face}", md.name), m) for d, m in PAGE_VIEW_DISK[view])
                     for n, view in views if n == sub), v.disk)
        out[space] = replace(v, html=html_, subspaces=own + names, open=opened, keep=names, disk=disk)
    return out


# ── a draft Task on the frame (b32 s41-task-draft-procedure; was b03 s13, b16 s13) ─────────────────
# Work is the seven step tabs, Studio · 1 · Plan · 2 · Write · 3 · Evidence · 4 · Display · 5 · Revise · Delivery, each
# Operation over Result (draft_steps.py); Report has the same tabs with the Results only, and keeps Table and
# Questions (s41 Ⓐ, JL 261015: "So it is the Studio, 1, Plan, ..... and Delivery as the last one").
# Description is the face alone: its Plan, Requirement and Records are cards of 1 · Plan. A theme whose Tasks
# are drafts returns draft_task_spaces(...) from its spaces() at Task level, and adds its own.
DRAFT_TASK_SUBS = {
    "Description": (),         # no third row: the face and its fields
    "Audience Report": STEPS + ("Table", "Questions"),
    "Work Details": STEPS,
    "Runs": (),                # no third row: the Page's own Runs view, by lane, a card per Run (b16 s13)
    "Delivery": (),            # no third row: one card per kind of delivery, its result embedded
}
# links made before the step tabs (261020) open the step that took their place (s41 Ⓐ)
# Revise was 4 · Revise until 4 · Display came in (261020)
OLD_SUBS = {"Draft-Scratch": "2 · Write", "Reading": "2 · Write", "Draft-Revise": "5 · Revise", "4 · Revise": "5 · Revise",
            "Evidence-Citation": "3 · Evidence", "Evidence-Display": "4 · Display", "Evidence-Value": "3 · Evidence",
            "Evidence-Supporting": "3 · Evidence", "Scope": "1 · Plan", "Plan": "1 · Plan", "Requirement": "1 · Plan",
            "Records": "1 · Plan"}
# a step tab or the Delivery Space -> its run cards, by label, from the Page's run-cards.md (b16 s13
# Decided 5, JL 261007): the Report is for reading, so its tabs carry none. A card not in run-cards.md
# yet is left out; the Studio's own Run (run-draw-<sNN>) comes from draft_steps.
DRAFT_TASK_RUNS = {
    "1 · Plan": ("Structure revise",),
    "2 · Write": ("Scratch", "Auto write"),
    "3 · Evidence": ("Bind / update citation", "Bind / update value", "Evidence embed"),
    "4 · Display": ("Build figure / table",),
    "5 · Revise": ("Section revise", "Paragraph revise", "Revise edits"),
    "Delivery": ("Build", "Check"),
}
# a Page run card -> the Run it makes (JL 261007: buttons named by their Runs; the Page skills' own
# names: haipipe-draft-logic (ref/scratch.md) · -structure · -writing · -revise · -evidence, haipipe-display); the two
# Supporting kinds are hard Runs of other Tasks
PAGE_RUN_NAMES = {"Scratch": "run-scratch-<target>", "Structure revise": "run-structure-<slug>",
                  "Evidence embed": "run-<value|display|citation>-<slug>", "Section revise": "run-section-<slug>",
                  "Paragraph revise": "run-paragraph-<slug>", "Revise edits": "run-revise-<target>",
                  "Auto write": "run-section-<slug>", "Bind / update citation": "run-citation-<slug>",
                  "Build figure / table": "run-display-<slug>", "Bind / update value": "run-value-<slug>",
                  "Task runs": "rNN_<slug> (a work Task)", "Discovery runs": "rNN_<author><year>_<subject>",
                  "Build": "run-delivery-<target>", "Check": "run-check-<page>"}
PAGE_QUESTION_RUNS = (
    {"label": "run-ask-<qNN>", "doing": "ask a question",
     "prompt": "Ask a new question of {folder}: its ## Questions row and reports/qNN_<topic>/.",
     "skills": ["haipipe-report"]},
    {"label": "run-report-<qNN>", "doing": "write the report",
     "prompt": "Write or update a question's report in {folder}/reports/qNN_<topic>/: "
               "Answer · Evidence · Limits · Next, and what it changed in the draft.",
     "skills": ["haipipe-report"]})
# a subspace -> the Page's (Space, Draft view, tab) it opens embedded
PAGE_TASK_VIEWS = {"Table": ("bullet", "table", "")}


def page_view_url(folder: Path, root: Path, sub: str) -> str:
    """The Page workbench's address for one of its views, embedded: path= the Block's face, file= the
    Task's face from the Block, as every Page link of a Board has it."""
    block, md = chain(folder, root).get("Block"), face(folder)
    if not block or not md or not face(block):
        return ""
    space, mode, tab = PAGE_TASK_VIEWS[sub]
    query = {"path": _rel(face(block), root), "file": md.relative_to(block).as_posix(), "embed": "1",
             "space": space, **({"view": mode} if mode else {}), **({"tab": tab} if tab else {})}
    return "/_board/draft?" + urlencode(query)


def _page_runs(sub: str) -> tuple:
    """The run cards of one Page view, as Runs-panel kinds; none for a view with no cards."""
    try:
        from live.runs_panel import run_types
        cards = {c["label"]: c for c in run_types()}
    except Exception:                               # no run cards: the view still opens
        return ()
    def skills(value):                              # run-cards.md gives a list, or "a · b"
        items = value if isinstance(value, (list, tuple)) else str(value or "").split("·")
        return [str(x).strip() for x in items if str(x).strip()]
    return tuple({"label": PAGE_RUN_NAMES.get(c["label"], c["label"]), "doing": c["label"].lower(),
                  "prompt": c["prompt"], "skills": skills(c.get("skills"))}
                 for c in (cards.get(label) for label in DRAFT_TASK_RUNS.get(sub, ())) if c)


def draft_task_spaces(folder: Path, root: Path, sub: str = "") -> dict:
    """{Space: Space} for a draft Task: Work and Report are the seven step tabs (draft_steps.py), Report also
    Table and Questions; Description is the face; Runs and Delivery open the Page's own views. Idea Studio is
    the Block's, as at every level."""
    folder, root = folder.resolve(), root.resolve()
    md = face(folder)
    sub = OLD_SUBS.get(sub, sub)
    work, report, step, runs = step_view(folder, root, sub if sub in STEPS else "")
    out = {"Description": Space(html="", open="Scope", page=True, run_types=(
        {"label": f"run-face-{folder.name.split('_', 1)[0]}", "doing": "update the description",
         "prompt": "Update the face of {folder}.", "skills": [LEVEL_SKILL["Task"]]},)),
        "Work Details": Space(html=work, subspaces=STEPS, open=step, run_types=tuple(runs) + _page_runs(step),
                              page=True)}
    reports = DRAFT_TASK_SUBS["Audience Report"]
    if sub == "Questions":                      # the Section's questions, Question │ Work │ Report
        rows, _ = question_rows("Task", folder, root)
        out["Audience Report"] = Space(html=rows, subspaces=reports, open=sub, run_types=PAGE_QUESTION_RUNS, page=True)
    elif sub == "Table":                        # the Page's Bullet table, embedded
        url = page_view_url(folder, root, sub)
        body = (f'<iframe class=space-frame title="{_e(sub)}" src="{_e(url)}"></iframe>' if url else
                '<p class=space-empty>This Task has no face under a Block, so it opens no Page view.</p>')
        out["Audience Report"] = Space(html=body, subspaces=reports, open=sub, page=True)
    else:                                       # a step's Results only, under the same name as in Work
        out["Audience Report"] = Space(html=report, subspaces=reports, open=step, page=True)
    block = chain(folder, root).get("Block")    # the Page Runs view, embedded (JL 261007: "is this a table what what?")
    src = ("/_board/runs?" + urlencode({"path": _rel(face(block), root), "file": md.relative_to(block).as_posix(),
                                        "embed": "1"}) if block and md and face(block) else "")
    out["Runs"] = Space(html=(f'<iframe class=space-frame title="Runs" src="{_e(src)}"></iframe>' if src else
                              '<p class=space-empty>This Task has no face under a Block, so it shows no Page Runs.</p>'),
                        run_types=(RUN_ANY,), page=True)
    out["Delivery"] = Space(html=delivery_cards(folder, root, md), run_types=_page_runs("Delivery"), page=True)
    return out


def work_card(task: Path, root: Path) -> str:
    """The Task's seven steps on its Work card in the Job (b32 s41): one tab each, its chip read from the Task's
    files, a click opens that step in the Task's Work."""
    from live.frame import theme_of
    task, root = task.resolve(), root.resolve()
    f = facts(task, root)
    st, k = states(f), len((f["draft"] or {}).get("previous", [])) + 1
    theme = theme_of(task, root)
    link = lambda s: ROUTE + "?" + urlencode({"path": _rel(task, root), **({"theme": theme} if theme != "vanilla" else {}),
                                             "space": "Work Details", "sub": s})
    now = current(st)
    return ('<nav class="row subs work-steps">' + "".join(
        f'<a class="tab{" on" if s == now else ""}" href="{_e(link(s))}">{_e(s)} '
        f'{CHIPS[st[s]].format(k=k)}</a>' for s in STEPS) + "</nav>")


# a Page view (`/_board/workbench?view=<view>`) -> the method that draws it, from this folder's modules (frame_view.py)
VIEW_METHODS = {"folder": "folderstat_view", "draft": "outline_view", "value": "value_view",
                "evidence": "evidence_tab_view", "delivery": "delivery_tab_view", "runs": "runs_view",
                "pageruns": "pageruns_view"}

spaces = draft_task_spaces          # what the frame calls for a draft Task (frame.task_layouts)
