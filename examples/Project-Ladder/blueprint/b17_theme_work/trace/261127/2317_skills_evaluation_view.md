---
title: An Evaluation top button on every Skill topic
date: 2026-11-27 23:17
topic: s75-studio-type-skills
aim: The Skills type lists an Evaluation view; every Skill topic shows, per skill, how good the skill is today, measured live from its files
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2317_skills_evaluation_view.md
  what: this trace's own record, written first
- do: add
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/skill_evaluation.py
  what: one skill measured from its files, as a live page
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/frame_view.py
  what: the live view skill-eval
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_views.py
  what: an Evaluation view after the skills, one item per skill
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_checklist.py
  what: Evaluation is no skill; its own line; also scripts/checks/scope.py
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/
  what: tests for the view and the measures
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
  what: 'the Evaluation view; the follow command and build: line; also ref/skills-topic.md, ref/studio-type.md, CHANGELOG.md'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/elements.md
  what: '## Evaluation; pages regenerated; delivered to types/skills'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s51 to s55, s60 to s63
  what: views regenerated with Evaluation
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2317_skills_evaluation_view.md
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/skill_evaluation.py
- plugins/haipipe-toolkit/servers/workbench/page/block_index_page/frame_view.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_views.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_checklist.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
- examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/elements.md
---

# An Evaluation top button on every Skill topic

## Prompts

- **23:17** we can also add the top view named Evaluation and check the quality of this skill, right? could you add it, and then update it to [the nine Skill topics] please go ahead and work on it.

## Check

- hai-studio tests 125 passed; studio tabs tests 42 passed; block page tests 37 passed
- a real page clicked: s51 Evaluation shows five left tabs and ten criteria; s60 shows its one skill full width
- skills_views --check: nine Skill topics fresh; type_follow check and checks/run.py on b17 pass; 7 types delivered

## Summary

Every Skill topic has an Evaluation button: each skill measured live from its files. It already shows real gaps, for example hai-work names ref/work-pages.md which is not on disk and its version and change log disagree.

