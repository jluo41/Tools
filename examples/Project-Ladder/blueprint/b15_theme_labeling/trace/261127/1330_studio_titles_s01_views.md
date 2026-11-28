---
title: Studio titles by band and s01 views as b17
date: 2026-11-27 13:30
topic: s01-labeling-ladder
aim: b15 topic titles start with their band's name (hai-studio A05), the old combined-workflow topics s13 and s32 leave, and s01 to s03 carry the same Structure, Draw and Examples items as b17's s01.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/1330_studio_titles_s01_views.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/s01-labeling-ladder.md
  what: Title "Block Structure: Itemization"; Views lines as b17
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/s02-labeling-workbench.md
  what: Title "Block Structure: Guideline Generation"
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/s03-agent-role.md
  what: Title "Block Structure: Labeling at Scale"
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s41-task-items-procedure/s41-task-items-procedure.md
  what: Title "Task Procedure: Items"
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s42-task-building-procedure/s42-task-building-procedure.md
  what: Title "Task Procedure: Building"
- do: delete
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s13-labeling-task/
  what: Old combined-workflow topic, kept in git at its blueprints/ path
- do: delete
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s32-labeling-element-ui/
  what: Old combined-workflow topic, kept in git at its blueprints/ path
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/board.md
  what: Links to s13 and s32 removed; Structure Studio titles
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/build.py
  what: Examples Folder tree of the example Block; Draw has Folder
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/studio-views.json
  what: Draw and Examples items as b17 s01
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/studio-views.json
  what: Same
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/studio-views.json
  what: Same
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/itemization.html
  what: Regenerated (with guideline.html, scale.html)
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench-labeling/labeling_theme.py
  what: Code comment no longer points at the removed s13 folder
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench-labeling/tests/test_labeling_theme.py
  what: Same comment
---

# Studio titles by band and s01 views as b17

## Prompts

- **13:30** http://100.121.165.84:5623/_board/workbench?path=examples/Project-Ladder/blueprint/b17_theme_work&layout=focus&section=studio check its s01, update yours accofdingly. go

## Check

- topic_titles_check.py on b15: 0 problems (the first run flagged missing band names while b17 was renumbering its Studio Type topics to s70-s79; the rerun passes with no bands: line needed).
- build.py --check passes; the Studio page serves 200; the Examples Folder tree reads b02_labeling_walkthrough as stored. Chrome was not connected, so the page was checked by served HTML only.

## Summary

Five topic titles start with their band name; s13 and s32 removed (kept in git at their blueprints/ paths). s01 to s03 now carry b17 s01's items: Structure three trees, Draw Folder plus two mind maps, Examples the real Folder, Job / Task Organization and Example 1, 2.
