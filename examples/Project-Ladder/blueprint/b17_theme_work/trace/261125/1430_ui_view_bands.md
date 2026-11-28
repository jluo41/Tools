---
title: ui view bands
date: 2026-11-25 14:30
aim: A Block UI · Job UI · Task UI · Run UI view groups its folds under bands like Main (🧩 Elements, 📐 Design, 🖥️ Pages, 🔍 Review), each band numbering from 1.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1430_ui_view_bands.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/focus_ui.py
    what: ui_view hands ui_sections bands of folds; ui_sections draws each band as a work-section-group with its h2
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
    what: a UI view's Review rounds open their own 🔍 Review band, numbered from 1
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1430_ui_view_bands.md
  - plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/focus_ui.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_ui_views.py
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/focus_scope.py
---

# ui view bands

## Prompts

- **14:30** for things here, we should have the band as well, right? [the Block UI view: 1 · Elements · Work Block ... 9 · Review rounds, all one flat list]
- **14:50** (relayed by Chat-Block-Folder-Icon) the grey titles in Files often repeat the folder name (j01_work_ladder_contract "Work ladder contract").

## Check

- 5623 b17 Block UI: 🧩 Elements 1-4 (Work, Blueprint, Collaboration, Inquiry Block), 📐 Design 1-2, 🖥️ Pages 1-2, 🔍 Review 1 plus 🙋 Interactions; no page reload on the switch.
- workbench 230, labeling 85 pass (two asserts moved from `2 · 🖥️ The page, live` to the bands and `1 · ...`).
- 14:50: `focus_scope.adds` keeps a grey title only when it adds words; j01/j02/j03/s01 now hover only, t01/t03/s02-s05 keep theirs; seen on 5623 j01 Files; workbench 230.
- Later the same day Chat-Block-Folder-Icon removed the grey titles at JL's word ("this will be hover over"); they live in `side_pane/files_tree/file_info.py`'s hover card now, so `adds()` is gone.

## Summary

`focus_ui.ui_view` hands `ui_sections` named bands; each band is a `work-section-group` with its h2, as in Main, and
numbers from 1. The fold titles drop their `🧩 Elements ·` prefix because the band names it. `work_process` puts a UI
view's Review rounds in their own 🔍 Review band.
