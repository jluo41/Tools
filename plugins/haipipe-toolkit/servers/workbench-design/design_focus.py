"""The design theme on the focus page (b12 j01, s51 to s59): a design Block, a Job and a Task, each Report
and Work in the cells' letters, on the shared page rules every theme's page follows (hai-ui "The person's page
rules", 261106; insight_focus is the model):

  every section a numbered bar, closed until opened, its state word on its right, read from its content; what waits
  on the person under the closed bar (ui_parts._section's `word` and `waits`); the fold script on Report too.
  Report shows results only, each view's big line first; Work has the same views, each ⚙️ Process then 📊 Results, the
  Results drawn by the same function as the Report's view. A row that waits on the person but is no form (sign a goal,
  approve a release, close a Job, agree a method proposal) is a Process step with its state word, never a 🙋 section
  of its own: 🙋 Interaction is the last section of every view, added by the page itself with that view's own forms
  (view_of_item). Lists of items are side tabs, their labels with no count; the MindMap is always a view, last.

    Block   Designs · Goals · Inputs · Rounds · Tests · MindMap         (s51 Report, s52 Work)
    Job     Setup · Ideas · Designs · Ranking · Release · MindMap       (s54 Report, s55 Work)
    Task    by its type, one view per step, then MindMap (s57 Report, s58 Work):
            💡 t00 reason ideas   Inputs · Chains · Ideas · Fence check
            ✏️ one design         Draft · Verify · Revise · State      (its drafts strip above every view)
            🏆 t99 review whole   Rank · Coverage · Kept

A person signs only at the Block (goals, shared rules, a method proposal) and the Job (Review and approve, the close);
no Task asks you. The Results reuse design_views' parts, so the focus page and the six-Space page agree; the only
write is the release, design_ladder_act.py's."""
from __future__ import annotations

import re
from pathlib import Path

# design_context, design_book and the tests read these as design_focus.X: kept importable here
from live import design_canvas as C  # noqa: F401
from live import design_reader as R
from live import design_views as V  # noqa: F401
from live import focus_draft as FD  # noqa: F401
from live.frame import esc, pop, reader, rel, table  # noqa: F401
from live.ui_parts import (GROUP_CSS, PB_CSS, PB_JS, PROMPT_CSS, PROMPT_JS, _cap, _kv, _numbered,  # noqa: F401
                           _pill, _side_tabs)

# The views live in sibling modules, one per part of the page; every name stays readable here (design_focus.X).
from live.design_focus_layout import (BLOCK_VIEWS, CAPTIONS, JOB_VIEWS, NEXT, OLD_BLOCK_VIEWS,  # noqa: F401
                                      TASK_STEPS, VIEW_SKILLS)
from live.design_focus_parts import (CSS, DONE_WORDS, POST_JS, _big, _chain, _closed, _copy,  # noqa: F401
                                     _has, _head_css, _href, _link, _link_btn, _page, _plain, _rows_word,
                                     _section, _session, _step, _tabs, _tiles, _todo, _views, _work_map,
                                     state_mark)
from live.design_focus_design import (_chain_words, _coverage, _coverage_md, _design_card,  # noqa: F401
                                      _design_state, _fence_verdict, _goal_name, _job_closed, _job_next,
                                      _md_lines, _pvo, _section_of, d_state)
from live.design_focus_block import (BLOCK_PARTS, BOARD_LAYOUT, _b_goals, _b_jobs, _b_methods,  # noqa: F401
                                     _b_rounds, _b_summary, _cost_table, _goal_panel, _moves, _picker,
                                     _proposals, _round_state, _rules_file, _split, _standing, _where,
                                     block_view)
from live.design_focus_job import (JOB_PARTS, _chain_panel, _frozen, _j_designs, _j_ideas,  # noqa: F401
                                   _j_ranking, _j_release, _j_setup, _release_line, job_view)
from live.design_focus_task import (NONE, _changes, _feedback, _flow, _key, _kept_table,  # noqa: F401
                                    _next_link, _opened_chain, _stays_out, _strip, _task_build, _topics,
                                    _walk, task_steps, task_view)


