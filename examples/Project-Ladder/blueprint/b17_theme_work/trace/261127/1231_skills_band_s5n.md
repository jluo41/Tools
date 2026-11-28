---
title: 'Studio bands: s5N Skills, s7N Side pane, s2N Report'
date: 2026-11-27 12:31
topic: s02-blueprint-structure
aim: A blueprint Block's Studio has a Skills band (s51-s54, one per Block type, each showing its live skills); Side pane moves to s7N so s3N stays the theme Guide; s2N is kept for Report; the skill's numbering table says the same.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1231_skills_band_s5n.md
  what: this trace's own record, written first
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work
  what: 'Skills: Work, face and studio-views.json'
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s52-skills-blueprint
  what: 'Skills: Blueprint'
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s53-skills-cowork
  what: 'Skills: CoWork'
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s54-skills-discovery
  what: 'Skills: Discovery'
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane
  what: to s31-files-pane
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/s32-trace-section
  what: to s32-trace-section
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/board.md
  what: bands line s5N Skills, s7N Side pane; Renumbered note
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
  what: BLUEPRINT_BANDS with Skills and s7N; tree rebuilt
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
  what: expects the five bands
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-numbering.md
  what: s2N Report, s5N Skills, s7N Side pane
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/new_topic.py
  what: BANDS report, skills, sidepane
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
  what: band line
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1231_skills_band_s5n.md
- examples/Project-Ladder/blueprint/b17_theme_work/board.md
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-numbering.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/new_topic.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
---

# Studio bands: s5N Skills, s7N Side pane, s2N Report

## Prompts

- **12:31** then what skills we have included for this blueprint block?

## Check

- served b17 Studio: 🧱 s01-s04 · 👀 s11-s14 · 🧰 s51-s54 · 📁 s71 s72 · 🧭 s99; s52 shows 12 skill tabs; workbench 354 pass (6 known draft-reader failures); hai-studio 41 pass; s02 tree rebuilt with five bands, its check still stops at the pre-existing work folder hash

## Summary

s5N Skills (s51-s54), Side pane to s7N, s2N kept for Report; the skill's band table, new_topic.py and the s02 tree say the same.

