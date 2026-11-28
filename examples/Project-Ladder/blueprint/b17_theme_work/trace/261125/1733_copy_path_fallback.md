---
title: copy path fallback
date: 2026-11-25 17:33
topic: s31-files-pane
aim: Copy path on the file card works over plain http too; when the browser turns its clipboard off, the card copies through a hidden text box, as ui_parts does.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1733_copy_path_fallback.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/file_info.py
  what: Copy path falls back to a hidden text box when the clipboard is off
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/tests/test_file_info.py
  what: the fallback is in the card's script
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1733_copy_path_fallback.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/file_info.py
- plugins/haipipe-toolkit/servers/workbench/tests/test_file_info.py
---

# copy path fallback

## Prompts

- **16:56** the copy does work here. We will new use the un prediefed short name here.
- **16:58** The short name, I mean "A", we cannot read it at the first glance.
- **17:33** what is the plan, and does it relfect in the folder panel?
- **18:00** yes, go ahead and do them.

## Check

- 5623 b17 Files (plain http, no clipboard): right-click a file, Copy path copies its full path through a hidden text box and reads Copied.
- workbench tests: 240 passed; test_file_info asserts the fallback.

## Summary

Copy path on the file card works over plain http too: when the browser has no clipboard, the card copies through a hidden text box, as ui_parts does.

