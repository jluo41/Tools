"""Goal, Plan, Execution and Results over existing work records.

A Block opts in with workbench-layout: workflow. Reading never creates plans,
changes Run status, or infers goal acceptance from completed execution counts.

The code lives in its parts; this module keeps every name importable as
`live.work_progress.<name>`:
- work_progress_records.py: faces, Run records, states, roles
- work_progress_html.py: links, cards, nodes, marks, tables, page scripts
- work_progress_deliverables.py: the Goal tree of deliverables
- work_progress_background.py: ## Background and its timeline drawings
- work_progress_about.py: the Job and Task pop-out pages
- work_progress_runs.py: Run tables and trees
- work_progress_views.py: Goal, Plan, Execution, Results and spaces()
- work_progress_browse.py: one Run's page and the set browser
"""
from live.work_progress_records import (  # noqa: F401
    VIEWS, MODES, PURPOSES, e, _LOADER, _READ,
    _TTL, read_yaml, top_level, kept, receipt_of, summary_line,
    said_of, text_of, section, face_fields, enabled, goal,
    task_folders, first_line, _RECORDS, records, _records, snapshot,
    show, moment, elapsed, location, plan_data, clock,
    ROLES, ROLE_ORDER, role_of, STATE, state_of, last_finish,
)
from live.work_progress_html import (  # noqa: F401
    TICKS, TREE_CSS, TREE_TOOLS, mark, chip, run_mark,
    means_html, node, address, run_link, nav, source_link,
    counts, runs_n, part, card, RUN_MARKS, RUN_LEGEND,
    run_tally, ZOOM, REFRESH, IMAGES, TEXTS, file_url,
    csv_preview, CSVP_CSS, NUMBER, rows_table,
)
from live.work_progress_deliverables import (  # noqa: F401
    SPACE_DIRS, deliverables, task_of, run_of, item_state, group_state,
    written, makers, short_folder, fast_rel, file_lines, run_line,
    batches, example_section, picture_of, open_link, details_box, item_node,
    items_nodes, tally, level_head, task_nodes, job_about, task_about,
    browse_url,
)
from live.work_progress_background import (  # noqa: F401
    background_md, timeline_svg, rule_parts, timeline_parts, background_html,
)
from live.work_progress_about import (  # noqa: F401
    topic_pictures, job_drawing, render_task_about, render_about,
)
from live.work_progress_runs import (  # noqa: F401
    child_rows, LEGEND, run_rows, run_node, role_nodes, task_pictures,
    task_run_node, status_tree, hot_runs, status_cards,
)
from live.work_progress_views import (  # noqa: F401
    goal_cards, studio, goal_view, plan_view, execution_view, results_view,
    status_board, spaces,
)
from live.work_progress_browse import (  # noqa: F401
    parquet_rows, data_tables, data_section, outputs, _parquet, fact,
    render_browse, render_run,
)
