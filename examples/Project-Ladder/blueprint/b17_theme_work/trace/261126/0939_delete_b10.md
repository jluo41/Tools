---
title: Delete b10
date: 2026-11-26 09:39
aim: b10_project_workbench is removed; its one live part, the Project page spec, moves to b17; every link to b10 becomes plain words.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0939_delete_b10.md
  what: this trace's own record, written first
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/project-views.md
  what: from examples/Project-Ladder/work/b10_project_workbench/delivery/page-spec/project-views.md (with project-preview.html; view-guide.json merged)
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/board.md
  what: takes the ui-project line
- do: delete
  path: examples/Project-Ladder/work/b10_project_workbench
  what: the whole Block, 78 MB
- do: edit
  path: plugins/haipipe-toolkit/servers
  what: b10 paths in docstrings, the guide note, share.py example
- do: edit
  path: blueprints
  what: 'about 90 links in b11 to b17, Project-Packages, Project-PageParts, RandomThoughts: b10 path to words'
- do: edit
  path: examples/Project-Ladder/project.md
  what: b10 row removed
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0939_delete_b10.md
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/project-views.md
- examples/Project-Ladder/blueprint/b17_theme_work/board.md
- examples/Project-Ladder/project.md
- plugins/haipipe-toolkit/servers/workbench/guide/method_canvas.py
- plugins/haipipe-toolkit/servers/workbench/guide/workbench_guide.py
- plugins/haipipe-toolkit/servers/_host/live/share.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/view-guide.json
- examples/Project-RandomThoughts/cowork/meetings/2026-10-10-workflow-design.md
---

# Delete b10

## Prompts

- **09:39** examples/Project-Ladder/work/b10_project_workbench <--- can we delete this? I don't think this is useful anymore.

## Check

- b10 removed (git rm + 87 generated leftovers); its one untracked meeting note moved to Project-RandomThoughts/cowork/meetings/
- Project page spec now in b17: project-views.md, project-preview.html, 6 guide sections; b17 Project UI view renders
- 118 files: b10 links turned to words marked removed 261126; 28 code lines put back unchanged; edited JSON and Python all load
- method_canvas.py restored beside the guide so its empty-state note still works
- workbench 306 passed (6 old draft-reader failures); studio and workbench-work failures are missing PIL and pandas

## Summary

b10 is gone; the Project page spec lives in b17 and every link to b10 says it was removed.

