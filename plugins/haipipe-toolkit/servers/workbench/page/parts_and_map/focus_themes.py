"""The focus page's theme hooks: draft, paper, insight and design views, and the Skills section."""
from __future__ import annotations

import re
import traceback
from collections import Counter
from pathlib import Path

from live import frame
from live import focus_interactions
from live.focus_base import WORK_SHAPE, markdown, page_level, page_module, page_url, tasks_below
from live.focus_interactions import interaction_item
from live.focus_studio import topic_rows
from live.focus_findings import work_paths


# ── HOOK: a draft Task (b32 s42-draft-task-focus-page) ─────────────────────────────────────────────────────────────
# A Task whose face says `task-type: draft` (a paper Section, the Abstract, a letter) fills Report, Work, Studio and
# Delivery from workbench-task-draft/page_shell/focus_draft.py, its one owner; this page only asks it (`draft_parts`), the way
# frame.task_card asks a layout's work_card. Everything draft-specific lives there.
def is_draft(folder: Path) -> bool:
    return page_level(folder) == "Task" and frame.task_type(folder) == "draft"


def page_skills(folder: Path, root: Path, theme: str, level: str, draft: bool, topics: bool, inbox: bool,
                paper: bool) -> str:
    """The rail's Skills section (skills_section.py): this theme's, this level's, its views' and its Runs' skills."""
    from live import skills_section as K
    if level in ("Block", "Job", "Task") and page_module(theme, folder, root)[1] == "prototype_":
        theme = "insight"                        # a Question Book is insight's: /hai-insight leads its Skills (round 1)
    views = type_skills(folder, root) + [a for v in VIEW_SKILLS.values() for a, _ in v] if theme in WORK_SHAPE else []
    if paper and level == "Block":
        try:
            from live.board_process import VIEW_SKILLS as PAPER_SKILLS
            views = [a for v in PAPER_SKILLS.values() for a, _ in v]
        except Exception:
            pass
    if theme in ("insight", "design", "discovery", "cowork") and level in ("Block", "Job", "Task"):
        try:                                     # a theme's own views' skills: live.<theme>_focus.VIEW_SKILLS (261106)
            import importlib
            own = getattr(importlib.import_module(f"live.{theme}_focus"), "VIEW_SKILLS", {})
            views = list(dict.fromkeys([a for v in own.values() for a, _ in v] + views))
        except ImportError:
            pass
    return K.skills_html(folder, root, theme, level, views, draft, topics, inbox)


def _draft_css() -> str:
    """The draft Task page's own CSS (its step words on the view buttons), for a view it does not build (Runs)."""
    try:
        from live import focus_draft
        return focus_draft.CSS
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (code review 261113)
        return ""


def draft_parts(folder: Path, root: Path) -> dict:
    """The draft Task's parts (focus_draft.parts), or {} for any other page or a draft that does not read."""
    if not is_draft(folder):
        return {}
    try:
        from live import focus_draft
        return focus_draft.parts(folder, root, lambda section, group="": page_url(folder, root, section, group))
    except Exception:                                   # a half-made draft never breaks the page
        return {}


def draft_branches(folder: Path, root: Path) -> list:
    try:
        from live import focus_draft
        return focus_draft.branches(folder, root)
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (code review 261113)
        return []


def paper_delivery(folder: Path, root: Path) -> str:
    """A paper version's Delivery (its assembled paper, then its Sections) or a Board's (each version's paper), from the
    Board's delivery/<version>/build-manifest.json; "" for any other page (paper_version.paper_delivery)."""
    if page_level(folder) not in ("Job", "Block"):
        return ""
    try:
        from live import paper_version
        return paper_version.paper_delivery(folder, root)
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (b16 review 261101)
        return ""


def paper_look() -> dict:
    """A paper version page's look, the same as a draft Task's: width, section verbs, view captions (focus_draft)."""
    try:
        from live import focus_draft
        from live import board_read, board_views, paper_version  # noqa: F401  (the last two fill board_read.PAPER_CAPTIONS)
        common = re.sub(r"\.focus-(?:page|rail)[^\n]*--fd-w[^\n]*\n", "",           # the common width, like every page
                        focus_draft.WIDE.replace(":root{--fd-w:min(1480px,calc(100vw - 32px))}", ""))   # (JL 261031, b10 r01 Q2)
        return {"css": common + board_views.PAGE_CSS + focus_draft.borrowed_css() + focus_draft.JS, "verbs": focus_draft.SECTION_VERBS,
                "captions": {**focus_draft.CAPTIONS, **board_read.PAPER_CAPTIONS}}
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (b16 review 261101)
        return {}


def paper_delivery_views(folder: Path, root: Path) -> dict:
    """A paper version's Delivery views, Paper · Word · Supplement · Files (paper_version.version_delivery_views); {} else."""
    if page_level(folder) != "Job":
        return {}
    try:
        from live import paper_version
        return paper_version.version_delivery_views(folder, root)
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (b16 review 261101)
        return {}


