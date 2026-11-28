---
title: task health runs
date: 2026-11-25 18:40
work: [j11, j12, j13]
aim: "Each Task of j11, j12 and j13 is a standing quality owner of its folder: it never closes, lists the checks a round runs, and each round is one run-check-<date> Run with its results; the first round is run today."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1840_task_health_runs.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/j11_workbench_page.md
    what: "goal: keep this part healthy; close: when the part is retired; Topic: a Task never closes, one check Run per round"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/j12_side_pane.md
    what: "goal: keep this part healthy; close: when the part is retired; Topic: a Task never closes, one check Run per round"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j13_workbench_tools/j13_workbench_tools.md
    what: "goal: keep this part healthy; close: when the part is retired; Topic: a Task never closes, one check Run per round"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/t01_block_index_page/t01_block_index_page.md
    what: "close: never while its folder lives; a ## Checks section lists what each round runs"
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/t01_block_index_page/runs/
    what: "its standing run-check-<folder> Run and the first pass, today's results"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/t02_job_task_views/t02_job_task_views.md
    what: "close: never while its folder lives; a ## Checks section lists what each round runs"
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/t02_job_task_views/runs/
    what: "its standing run-check-<folder> Run and the first pass, today's results"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/t03_element_marks/t03_element_marks.md
    what: "close: never while its folder lives; a ## Checks section lists what each round runs"
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/t03_element_marks/runs/
    what: "its standing run-check-<folder> Run and the first pass, today's results"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/t04_parts_and_map/t04_parts_and_map.md
    what: "close: never while its folder lives; a ## Checks section lists what each round runs"
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/t04_parts_and_map/runs/
    what: "its standing run-check-<folder> Run and the first pass, today's results"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/t05_home_and_project/t05_home_and_project.md
    what: "close: never while its folder lives; a ## Checks section lists what each round runs"
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/t05_home_and_project/runs/
    what: "its standing run-check-<folder> Run and the first pass, today's results"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t01_files_tree/t01_files_tree.md
    what: "close: never while its folder lives; a ## Checks section lists what each round runs"
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t01_files_tree/runs/
    what: "its standing run-check-<folder> Run and the first pass, today's results"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t02_rail_sections/t02_rail_sections.md
    what: "close: never while its folder lives; a ## Checks section lists what each round runs"
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t02_rail_sections/runs/
    what: "its standing run-check-<folder> Run and the first pass, today's results"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j13_workbench_tools/t01_studio/t01_studio.md
    what: "close: never while its folder lives; a ## Checks section lists what each round runs"
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/j13_workbench_tools/t01_studio/runs/
    what: "its standing run-check-<folder> Run and the first pass, today's results"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j13_workbench_tools/t02_guide/t02_guide.md
    what: "close: never while its folder lives; a ## Checks section lists what each round runs"
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/j13_workbench_tools/t02_guide/runs/
    what: "its standing run-check-<folder> Run and the first pass, today's results"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j13_workbench_tools/t03_draft_lab/t03_draft_lab.md
    what: "close: never while its folder lives; a ## Checks section lists what each round runs"
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/j13_workbench_tools/t03_draft_lab/runs/
    what: "its standing run-check-<folder> Run and the first pass, today's results"
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1840_task_health_runs.md
  - examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/ (face, t01 to t05 faces and runs/run-check-*)
  - examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/ (face, t01 and t02 faces and runs/run-check-*)
  - examples/Project-Ladder/blueprint/b17_theme_work/j13_workbench_tools/ (face, t01 to t03 faces and runs/run-check-*)
  - plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/reader/tests/test_runs_panel.py
  - plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/reader/tests/test_run_family_lists.py
  - plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/reader/tests/test_space_views.py
---

# task health runs

## Prompts

- **18:30** what isthe current status for these tasks and jobs, are they finished or not? I think each tasks focusing more on the quality check and udpating, right? what is your thoughts?
- **18:40** yes, go ahead

## Check

- soft_run.py refused a dated Run name (a soft Run's passes carry the date), so each Task keeps one runs/run-check-<folder> and today is its pass p01-1125.
- Each Task's own tests, found by which live modules a test imports: all pass except: reader/tests lost runs_panel.py (page/ on sys.path), fixed to page/job_task_views in 3 tests (◆); test_standalone_server.py fails 5, the same 5 at HEAD in a worktree; two workbench-paper tests fail only when run alone (order dependence).
- No file in any Task folder passes 700 lines (the largest is 617 lines, in page/block_index_page/).
- page_words.py --running over 301 pages: findings written in j11t04's pass; 19 unread pages are 5599's.
- 5602, 5607 and 5599 serve this repo through Tools -> ../Tools-SPACE and still run the pre-move code; 5602's log shows No module named 'live.work_sections'. Their restart was refused by the permission check here and waits on JL; every pass is `waiting` for it.
- new_job.py check: j11, j12, j13 agree; b17 on 5623 lists the 10 run-check Runs.

## Summary

The 10 Tasks are standing quality owners: close: never while the folder lives, a ## Checks list, one run-check-<folder> Run each with its first pass. Owed: restart 5602, 5607, 5599, then add a pass that marks the live check done.
