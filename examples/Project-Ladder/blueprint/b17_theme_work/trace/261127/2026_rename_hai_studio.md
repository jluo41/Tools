---
title: Rename hai-studio to hai-studio
date: 2026-11-27 20:26
topic: s60-skill-studio
aim: 'The Studio skill is named hai-studio everywhere: its folder, its name, its reviewer agent and every mention, in one sweep; its logic drawn in s60'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2026_rename_hai_studio.md
  what: this trace's own record, written first
- do: move
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio
  what: 'folder becomes hai-studio; name: hai-studio; /hai-studio and /workbench-studio still trigger it'
- do: move
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/agents/hai-studio-reviewer-agent.md
  what: was hai-studio-reviewer-agent
- do: move
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_hai_studio.py
  what: was test_hai_studio.py
- do: edit
  path: plugins/
  what: every mention and path, all file types (about 230 files)
- do: edit
  path: examples/
  what: every mention and path, drawings and generated pages included (about 850 files)
- do: edit
  path: AGENTS.md
  what: the mentions; also .gitignore
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s60-skill-studio
  what: its drawing shows the logic of hai-studio
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2026_rename_hai_studio.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/agents/hai-studio-reviewer-agent.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_hai_studio.py
- AGENTS.md
---

# Rename hai-studio to hai-studio

## Prompts

- **20:26** I want to understand the logic of the /hai-studio, I think you can make a draw for it as well

## Check

- no hai-studio left outside CHANGELOG.md files and one session .jsonl
- hai-studio tests 74 passed; studio tabs tests 31 passed; studio tests in 4 other packages passed
- checks/run.py on b17: only s11 to s14 and s72 fail, from another session's work in progress, not from the rename
- 5623 restarted; the Block Studio page loads with no old name

## Summary

hai-studio is hai-studio in 1194 files; installed links re-pointed; /hai-studio still triggers it; s60 has a drawing of the skill's logic. The Skills type has no Draw view, so the drawing does not show on the s60 page yet.

