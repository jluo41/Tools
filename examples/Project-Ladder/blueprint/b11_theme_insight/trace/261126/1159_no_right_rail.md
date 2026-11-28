---
title: no right rail
date: 2026-11-26 11:59
aim: 'A page has no right rail: the right Sections handle and its drawer go, and the right rail''s list stays in the markup hidden at every width (tests and the element harvest read it); sections are picked from the title''s menu'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261126/1159_no_right_rail.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_shell.py
  what: no right handle, no Sections drawer
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css
  what: the right rail hidden at every width
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_work_frame.py
  what: asserts no right handle and the rail hidden
changed:
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261126/1159_no_right_rail.md
---

# no right rail

## Prompts

- **11:59** ok

## Check

- 5623: Insight-Example's page has no right handle and no Sections drawer; the left Pages handle stays
- pytest workbench/page, workbench-insight, side_pane, workbench-paper, workbench-labeling, workbench-task-draft: 573 passed, 7 failed, none about the rail (6 reader and 1 paper Word test, failing before)

## Summary

A page has no right rail: its handle and Sections drawer are gone and its list is hidden at every width; sections are the title's ▾ menu.

