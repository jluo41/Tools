---
title: studio no mindmap
date: 2026-11-25 16:25
aim: A Studio fold's top-view has no MindMap button; the topic's .mindmap.md and .mindmap.html stay on disk and in Files.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1625_studio_no_mindmap.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
    what: render no longer adds the MindMap view; the module line says Slide, Draw
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_focus_studio.py
    what: a topic with a .mindmap.md shows no MindMap button
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/ref/top-view-left-tab-right-content.md
    what: the sketch, the parts list and the s31 example drop MindMap
  - do: edit
    path: AGENTS.md
    what: the UI design example list reads (Page, Draw, Delivery)
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1625_studio_no_mindmap.md
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_focus_studio.py
  - plugins/haipipe-toolkit/servers/workbench/ref/top-view-left-tab-right-content.md
  - AGENTS.md
---

# studio no mindmap

## Prompts

- **16:25** I think I can delete the mindmap, it is not that important so far. [Studio s31's MindMap view: one node, "Not written yet."]
- **16:30** okay

## Check

- 5623 b17 Studio: s31's top-view reads Page · Draw · Delivery; no `>MindMap</button>` anywhere on the page; `s31-files-pane.mindmap.md` still on disk. workbench 236.

## Summary

`studio_tabs.render` no longer adds a MindMap view; the files stay. The Report's MindMap band (`view_bands.CORE`) is untouched.
