---
title: ui preview kinds
date: 2026-11-26 10:16
work: [s11]
aim: "A UI preview topic names its kind on its face (UI preview line): Job UI Preview (s11, a Job and its Tasks over work/b01_example_work), Cowork UI Preview (s12, over cowork/b01_example_cowork) and Discovery UI Preview (s13, over discovery/b01_example_discovery); b17's examples line names all three Blocks."
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261126/1016_ui_preview_kinds.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/ui-preview-topic.md
    what: a Kinds section (Job, Cowork, Discovery, each with its example Block) and the face's UI preview line
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: UI preview line, Job
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/s12-cowork-job-preview/
    what: Cowork UI Preview by new_topic.py (over the limit, as JL asked), Page the live cowork example Block and one Job
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/s13-discovery-job-preview/
    what: Discovery UI Preview by new_topic.py (over the limit, as JL asked), Page the live discovery example Block, one Job and one Task
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/board.md
    what: the examples line adds cowork/b01_example_cowork and discovery/b01_example_discovery
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261126/1016_ui_preview_kinds.md
  - plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/ref/ui-preview-topic.md (a Kinds section)
  - blueprints/Project-Ladder/work/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md (UI preview, Job)
  - blueprints/Project-Ladder/work/b17_theme_work/s99-guide-view/s99-guide-view.md (UI preview, Guide)
  - blueprints/Project-Ladder/work/b17_theme_work/s12-cowork-job-preview/
  - blueprints/Project-Ladder/work/b17_theme_work/s13-discovery-job-preview/
  - blueprints/Project-Ladder/work/b17_theme_work/board.md (examples line)
---

# ui preview kinds

## Prompts

- **10:14** I think you shoud also have other sNN for the UI preview. I think we should just call it Job UI Preview. we will have the new sNN for blueprints/Project-Ladder/cowork/b01_example_cowork and blueprints/Project-Ladder/discovery/b01_example_discovery do you get what I mean? we might have other UI preview example, but they are different from the Job UI Preview, do you get it?
- **10:16** go

## Check

- s12 and s13 made by new_topic.py with --over-limit (b17 now holds 10 topics; JL asked for both).
- Each live page they show returns 200 with no traceback: the cowork Block and its j01, the discovery Block, its j01 and that Job's t01.
- b17's Studio: s11 Page, Effect, Draw, Delivery; s12 Page (2 live views), Draw, Delivery; s13 Page (3 live views), Draw, Delivery.
- ui_preview_check.py on b17: s11, s12, s13 pass; the problems left are older topics with no page and s99-guide-view, whose live view waits for the Guide section.
- s99-guide-view's face also names its kind (UI preview, Guide), as the Kinds table lists it.

## Summary

A UI preview names its kind: Job (s11 over work/b01_example_work), Cowork (s12 over the cowork example) and Discovery (s13 over the discovery example), each a topic of its own with live pages under Page; b17's Files pane lists the three example Blocks.
