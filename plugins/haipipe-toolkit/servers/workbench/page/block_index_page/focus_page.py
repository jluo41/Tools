"""Read-only, single-section workbench, selected with layout=focus.

The current folder's face owns Goal, completion criteria and Takeaways. Opening
the page never writes a summary or inherits one from another level.

render() builds the page in named steps (focus_render) on one PageContext (focus_context). The names the focus_*
modules hold are re-exported below, so `F.<name>` callers keep working.
"""
from __future__ import annotations

import datetime as dt  # noqa: F401  re-exported
import json  # noqa: F401  re-exported
import re  # noqa: F401  re-exported
from functools import lru_cache  # noqa: F401  re-exported
import traceback  # noqa: F401  re-exported
import subprocess  # noqa: F401  re-exported
from collections import Counter  # noqa: F401  re-exported
from pathlib import Path
from urllib.parse import quote, urlencode  # noqa: F401  re-exported

import yaml  # noqa: F401  re-exported

from live import frame, page_reader, task_questions, matrix_help  # noqa: F401  re-exported
from live.ui_parts import (COPY_JS, PB_CSS, PB_JS, WORD_CSS, _side_tabs, copy_verb, waits_on_you,  # noqa: F401
                           word_span, icon_label)  # noqa: F401  re-exported
from live import interaction_section as IX  # noqa: F401  re-exported
from live.focus_base import (owned_register, inside, read_face, UI_VIEWS, WORK_SHAPE, page_module, _own, theme_parts, theme_status,  # noqa: F401
    page_url, markdown, report_path, state_label, said_word, tasks_below, count_words, STATE_KINDS, state_kind,  # noqa: F401
    task_tally, one_line, THEMES, page_level, is_run, is_space, holds_projects, holds_blocks, kids, rollup,  # noqa: F401
    descendants, origin, OTHER, in_group, GOAL_WORD, band_title, plural, face_title, state_words, page_title,  # noqa: F401
    job_short, is_topic, topic_home, face_parts, part, first_sentence, document)  # noqa: F401  re-exported
from live.focus_styles_bands import (DC_CSS, FOLD_CSS, FIT_MAP, FRAMED_SCROLL, MAP_PHONE, map_html, STAGE_MARK, BAND_CSS,  # noqa: F401
    band_sec, FINDINGS_CSS, DESIGN_JS, FIT_FRAME_JS, numbered, OPEN_HASH_JS, side_css, RAIL_IX_CSS)  # noqa: F401  re-exported
from live.focus_runs import (RUN_SHOW, RUN_BIG, _read, _run_file, _values_of, run_order, _yaml, ref_link,  # noqa: F401
    RUN_USE_CASE, run_identity_html, data_card, data_card_html, run_document, _file_kind, run_url, RUN_MARK,  # noqa: F401
    run_rows, _yaml_status, run_goal, STAGE_WORD, run_headline, output_run, mark_word, csv_table, table_section,  # noqa: F401
    run_files, headline_section)  # noqa: F401  re-exported
from live.focus_ui import (ui_base, ui_kind, ui_matrix_html, ui_structure_html, ui_walk_path, ui_walk_checklist,  # noqa: F401
    ui_view, ui_sections, home_section, ui_todo)  # noqa: F401  re-exported
from live.focus_interactions import (interactions, card_interactions, INTERACTION_STATE, interaction_topic, known,  # noqa: F401
    page_interactions, interaction_button, answer_link, interaction_items, interaction_item, asked_where,  # noqa: F401
    interaction_where, standard_interactions)  # noqa: F401  re-exported
from live.focus_reports import (question_cards, reports_html, overview_report_html, deliverables_html, report_states,  # noqa: F401
    VERBS, OLD_KEYS, OLD_VIEWS, blocks_under, all_questions, LEAD, WAITS, TOPIC_ANSWER, topic_answer, first_answer,  # noqa: F401
    overview_summary, themes_view, THEME_TITLES, THEME_ORDER, theme_title, BLOCK_WORD_MARKS, block_mark,  # noqa: F401
    blocks_under_projects, VIEW_WORDS, answer_stage, status_view)  # noqa: F401  re-exported
from live.focus_tree import (output_of, picture_of, kid_row, PARTS, part_verbs, work_root, kid_group, FAMILY_MIN,  # noqa: F401
    task_families, family_words, fold_tree, status_html)  # noqa: F401  re-exported
from live.focus_studio import (topic_rows, studio_none, studio_html, log_events, TIMELINE_MAX, timeline_events,  # noqa: F401
    KIND_WORDS, kind_count, timeline_html, folder_html, related_html)  # noqa: F401  re-exported
