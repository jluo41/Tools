---
title: ui means one thing
date: 2026-11-25 21:47
topic: s31-files-pane
aim: 'The word ui names one thing only: a Studio topic''s delivery/ui/ (its UI previews). A theme Block''s page spec moves from ui/ to delivery/page-spec/ (what the Block hands to the code and skills; its Job writes it from its topics'' decisions) in all six Blocks, and the Files pane''s code part is named Code.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2147_ui_means_one_thing.md
  what: this trace's own record, written first
- do: move
  path: examples/Project-Ladder/work/b10_project_workbench/delivery/page-spec
  what: from examples/Project-Ladder/work/b10_project_workbench/ui (git mv)
- do: move
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/page-spec
  what: from examples/Project-Ladder/blueprint/b11_theme_insight/ui (git mv)
- do: move
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/page-spec
  what: from examples/Project-Ladder/blueprint/b12_theme_design/ui (git mv)
- do: move
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/page-spec
  what: from examples/Project-Ladder/blueprint/b15_theme_labeling/ui (git mv)
- do: move
  path: examples/Project-Ladder/blueprint/b16_theme_paper/delivery/page-spec
  what: from examples/Project-Ladder/blueprint/b16_theme_paper/ui (git mv)
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec
  what: from examples/Project-Ladder/blueprint/b17_theme_work/ui (git mv)
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/ui_docs.py
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/focus_ui.py
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/focus_ui_elements.py
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/ui_elements_harvest.py
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_runs.py
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_identity.py
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/ref/focus-views.md
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/tests/test_ui_docs.py
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/tests/test_ui_elements.py
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench-design/tests/test_design_context.py
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench-design/README.md
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/work/hai-work/SKILL.md
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/work/hai-work/ref/update.md
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper/SKILL.md
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/SKILL.md
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/SKILL.md
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-run/SKILL.md
  what: a Block's ui/ is delivery/page-spec/
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
  what: the Files pane part UI is named Code
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2147_ui_means_one_thing.md
- plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/ui_docs.py
- plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/focus_ui.py
- plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/focus_ui_elements.py
- plugins/haipipe-toolkit/servers/workbench/page/element_marks/ui_elements_harvest.py
- plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_runs.py
- plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
- plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_identity.py
- plugins/haipipe-toolkit/servers/workbench/ref/focus-views.md
- plugins/haipipe-toolkit/servers/workbench/tests/test_ui_docs.py
- plugins/haipipe-toolkit/servers/workbench/tests/test_ui_elements.py
- plugins/haipipe-toolkit/servers/workbench-design/tests/test_design_context.py
- plugins/haipipe-toolkit/servers/workbench-design/README.md
- plugins/haipipe-toolkit/skills/2_work/work/hai-work/SKILL.md
- plugins/haipipe-toolkit/skills/2_work/work/hai-work/ref/update.md
- plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/SKILL.md
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/SKILL.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-run/SKILL.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
- plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/page_spec.py
- plugins/haipipe-toolkit/servers/workbench/tests/test_work_frame.py
- plugins/haipipe-toolkit/servers/workbench-labeling/README.md
- plugins/haipipe-toolkit/skills/2_work/work/workbench-work/SKILL.md
- plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
- plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper/scripts/paper_check.py
- examples/Project-Ladder/work/b10_project_workbench/board.md
- examples/Project-Ladder/blueprint/b11_theme_insight/board.md
- examples/Project-Ladder/blueprint/b11_theme_insight/j01_insight_workbench_pages/j01_insight_workbench_pages.md
- examples/Project-Ladder/blueprint/b12_theme_design/board.md
- examples/Project-Ladder/blueprint/b12_theme_design/j01_design_workbench_pages/j01_design_workbench_pages.md
- examples/Project-Ladder/blueprint/b12_theme_design/j01_design_workbench_pages/t01_block_page/s51-block-ui-report/s51-block-ui-report.md
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/page-spec/structure.md
---

# ui means one thing

## Prompts

- **21:47** I think the ui here is confusing, as the sNN aslo have the ui, right? How do you think about it?
- **21:51** how could you call it b17_theme_work/delviery/page-spec? who generate page-spec? the sNN or jNN?
- **22:01** okay, good, if so, plsae update them accordingly

## Check

- git mv ui -> delivery/page-spec in b10, b11, b12, b15, b16, b17 (54 files, uncommitted edits carried); no ui/ spec folder left
- every Block resolves its spec to delivery/page-spec and renders its views table (b10 has project-views only); b11 structure.md relative links fixed, 0 broken
- workbench tests 243 passed, workbench-design 58 passed; 5623 restarted; the Files pane shows 1 · Block, 2 · Code, 3 · Skills
- no plugin or Block face names a spec file under ui/ any more; Chat-Block-Framework and tools-space-ce told

## Summary

The word ui now names one thing, a Studio topic's delivery/ui/ previews. Each theme Block's page spec, what it hands to the code and skills, moved to delivery/page-spec/; the topics decide it, the Job writes it, ui_elements_harvest writes the elements lists, as the new live.page_spec module says. Every reader goes through page_spec.spec_dir(block), which falls back to ui/ only for a Block (in another SPACE) not moved yet. Docs, skills, tests and Block faces name the new path, and the Files pane's server part is named Code.

