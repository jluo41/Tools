---
title: s76 Skills type laid out as its instances
date: 2026-11-27 13:57
topic: s75-studio-type-skills
aim: 's76 · Studio Type: Skills shows the same top views (SKILL, Rules, Refs, Scripts) and left tabs as its instances; its right side is the requirement for that part, an instance''s right side the real skill file; an Instances view lines the skill topics up against it.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1357_s76_skills_type.md
  what: this trace's own record, written first
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/elements.md
  what: the four views and their left tab, each with what, must, from, why
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/build_type_pages.py
  what: writes each part's requirement page and the Instances table, as s72's does
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/delivery/ (skill, rules, refs, scripts, instances .html)
  what: built requirement pages
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/studio-views.json
  what: views SKILL, Rules, Refs, Scripts, Instances
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/s75-studio-type-skills.md
  what: Holds line names the four views
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work/studio-views.json (and s52, s53, s54)
  what: views SKILL and Rules in place of one Skills view
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s60-skill-studio/studio-views.json (and s61)
  what: views SKILL, Rules, Refs, Scripts in place of one Skill view
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1357_s76_skills_type.md
- examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/elements.md
- examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/s75-studio-type-skills.md
- examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/delivery/requirements/ (4 pages, built)
- examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work, s52-skills-blueprint, s53-skills-cowork, s54-skills-discovery (studio-views.json, one face line each)
- examples/Project-Ladder/blueprint/b17_theme_work/s60-skill-studio, s61-skill-trace (studio-views.json, one face line each)
---

# s76 Skills type laid out as its instances

## Prompts

- **13:57** let's make the s76 first. what is the top, left, and right
- **14:00** you will focus on the s76, go

## Check

- type_requirements.py --check on s76: 4 requirement pages, not stale
- served Studio on 5623: s76 shows SKILL, Rules, Refs, Scripts; s51, s53, s54 SKILL; s52 SKILL and Rules; s60 all four (Rules 5, Refs 20, Scripts 18 tabs); s61 SKILL, Rules, Scripts
- not built: s76's own build_type_pages.py and the Instances view; the shared type_requirements.py replaced the first and has no Instances table

## Summary

s76 is laid out as its instances: SKILL, Rules, Refs, Scripts on top, each with its requirement on the right, built from elements.md by the shared type_requirements.py; the six skill topics use the same views with real files.

