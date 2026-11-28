---
title: One command makes a topic follow its Studio Type
date: 2026-11-27 23:15
topic: s71-studio-type-block-structure
aim: 'type_follow.py follow <topic> runs the builders its type names, rebuilds the Check view and reports whether the topic follows the type. s71 names its builders on a build: line.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2315_follow_command.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_follow.py
  what: 'a follow command: build, then check'
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
  what: 'a type may carry a build: line'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
  what: 'build: names the two builders; kept copy delivered'
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_type_follow.py
  what: the follow command
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2315_follow_command.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_follow.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_type_follow.py
---

# One command makes a topic follow its Studio Type

## Prompts

- **23:15** go, and please explain why the studio type is not followed by the studio instance/

## Check

- type_follow.py follow on s01, s02, s03, s04: all follow; hai-studio tests 125 pass, Studio tests 39 pass; checks/run.py --target passes on s71 and the four topics; types_deliver.py --check passes

## Summary

type_follow.py follow <topic> builds a topic with the scripts its type names on build:, rebuilds its Check view and reports. s71 names block_structure_page.py and block_types_pages.py.

