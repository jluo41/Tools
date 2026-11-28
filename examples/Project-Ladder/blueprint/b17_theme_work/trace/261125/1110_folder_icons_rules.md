---
title: folder icons rules
date: 2026-11-25 11:10
topic: s31-files-pane
aim: The Files pane's icon and trace rules live in hai-ui's constitution, each with a check that runs.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1110_folder_icons_rules.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
    what: a Folder icons part, one article per rule JL gave
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/folder_icons_check.py
    what: every tree takes its icons and marks from file_icons.py
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A05-one-icon-table.md
    what: report for A05
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A06-real-folders-in-parts.md
    what: report for A06
  - do: add
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A07-trace-plan-and-states.md
    what: report for A07
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1110_folder_icons_rules.md
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1051_trace_view.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/folder_icons_check.py
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A05-one-icon-table.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A06-real-folders-in-parts.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A07-trace-plan-and-states.md
---

# folder icons rules

## Prompts

- **11:10** plese cotninue
- **11:15** the prompt is limited, I think this prompt should be many, right? I asked many things.

## Check

- folder_icons_check.py --url on 5623: 0 problems; a closed trace with an empty Check was caught (tried, then put back).
- constitution.py --check: hai-ui A05, A06, A07 listed with reports.

## Summary

hai-ui CONSTITUTION has a Folder icons part: A05 one icon table, A06 real folders in parts, A07 a trace's
plan and states (open: the hai-chat hook must write prompts and changed:). 1105_trace_view became
1051_trace_view, named for its first prompt, with all 8 prompts.
