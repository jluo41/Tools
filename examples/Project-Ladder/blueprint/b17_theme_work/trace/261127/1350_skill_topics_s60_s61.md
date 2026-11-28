---
title: 's60 Skill: Studio and s61 Skill: Trace'
date: 2026-11-27 13:50
topic: s77-studio-type-studio-type
aim: 'b17''s Studio has a Skill band (s6N), one topic per skill read live: s60 the Studio skill, s61 the Trace skill; s52 Skills: Blueprint no longer repeats them.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1350_skill_topics_s60_s61.md
  what: this trace's own record, written first
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s60-skill-studio
  what: 'face and studio-views.json: hai-studio''s SKILL, rules and refs'
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s61-skill-trace
  what: 'face and studio-views.json: hai-trace''s SKILL, rules and script'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/board.md
  what: 'bands: s6N 🔧 Skill'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s52-skills-blueprint/studio-views.json
  what: hai-studio and hai-trace tabs moved out
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-numbering.md
  what: 's60-s69 in a blueprint Block: Skill (new_topic.py band skill)'
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1350_skill_topics_s60_s61.md
- examples/Project-Ladder/blueprint/b17_theme_work/board.md
- examples/Project-Ladder/blueprint/b17_theme_work/s52-skills-blueprint/studio-views.json
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-numbering.md
---

# s60 Skill: Studio and s61 Skill: Trace

## Prompts

- **13:50** please have the s60 for the skill studio, and also s61 for the skill trace. Do it.

## Check

- served Studio: 🔧 Skill band with s60 (8 tabs of hai-studio) and s61 (3 tabs of hai-trace); b17 titles clean; hai-studio tests pass

## Summary

s60 Skill: Studio and s61 Skill: Trace, in b17's s6N Skill band; s52 no longer repeats the two skills.

