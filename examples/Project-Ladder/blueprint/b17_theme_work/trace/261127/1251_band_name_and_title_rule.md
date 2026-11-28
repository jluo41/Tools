---
title: Block Job UI Preview band; titles named by their band, in the skill
date: 2026-11-27 12:51
topic: s02-work-skills
aim: The s1N band reads Block Job UI Preview, as its topics' titles do; hai-studio writes and checks the rule that a topic's title starts with its band's name.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1251_band_name_and_title_rule.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/board.md
  what: s1N 👀 Block Job UI Preview (and b11, b12 board.md)
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
  what: BLUEPRINT_BANDS name; tree rebuilt; check_organization.py the same
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work/s51-skills-work.md
  what: band name in Excluded (s52, s53, s54, s12 the same)
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/new_topic.py
  what: 'a named band prefixes the title: <band>: <title>'
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/topic_titles_check.py
  what: every topic in a named band, its title starting with the band's name
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-face.md
  what: the title rule
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
  what: 'article: a topic''s title names its band, with its Run line'
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_hai_studio.py
  what: new_topic prefixes the band name
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1251_band_name_and_title_rule.md
- examples/Project-Ladder/blueprint/b17_theme_work/board.md
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
- examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work/s51-skills-work.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/new_topic.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/topic_titles_check.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-face.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_hai_studio.py
---

# Block Job UI Preview band; titles named by their band, in the skill

## Prompts

- **12:51** "Block Job UI Preview <--- I want to use this one.

## Check

- served Studio bands: 🧱 Block Structure, 👀 Block Job UI Preview, 🧰 Skills, 🧩 UI Plugin, 🧭 Guide; s02 tree rebuilt; hai-studio tests 42 pass (new: band name titles the topic); topic_titles_check: b17 clean, 11 titles in b11 and b12 left to their sessions

## Summary

The s1N band is Block Job UI Preview; hai-studio writes and checks that a topic's title starts with its band's name (A05, open for b11 and b12).

