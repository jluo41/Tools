---
title: ui preview type
date: 2026-11-26 09:50
work: [s11, j13t01]
aim: "A UI preview is a Studio topic type (Delivery type: ui): its page lists its views; a live view is the page the server renders over a real example Block, a quick view is an html in delivery/ui/ for what the code cannot draw yet, faded (old) once the design is in the code. Each theme keeps one example Block, made by the scripts, holding every state."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0950_ui_preview_type.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-contract.md
    what: a one-line pointer to ref/ui-preview-topic.md where its section was; and in Numbering a row for s99, the Block's own Guide, one per Block, always last
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/ui-preview-topic.md
    what: the UI preview topic type in its own ref; its folder, Page (live views) and Effect (quick views), when a quick view fades, the example Block, s99, its check
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
    what: lists ref/ui-preview-topic.md in its file tree and beside the topic-contract pointer
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
    what: article A08, a page design is looked at on an example Block's live page, with its Rule, Check and Run
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A08-preview-on-example-block.md
    what: the case that raised it (s11's Topic rows drawn by hand, its data a snapshot) and the fix
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/ui_preview_check.py
    what: every Delivery type ui topic has at least one live view; a quick view whose design is in the code is marked old
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/hai-block/ref/board-contract.md
    what: example Blocks, one per theme, scaffolded by new_board.py, new_job.py and soft_run.py, holding every Job and Task state; no real work in them
  - do: edit
    path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/SKILL.md
    what: the work theme's example Block is examples/Project-Ladder/work/b01_example_work
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/s99-guide-view/
    what: the Block Guide view's UI preview topic, its face, its page with one quick view, delivery/ui/guide.html
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0950_ui_preview_type.md
  - plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-contract.md
  - plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/ui-preview-topic.md
  - plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A08-preview-on-example-block.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/ui_preview_check.py
  - plugins/haipipe-toolkit/skills/1_base/project/hai-block/ref/board-contract.md
  - plugins/haipipe-toolkit/skills/2_work/work/workbench-work/SKILL.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s99-guide-view/ (s99-guide-view.md, s99-guide-view.html, delivery/ui/guide.html)
---

# ui preview type

## Prompts

- **09:45** How do we call this type of sNN? Job-Task-UI-Preview. I think we also need to make it as a type, right? what skills you think you might want to update it so we can things to follow?
- **09:50** okay, yes, can I see your plan in the folder panel?

## Check

- Live views sit under Studio's Page and quick views under Effect (correction relayed while working); written into topic-contract.md, A08 and the s99 face; studio_tabs.py left to the session that draws it.
- ui_preview_check.py runs: 84 UI preview topics under examples/, 83 problems; only s11-work-job-preview passes. Most older topics have no page at all; s31-files-pane and b11's s11 have pages with only quick views; s99-guide-view owes its live view until the Guide section is in the code. No other topic edited.
- folder_icons_check.py: this trace passes; the one problem left is 2147_ui_means_one_thing (b10 removed by another session).
- 5623 serves s99-guide-view.html and delivery/ui/guide.html (200); b17's Studio page lists s99-guide-view.
- The UI preview type moved into its own ref, hai-studio/ref/ui-preview-topic.md (57 lines); topic-contract.md keeps a one-line pointer and the s99 row; SKILL.md, A08, its report and board-contract.md point at the new ref; no link to the old section is left (grep).
- The trace's front matter loads with yaml.safe_load.

## Summary

A UI preview is now a written Studio topic type (hai-studio ref/ui-preview-topic.md, hai-ui A08 with ui_preview_check.py, example Blocks in board-contract.md), and s99 is the Block's own Guide slot. s99-guide-view previews the 🧭 Guide section over b01_example_work as a quick view, waiting for JL before any server code.
