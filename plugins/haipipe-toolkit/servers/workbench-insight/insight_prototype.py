"""A Question Book's own parts on the shared work page (b11 design loop round 1, 261106: "a Prototype is insight's"). A
Question Book Block (`board-kind: prototype`) holds the questions and their scripts, one Job per release; the shared page
asks insight_focus.prototype_parts for its Findings parts (before 📦 Delivery) and insight_focus.prototype_status for
its Status bars, both here:

  Findings  the questions in words with their scripts, a side tab per release (Block) or per DIKW level (a release);
            then the proposals and the segments, a side tab each.
  Status    each release by its mark (✅ once a person signed it, ⬜ until then; what waits on the person is a 🙋 line),
            each question by question.md and its Runs ("agreed · script reviewed"); a question its Runs, each verdict.

[(title, word, html, waits)] each, a title plain words. Read-only: nothing here writes."""

from __future__ import annotations

from live.insight_prototype_facts import (  # noqa: F401 · this module keeps answering these names
    ORDER, LEVEL, RUN_WORDS, CSS, block_of, _proto, _verdict, _newest_pass, _soft, _computes, _scripts, _done,
    q_state, q_word, _ready, r_word, _closed_r, tally_word, _release_of, _label, _proposals, _p_word, _focus,
    KIND_WORD)
from live.insight_prototype_parts import (  # noqa: F401 · this module keeps answering these names
    _q_row, _by_level, _level_word, _questions_by_release, _questions_newest, _version_part,
    _questions_by_level, _proposals_part, _cuts_part, parts)
from live.insight_prototype_status import (  # noqa: F401 · this module keeps answering these names
    _row, _open_btn, _q_rows, _release_runs, _release_waits, _share, status, _task_status, delivery_tabs,
    FILE_WORDS, _handed, _cap, lead, _status_line, _findings_line, _is_open, _skill, _li, _next_step, process,
    map_branches, map_top)
