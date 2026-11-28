---
title: Page loads faster
date: 2026-11-25 23:59
aim: Each CSS and guarded script block is sent once per page, so the 2.3 MB Block page drops by about half.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2359_page_loads_faster.md
  what: this trace's own record, written first
- do: add
  path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/page_once.py
  what: drop repeated identical style blocks and guarded scripts
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_page.py
  what: run the finished page through page_once
- do: add
  path: plugins/haipipe-toolkit/servers/workbench/tests/test_page_once.py
  what: repeats dropped, unguarded scripts kept
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2359_page_loads_faster.md
- plugins/haipipe-toolkit/servers/workbench/page/block_index_page/page_once.py
- plugins/haipipe-toolkit/servers/workbench/page/block_index_page/focus_page.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- plugins/haipipe-toolkit/servers/workbench/page/block_index_page/tests/test_page_once.py
---

# Page loads faster

## Prompts

- **23:59** what is the good way to make it easier? pelase go ahead and do it. make a plan first?
- **00:12** i also find loading this is also slow, right? maybe by default, the metro map should be hiden.

## Check

- b17 page 2.3 MB to 1.1 MB, 28 style blocks instead of 293
- Files panel 5.6 s to 0.45 s (one git status per page, traces read once)
- workbench tests: 300 passed, 6 failed in the draft reader, failing without this change too

## Summary

Repeated styles and guarded scripts are sent once; the Files panel asks git once per page instead of once per trace.

