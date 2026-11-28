---
title: Studio Types are delivered into hai-studio and named, not addressed
date: 2026-11-27 23:06
topic: s60-skill-studio
aim: A blueprint Block designs a type; its elements.md is delivered into hai-studio/gallery/<name>/; a topic names its type by that name, in any SPACE
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2306_types_into_hai_studio.md
  what: this trace's own record, written first
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/
  what: one folder per delivered type, its elements.md as in the blueprint
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/types_deliver.py
  what: 'deliver every blueprint type; --check: the two copies are the same'
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/render_delivery.py
  what: 'a file piece: one file of the topic copied whole to its target'
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
  what: 'type_home: a type by name (this SPACE''s blueprint, then hai-studio/types) or by path'
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_follow.py
  what: names; also check_views.py, skills_checklist.py, type_requirements.py (refuses a topic that is no type)
- do: edit
  path: plugins/haipipe-toolkit/checks/skills/studio
  what: manifest.py and scope.py accept a type's name
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
  what: blueprint designs, the skill keeps; the new scripts named; also ref/studio-type.md, ref/skills-topic.md, CONSTITUTION.md, CHANGELOG.md, tests
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s7N-studio-type-*/delivery/render.yaml
  what: where the type is delivered
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work Skills and Block Structure topics
  what: check_type is the type's name; Check pages regenerated
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s60-skill-studio
  what: the drawing shows the blueprint delivering to the skill
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2306_types_into_hai_studio.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/types_deliver.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/render_delivery.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_follow.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
---

# Studio Types are delivered into hai-studio and named, not addressed

## Prompts

- **23:06** go

## Check

- hai-studio tests 92 passed; checks tests 31; studio tabs tests 38
- types_deliver.py --check: 7 types, each kept copy is the blueprint's
- type_follow.py check on b17: 18 of 18 topics that name a type follow it; 12 name it by name
- 5623 restarted; the b17 Studio page serves s60 (hai-studio, Draw, Check) and the Skills type

## Summary

Seven b17 types are kept in hai-studio/types and found by name; Skills and Block Structure topics name skills and block-structure. s11 to s15 and their type keep a path, since their own builder writes it; their generated pages are stale from an earlier style change by another session.

