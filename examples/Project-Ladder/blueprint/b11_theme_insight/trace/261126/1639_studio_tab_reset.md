---
title: studio tab reset
date: 2026-11-26 16:39
aim: 'A Studio UI preview''s tab opens at its own address each time it is picked: clicks made inside a view do not carry to the next time it is shown'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261126/1639_studio_tab_reset.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  what: picking a left tab or a top view reloads its frame at its data-studio-src
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests (a studio tabs test)
  what: asserts the reload
changed:
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261126/1639_studio_tab_reset.md
---

# studio tab reset

## Prompts

- **16:39** go ahead and fix them

## Check

- 5623 Chrome: in s11, j02 clicked inside job-rows, job-overview picked, job-rows picked again: back to j03 · Main with the red outline; the same src set again did not reload, so the frame is navigated by location.replace
- pytest workbench/studio: 4 passed

## Summary

Picking a Studio UI preview's tab opens it again at its own address; clicks made in it before do not carry over.

