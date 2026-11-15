"""The insight pages on the focus page (b11 j01): a Board, a Job and a Task, each with its Report and its Work, on the
shared page rules every theme's page follows (haipipe-ui "The person's page rules", 261106):

  every section a numbered bar, closed until opened, its state word on its right; what waits on the person under the
  closed bar (ui_parts._section's `word` and `waits`); the fold script on Report too.
  Report shows results only; Work has the same views, each ⚙️ Process then 📊 Results, the Results drawn by the same
  function as the Report's view. Whatever does something (sign the plan, triage the proposals, close the Job, sign the
  handoff, launch, write, check, ask) is a Process step with its state word, never a 🙋 section of its own: 🙋
  Interaction is the last section of every view, added by the page itself with that view's own forms (view_of_item).
  Lists of items are side tabs, their labels with no count; the MindMap is always a view.

Board: Findings · Questions · Data · Advice · Jobs · MindMap. Question Book: Questions · Ideas · Versions · MindMap.
Job: Findings · Changes (from the second Job) · Progress · MindMap. Task: Answer · Changes · Method · MindMap (By
segment is a section of Answer; plain words; the keys stay). The facts are insight_plan_c's; the older views' parts
insight_views'; the person's actions insight_act's. Nothing here writes."""

from __future__ import annotations

import re
from pathlib import Path

from live import insight_plan_c as P
from live.insight_focus_parts import (  # noqa: F401 · this module keeps answering these names
    VIEWS, VIEW_SKILLS, POST_JS, CSS, _ctable, _old_css, is_job, _session, _facts, _copy, _ask, _pop, _todo,
    _rows_word, _step, _big, _focus, _proto_work, _jlink, _pair, _written, _page_word, _dot, DOT, JOB_KEY, KEY,
    _head, _cap1, _page, _work_page, _map_view, _parts_map, _done, draw_map, MOVED, _qname, _in_job, _prompt,
    _copy_btn, _writing)
from live.insight_focus_task_report import (  # noqa: F401 · this module keeps answering these names
    _task_mindmap, TASK_VIEWS, is_task, _task_x, _state, _cited, _blank, _figures, FIG_NAME, TILE_WORDS, _tiles,
    _sourced, _cite_only, _plan_cites, _qlabel, _answer_pop, _aligned, _answer_word, _last_answer, _t_answer,
    _power, CUT_WORD, _t_cuts, _cite_word, _gather_word, CHAIN_CSS, _cite_chain, ACROSS_CSS, _t_across, _t_plan,
    TASK_PARTS)
from live.insight_focus_task import (  # noqa: F401 · this module keeps answering these names
    _chain, CHAIN, _tw_answer, _tw_cuts, _tw_across, _tw_plan, TASK_PROC, task_views)
from live.insight_focus_job import (  # noqa: F401 · this module keeps answering these names
    WAIT_WORD, _plan_signed, _sign_rows, _overall_state, _overall_proc, _overall_res, _cuts, QA_CSS, _grid,
    _grid_word, _grid_res, _grid_proc, _vs_res, _vs_proc, _job_mindmap, job_work_views, job_report_views)
from live.insight_focus_board import (  # noqa: F401 · this module keeps answering these names
    BOARD_VIEWS, is_board, _href, _preview, _job_state, _map_word, _plans_grid, _answers, _answering, _canvas,
    _open_proposals, _questions_view, _strip, _job_tasks, _jobs_view, _version_panel, _data_view, _cuts_tabs,
    _draft_handoff, _sign_handoff_row, _handoff_view, BOARD_PARTS, board_report_views, _board_x, _session_of,
    _bw_answers, _bw_questions, _job_steps, _bw_jobs, _bw_data, _bw_handoff, BOARD_PROC, board_work_views)
from live.insight_focus_book import (  # noqa: F401 · this module keeps answering these names
    prototype_parts, prototype_delivery_tabs, prototype_status, prototype_process, prototype_lead,
    prototype_map_branches, prototype_map_top, PROTO_VIEWS, prototype_views, prototype_CAPTIONS)


# ── which view a form belongs to (focus_page.view_items asks; R2, 261106) ──────────────────────────────────────────
def view_of_item(row: dict, folder: Path, root: Path, level: str, keys) -> str | None:
    """The view whose 🙋 Interaction shows a form, by what it is about: at a Board, a Wisdom Task's form under Handoff,
    an Executive one's under Answers, a form about the questions or the data under that view, the rest of its Jobs'
    under Jobs; at a Job, an Executive Task's form under Overall, the rest under Grid; at a Task, under Answer. None
    leaves it to the page's default (the page's own forms under MindMap)."""
    page = Path(row.get("page") or folder)
    topic = row.get("topic")
    about = (getattr(topic, "name", "") or "") + " " + str(row.get("about") or "")
    m = next((P.TASK_NAME.match(p.name) for p in [page, *page.parents] if P.TASK_NAME.match(p.name)), None)
    qid = m.group(1) if m else ""
    if level == "Block":
        if qid[:1] == "W" or re.search(r"handoff|counsel", about, re.I):
            return "handoff"
        if qid[:1] == "X":
            return "answers"
        if page == folder and re.search(r"question|proposal|plan", about, re.I):
            return "questions"
        if page == folder and re.search(r"data|freeze|cut", about, re.I):
            return "data"
        return "jobs" if page != folder else None
    if level == "Job":
        return "overall" if qid[:1] == "X" or page == folder else "grid"
    if level == "Task":
        return "answer"
    return None