def paper_board_report(folder: Path, root: Path) -> dict:
    """A paper Board's own parts as Report views, Idea · Story · Venue · Data flow · Paper flow · Related work
    (board_views.board_report_views; JL 261031); {} for any other page."""
    if page_level(folder) != "Block":
        return {}
    try:
        from live import board_views, idea_block
        if idea_block.is_idea_block(folder):        # an Idea Block in paper/: its Idea Jobs, no Paper Board views
            return idea_block.report_views(folder, root)
        # Interactions and the mind map are sections inside each part's view, not views (JL 261031)
        return board_views.board_report_views(folder, root, lambda text, base: markdown(text, base, root),
                                              focus_interactions.interactions(folder, root))
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (b16 review 261101)
        return {}


def paper_board_work(folder: Path, root: Path, versions: str) -> dict:
    """A paper Board's Work: the Report's view list, each part's work (board_views.board_work_views; JL 261031: "the
    work and report should share the same view list"); Draft holds `versions`, the base Job-Versions rows. {} else."""
    if page_level(folder) != "Block":
        return {}
    try:
        from live import board_views
        return board_views.board_work_views(folder, root, lambda text, base: markdown(text, base, root), versions,
                                            focus_interactions.interactions(folder, root), lambda r: interaction_item(r, folder, root))
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (b16 review 261101)
        return {}


def paper_version_work(folder: Path, root: Path) -> dict:
    """A paper version's Work: Draft-Main · Draft-Appendix · Display-Main · Display-Appendix (focus_draft; JL 261031,
    s36-D01, D02); {} for any other page."""
    if page_level(folder) != "Job":
        return {}
    try:
        from live import paper_version
        return paper_version.version_work_views(folder, root, focus_interactions.interactions(folder, root), lambda r: interaction_item(r, folder, root))
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (b16 review 261101)
        return {}


def paper_version_report(folder: Path, root: Path) -> dict:
    """A paper version's Report: its Work's six views, the Results alone (paper_version.version_report_views; JL 261106,
    decision 1); {} for any other page."""
    if page_level(folder) != "Job":
        return {}
    try:
        from live import paper_version
        return paper_version.version_report_views(folder, root)
    except Exception:
        traceback.print_exc()   # in the server log, not hidden
        return {}


def paper_job_views(folder: Path, root: Path, section: str) -> dict:
    """A paper Board's evidence or submission Job, Report or Work (paper_jobs.job_views; JL 261106: they fell back to the
    old Progress view); {} for any other page."""
    if page_level(folder) != "Job":
        return {}
    try:
        from live import idea_block, paper_jobs
        if idea_block.idea_block_of(folder) is not None:   # an Idea Job: its face, not a paper Job's views
            return idea_block.job_views(folder, root)
        return paper_jobs.job_views(folder, root, section == "work")
    except Exception:
        traceback.print_exc()   # in the server log, not hidden
        return {}


def view_items(theme: str, folder: Path, root: Path, level: str, view: str, keys, rows: list, questions: list) -> list:
    """The items a view's own 🙋 Interaction shows (JL 261106: "a view's bottom section shows that view's own items, and
    the rail shows everything at this page and below"). A paper Board: the forms about one of the view's parts (their
    `for:` topic), a form about no part by where it was asked (an evidence Job's under Evidence or Displays, the rest
    under Writing). A work page: the forms at a Question's work under Findings, the forms below the page under Status
    (a Task's own too, beside its Runs), the rest (the page's own, about its topics) under MindMap. A paper version, Section or evidence Job: its own forms.
    Any other page: every item, as before."""
    strip = lambda k: k.removeprefix("work-").removeprefix("report-")
    key, keys = strip(view), [strip(k) for k in keys]
    if theme in ("insight", "design") and keys:   # each view its own forms (261106): the theme says where an item
        try:                                      # belongs (live.<theme>_focus.view_of_item), else a child page's go
            import importlib                      # to the view of its children, the page's own to MindMap
            own = getattr(importlib.import_module(f"live.{theme}_focus"), "view_of_item", None)
        except ImportError:
            own = None

        def home(r):
            k = own(r, folder, root, level, keys) if own else None
            if k in keys:
                return k
            if Path(r["page"]) != folder:
                return next((k for k in ("jobs", "grid", "designs", "standing") if k in keys), keys[0])
            return "mindmap" if "mindmap" in keys else keys[0]
        return [r for r in rows if home(r) == key]
    if theme == "paper" and level == "Block":
        from live import paper_focus
        return paper_focus.scope(folder, root, key, topic_rows(folder, root), rows, [])['interactions']
    if theme == "paper":
        return [r for r in rows if Path(r["page"]) == folder]
    if theme in WORK_SHAPE:
        def home(r):
            explicit = str(r.get('view') or '').removeprefix('report-').removeprefix('work-')
            explicit = {'overview': 'mindmap', 'status': 'standing'}.get(explicit, explicit)
            if explicit in keys:
                return explicit
            page = Path(r["page"])
            if "findings" in keys and any(page == w or w in page.parents for q in questions for w in work_paths(q, folder, root)):
                return "findings"
            if "standing" in keys and (page != folder or level == "Task"):
                return "standing"
            return "mindmap" if "mindmap" in keys else keys[0]
        return [r for r in rows if home(r) == key]
    return rows


