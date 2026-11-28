---
title: rename hai-stack
date: 2026-11-25 18:19
aim: 'The haistack skill is named hai-stack everywhere: its folder, its name and trigger (/hai-stack), every Run line and mention in the repo, and the installed link in ~/.claude/skills.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1819_rename_hai_stack.md
  what: this trace's own record, written first
- do: move
  path: plugins/haipipe-toolkit/skills/0_utils/hai-stack
  what: git mv from skills/0_utils/haistack; SKILL.md name and trigger
- do: edit
  path: AGENTS.md
  what: /haistack sweep becomes /hai-stack sweep
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  what: Run lines point at hai-stack (same for the other skills' constitutions and reports that name it)
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
  what: SHARED_SKILLS names hai-stack
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
  what: expects hai-stack
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/space_constitution.py
  what: its path to constitution.py, after asking the session that owns SPACE Home
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/home/space_home.py
  what: its mention, after asking the same session
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1819_rename_hai_stack.md
- AGENTS.md
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/work_files.py
- plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
- plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/space_constitution.py
- plugins/haipipe-toolkit/servers/workbench/home/space_home.py
- plugins/haipipe-toolkit/skills/1_base/draft/hai-draft/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
---

# rename hai-stack

## Prompts

- **18:19** could you rename haistack to be hai-stack?
- **21:14** do the rename

## Check

- git grep haistack outside traces and references: 0 left
- ~/.claude/skills/hai-stack links to skills/0_utils/hai-stack; the skill list now shows hai-stack
- hai-stack/scripts/constitution.py lists every article; workbench tests: 242 passed

## Summary

The skill folder moved to skills/0_utils/hai-stack with git mv; its name, trigger (/hai-stack), every Run line and mention in AGENTS.md, the constitutions, their reports, the workbench code and the test now say hai-stack, and its check flag is HAI_STACK_CHECKING. The installed link was replaced. Past trace files keep the old name as JL's words were typed.

