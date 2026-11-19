"""The insight theme's plan-C views: what each Space shows at the Board, a Job and a Task (b11 s11 · s12 · s13).

Drawn from the folders (insight_plan_c.py) in the base's look only: .topic folds, .wf-table, the q-row
Question │ Work │ Report rows, .chip, .st-ok / .st-warn, and the frame's own tab row (.row.subs .tab) for a
Space's second row of buttons. A Space with two dimensions (Segment × Reading at the Board, Segment ×
Period at a Job) keeps the first in the frame's third row and draws the second as a row of the same tabs
under it; `sub` carries both as "<first>/<second>". Read-only: a run type only copies its prompt.

The design's open points (b11 goal spec, "still open") are drawn as nothing: no rule for "held" (the
compare report is shown as its run wrote it), no backfill Job, no stale handoff, Findings the same on
every segment, no automatic re-run, no Board Run pop-out of its own, no Question Book steps in the Guide.
"""

from __future__ import annotations

from live.insight_view_parts import (  # noqa: F401 · this module keeps answering these names
    LEVELS, READINGS, PERIODS, STATUS, OK, QUIET, SKILLS, RUNS, _kind, _CARDS_DIR, _CARDS, ALIAS, run_cards,
    _card_kind, _NEXT, _next_line, _next_now, _carded, _rows, _st, _fold, _chip, run_url, _run_link, page_link,
    open_url, _open, second_row, split, _qwr_head, _qwr, _by_level, _release_links, OPS, _where, WORDS, _label,
    _part_names, _part_key, LEVEL_WORD, MARK, _job_link, _rlabel, _vlabel, WRITTEN, _runs_table, _band,
    RUN_LEVELS, _rtype, _closed, is_written, written_of, page_word, far, mark, _task_link)
from live.insight_view_overall import (  # noqa: F401 · this module keeps answering these names
    STEP, _SPEC, _spec, _leads, _cap, _q_logic, _needs, _goes, _q_work, _takeaway, _q_report, OVERALL, CITE,
    _executive, _sections, _cites, _fig_png, _figure, _overall, _overall_tabs, OV_CSS, _board_overall)
from live.insight_view_board import (  # noqa: F401 · this module keeps answering these names
    board_spaces, _map, _prototype_tabs, _prototype, _dataset, _raw, _version, columns_table,
    _partitions, _questions, newest_task, _cell, _newest_word, _coverage, _tracks, _consistency, _findings,
    _answered, _jobs, _board_runs, _handoff)
from live.insight_view_work import (  # noqa: F401 · this module keeps answering these names
    _cut_table, _job_current, _vs_previous, VS_CSS, _full_answers, _tree, WORK_STEPS, STEP_KEY, OLD_WORK,
    STEP_EMOJI, FINAL, WRITE_ORDER, WRITE_CARD, _work_facts, _work_states, _work_step, _card_prompt, _still,
    _names, _level_card, _page_link, _launch_step, _job_prototype_line, _run_step, _write_step, _check_step,
    _check_form, _compare_step, _close_step, _close_sign, _kv_table, WORK_PARTS, WORK_RUNNING, _work_view,
    _work_kinds)
from live.insight_view_job import (  # noqa: F401 · this module keeps answering these names
    job_spaces, _job_prototype, _job_dataset, _job_runs, _job_delivery)
from live.insight_view_task import (  # noqa: F401 · this module keeps answering these names
    task_spaces, _question, _records, _task_table, _task_reading, _task_parts, render_task_page, render_run_page)
