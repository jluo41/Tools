---
title: open planned
date: 2026-11-25 15:34
topic: s31-files-pane
aim: A trace still open opens the Files tree down to every file it plans to change, so each one shows with its mark without a click; a planned file outside Block, UI and Skills shows in an Also touched part at the bottom.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1534_open_planned.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
    what: open the folders down to an open trace's files as they load; an Also touched part for files outside the parts
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
    what: hand trace_view the folders each part starts at
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
    what: the open list and the Also touched part
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
    what: s31-D10, planned files open by themselves; s31-D11, Also touched
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1534_open_planned.md
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
  - examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/s31-files-pane.md
---

# open planned

## Prompts

- **15:33** so what files will be changed? are then show in the right panel now>
- **15:34** for the files, if they are about to be changed by this plan, could you explan and show them?

## Check

- 5623 b17 Files: the open traces open s31-files-pane, trace, servers/workbench, page, studio and tests by
  themselves; every planned file shows with its mark. Also touched lists AGENTS.md, hai-ui CONSTITUTION.md, its
  A05 to A07 reports, folder_icons_check.py and two labeling tests, each by its full path.
- First try opened one level only: a folder whose rows are already on the page changes nothing, so reach() now runs
  again after each opening. workbench tests: 235 passed.

## Summary

An open trace opens the Files tree down to every file it plans (s31-D10); a planned or touched file under none of the
parts shows in an Also touched part by its full path (s31-D11). work_files hands trace_view the folders the parts cover.
