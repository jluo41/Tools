---
title: tests by task
date: 2026-11-25 23:55
work: [j11, j12, j13, j14, j11t01, j11t02, j11t03, j11t04, j11t05, j12t01, j12t02, j13t02, j14t01, j14t03, j14t04]
aim: "workbench/tests/ is split into each Task folder's own tests/, so a Task's run-check runs the folder beside its code; focus_page_fixtures.py stays in workbench/tests/ and the tests that use it find it from any depth."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2355_tests_by_task.md
    what: this trace's own record, written first
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/tests/
    what: from workbench/tests/ (test_focus_faces, test_focus_status_map)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/
    what: from workbench/tests/ (test_focus_findings, test_focus_interactions, test_focus_jobs, test_focus_runs, test_work_frame, test_work_sections)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/tests/
    what: from workbench/tests/ (test_address_links, test_element_info, test_item_cards, test_ladder_cards, test_section_eval, test_ui_elements, test_tab_paragraph_cards)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/tests/
    what: from workbench/tests/ (test_focus_ui_views, test_space_constitution, test_ui_docs, test_page_words)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/home/tests/
    what: from workbench/tests/ (test_project_branches, test_project_ui)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/
    what: from workbench/tests/ (test_file_info, test_trace_view)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/tests/
    what: from workbench/tests/ (test_focus_studio, test_frame_sessions)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/guide/tests/
    what: from workbench/tests/ (test_use_case_examples)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/page_shell/tests/
    what: from workbench/tests/ (test_focus_draft, test_draft_lab_flow_card, test_draft_lab_support, test_draft_lab_title_scores)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/evidence_steps/tests/
    what: from workbench/tests/ (test_draft_lab_cite_cards)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/revise_steps/tests/
    what: from workbench/tests/ (test_draft_lab_split_accept, test_draft_lab_mustcheck, test_note_list_lines, test_review_fix_sentence)
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/
    what: the moved tests that import focus_page_fixtures find workbench/tests/ from their own path; parents[N] one or two levels deeper (draft_lab_support, focus_interactions, page_words, tab_paragraph_cards); old test paths in docs and skills rewritten
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/
    what: each owning Task face's Checks line names its folder's tests/
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/README.md
    what: tests live beside the code they check; workbench/tests/ keeps the shared fixtures
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2355_tests_by_task.md
  - plugins/haipipe-toolkit/servers/workbench/tests/ (33 tests moved into 11 Task folders' tests/; focus_page_fixtures.py stays)
  - 12 moved tests find the shared fixtures from their own path; 5 parents[N] one level deeper (test_trace_view's root was parents[4], plugins/, so its b17 check never ran; now the Tools-SPACE root)
  - 19 Task faces in j11 to j15 (Tests line)
  - plugins/haipipe-toolkit/servers/workbench/README.md and focus-assets/README.md
  - 12 docs and skills with an old workbench/tests/ path (trace and pass records left as they ran)
---

# tests by task

## Prompts

- **23:40** [Image #8] for all the tasks here, how do you think, do we wnat to make them to be with submodules as well?
- **23:55** okay, go ahead and do it.

## Check

- Tests before: workbench/tests 243 passed. After: workbench 300 passed, 6 failed (the reader's known 6); _host 152, workbench-paper 112, workbench-work 62, workbench-design 58 passed; hai-draft 1009 passed, 3 failed (the known test_home 3). The hai-ui route check passes at its new path.
- One run failed test_focus_runs while another session was editing focus_plan_results.py (23:56 to 23:58); it passes alone, from the old folder and in the full rerun.
- No live code changed (a tests/ folder is not a live folder), so no restart.
- folder_icons_check.py: 0 problems.

## Summary

Each Task keeps its tests in its own folder's tests/, so a run-check runs the folder beside the code; workbench/tests/ holds only the shared fixtures.
