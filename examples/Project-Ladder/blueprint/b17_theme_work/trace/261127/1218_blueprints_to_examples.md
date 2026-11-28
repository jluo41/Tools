---
title: examples/ is examples/; the theme Blocks move to Project-Ladder/blueprint/
date: 2026-11-27 12:18
topic: s02-blueprint-structure
aim: The top folder of Projects is examples/, and the five theme Blocks that plan the tools sit in examples/Project-Ladder/blueprint/, apart from the example Blocks; every path, link, glob and old address follows.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1218_blueprints_to_examples.md
  what: this trace's own record, written first
- do: move
  path: blueprints
  what: to examples (plain mv; other sessions' changes kept as they are)
- do: move
  path: examples/Project-Ladder/blueprint/b11_theme_insight
  what: to examples/Project-Ladder/blueprint/, with b12, b15, b16, b17
- do: edit
  path: examples
  what: 'every text file: examples/ to examples/, Project-Ladder/work/b1N_theme to Project-Ladder/blueprint/b1N_theme (also %2F forms)'
- do: edit
  path: plugins
  what: 'every text file: the same two path changes'
- do: edit
  path: plugins/haipipe-toolkit/servers/_host/serve.py
  what: old examples/ and work/b1N_theme addresses redirect to the new place
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  what: globs read examples/, any theme folder
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/file_info.py
  what: trace glob reads examples/*/*/*/trace
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-block/scripts/job_close_check.py
  what: Job glob reads work/ and blueprint/
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-evidence/scripts/paper_text.py
  what: SPACE found by examples/
- do: edit
  path: AGENTS.md
  what: examples/ holds the Projects; blueprint/ holds the theme Blocks
- do: edit
  path: PRINCIPLE.md
  what: same path words
- do: edit
  path: examples/Project-Ladder/project.md
  what: Blocks list under blueprint/
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1218_blueprints_to_examples.md
- plugins/haipipe-toolkit/servers/_host/serve.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/file_info.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-block/scripts/job_close_check.py
- plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-evidence/scripts/paper_text.py
- AGENTS.md
- PRINCIPLE.md
- examples/Project-Ladder/project.md
---

# examples/ is examples/; the theme Blocks move to Project-Ladder/blueprint/

## Prompts

- **12:18** I think I want to do this, plesae rename it to examples.
- **12:24** (b11 session) s99-guide.html relative link broke by the move

## Check

- no blueprints/ path left outside .git, references, .claude; 354 tests pass (6 known draft-reader failures); old URLs 301 to the new place; render check 17 problems = 16 known goals + b12's own unquoted title; 36 relative links fixed, 0 unresolved; theme_of reads all five as work

## Summary

blueprints/ is examples/; the five theme Blocks live in examples/Project-Ladder/blueprint/; paths, globs, redirects, rules and relative links follow.

