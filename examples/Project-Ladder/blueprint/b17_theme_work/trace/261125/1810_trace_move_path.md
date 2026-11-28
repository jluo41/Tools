---
title: trace move path
date: 2026-11-25 18:10
work: [j12t01]
aim: "A trace's do: move line names the file's new place in path: and the old one in what: (from <old>), so a closed move leaves no ghost + rows in the Files pane; the A07 check reports a closed trace whose move path is not on disk."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1810_trace_move_path.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
    what: A07 Rule and Check gain the move line (path new, what from old; a closed move's path exists)
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A07-trace-plan-and-states.md
    what: the case that raised it (1748_page_subfolders, 78 ghost rows) and the fix
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/folder_icons_check.py
    what: "a closed trace's do: move path that is not on disk is a problem"
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1810_trace_move_path.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A07-trace-plan-and-states.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/folder_icons_check.py
---

# trace move path

## Prompts

- **18:06** [Image #2] will the things be clean here? or it will still be put here? what is your thougths?
- **18:10** what is the next sstep? I agree, pleae go ahead and move on.

## Check

- folder_icons_check.py: this trace and 1748_page_subfolders pass; the one problem left is 1751_jobs_flat_or_topics.md (another session's, no front matter).
- The guard catches the case: 1748's plan rebuilt with the old paths reports all 78 move lines.
- 5623's Files pane data for b17 has no missing (+) entry.

## Summary

A07 now says how a move is written: the new place in path:, from <old> in what:. The check fails a closed trace whose move path is not on disk, so the 78 + rows of 1748 cannot come back unseen.
