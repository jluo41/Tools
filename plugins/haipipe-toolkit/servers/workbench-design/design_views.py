"""The design theme's ladder views: what each Space shows at the Block, a Job and a Task (b12 s11 · s12 · s13).

Drawn from the folders (design_reader.py) in the base's look only: .topic folds, .wf-table, the q-row
three-column cards, .st-ok / .st-warn, the frame's tab row (.row.subs .tab); no tags: an id is mono text, its words after
it (b03 s32-D09). A design is shown as it reads, the theme's own element (b12 s32): an SMS as one bubble on a phone, its
{LINK} where the platform puts it; a UI design as its rendered screen (its Task's screens/ PNG).
Every Space is laid out here (`page=True`), so its views and run types are exactly the design's. A Runs-panel
entry is named as its Run is, run-<type>-<target> (hard or soft), and carries its run card's skill, agent,
sign and prompt (haipipe-design-workflow/references/run-cards.md, `<Level> › <Space>`); a Run with no card keeps
the prompt written here. Read-only: a run type only copies its prompt.

What the design leaves open (b12 s11 · s12 · s13, red) is drawn as nothing or "—": tokens while a Run receipt has
no `usage:`. The method registry is read by design_reader (haipipe-design-method/methods/).
"""
from __future__ import annotations

import re  # noqa: F401  (kept for readers of V.<name>, as before the split)
from pathlib import Path  # noqa: F401

from host_paths import skill_dir  # noqa: F401
from live import design_reader as R  # noqa: F401
from live.frame import Space, delivery_view, esc, pop, reader, rel, table, themes  # noqa: F401

# The views live in design_views_<part>.py, one module per part of the ladder; every name stays importable
# from here (design_focus, design_book, design_theme, task_design and the tests read them as V.<name>).
from live.design_views_parts import (  # noqa: F401
    GUIDE_METHOD, OK, WARN, CARDS, _CARD_LINE, _ALIAS, _cache, ladder_cards, card_for, _kind, _rows, _st, _fold,
    _pairs, _open, _ideas_text, _id, TESTS, _test, _qrow, _qhead, _mins, _job_link, _live, _pred, _passed, _cost)
from live.design_views_channel import (  # noqa: F401
    phone, PHONE_LABEL, CARD_LABEL, _ITEM, _DONE, _ANSWER, _parse, _channel_card, checklist_card, _answer_box,
    questionnaire_card, FENCED, words_of, draft_files, as_read, screen_of, as_it_reads)
from live.design_views_disk import (  # noqa: F401
    J, DISK, _disk)
from live.design_views_block import (  # noqa: F401
    B_SKILLS, _bk, block_spaces, _cells, _map, _compare, _goals, _methods, _inputs, _run_state, _preview, _jobs,
    _block_runs, _block_delivery)
from live.design_views_report import (  # noqa: F401
    _MARK, _WORD, _pill, _report_page, _q_status, _q_asks, _q_evidence, _opening, _report_side, _task_work,
    _questions, _costs, _rank1, _approved, _summary, _rounds, _predicted, _scorecard)
from live.design_views_job import (  # noqa: F401
    J_SKILLS, _task_runs, job_spaces, _setup_strip, _md_body, _bullets, _keyed, _ul, _job_goal, _job_method,
    _job_inputs, _file_cell, _reason_ideas, _display, _card, _review_whole, _job_observed, _performance,
    _wd_reason, _wd_conduct, _wd_whole, _job_runs, _approve_panel, _job_delivery)
from live.design_views_task import (  # noqa: F401
    task_spaces, _work, _t00_task, _t00_ideas, _t00_chains, _t99_task, _coverage, _kept, _task_runs_table, _design,
    _evaluation, _tests, _drafts, _task_perf, _elements, _task_delivery)
