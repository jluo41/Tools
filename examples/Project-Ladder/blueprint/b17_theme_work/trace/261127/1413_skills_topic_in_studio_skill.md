---
title: The Skills topic layout written into hai-studio
date: 2026-11-27 14:13
topic: s75-studio-type-skills
aim: 'hai-studio owns the Skills topic layout: a rule (skills on top, the skill''s whole top level on the left, a folder as folds), a ref, and a script that writes and checks each Skills topic''s studio-views.json; the six Skills topics of b17 are written by it. s60 and s61 keep their numbers in the Skills band.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1413_skills_topic_in_studio_skill.md
  what: this trace's own record, written first
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_views.py
  what: writes a Skills topic's studio-views.json from its skills' folders; --check when stale
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/tests/test_skills_views.py
  what: tab order, missing parts, stale check
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/TYPE.md
  what: 'the Skills topic: top, left, right, how to add a skill'
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
  what: A07 the Skills topic rule with its check; A06 Cases names s76
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
  what: two lines pointing at ref/skills-topic.md
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/ (elements.md intro, face Examples, rebuilt pages)
  what: s6N continues the band
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work, s52-skills-blueprint, s53-skills-cowork, s54-skills-discovery, s60-skill-studio, s61-skill-trace (studio-views.json, face Topic line)
  what: written by skills_views.py; the face names the whole top level
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1413_skills_topic_in_studio_skill.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_views.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/tests/test_skills_views.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/TYPE.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
- examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/ (elements.md intro, face, rebuilt pages)
- examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work, s52-skills-blueprint, s53-skills-cowork, s54-skills-discovery, s60-skill-studio, s61-skill-trace (face Topic line; s60, s61 Covers line; studio-views.json unchanged, already what the script writes)
---

# The Skills topic layout written into hai-studio

## Prompts

- **14:13** yes, go ahead, and try to udate [the six Skills topics, s51-s54, s60, s61] accordingly, I will check it muself.

## Check

- skills_views.py --check on b17: six Skills topics, none stale
- type_requirements.py --check on s76: 6 pages, not stale; topic_titles_check.py: 0 problems
- hai-studio tests (see the reply for the count); test_skills_views.py 4 passed
- served Studio on 5623: s60 shows the new ref, script and test as folds, read live
- s60 and s61 were not renumbered: another session had already put them in the Skills band with their numbers

## Summary

hai-studio now owns the Skills topic layout: rule A07, ref/skills-topic.md and skills_views.py, which writes and checks every Skills topic's views file; b17's six are what it writes.

