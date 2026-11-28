---
title: 's01 to s04: one drawing each of the Block type structure'
date: 2026-11-27 23:33
topic: s71-studio-type-block-structure
aim: Each Block Structure topic has one Excalidraw drawing of its folders, its Job-Task levels and its Studio bands, drawn from its structure.md so the names match Structure. The earlier five-part drawings and their builders move to history/ in each topic.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2333_s0N_drawings.md
  what: this trace's own record, written first
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/block-structure/scripts/block_structure_draw.py
  what: draws a topic's one drawing from its structure.md
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/block-structure/tests/test_block_structure_draw.py
  what: the drawing holds every name of structure.md
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/block-structure/TYPE.md
  what: the drawing script
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
  what: 'build: also draws; Draw names its check'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure
  what: new drawing and preview; old drawing and builder to history/
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s02-blueprint-structure
  what: new drawing and preview; old drawing and builder to history/
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s03-cowork-structure
  what: new drawing and preview; old drawing to history/
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s04-discovery-structure
  what: new drawing and preview; old drawing and builder to history/
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2333_s0N_drawings.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/block-structure/scripts/block_structure_draw.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/block-structure/tests/test_block_structure_draw.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/block-structure/TYPE.md
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_type_follow.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
---

# s01 to s04: one drawing each of the Block type structure

## Prompts

- **23:33** for each of the s0N, could you use the /hai-draw to have the draw for them? in one excalidraw file.

## Check

- block_structure_draw.py --check passes on s01 to s04; hai-draw check.py: no ❌, V lines all ✅ (pictures, short text, a big number); type_follow.py follow: all four follow; checks/run.py passes on the four and s71; hai-studio and gallery tests pass; previews read in the session

## Summary

One drawing per Block Structure topic, drawn from structure.md: folders as a tree of folder and file pictures, Job-Task levels as steps, Studio bands as a column. Old five-part drawings and builders are in each topic history/261127-five-part/.

