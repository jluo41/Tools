---
title: 's71: the Pattern is drawn as s05 draws its tree; the Example fold goes'
date: 2026-11-27 22:54
topic: s71-studio-type-block-structure
aim: 'One tree per requirement: the Pattern carries the level colours, the small level words and the connector lines of an instance tree, so no separate Example is shown.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2254_s71_one_tree.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_requirements.py
  what: 'Pattern tree: level colours, level words, connector lines'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
  what: Job-Task pattern names its levels as s05 does; pages rebuilt
- do: delete
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/examples.json
  what: no Example fold on this type
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2254_s71_one_tree.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_requirements.py
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/examples.json
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_requirement_examples.py
---

# s71: the Pattern is drawn as s05 draws its tree; the Example fold goes

## Prompts

- **22:54** you see the pattern and examples are not the same. I want to make them the same and delete the Examples, do you get it?

## Check

- type_requirements.py --check and checks/run.py --target s71 pass; test_requirement_examples.py 8 pass; three pages rendered from the server in headless Chrome

## Summary

s71 shows one tree per requirement: the Pattern with level colours, level words and connector lines; its Example fold and examples.json are gone. Other type topics rebuilt for the shared style; s72, s11-s15 and the Skills topics left to their owners.

