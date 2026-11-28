---
title: 'Skills topics: left tabs carry the real file and folder names'
date: 2026-11-27 14:20
topic: s76-studio-type-skills
aim: 'A skill''s left tabs read as its folder does: SKILL.md, CONSTITUTION.md, ref/, scripts/, each other folder with its slash, then each loose file by its own name; no Rules or other alias. s76 shows the same with 〈folder〉/ and 〈file〉.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1420_skills_real_names.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/skills_views.py
  what: tabs named by the file or folder; one tab per loose file
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_skills_views.py
  what: the expected names
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/skills-topic.md
  what: the left, in real names
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
  what: A08 rule sentence and JL's words
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s76-studio-type-skills/ (elements.md, face, rebuilt pages)
  what: SKILL.md, CONSTITUTION.md, ref/, scripts/, 〈folder〉/, 〈file〉
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work, s52-skills-blueprint, s53-skills-cowork, s54-skills-discovery, s60-skill-studio, s61-skill-trace (studio-views.json, face Topic line)
  what: rewritten by the script
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1420_skills_real_names.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/skills_views.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_skills_views.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/skills-topic.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
- examples/Project-Ladder/blueprint/b17_theme_work/s76-studio-type-skills/ (elements.md, face, rebuilt pages)
- examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work, s52-skills-blueprint, s53-skills-cowork, s54-skills-discovery, s60-skill-studio, s61-skill-trace (studio-views.json, face Topic line)
---

# Skills topics: left tabs carry the real file and folder names

## Prompts

- **14:20** I think in the left, the left tab should be the same as the file names, or folder names, how do you think?
- **14:20** yes, update s76 as well.

## Check

- hai-studio tests: 46 passed
- skills_views.py --check: six topics fresh; type_requirements.py --check on s76: 6 pages; placeholder_check and topic_titles_check: 0 problems
- served Studio on 5623 (no restart needed): s76 left SKILL.md, CONSTITUTION.md, ref/, scripts/, 〈folder〉/, 〈file〉; s60 left SKILL.md, CONSTITUTION.md, ref/, scripts/, agents/, constitution/, tests/, CHANGELOG.md
- off the plan: SKILL.md, one phrase in the pointer line

## Summary

A skill's left tabs now read as its folder does on disk: files by name, folders with a slash, loose files as their own tabs; the aliases Rules and other are gone, in the six topics, the type s76 and the skill's rule A08.

