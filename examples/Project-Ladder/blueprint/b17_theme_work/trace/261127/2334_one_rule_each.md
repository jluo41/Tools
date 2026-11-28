---
title: 'One rule each: four competing rules cleaned'
date: 2026-11-27 23:34
aim: A topic that names a type is that type, not a slide draft; a type's instances are the topics that name it; one icon file per name; s51 no longer shows a skill that is going away
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2334_one_rule_each.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/canvas.py
  what: a topic that names a Studio Type is never read as a slide draft
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
  what: 'a type''s instances are the topics that name it; the instances: line is no longer needed'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71 and s75 elements.md
  what: 'the instances: line removed; delivered again'
- do: move
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/icons/icons.excalidrawlib
  what: becomes own-icons.excalidrawlib; icons.py and the mentions follow
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work
  what: workbench-work removed from its skills
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/TYPE.md
  what: the example line; also CHANGELOG.md, tests
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2334_one_rule_each.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/canvas.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/icons/icons.excalidrawlib
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/TYPE.md
---

# One rule each: four competing rules cleaned

## Prompts

- **23:34** plugins/haipipe-toolkit/skills/2_work/work/workbench-work <--- I will delete this, it is not useful anymore.

## Check

- tests: hai-studio, both gallery folders, studio tabs and hai-draw all pass, with two new ones
- hai-draw check.py no longer reads b17 s60 as a slide draft
- checks/run.py on b17 exits 0; no topic differs from its type; 7 types delivered the same

## Summary

Three of the four competing rules are gone (slide draft by number, instances listed in the type, two icon files of one name) and s51 no longer shows workbench-work. The fourth is half done: seven topics of the knowledge types still name their type by path; they belong to another session.

