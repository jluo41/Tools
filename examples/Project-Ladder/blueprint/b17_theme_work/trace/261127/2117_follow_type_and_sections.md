---
title: A topic follows its type; one Markdown file reads as section tabs
date: 2026-11-27 21:17
aim: Any Studio Type can start a topic and hold it; inside a topic every view is top, left, right
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2117_follow_type_and_sections.md
  what: this trace's own record, written first
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_follow.py
  what: 'new: start a topic from a type; check: hold it to the type'
- do: add
  path: plugins/haipipe-toolkit/checks/skills/studio/follow.py
  what: the follow check inside checks/run.py
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
  what: 'a type''s when: line'
- do: add
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/md_sections.py
  what: a Markdown file as a left tab per section
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/page_reader.py
  what: the reader shows one section
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
  what: the two rules; also ref/studio-type.md, ref/studio-section.md, CONSTITUTION.md A10 A11, CHANGELOG.md, tests
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/elements.md
  what: 'when: lines on the conditional parts'
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2117_follow_type_and_sections.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_follow.py
- plugins/haipipe-toolkit/checks/skills/studio/follow.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/md_sections.py
- plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/page_reader.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
- examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/elements.md
---

# A topic follows its type; one Markdown file reads as section tabs

## Prompts

- **21:17** with the new studio type, to use hai-studio to create that studio type, how to make it really follow it?

## Check

- hai-studio tests 82 passed; checks tests 31; studio tabs tests 36; page parts tests 22
- a real page clicked in a headless browser: Grant-Example s21 Page shows three left tabs, the second shows only its section
- type_follow.py check on b17: Skills topics and s11 follow; s01 to s04 and s13 differ from their types

## Summary

A topic can be started from any Studio Type and is held to it by checks/run.py; a view's one Markdown file reads as a left tab per section. b17 no longer exits 0: s01 to s04 and s13 differ from their types, which is the finding the check was made for.

