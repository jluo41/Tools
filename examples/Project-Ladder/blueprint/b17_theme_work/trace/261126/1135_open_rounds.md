---
title: open rounds
date: 2026-11-26 11:35
work: [j11t02, s11]
aim: "On a Job's Main, a Run row and a round row open in the page's viewer: a round its pass.md, a Run its Run page; and the work example's Task groups and Tasks read as placeholders (Task Group 1, t01 · Task 01 name)."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1135_open_rounds.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
    what: a Task fold's Run row and round rows are data-pop links, a round to its pass.md, a Run to its Run page
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_open_rounds.py
    what: a round row opens its pass.md, a Run row its Run
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/tests/test_focus_status_map.py
    what: its two round and Run rows are links now
  - do: edit
    path: examples/Project-Ladder/work/b01_example_work/
    what: j11's bands Task Group 1 and Task Group 2; every Task's title Task NN name, in its face and its Job's Tasks list
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1135_open_rounds.md
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_open_rounds.py
  - plugins/haipipe-toolkit/servers/workbench/page/block_index_page/tests/test_focus_status_map.py
  - examples/Project-Ladder/work/b01_example_work/ (j11 bands; 15 Task faces and their Jobs' Tasks lists)
---

# open rounds

## Prompts

- **11:30** [Image #25] for this, how do you think I can open the preview content for that run or that pass? what is your thougths?
- **11:34** yes, that is what I want. [Image #26] for the content, how do you think you can make it like Task Group 1, and then t01 to be task 01 name, etc. Just the fake names.

## Check

- Chrome, b01_example_work Jobs, j11 picked: Task groups read 1 · Task Group 1 and 2 · Task Group 2; Tasks t01 · Task 01 name to t12 · Task 12 name.
- A click on a round opens the viewer on that pass's pass.md (first check round: Ask, Summary, Changed); a click on run-check-02-name opens its Run page (what happened, what it made, how it ran, passes p02-1125 and p01-1120).
- test_open_rounds.py passes; workbench tests as before (the reader's known 6 fail) after test_focus_status_map's two rows were made links.
- 5623, 5602, 5607, 5599 restarted, 200. b11's session told the rule before it aligns its previews.

## Summary

A Job's Task folds open their Run and rounds in the page's viewer, a round its pass.md, a Run its Run page; the work example reads as placeholders, Task Group 1 and Task NN name.
