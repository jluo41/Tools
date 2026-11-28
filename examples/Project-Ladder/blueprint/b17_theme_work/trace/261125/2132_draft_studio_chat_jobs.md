---
title: draft studio chat jobs
date: 2026-11-25 21:32
work: [j13, j14, j15, j13t01, j13t03, j13t04]
aim: "workbench-task-draft/ and studio/ split into module folders, one per Task: j14 Draft Lab (7 Tasks) takes over j13 t03; j13 becomes Studio and Guide (t01 tabs, t02 guide, t04 canvas); j15 Chat and terminal (t01 chat, t02 terminal) takes chat and the terminal out of studio/. live.<module> names stay flat."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2132_draft_studio_chat_jobs.md
    what: this trace's own record, written first
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/j14_draft_lab/
    what: Job face and Tasks t01 page shell, t02 plan and outline, t03 evidence steps, t04 revise steps, t05 run views, t06 delivery and export, t07 reader; a run-check Run each
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/j15_chat_terminal/
    what: Job face and Tasks t01 chat, t02 terminal; a run-check Run each
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/j13_workbench_tools/
    what: title Studio and Guide; t01 owns studio/tabs/; t03 superseded by j14; new t04 canvas with its run-check Run
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/page_shell/
    what: from workbench-task-draft/ (19 files, focus_draft*, task_draft, space_views*, draft_steps*, small helpers, board_checks)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/plan_outline/
    what: from workbench-task-draft/ (21 files, outline*, draft_step_plan)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/evidence_steps/
    what: from workbench-task-draft/ (16 files, evidence*, draft_step_evidence*, draft_step_cite_items, value)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/revise_steps/
    what: from workbench-task-draft/ (7 files, draft_step_revise*, draft_rubric)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/run_views/
    what: from workbench-task-draft/ (15 files, runs*, pageruns, plugview*, folderstat)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/delivery_export/
    what: from workbench-task-draft/ (8 files, delivery, export*, focus_draft_delivery); exporters/ stays beside it
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/
    what: from studio/ (studio_tabs, api_proxy)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/studio/canvas/
    what: from studio/ (xcal, xcal_linked, xcal_outline, excalidraw_proxy, autodraw, autodeck)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/chat_drawer/
    what: from studio/ (chat*, turnring)
  - do: move
    path: plugins/haipipe-toolkit/servers/workbench/terminal/
    what: from studio/ (term, term_pty, term_ws)
  - do: edit
    path: plugins/haipipe-toolkit/servers/_host/host_registry.py
    what: BASE_GROUPS gains studio/tabs, studio/canvas, chat_drawer, terminal; a Task type folder's module folders (TASK_GROUPS) are live folders
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/README.md
    what: the Folders table gains j13 t04, j14 and j15 rows
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/
    what: one level deeper where a moved module finds files from its own path (excalidraw_proxy, draft_steps_common, draft_rubric, export_common), and the text sweep of old paths in docs, tests and code
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2132_draft_studio_chat_jobs.md
  - examples/Project-Ladder/blueprint/b17_theme_work/j14_draft_lab/ (face, t01 to t07, a run-check Run each)
  - examples/Project-Ladder/blueprint/b17_theme_work/j15_chat_terminal/ (face, t01, t02, a run-check Run each)
  - examples/Project-Ladder/blueprint/b17_theme_work/j13_workbench_tools/ (face, t01, t03 superseded, t04 canvas)
  - plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/ (86 modules into 6 module folders)
  - plugins/haipipe-toolkit/servers/workbench/studio/ (19 modules into studio/tabs, studio/canvas, chat_drawer, terminal)
  - plugins/haipipe-toolkit/servers/_host/host_registry.py
  - plugins/haipipe-toolkit/servers/workbench/README.md
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/frame_tasks.py (a Task type's layout found in a module folder)
  - plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/guide/guide.yaml (presenter: plan_outline/outline.py)
  - excalidraw_proxy.py, draft_steps_common.py, draft_rubric.py, export_common.py (one level deeper)
  - 3 reader tests and test_board_registered_page.py (import paths)
  - 166 old paths in 90 files rewritten (references/ left alone)
---

# draft studio chat jobs

## Prompts

- **21:00** [Image #5] who are taking care of this? I think we can have many or more module foder to manage it as well, how do you propose the job and tasks.
- **21:15** [Image #6] for te studio and chat, I wnat to seperate them as well. plesae think what is the job and task for it.
- **21:30** yes, please go ahead and do them accordingly
- **21:31** I agree, and you just go ahead to update them.

## Check

- Tests, before and after: _host 152, workbench 243, paper 112, work 62, design 58, labeling 85, insight 69, exporters 20, hai-draft 1009, hai-draft-workflow 19 passed; failures the same set before and after (reader 6, hai-draft 3).
- Size: no moved file over 700 lines (largest draft_step_revise.py, 570).
- Live: 5623, 5602, 5607 and 5599 restarted; a draft Task page and its outline, runs, delivery, evidence and folderstat routes return 200 with no traceback; logs show no new error.
- new_job.py check: j13, j14, j15 agree with their Task folders. folder_icons_check.py: 0 problems.

## Summary

workbench-task-draft/ is six module folders plus reader/, one per j14 Task; studio/ is tabs/ and canvas/ (j13 t01, t04) and chat_drawer/ and terminal/ moved beside it (j15). host_registry lists them all as live folders, so every live.<module> name is unchanged.
