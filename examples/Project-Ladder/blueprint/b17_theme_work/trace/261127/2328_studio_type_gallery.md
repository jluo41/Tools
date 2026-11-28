---
title: hai-studio keeps each Studio Type in its own gallery folder
date: 2026-11-27 23:28
topic: s60-skill-studio
aim: 'gallery/<type>/ holds everything of one type: its delivered elements.md, its TYPE.md, its scripts and tests, one real example'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2328_studio_type_gallery.md
  what: this trace's own record, written first
- do: move
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/types
  what: becomes gallery/, one folder per type
- do: move
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/TYPE.md
  what: becomes gallery/skills/TYPE.md; ref/ui-preview-topic.md becomes gallery/block-job-ui-preview/TYPE.md
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/block-structure/TYPE.md
  what: how a Block Structure topic is built
- do: move
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_views.py
  what: into gallery/skills/scripts/ with skills_checklist.py; the three block_* scripts into gallery/block-structure/scripts/; their tests beside them
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/<type>/example.md
  what: one real topic of the type and its picture, for the three types that have one
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/types_deliver.py
  what: delivers into gallery/; also type_follow.py, checks/paths.py, skill_text_check.py find a type's scripts
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
  what: the kept types are in gallery/; skill_evaluation.py counts gallery scripts and tests
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
  what: section 1 points to gallery/; also ref/studio-type.md, CONSTITUTION.md, CHANGELOG.md
- do: edit
  path: plugins/, examples/
  what: every mention of a moved file's path
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2328_studio_type_gallery.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/TYPE.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/block-structure/TYPE.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/skills/scripts/skills_views.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/types_deliver.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
---

# hai-studio keeps each Studio Type in its own gallery folder

## Prompts

- **23:28** okay, I agree, please think about it and update it accoridngly

## Check

- tests: hai-studio 111, gallery/skills 12, gallery/block-structure 2, studio tabs 42, block page 37, all passed
- skill_text_check passes; types_deliver --check: 7 types the same; type_follow check: 19 topics follow; checks/run.py on b17 exits 0
- type_follow.py follow on s01 runs the two block-structure scripts from their gallery folder
- 5623 restarted; s60 lists gallery/<type>/ folders on its left

## Summary

gallery/<type>/ holds a type's elements.md, TYPE.md, scripts, tests and example; three types have all five, four have elements.md only. ref/gallery.md (b35's count of every topic) is kept and is a different thing; base-types/learning (another session's) is not moved.

