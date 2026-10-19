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
from urllib.parse import quote, urlencode

from src.common import delivery_read_lane_dir
from live.frame import (LEVEL_SKILL, ROUTE, RUN_ANY, Space, _e, _link, _reader, _rel, _table, chain, face, pop,
                        question_rows)

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


# ── a Page Task on the frame (b03 s13-task-variants, b16 s13-paper-task; 261007) ───────────────────
# A Task that is a Page (its face is a Page under its Block, as a paper Section is) shows the Page's own
# views in the six Spaces. Each view is the Page itself, embedded (`/_board/draft?…&embed=1`, workbench-task-draft/
# outline.py EMBED_HTML), so its tables, Scratch and Revise work exactly as in the Page workbench. A theme
# whose Tasks are Pages returns draft_task_spaces(...) from its spaces() at Task level, and adds its own.
DRAFT_TASK_SUBS = {
    "Description": ("Scope", "Plan", "Requirement", "Records"),
    "Audience Report": ("Table", "Reading", "Questions"),
    "Work Details": ("Draft-Scratch", "Draft-Revise", "Evidence-Citation", "Evidence-Display",
                     "Evidence-Value", "Evidence-Supporting"),
    "Runs": (),                # no third row: the Page's own Runs view, by lane, a card per Run (b16 s13)
    "Delivery": (),            # no third row: one card per kind of delivery, its result embedded
}
# a Work Details or Delivery view -> its run cards, by label, from the Page's run-cards.md (b16 s13
# Decided 5, JL 261007): the Audience Report is for reading, so Table and Reading carry none; the
# Runs in Work Details change the content. A card not in run-cards.md yet is left out.
DRAFT_TASK_RUNS = {
    "Draft-Scratch": ("Scratch", "Structure revise", "Evidence embed"),
    "Draft-Revise": ("Section revise", "Paragraph revise", "Revise edits", "Auto write"),
    "Evidence-Citation": ("Bind / update citation",), "Evidence-Display": ("Build figure / table",),
    "Evidence-Value": ("Bind / update value",), "Evidence-Supporting": ("Task runs", "Discovery runs"),
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
RUBRIC = Path(__file__).resolve().parents[3] / "skills/1_base/draft/haipipe-draft-review/ref/evaluation-rubric.md"
# a subspace -> the Page's (Space, Draft view, tab) it opens embedded
PAGE_TASK_VIEWS = {
    "Table": ("bullet", "table", ""), "Reading": ("bullet", "reading", ""),
    "Draft-Scratch": ("bullet", "scratch", ""), "Draft-Revise": ("bullet", "revise", ""),
    "Evidence-Citation": ("evidence", "", "citations"), "Evidence-Display": ("evidence", "", "displays"),
    "Evidence-Value": ("evidence", "", "values"), "Evidence-Supporting": ("evidence", "", "supporting"),
}


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


def _rubric(root: Path) -> str:
    """The shared prose rubric the draft is judged by (haipipe-draft-review base-v1), folded."""
    if not RUBRIC.is_file():
        return ""
    inside = root.resolve() in RUBRIC.parents                  # a reader link only for a file the root serves
    body = (_source(RUBRIC, root, "") if inside else
            f'<pre class=space-source>{_e(RUBRIC.read_text(encoding="utf-8", errors="replace"))}</pre>')
    return (f'<details class=topic><summary><b>Rubric · Mechanics · Function · Evidence · Readability</b>'
            f'<span class=topic-meta>the four axes the draft is judged by</span></summary>'
            f'<div style="padding:8px 14px">{body}</div></details>')


def _source(path: Path | None, root: Path, empty: str) -> str:
    """A Markdown file shown as it is, with a link to the Page reader; or why there is none."""
    if not path or not path.is_file():
        return f'<p class=space-empty>{_e(empty)}</p>'
    return (f'<p class=space-reads>{pop(_reader(path, root), path.name, _rel(path, root) + " ↗")}</p>'
            f'<pre class=space-source>{_e(path.read_text(encoding="utf-8", errors="replace"))}</pre>')


LANE_ICON = {"web": "🌐", "latex": "📄", "word": "📝", "slide": "🖥", "render": "🖼"}


def _delivery_cards(folder: Path, root: Path, md: Path | None) -> str:
    """Delivery (JL 261007: "each card is a type of delivery … the card and the preview of the results,
    the embedded content", as the old paper page's Preview did): one card per kind of delivery, from
    the Page's own read-only check (workbench-task-draft/delivery.py check_delivery). Its head: the kind, its
    state (current · stale · not built), its files as ↗ links; its body: the result embedded (the web
    page, the PDF, Word through the PDF twin the build writes beside the .docx, the deck), a LaTeX
    piece with no PDF yet shown as it is, or "not built yet: run Build"."""
    stem = md.stem if md else folder.name
    try:
        from live.delivery import check_delivery
        lanes = check_delivery(md).get("lanes", []) if md else []
    except Exception:                               # no Page engine: no cards, never no page
        lanes = []
    url = lambda f: "/" + quote(_rel(f, root))
    cards = []
    for lane in lanes:
        key = lane.get("lane", "")
        ldir = delivery_read_lane_dir(folder, key)
        files = sorted(f for f in ldir.rglob("*") if f.is_file() and not f.name.startswith(".")) if ldir.is_dir() else []
        state = lane.get("state", "")
        legacy_note = ('<p class="mut dl-note">Old local output: read only; rebuild from source into Block Delivery.</p>'
                       if lane.get("legacy") else "")
        mark = {"pass": "st-ok", "stale": "st-warn"}.get(state, "mut")
        word = {"pass": "current", "stale": "stale", "not-built": "not built"}.get(state, state)
        show = {"web": [ldir / "index.html"], "latex": [ldir / f"{stem}.pdf"], "word": [ldir / f"{stem}.pdf"],
                "slide": [ldir / f"{stem}-deck.html"]}.get(key, [f for f in files if f.suffix in (".pdf", ".html")][:1])
        shown = next((f for f in show if f.is_file()), None)
        links = " · ".join(pop(url(f), f.name, f.relative_to(ldir).as_posix()) for f in files)
        head = (f'<div class=st-bar><span><b>{LANE_ICON.get(key, "")} {_e(lane.get("label", key))}</b> '
                f'<span class={mark}>{_e(word)}</span></span><span class=mut>{links}</span></div>')
        if shown:
            body = f'<iframe class=dl-frame loading=lazy title="{_e(shown.name)}" src="{_e(url(shown))}"></iframe>'
        elif key == "latex" and (ldir / f"{stem}.tex").is_file():     # no PDF compiled yet: the piece itself
            body = (f'<p class="mut dl-note">{_e(stem)}.pdf is not compiled yet; the piece:</p>'
                    f'<pre class="space-source dl-src">{_e((ldir / f"{stem}.tex").read_text(encoding="utf-8", errors="replace"))}</pre>')
        elif files:
            body = '<p class="mut dl-note">built; no preview for this kind yet</p>'
        else:
            body = '<p class="mut dl-note">not built yet: run Build</p>'
        cards.append(f'<div class=topic>{head}{legacy_note}{body}</div>')
    return ("<h2>Deliveries</h2>" + "".join(cards) if cards else
            '<p class=space-empty>Nothing built yet: delivery/ holds no files. Run Build.</p>')


def draft_task_spaces(folder: Path, root: Path, sub: str = "") -> dict:
    """{Space: Space} for a Page Task: Description is Scope (its face) · Plan · Requirement · Records;
    Audience Report, Work Details and Delivery each open the Page's own view, embedded. Idea Studio
    and Runs are the vanilla defaults."""
    folder, root = folder.resolve(), root.resolve()
    md = face(folder)
    out = {}
    for space, subs in DRAFT_TASK_SUBS.items():
        if space == "Runs":                             # the Page Runs view, embedded (JL 261007: "is this
            block = chain(folder, root).get("Block")    # a table what what?"): lanes, counts, a card per Run
            src = ("/_board/runs?" + urlencode({"path": _rel(face(block), root), "file": md.relative_to(block).as_posix(),
                                                "embed": "1"}) if block and md and face(block) else "")
            out[space] = Space(html=(f'<iframe class=space-frame title="Runs" src="{_e(src)}"></iframe>' if src else
                                     '<p class=space-empty>This Task has no face under a Block, so it shows no Page Runs.</p>'),
                               run_types=(RUN_ANY,), page=True)
            continue
        if space == "Delivery":                         # no third row: item cards, Build · Check
            out[space] = Space(html=_delivery_cards(folder, root, md), run_types=_page_runs("Delivery"), page=True)
            continue
        opened = sub if sub in subs else subs[0]
        if space == "Description":
            if opened == "Scope":
                body = ""                               # the vanilla Description: the face and its fields
            elif opened == "Plan":
                try:
                    from src.outline_version import latest_outline, plan_dir
                    plan = latest_outline(plan_dir(folder), md.stem) if md else None
                except Exception:                       # no Page engine: say so, never break the frame
                    plan = None
                body = _source(plan, root, "No plan yet: the Page's plan is written by its Structure Run.")
            elif opened == "Requirement":                # its V (venue) and W (own) rules, then the rubric
                req = folder / "draft" / "records" / f"{md.stem if md else folder.name}-requirement.md"
                body = (_source(req, root, "No requirement record yet (draft/records/<stem>-requirement.md).")
                        + _rubric(root))
            else:
                recs = sorted((folder / "draft" / "records").glob("*.md")) if (folder / "draft" / "records").is_dir() else []
                body = (_table(("record", "bytes"), [(pop(_reader(r, root), r.name, r.name + " ↗"), _e(r.stat().st_size))
                                                     for r in recs]) if recs else
                        '<p class=space-empty>No records yet (draft/records/).</p>')
            out[space] = Space(html=body, subspaces=subs, open=opened, page=True, run_types=(
                {"label": f"run-face-{folder.name.split('_', 1)[0]}", "doing": "update the description",
                 "prompt": "Update the face of {folder}.", "skills": [LEVEL_SKILL["Task"]]},))
            continue
        if opened == "Questions":                   # the Section's questions, Question │ Work │ Report
            rows, _ = question_rows("Task", folder, root)
            out[space] = Space(html=rows, subspaces=subs, open=opened, run_types=PAGE_QUESTION_RUNS, page=True)
            continue
        url = page_view_url(folder, root, opened)
        body = (f'<iframe class=space-frame title="{_e(opened)}" src="{_e(url)}"></iframe>' if url else
                '<p class=space-empty>This Task has no face under a Block, so it opens no Page view.</p>')
        # no read-only note in the Runs panel (JL 261008: "we don't need to add these details")
        out[space] = Space(html=body, subspaces=subs, open=opened, run_types=_page_runs(opened), page=True)
    return out


# a Page view (`/_board/workbench?view=<view>`) -> the method that draws it, from this folder's modules (frame_view.py)
VIEW_METHODS = {"folder": "folderstat_view", "draft": "outline_view", "value": "value_view",
                "evidence": "evidence_tab_view", "delivery": "delivery_tab_view", "runs": "runs_view",
                "pageruns": "pageruns_view"}

spaces = draft_task_spaces          # what the frame calls for a draft Task (frame.task_layouts)