from live.focus_delivery import (own_delivery_tabs, live_page_blocks, live_pages_html, block_delivery_part,  # noqa: F401
    delivery_sources, delivery_html, PICTURES, delivered_picture, DELIVERY_LANES, delivery_tabs, service_section,  # noqa: F401
    PIECE_STATE, READ_AS_TEXT, readable, topic_delivery, rendered_region, delivery_document, delivery_views,  # noqa: F401
    views_bar)  # noqa: F401  re-exported
from live.focus_themes import (is_draft, page_skills, _draft_css, draft_parts, draft_branches, paper_delivery,  # noqa: F401
    paper_look, paper_delivery_views, paper_board_report, paper_board_work, paper_version_work, paper_version_report,  # noqa: F401
    paper_job_views, view_items, insight_job_work, insight_board_report, insight_views_for, design_views,  # noqa: F401
    VIEW_SKILLS, TYPE_SKILLS, type_skills)  # noqa: F401  re-exported
from live.focus_mindmap import (part_document, ANSWER_PILL, LADDER_NAME, parts_mindmap, ladder_words,  # noqa: F401
    mindmap_document)  # noqa: F401  re-exported
from live.focus_findings import (FOUND_STAGE, task_reading, work_paths, answer_state, finding_item, value_sections,  # noqa: F401
    display_sections, design_sections, map_sections, findings_board, task_values, output_sections, display_rows,  # noqa: F401
    job_findings)  # noqa: F401  re-exported
from live.focus_plan_results import (runs_section, studio_section, tasks_section, steps_word, answer_verb, work_process,  # noqa: F401
    work_views, job_progress, JOB_USE_CASE, job_type, job_row, band_board, status_now_html, state_lead)  # noqa: F401  re-exported
from live.focus_identity import (TASK_USE_CASE, TYPE_TABLES, type_use_cases, plain_type, page_type,  # noqa: F401
    page_identity_html, job_identity_html)  # noqa: F401  re-exported
from live.focus_shell import (rail_url, static_page, rail_kids, rail_link, page_shell)  # noqa: F401  re-exported
from live.focus_render import (page_route, report_view_map, work_view_map, rail_sections, section_body,  # noqa: F401
    around_work, left_rail, crumbs_goal_source, page_document)  # noqa: F401  re-exported


def render(theme, root: Path, folder: Path, section="", group="", *, files_panel=False, panel="") -> str:
    """One page: path, name and goal on top; five sections on the right rail, each with its verb (hai-ui):
    Overview read · Work do · Studio think (its groups under it) · Delivery hand over · Related take in."""
    root, folder = root.resolve(), folder.resolve()
    if not inside(folder, root):
        raise ValueError("Folder outside root")
    if is_topic(folder):                             # an old sNN link (the server answers it with a 302 first)
        home = frame.esc(topic_home(folder, root))
        return document(folder.name, f'<meta http-equiv="refresh" content="0;url={home}"><a href="{home}">{frame.esc(folder.name)}</a>')
    if is_run(folder):                               # a Run opens as its Run page, wherever the link came from (JL 261108:
        return run_document(folder, root)            # "it should be something like showing the content or the run")
    panel = panel or ('files' if files_panel else '')  # a right-rail section alone, for the side pane (focus_shell)
    if section == 'files' and not panel:             # Files lives only in the side pane, never as a page: an old
        section, group = '', ''                      # link lands on the page and focus.js opens Files beside it
    ctx = page_route(theme, root, folder, panel or section, group)
    # The panel reuses the Files section without a second shell or navigation.
    report_view_map(ctx)                             # the Report's views
    work_view_map(ctx)                               # the Work's views (they read ctx.inbox only when built)
    rail_sections(ctx)                               # Delivery, Related, Interactions, Know, and the right rail
    section_body(ctx)                                # the open section: its view, body, heading and bar
    if panel:
        from live import focus_scope                 # 📁 the page's own folder marked, the rest faded (JL 261125)
        return document(panel, f'<main class="files-panel-content focus-content">{ctx.body}</main>'
                        + (focus_scope.assets(folder, root) if panel == "files" else ""))
    around_work(ctx)                                 # 🧭 Around the Work under a shared frame's Report
    from live import section_eval                    # each numbered section's ★ AI readability on its bar (JL 261114)
    from live.page_once import once                  # each shared style and guarded script sent once (JL 261125)
    return once(section_eval.mark(page_document(ctx), folder))   # the shell, both rails, the path and the goal


def __getattr__(name: str):
    """Names that moved to project_page still answer here, so old callers keep working."""
    if name.startswith("__"):                        # `from live.focus_page import X` asks for __path__ first
        raise AttributeError(name)
    from live import project_page
    if name in project_page.__all__:
        return getattr(project_page, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
