---
title: The 〈 〉 rule in hai-studio, with a check
date: 2026-11-27 14:16
topic: s71-studio-type-block-structure
aim: hai-studio carries the rule that a name not fixed is written in 〈 〉 (AGENTS.md Page words), as an article with a check over every Studio Type topic's slots.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1416_placeholder_rule_in_studio_skill.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
  what: article A07
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
  what: one line under the topic rules
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-face.md
  what: the rule beside the title rule
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/placeholder_check.py
  what: a numbered slot name outside 〈 〉 in a type topic
- do: edit
  path: AGENTS.md
  what: the rule names its check
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1416_placeholder_rule_in_studio_skill.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-face.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/placeholder_check.py
- AGENTS.md
---

# The 〈 〉 rule in hai-studio, with a check

## Prompts

- **14:16** update the AGETNS.md so everyone will follow it, and Ithink you should also add this to the /hai-studio

## Check

- placeholder_check over examples: 18 Studio Type topics, 0 bare slot names; the pattern catches 'Job type 1' and 'Example 2', passes 〈Job type 1〉, Folder, Job-Task

## Summary

The 〈 〉 rule is in AGENTS.md and in hai-studio (A07, SKILL.md, ref/topic-face.md) with a check.

