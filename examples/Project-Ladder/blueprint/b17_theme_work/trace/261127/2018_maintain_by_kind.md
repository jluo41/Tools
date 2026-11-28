---
title: maintain by kind
date: 2026-11-27 20:18
topic: s31-files-pane
aim: 'The Files pane shows what the Block maintains as one part per kind (Maintain: ServerUI, Maintain: Skills, Maintain: Block-Example, Maintain: Blueprint Blocks), each numbering its own rows; the example Blocks leave Read-From, and another blueprint Block a trace touched leaves Touch.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2018_maintain_by_kind.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
  what: Maintain split by kind; examples move out of Read-From
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  what: the blueprint Blocks this Block's traces touched
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_role_parts.py
  what: the new parts
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_trace_view.py
  what: a touched blueprint Block is found
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_work_frame.py
  what: Maintain headings by kind
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/folder_icons_check.py
  what: accept Maintain parts by kind
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  what: Maintain parts by kind
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A06-real-folders-in-parts.md
  what: the parts table
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
  what: 'Decided: Maintain by kind'
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2018_maintain_by_kind.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_role_parts.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/tests/test_trace_view.py
- plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_work_frame.py
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/folder_icons_check.py
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A06-real-folders-in-parts.md
- examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
---

# maintain by kind

## Prompts

- **20:18** ok

## Check

- files_tree tests: 22 passed (one new: one part per kind, each numbered from one, an untouched blueprint Block left out, a work Block has none); test_work_frame.py: 27 passed
- Live Files panel of b17 on 5623, driven in Chrome: Block, Maintain: ServerUI (2 rows under plugins/haipipe-toolkit/servers/), Maintain: Skills (5 rows), Maintain: Block-Example (4 rows), Maintain: Blueprint Blocks (b11, b12, b15, b16), Touch; no Read-From, as b17 waits for no Block and has no local data; b11_theme_insight expands and its traced file is marked in place
- folder_icons_check.py --url http://127.0.0.1:5623: no problem on the Files parts; its 12 problems are other traces

## Summary

What the Block maintains is now one part per kind, each numbering its own rows: ServerUI, Skills, Block-Example and Blueprint Blocks (and OneDrive when declared). The example Blocks left Read-From, which keeps the Blocks it waits for and local data; another blueprint Block that this Block's traces planned or changed is one row under Blueprint Blocks, its files marked in place, and no longer a list of loose paths under Touch.

