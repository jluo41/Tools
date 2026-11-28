---
title: hai-studio reads the Studio Type; Skills topics get a Draw button
date: 2026-11-27 20:59
topic: s60-skill-studio
aim: SKILL.md holds no copied band-to-type table; how a type is written is one ref file; the Skills Checklist reads its parts from the type; a Skills topic with a drawing shows it
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2059_studio_type_first.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
  what: 'section 1: no table; three steps: find the type the topic names, read it, none: write the type first'
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/studio-type.md
  what: how a type's elements.md is written and the four questions that give top, left, right
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_views.py
  what: a Draw view when the topic has its own drawing
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_checklist.py
  what: the parts come from the type the topic names; a Draw line
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/skill_text_check.py
  what: SKILL.md may not name one type topic by number
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/
  what: tests for the three scripts
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/TYPE.md
  what: the Draw button; also CONSTITUTION.md A08 and CHANGELOG.md
- do: edit
  path: plugins/haipipe-toolkit/checks/skills/studio
  what: scope.py and freshness.py accept a Skills topic's Draw view
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/elements.md
  what: a Draw view; pages regenerated
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s5N and s6N Skills topics
  what: views and Checklist regenerated
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2059_studio_type_first.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/studio-type.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_views.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_checklist.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/skill_text_check.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/TYPE.md
- examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/elements.md
---

# hai-studio reads the Studio Type; Skills topics get a Draw button

## Prompts

- **20:59** yes, I asked to make all the changes, please continue

## Check

- hai-studio tests 78 passed; checks tests 31 passed; studio tabs tests 31 passed
- skill_text_check.py passes on hai-studio
- checks/run.py on b17 exits 0
- the s60 page shows the Draw button and links the drawing (read from the served page)

## Summary

SKILL.md section 1 points to the Studio Type band, no table; ref/studio-type.md added; Skills type has Draw; the Checklist reads its parts from the type. Open: no check holds a topic against its type's buttons; s01 to s04 differ from s71; s05, s55, s62 name no type.

