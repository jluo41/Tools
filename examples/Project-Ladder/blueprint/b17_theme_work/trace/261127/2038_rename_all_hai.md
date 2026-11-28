---
title: Rename every hai- skill and agent to hai-
date: 2026-11-27 20:38
aim: 'Every skill and agent named hai-<x> is hai-<x>: folders, names, files and every mention, in one sweep; the packages haipipe-toolkit and haipipe-utils keep their names'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2038_rename_all_hai.md
  what: this trace's own record, written first
- do: move
  path: plugins/haipipe-toolkit/skills, plugins/haipipe-utils/skills
  what: '99 skill folders hai-<x> become hai-<x>, with their name: lines'
- do: move
  path: plugins/**/agents/hai-*-agent.md
  what: 29 agent files become hai-*-agent.md
- do: move
  path: files named hai-<x> anywhere outside references/
  what: renamed to hai-<x> (guides, drawings, change notes)
- do: edit
  path: plugins/, examples/, AGENTS.md, README.md, PRINCIPLE.md, install files
  what: every hai-<x> mention becomes hai-<x>, all file types (about 4000 files)
- do: edit
  path: ~/.claude/skills, ~/.claude/agents
  what: the installed links point at the new folders under the new names
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2038_rename_all_hai.md
---

# Rename every hai- skill and agent to hai-

## Prompts

- **20:38** Okay,I think how about for all the hai-xxx, change them to hai-xxx what is your thoughts? Please do it.

## Check

- no haipipe-<x> name left in plugins/ and examples/ outside CHANGELOG.md files and two session .jsonl files
- 77 test folders run before and after: 6 new failures; 4 gone after sweeping the skills' own references/ folders, 2 come from table-workbench, deleted by another session
- checks/run.py on b17 exit 0; 5623 restarted, five blueprint Studio pages load with no old name

## Summary

159 names moved and about 34000 mentions replaced in 3557 files; 130 installed links re-pointed. Kept: packages haipipe-toolkit and haipipe-utils, underscore names, schema names, CHANGELOG history. Not swept: other SPACEs' data, which may still name haipipe-<x> skills and agents.

