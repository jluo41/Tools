---
title: hai-studio SKILL.md made clean
date: 2026-11-27 20:09
topic: s60-skill-studio
aim: 'hai-studio''s SKILL.md is a short entry a reader follows top to bottom: find the Studio Type first, the first principle, what a topic is, the commands, what to check, which ref to read; no render marker, no quoted request, no file named that is not on disk. Its long sections live in ref/, their words kept.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2009_studio_skill_clean.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
  what: rewritten as the short entry
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-delivery.md
  what: one topic one delivery, delivery types, themes, render.yaml (moved from SKILL.md)
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/studio-section.md
  what: where a topic opens, groups, Runs, Timeline, Folder (moved from SKILL.md)
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/job-results.md
  what: a Job's current results (moved from SKILL.md)
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-look.md
  what: the look and change notes in full (moved from SKILL.md), no quoted request
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-builder.md
  what: add, redraw, save steps (moved from SKILL.md), no quoted request
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-contract.md
  what: the list of ref files as it is now
- do: delete
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-scripts.md
  what: three stale rows; the commands are in SKILL.md
- do: delete
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-buttons.md
  what: three stale rows; the commands are in SKILL.md
- do: edit
  path: examples/Project-PageParts/work/b35_studio/s01-studio-skill/delivery/render.yaml
  what: its five text pieces into SKILL.md go; SKILL.md owns that text now
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s60-skill-studio (studio-views.json, face Checklist)
  what: rewritten by the scripts after the ref files change
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2009_studio_skill_clean.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-delivery.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/studio-section.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/job-results.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-look.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-builder.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-contract.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-scripts.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-buttons.md
- examples/Project-PageParts/work/b35_studio/s01-studio-skill/delivery/render.yaml
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-rounds.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-scripts.md (deleted)
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-buttons.md (deleted)
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/draw.md, reader-review.md, infer-topics.md, proposal-topic.md, screen.md, topic-face.md (who-and-when notes removed)
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/skill_text_check.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_skill_text_check.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CHANGELOG.md
- examples/Project-Ladder/blueprint/b17_theme_work/s51-s54, s60, s61 and s76 (generated pages rebuilt after another session changed type_requirements.py at 20:06)
---

# hai-studio SKILL.md made clean

## Prompts

- **20:09** no, remove them. make them as clean as possible, clean, easy to follow, and tell them what to check. [the ref/ folds] what does this for? We have so many studio types, how does the hai-studio will make them as the highest priority?
- **20:09** [ref/topic-scripts.md] I am not sure why this is related to hai-studio??
- **20:13** In the skill.md, never show the annotation, or things like (JL 261112: "this is not vivid, I want the vivid ones")

## Check

- skill_text_check.py on hai-studio: passes (no who-and-when note or marker in SKILL.md and 23 ref files; every named file exists; every ref and script is named); ref/gallery.md is generated and skipped
- SKILL.md: 591 lines, 41 notes, 6 marker lines before; 192 lines, 0 and 0 after
- hai-studio tests: 74 passed (4 new); checks/run.py on s51-s54, s60, s61, s76: exit 0; skills_views.py and skills_checklist.py --check: 8 fresh
- browser (headless Chromium): s60 SKILL.md shows 7 numbered sections, no marker text, no note; ref/ has 24 folds with the three new files and without topic-scripts.md
- the before text is kept outside the repo in this session's scratchpad (studio-skill-before/)
- not done: no fresh-context agent has used the new SKILL.md on a real task; ref/gallery.md still carries generated marker lines; the other skills are not swept

## Summary

hai-studio's SKILL.md is a short entry that starts with the Studio Type and ends with what to check; its long sections moved to ref/ with their rules kept and their who-and-when notes gone; rule A09 and skill_text_check.py keep it so.

