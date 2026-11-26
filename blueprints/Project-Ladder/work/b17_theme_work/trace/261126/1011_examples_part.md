---
title: examples part
date: 2026-11-26 10:11
work: [j12t01, s11]
aim: "A Block's Files pane has an Examples part, the example Blocks its face names on an examples line, so b17 shows b01_example_work beside its own folders; b01_example_work holds Studio topics too (a concept with its drawing, a UI preview with Page, Effect and Draw, and s99 its own Guide), as a real Block does."
closed: true
plan:
  - do: add
    path: blueprints/Project-Ladder/work/b17_theme_work/trace/261126/1011_examples_part.md
    what: this trace's own record, written first
  - do: edit
    path: blueprints/Project-Ladder/work/b17_theme_work/board.md
    what: examples line naming b01_example_work
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/haipipe-block/ref/board-contract.md
    what: the examples face line in its Example Blocks section
  - do: add
    path: blueprints/Project-Ladder/work/b01_example_work/s01-what-it-checks/
    what: a concept topic by new_topic.py, its five-part drawing built
  - do: add
    path: blueprints/Project-Ladder/work/b01_example_work/s02-html-report-layout/
    what: a UI preview topic, Page the live t12 HTML report Task page, Effect one quick html
  - do: add
    path: blueprints/Project-Ladder/work/b01_example_work/s99-guide/
    what: the Block's own Guide, a UI preview topic whose quick view is b17 s99-guide-view's guide.html until the Guide section is coded
changed:
  - blueprints/Project-Ladder/work/b17_theme_work/trace/261126/1011_examples_part.md
  - blueprints/Project-Ladder/work/b17_theme_work/board.md (examples line)
  - plugins/haipipe-toolkit/skills/1_base/project/haipipe-block/ref/board-contract.md (the examples line, Studio topics in an example Block)
  - blueprints/Project-Ladder/work/b01_example_work/s01-what-it-checks/
  - blueprints/Project-Ladder/work/b01_example_work/s02-html-report-layout/
  - blueprints/Project-Ladder/work/b01_example_work/s99-guide/
---

# examples part

## Prompts

- **10:10** [Image #14] I think for this, it should be added to folder panel, and as a nwe section. forthe b01 here theraere no things like the sNN? it is very werid. Please go ahead and work on it.

## Check

- The Files pane code was done at the same minute by another session (work_files.py examples_tree, the Block Examples part, tests/test_block_examples.py, for b11); this trace only names b01_example_work on b17's face and uses it. Its plan lost the two code lines it no longer does.
- b17's Files panel: 1 · Block, 2 · Code, 3 · Skills, 4 · Block Examples (b01_example_work).
- b01's Studio, after a restart of 5623: s01 Draw, Delivery; s02 Page (the live t12 Task page), Effect (the quick layout), Draw, Delivery; s99 Page, Draw, Delivery; no traceback. Each page and quick view returns 200.

## Summary

b17's Files pane shows its example Block, b01_example_work, as a part of its own; b01 now holds Studio topics as a real Block does, a concept with its drawing, a UI preview with Page and Effect, and its own s99 Guide.
