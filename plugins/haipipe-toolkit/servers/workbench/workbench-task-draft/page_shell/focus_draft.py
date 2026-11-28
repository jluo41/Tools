"""Draft Task content in the common Report frame.

Text, the five drafting steps, Runs, MindMap and Status share one Report surface.
Each step retains draft_steps' editors, prompts and sign actions, under Review
Content. draft_context supplies the standard Around the Work sections. Legacy
Work URLs still select the same step; all writes use the existing handlers.
"""
from __future__ import annotations

import html as _html
import re
from pathlib import Path
from urllib.parse import quote

from live import draft_steps as ds
from live.frame import esc, face, runs_of
from live.ui_parts import GROUP_CSS, WORD_CSS, _numbered, _file_link, _section, _when

# The parts of this module live in their own files; every name still answers here.
from live.focus_draft_words import (  # noqa: F401
    ASKS, CAPTIONS, DRAFT, FOLD, INPUT, LAZY, PROMPT, RUN_PREFIX, SIGN, STATE_WORD, VERBS, WAITS, WIDE, WORK,
)
from live.focus_draft_assets import (  # noqa: F401
    BORROW, CSS, JS, TOKENS, _rules, borrowed_css,
)
from live.focus_draft_steps import (  # noqa: F401
    ASK_STEPS, NO_TEXT, SECTION_VERBS, _after_first_section, _ask, _drop_repeats, _facts, _prompts, _run_rows,
    _runs, _top_sections, bib_section, boxes_of, flatten, input_word, is_draft, quiet, step_html, word, work_views,
)
from live.focus_draft_report import (  # noqa: F401
    CONTENT_CSS, READ_ONLY, REPLY_CSS, STATUS_WHAT, _section_open, aims, answers_line, bib_entries, bib_href,
    content_read, md_tables, now_line, paragraphs, reply_board, report_views, responds_to, review_items,
    review_points, status_html, text_count, text_html,
)
from live.focus_draft_delivery import (  # noqa: F401
    PREVIEW_CSS, READER, SENT, aim, answers_branch, branches, build_prompts, content_branches, delivery_html, parts,
    preview, section_delivery_views, studio_inventory, studio_top,
)
