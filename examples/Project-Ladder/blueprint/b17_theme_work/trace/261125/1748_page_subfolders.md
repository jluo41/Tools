---
title: page subfolders
date: 2026-11-25 17:48
work: [j11t04, j11t01, j11t02, j11t03, j11t05, j12t01, j12t02]
aim: "servers/workbench/page/ is split into one subfolder per Task (j11 t01 to t04 in page/, j11 t05 in home/, j12 t01 and t02 in a new side_pane/), so a file's folder names the Task that owns it; every live.<module> import stays as it is."
closed: true
before: "Chat-Block-Framework and Chat-Block-Folder-Icon have committed their page/ changes and stopped editing page/ until this trace closes (AGENTS.md: split a shared file only when no other session is editing it)."
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1748_page_subfolders.md
    what: "this trace's own record, written first"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_render.py
    what: "from page/focus_render.py (j11 t01); its live.focus_render name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_page.py
    what: "from page/focus_page.py (j11 t01); its live.focus_page name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_shell.py
    what: "from page/focus_shell.py (j11 t01); its live.focus_shell name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_views.py
    what: "from page/focus_views.py (j11 t01); its live.focus_views name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/view_bands.py
    what: "from page/view_bands.py (j11 t01); its live.view_bands name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_base.py
    what: "from page/focus_base.py (j11 t01); its live.focus_base name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_context.py
    what: "from page/focus_context.py (j11 t01); its live.focus_context name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_identity.py
    what: "from page/focus_identity.py (j11 t01); its live.focus_identity name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/frame.py
    what: "from page/frame.py (j11 t01); its live.frame name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/frame_base.py
    what: "from page/frame_base.py (j11 t01); its live.frame_base name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/frame_view.py
    what: "from page/frame_view.py (j11 t01); its live.frame_view name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/frame_nav.py
    what: "from page/frame_nav.py (j11 t01); its live.frame_nav name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/frame_css.py
    what: "from page/frame_css.py (j11 t01); its live.frame_css name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/frame_js.py
    what: "from page/frame_js.py (j11 t01); its live.frame_js name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_styles.py
    what: "from page/focus_styles.py (j11 t01); its live.focus_styles name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_styles_bands.py
    what: "from page/focus_styles_bands.py (j11 t01); its live.focus_styles_bands name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_tree.py
    what: "from page/focus_tree.py (j11 t01); its live.focus_tree name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_standing.py
    what: "from page/focus_standing.py (j11 t01); its live.focus_standing name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py
    what: "from page/focus_jobs.py (j11 t02); its live.focus_jobs name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_runs.py
    what: "from page/focus_runs.py (j11 t02); its live.focus_runs name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_plan_results.py
    what: "from page/focus_plan_results.py (j11 t02); its live.focus_plan_results name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_findings.py
    what: "from page/focus_findings.py (j11 t02); its live.focus_findings name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_delivery.py
    what: "from page/focus_delivery.py (j11 t02); its live.focus_delivery name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_reports.py
    what: "from page/focus_reports.py (j11 t02); its live.focus_reports name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_mindmap.py
    what: "from page/focus_mindmap.py (j11 t02); its live.focus_mindmap name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_interactions.py
    what: "from page/focus_interactions.py (j11 t02); its live.focus_interactions name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/frame_tasks.py
    what: "from page/frame_tasks.py (j11 t02); its live.frame_tasks name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/frame_runs.py
    what: "from page/frame_runs.py (j11 t02); its live.frame_runs name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/frame_work.py
    what: "from page/frame_work.py (j11 t02); its live.frame_work name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/frame_report.py
    what: "from page/frame_report.py (j11 t02); its live.frame_report name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/frame_delivery.py
    what: "from page/frame_delivery.py (j11 t02); its live.frame_delivery name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/runs_panel.py
    what: "from page/runs_panel.py (j11 t02); its live.runs_panel name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/runs_panel_assets.py
    what: "from page/runs_panel_assets.py (j11 t02); its live.runs_panel_assets name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/work_frame.py
    what: "from page/work_frame.py (j11 t02); its live.work_frame name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/work_sections.py
    what: "from page/work_sections.py (j11 t02); its live.work_sections name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/work_items.py
    what: "from page/work_items.py (j11 t02); its live.work_items name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/work_map.py
    what: "from page/work_map.py (j11 t02); its live.work_map name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/element_info.py
    what: "from page/element_info.py (j11 t03); its live.element_info name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/item_address.py
    what: "from page/item_address.py (j11 t03); its live.item_address name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/item_card_route.py
    what: "from page/item_card_route.py (j11 t03); its live.item_card_route name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/item_cards.py
    what: "from page/item_cards.py (j11 t03); its live.item_cards name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/item_marks.py
    what: "from page/item_marks.py (j11 t03); its live.item_marks name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/ladder_cards.py
    what: "from page/ladder_cards.py (j11 t03); its live.ladder_cards name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/tab_cards.py
    what: "from page/tab_cards.py (j11 t03); its live.tab_cards name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/paragraph_cards.py
    what: "from page/paragraph_cards.py (j11 t03); its live.paragraph_cards name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/interaction_section.py
    what: "from page/interaction_section.py (j11 t03); its live.interaction_section name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/section_eval.py
    what: "from page/section_eval.py (j11 t03); its live.section_eval name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/ui_elements_harvest.py
    what: "from page/ui_elements_harvest.py (j11 t03); its live.ui_elements_harvest name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/address_links.py
    what: "from page/address_links.py (j11 t03); its live.address_links name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/ui_parts.py
    what: "from page/ui_parts.py (j11 t04); its live.ui_parts name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/focus_ui.py
    what: "from page/focus_ui.py (j11 t04); its live.focus_ui name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/focus_ui_elements.py
    what: "from page/focus_ui_elements.py (j11 t04); its live.focus_ui_elements name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/focus_themes.py
    what: "from page/focus_themes.py (j11 t04); its live.focus_themes name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/frame_groups.py
    what: "from page/frame_groups.py (j11 t04); its live.frame_groups name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/frame_group_op.py
    what: "from page/frame_group_op.py (j11 t04); its live.frame_group_op name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/matrix_help.py
    what: "from page/matrix_help.py (j11 t04); its live.matrix_help name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/page_reader.py
    what: "from page/page_reader.py (j11 t04); its live.page_reader name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/ui_docs.py
    what: "from page/ui_docs.py (j11 t04); its live.ui_docs name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/space_constitution.py
    what: "from page/space_constitution.py (j11 t04); its live.space_constitution name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/frame_pptx.py
    what: "from page/frame_pptx.py (j11 t04); its live.frame_pptx name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/home/space_home.py
    what: "from page/space_home.py (j11 t05); its live.space_home name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/home/project_page.py
    what: "from page/project_page.py (j11 t05); its live.project_page name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/home/project_face.py
    what: "from page/project_face.py (j11 t05); its live.project_face name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/home/project_findings.py
    what: "from page/project_findings.py (j11 t05); its live.project_findings name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/home/project_branches.py
    what: "from page/project_branches.py (j11 t05); its live.project_branches name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/focus_scope.py
    what: "from page/focus_scope.py (j12 t01); its live.focus_scope name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
    what: "from page/work_files.py (j12 t01); its live.work_files name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/frame_folders.py
    what: "from page/frame_folders.py (j12 t01); its live.frame_folders name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/file_info.py
    what: "from page/file_info.py (j12 t01); its live.file_info name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/file_icons.py
    what: "from page/file_icons.py (j12 t01); its live.file_icons name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
    what: "from page/trace_view.py (j12 t01); its live.trace_view name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/focus_studio.py
    what: "from page/focus_studio.py (j12 t02); its live.focus_studio name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/frame_studio.py
    what: "from page/frame_studio.py (j12 t02); its live.frame_studio name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/frame_related.py
    what: "from page/frame_related.py (j12 t02); its live.frame_related name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/frame_sessions.py
    what: "from page/frame_sessions.py (j12 t02); its live.frame_sessions name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/frame_timeline.py
    what: "from page/frame_timeline.py (j12 t02); its live.frame_timeline name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/frame_spaces.py
    what: "from page/frame_spaces.py (j12 t02); its live.frame_spaces name stays"
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/skills_section.py
    what: "from page/skills_section.py (j12 t02); its live.skills_section name stays"
  - do: edit
    path: plugins/haipipe-toolkit/servers/_host/host_registry.py
    what: "BASE_GROUPS lists the new folders (page/block_index_page ... side_pane/rail_sections) so every live.<module> name stays flat"
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_base.py
    what: "line 417: Path(__file__).parents[N] goes one level deeper (+1)"
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_identity.py
    what: "line 30: Path(__file__).parents[N] goes one level deeper (+1)"
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/frame_related.py
    what: "line 92: Path(__file__).parents[N] goes one level deeper (+1)"
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/skills_section.py
    what: "line 25: Path(__file__).parents[N] goes one level deeper (+1)"
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
    what: "line 89: Path(__file__).parents[N] goes one level deeper (+1)"
  - do: edit
    path: plugins/haipipe-toolkit/servers/_host/tests/test_page_view_routes.py
    what: "line 34: its sys.path entry points at the new folders, not workbench/page"
  - do: edit
    path: plugins/haipipe-toolkit/servers/_host/tests/test_frame_routes.py
    what: "line 102: frame.py sits one level deeper (+1)"
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/README.md
    what: "the folder table: page/ subfolders, side_pane/, each with its Job and Task"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/t01_block_index_page/t01_block_index_page.md
    what: "## Files names its one folder instead of a file list"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/t02_job_task_views/t02_job_task_views.md
    what: "## Files names its one folder instead of a file list"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/t03_element_marks/t03_element_marks.md
    what: "## Files names its one folder instead of a file list"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/t04_parts_and_map/t04_parts_and_map.md
    what: "## Files names its one folder instead of a file list"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/t05_home_and_project/t05_home_and_project.md
    what: "## Files names its one folder instead of a file list"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t01_files_tree/t01_files_tree.md
    what: "## Files names its one folder instead of a file list"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t02_rail_sections/t02_rail_sections.md
    what: "## Files names its one folder instead of a file list"
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1748_page_subfolders.md
  - plugins/haipipe-toolkit/servers/workbench/page/block_index_page/ (18 files moved in)
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/ (19 files moved in)
  - plugins/haipipe-toolkit/servers/workbench/page/element_marks/ (12 files moved in)
  - plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/ (11 files moved in)
  - plugins/haipipe-toolkit/servers/workbench/home/ (5 files moved in)
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/ (6 files moved in)
  - plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/ (7 files moved in)
  - plugins/haipipe-toolkit/servers/_host/host_registry.py
  - plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_base.py
  - plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_identity.py
  - plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/frame_related.py
  - plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/skills_section.py
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
  - plugins/haipipe-toolkit/servers/_host/tests/test_page_view_routes.py
  - plugins/haipipe-toolkit/servers/_host/tests/test_frame_routes.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_work_frame.py
  - plugins/haipipe-toolkit/servers/workbench/README.md
  - examples/Project-Ladder/blueprint/b17_theme_work/j11_workbench_page/ (t01 to t05 ## Files)
  - examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/ (t01, t02 ## Files)
---

# page subfolders

## Folders

```text
servers/workbench/
├─ page/block_index_page/   j11 t01  (18 files)
├─ page/job_task_views/     j11 t02  (19)
├─ page/element_marks/      j11 t03  (12)
├─ page/parts_and_map/      j11 t04  (11)
├─ home/                    j11 t05  (+5 project and space_home files)
├─ side_pane/files_tree/    j12 t01  (6)
└─ side_pane/rail_sections/ j12 t02  (7)
```

## Steps

1. Before: the two sessions commit and stop editing page/.
2. `git mv` each file to its folder, in one change.
3. `_host/host_registry.py` BASE_GROUPS lists the new folders; the five `parents[N]` lines and two host tests move one level.
4. Tests: workbench, _host, paper, design, labeling, insight, work suites through uv.
5. Restart 5623; open b16, b17 and one page of each theme; the 🙋 tray, side pane, Studio and Files tree work.
6. Each Task face's ## Files names its folder; README's folder table matches.

## Prompts

- **17:47** [Image #1] for the page, I want to create the submodules for them, how do you think? How could i map them to the tasks as well? Do you understand what I mean? which jobs and tasks will take care of this?
- **17:48** yes, is this what I want to do. could you make a plan and use the trace? do you know what is the trace, right?
- **17:52** 1748_page_subfolders.md <--- for this, I want to know could you add the job index to it as well, so we know which jNN or jNNtNN, or sNN it is working on, do you get what I mean?

- **17:55** yes, go ahead and doing them.

## Check

- Before: Chat-Block-Folder-Icon replied paused; Chat-Block-Framework was idle with no edit running (message sent, no reply).
- Baseline before the move, through uv: workbench 240, _host 152, paper 112, design 58, labeling 85, insight 69, work 62, all passed.
- After: the same seven suites, all passed (test_work_frame.py needed its focus-assets path one level deeper, which this trace adds as ◆).
- Path text: 904 old `page/<module>.py` mentions in 368 files rewritten to the new folders (references/ and this trace's own path lines left); `git grep` finds none left and no doubled folder.
- 5623 restarted 18:04: b17, b16, j11, a j03 Task, cowork, discovery, paper, Project-Ladder, SPACE Home and the five side-pane panels all 200 with no Traceback; b17's page is the same size as before (2,303,437 vs 2,303,438 bytes).

## Summary

page/ is now one folder per Task: j11 t01 to t04 in page/, t05 in home/, j12 t01 and t02 in side_pane/. `BASE_GROUPS` lists them, so every `live.<module>` import is unchanged; seven depth-based paths moved one level. The README's Folders table and each Task's ## Files name the folder. Not done: a check script that a new file lands in a Task folder (the folders now make it a folder listing).
