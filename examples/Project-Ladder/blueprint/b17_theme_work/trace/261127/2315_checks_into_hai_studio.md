---
title: checks into hai-studio
date: 2026-11-27 23:15
aim: The Studio checks live in the skill that owns their rules, hai-studio/scripts/checks/, with their tests in hai-studio/tests/; the top-level plugins/haipipe-toolkit/checks/ folder is gone and every command and import points at the new place.
closed: false
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2315_checks_into_hai_studio.md
  what: this trace's own record, written first
- do: move
  path: plugins/haipipe-toolkit/checks/
  what: to plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/checks/ (tests to plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/)
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_views.py
  what: import from the new place
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
  what: the command path
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
  what: the command path
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/studio-type.md
  what: the command path
- do: edit
  path: AGENTS.md
  what: the command path
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
  what: the path
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2315_checks_into_hai_studio.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_views.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/studio-type.md
- AGENTS.md
- plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
---

# checks into hai-studio

## Prompts

- **23:15** yes, go ahead.

## Check

## Summary