# ── what a page is ──────────────────────────────────────────────────────────────────────────────────────────────
def level_of(folder: Path) -> str:
    """Block, Job or Task of a design Board on the ladder; "" for anything else (an older Board keeps its page)."""
    if R.is_job(folder):
        return "Job" if R.is_ladder(folder.parent) else ""
    if re.match(r"^t\d+_", folder.name) and R.is_job(folder.parent) and R.is_ladder(folder.parent.parent):
        return "Task"
    if (folder / "board.md").is_file() and (R.is_ladder(folder) or R.is_method_book(folder)):
        return "Block"                                       # a Design Method Book is a Block too
    return ""


# ── where a form belongs (R2: each view its own 🙋 Interaction) ──────────────────────────────────────────────────
ABOUT_JOB = (("ranking", r"\brank"), ("release", r"release|test.?arm|next.?test|send|freeze|predict"),
             ("ideas", r"idea|chain|fence|reason"), ("designs", r"design|draft|verify|revise"),
             ("setup", r"goal|method|input|pin|setup"))
ABOUT_BLOCK = (("goals", r"goal|rule"), ("inputs", r"inputs"), ("tests", r"observed|experiment|method|score|predict|test"),
               ("rounds", r"round|\bjob|launch"))


def view_of_item(row: dict, folder: Path, root: Path, level: str, keys) -> str | None:
    """The view whose 🙋 Interaction shows a form, by what it is about: at a Block, a Job's or a Task's form under Jobs,
    the Block's own by its words (goals, rounds, methods), else Summary; at a Job, a Task's form under its step's view
    (t00 Ideas, a design Designs, t99 Ranking), the Job's own by its words, else Release; at a Task, its first step's
    view unless its words name another. None leaves it to the page's default."""
    page = Path(row.get("page") or folder)
    topic = row.get("topic")
    about = " ".join(str(x or "") for x in (getattr(topic, "name", ""), row.get("about"), row.get("title"))).lower()
    keys = list(keys)

    def by_words(table_, default):
        return next((k for k, pat in table_ if k in keys and re.search(pat, about)), default)
    if level == "Block":
        return "rounds" if page != folder else by_words(ABOUT_BLOCK, "designs")
    if level == "Job":
        if page != folder:
            kind = R.kind_of(next((p for p in [page, *page.parents] if p.parent == folder), page))
            return {"t00": "ideas", "t99": "ranking"}.get(kind, "designs")
        return by_words(ABOUT_JOB, "release")
    if level == "Task":
        steps = [k for k in keys if k != "mindmap"]
        return next((k for k in steps if re.search(k.replace("-", ".?"), about)), steps[0] if steps else None)
    return None


def goal_line(folder: Path, goal: str) -> str:
    """The goal-line of a design Job or Task in words: its pinned goal (G01, or `G01 · <name>`) becomes the goal's aim."""
    gid = R.goal_pin(goal)
    if not gid or level_of(folder) not in ("Job", "Task"):
        return ""
    jdir = folder if level_of(folder) == "Job" else folder.parent
    b = R.board(R.block_of(jdir.parent) or jdir.parent, with_jobs=False)
    return _goal_name(b, gid)


# ── what focus_page.py asks ─────────────────────────────────────────────────────────────────────────────────────
def views(folder: Path, root: Path, section: str, items=(), item_html=None) -> dict:
    """{key: (name, build)} for the page's Report (section "report", plain keys; the page adds the MindMap last) or
    Work (`work-<key>`, its MindMap last); {} for a folder that is not a design Block, Job or Task on the ladder, so the
    base page stays. `items` and `item_html` are not drawn here: the page's own 🙋 Interaction shows each view's forms."""
    root = root.resolve()
    level = level_of(folder)
    report = section == "report"
    if level == "Block" and R.is_method_book(folder):        # the Book's own views: Method · Versions · Ideas · Scorecard
        from live import design_book as BK
        return _views(BK.BOOK_VIEWS, lambda k: ("", "", *BK.book_view(folder, root, k), ""), report, folder, root)
    if level == "Block":
        return _views(BLOCK_VIEWS, lambda k: block_view(folder, root, k), report, folder, root)
    if level == "Job":
        return _views(JOB_VIEWS, lambda k: job_view(folder, root, k), report, folder, root)
    if level == "Task":
        _icon, _typ, steps = task_steps(folder)
        return _views([(_key(s), s) for s in steps], lambda k: _task_build(folder, root, k, steps), report, folder, root)
    return {}
