---
title: jobs four rows live
date: 2026-11-25 20:58
topic: s11-work-job-preview
aim: The Block's 💼 Jobs reads as s11's Topic rows preview; four fixed rows, each one line that scrolls sideways with faded edges; row 3 (Main and the Task topics) always shown; row 4 (that topic's Tasks) only once a Task topic is picked; topics named from bands lines.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2058_jobs_four_rows_live.md
    what: this trace's own record, written first
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/scroll_rows.py
    what: the CSS and script of a one-line row (no wrap, sideways scroll, faded edges, mouse drag, picked one in view)
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
    what: four fixed rows; row 3 always; row 4 on a Task topic; remembered Task per topic
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_focus_jobs.py
    what: tests for the four fixed rows
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/board.md
    what: a bands line naming the Job topics
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j*/j*.md
    what: a bands line naming each Job's Task topic
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: the Topic rows preview recorded as taken
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2058_jobs_four_rows_live.md
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/scroll_rows.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_jobs.py
  - examples/Project-Ladder/blueprint/b17_theme_work/board.md
  - examples/Project-Ladder/blueprint/b17_theme_work/j01_work_ladder_contract/j01_work_ladder_contract.md
  - examples/Project-Ladder/blueprint/b17_theme_work/j02_workbench_work_skill/j02_workbench_work_skill.md
  - examples/Project-Ladder/blueprint/b17_theme_work/j03_work_workbench_pages/j03_work_workbench_pages.md
  - examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/j11_workbench_page.md
  - examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/j12_side_pane.md
  - examples/Project-Ladder/blueprint/b17_theme_work/j13_workbench_tools/j13_workbench_tools.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
---

# jobs four rows live

## Prompts

- **20:50** what I want is this version.
- **20:54** I think this one is good [Image] How do you want to implemtn thatm? what is your thougths?
- **20:57** [Image] this is not updated yet. Please rethink about it.

## Check

- workbench tests: 242 passed
- 5623, b17 💼 Jobs, clicked by script: row 1 Workbench · j1N, Earlier design · j0N; row 2 j11 j12 j13; row 3 Main, Page components · t0N; row 4 hidden on Main, shown with t01 to t05 once the topic is picked; t03 remembered after Main; j0N picks j01; rows nowrap, overflow auto
- 620px window: row 4 scrolls (861 wide in 832), its right edge faded; row 2 to row 3 gap 8px

## Summary

The 💼 Jobs section now prints four fixed rows. `scroll_rows.py` holds the one-line row (no wrap, sideways scroll, faded edges, mouse drag, picked one in view); `focus_jobs.py` prints row 1 and row 2 in the bar and rows 3 and 4 in each Job pane, row 4 hidden until a Task topic is picked; b17's board and Job faces name their topics with `bands:` lines.