def insight_job_work(folder: Path, root: Path) -> dict:
    """An insight Job's Work: Findings · Questions · Changes · MindMap, each ⚙️ Process then 📊 Results (insight_focus.
    job_work_views; b11 j01 s55, JL 261101); its forms in each view's own 🙋 Interaction (view_items, 261106), never
    in a section of the theme's own; {} for any other page."""
    if page_level(folder) != "Job":
        return {}
    try:
        from live import insight_focus
        return insight_focus.job_work_views(folder, root)
    except Exception:
        traceback.print_exc()   # in the server log, not hidden
        return {}


def insight_board_report(folder: Path, root: Path) -> dict:
    """An insight Board's Report: Findings · Questions · Data · Rounds · Advice, numbered sections only
    (insight_focus.board_report_views; b11 j01 s51, JL 261101); {} for any other page."""
    if page_level(folder) != "Block":
        return {}
    try:
        from live import insight_focus
        return insight_focus.board_report_views(folder, root)
    except Exception:
        traceback.print_exc()   # in the server log, not hidden
        return {}


def insight_views_for(folder: Path, root: Path, section: str) -> dict:
    """An insight Board's Work, a Job's Report, a Task's Report or Work, in the b11 j01 letters (insight_focus; s52,
    s54, s57, s58, JL 261102); {} for any other page."""
    try:
        from live import insight_focus as IF
        level = page_level(folder)
        if level == "Block" and section == "work":       # its forms in each view's own 🙋 Interaction (261106)
            return IF.board_work_views(folder, root)
        if level == "Job" and section == "report":
            return IF.job_report_views(folder, root)
        if level == "Task":
            return IF.task_views(folder, root, section)
    except Exception:
        traceback.print_exc()   # in the server log, not hidden
    return {}


def design_views(folder: Path, root: Path, section: str) -> dict:
    """A design Block's, Job's or Task's Report (plain keys; the page adds the shared MindMap last) or Work (`work-<key>`,
    its MindMap last) in the j01 letters (design_focus.views; b12 j01 s51 to s58, JL 261101; the shared page rules,
    261106); its forms in each view's own 🙋 Interaction (view_items asks design_focus.view_of_item); {} for any other
    page."""
    try:
        from live import design_focus
        return design_focus.views(folder, root, section)
    except Exception:
        traceback.print_exc()   # in the server log, not hidden
        return {}


VIEW_SKILLS = {"mindmap": (("hai-mindmap", "draws and refreshes this map"),),
               "overview": (("hai-block", "defines goals and requirements"), ("hai-mindmap", "organizes the Topics")),
               "delivery": (("hai-delivery", "keeps outputs and handoff records"),),
               "standing": (("hai-job", "adds a Job and keeps its Tasks in order"),
                            ("hai-task", "plans, builds and runs each Task"),
                            ("hai-run", "keeps each Run's card and receipt")),
               "findings": (("hai-report", "writes each answer from its Results"),
                            ("hai-task", "reads a Run's Result into its Task"),
                            ("hai-delivery", "keeps what it hands over in delivery/"))}


# the skill a Task's own `task-type:` names (hai-task's routing), so a data Task lists /hai-data and a value
# Task /hai-paper-evidence, never the other way round (round 3: "Skills still /hai-paper-evidence, no /hai-data")
TYPE_SKILLS = {"data": "hai-data", "raw": "hai-data", "value": "hai-paper-evidence",
               "display": "hai-display", "evidence": "hai-evidence", "fit": "hai-nn", "algo": "hai-nn",
               "eval": "hai-nn", "endpoint": "hai-end", "delivery": "hai-delivery", "draft": "hai-draft",
               "labeling": "hai-labeling", "individual": "hai-individual"}


def type_skills(folder: Path, root: Path) -> list:
    """The skills the `task-type:` of this Task, or of the Tasks under this Job or Block, name; most Tasks first."""
    level = page_level(folder)
    tasks = [folder] if level == "Task" else tasks_below(folder, level, root)
    used = Counter(TYPE_SKILLS.get(frame.task_type(t), "") for t in tasks)
    return [s for s, _ in used.most_common() if s]
