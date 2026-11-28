---
title: example block names
date: 2026-11-26 11:53
work: [j12t01, s12, s13]
aim: "The example Blocks are named for their theme, cowork/b01_example_cowork and discovery/b01_example_discovery, an old link still opening (renamed-from); the Files pane's Block Examples shows each under its own theme folder."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1153_example_block_names.md
    what: this trace's own record, written first
  - do: move
    path: examples/Project-Ladder/cowork/b01_example_cowork/
    what: from cowork/b01_example_cowork/ (git mv), its face gains renamed-from
  - do: move
    path: examples/Project-Ladder/discovery/b01_example_discovery/
    what: from discovery/b01_example_discovery/ (git mv), its face gains renamed-from
  - do: edit
    path: examples/
    what: every reference to the two old names (about 34 files, b17's face, s12, s13, page-spec, Paper-Example, skills) rewritten
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
    what: examples_tree puts each example under its own theme folder (work, cowork, discovery), opened
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_block_examples.py
    what: examples in two theme folders each show under their folder
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
    what: a Run's bar is no longer one link; only its name opens it, the rest of the bar folds it (asked mid-turn, 11:58)
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_open_rounds.py
    what: the Run's name is the link
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1153_example_block_names.md
  - examples/Project-Ladder/cowork/b01_example_cowork/ (from b01_example_data_request)
  - examples/Project-Ladder/discovery/b01_example_discovery/ (from b01_example_prior_work)
  - 34 files naming the old folders
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_block_examples.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_open_rounds.py
---

# example block names

## Prompts

- **11:52** [Image #30] for these, the three blocks are not happened in the same folder of work, [Image #31] can you check this? I want to make the b01_exapmle_prior_work to tbe b01_example_discovery and examples/Project-Ladder/cowork/b01_example_cowork to be b01_example_cowork, do you get what I mean here?
- **11:58** [Image #32] for this one, how to make that when I click [Image #33], the file will pop out, and for the blank part, we will just collapse and open it? do you get what I mean?
- **11:54** go

## Check

- The old addresses answer 302 to the new ones (renamed-from): cowork/b01_example_data_request to cowork/b01_example_cowork, discovery/b01_example_prior_work to discovery/b01_example_discovery; both new pages 200, no traceback. No file outside references/ names an old folder except the two renamed-from lines.
- b17's Files panel, 4 · Block Examples: work › b01_example_work, cowork › b01_example_cowork, discovery › b01_example_discovery, each under its theme folder; b11's three insight examples keep one base (test_block_examples.py, with one added test).
- Chrome, b01_example_work Jobs, j11 › t01: a click on the blank of run-check-02-name's bar folds it, no viewer; a click on its name opens the Run page and leaves the fold as it was.
- Tests: workbench, _host, workbench-work: the reader's known 6 and the b10 drawing fail; test_work_frame failed once while b11 edited focus_shell.py (11:59) and passes on rerun.
- git's index.lock is from 10:18 with no git writing; left in place for JL (a stale lock blocks every git write here).
- 5623, 5602, 5607, 5599 restarted, 200.

## Summary

The example Blocks are b01_example_cowork and b01_example_discovery, old links still open, and the Files pane shows each example under its own theme folder; a Run's name opens it while the rest of its bar folds it.
