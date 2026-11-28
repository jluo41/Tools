---
title: "Design structure Studios as b17's folder tree"
date: 2026-11-27 13:05
topic: s01-design
aim: s01 and s02 show Folder, Job / Task Organization and Studio Organization as b17 does (naming rules under Structure and Draw, real records under Examples), drawn by b17's shared tree and mind-map code, with Job group and Task group in place of Job Type and Task Type.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1305_folder_tree_structure.md
  what: this trace's own record, written first
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/structure/build_organization.py
  what: design-board and design-methodbook trees; imports b17's tree_html, organization_map and STYLE; --check
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/structure/design-board.html
  what: built
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/structure/design-methodbook.html
  what: built
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/studio-views.json
  what: b17's manifest shape over design-board.html
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/studio-views.json
  what: b17's manifest shape over design-methodbook.html
- do: move
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/ and s02-workbench-ui/delivery/
  what: the mind-map files no view uses any more (structure.html, mindmap.html, *.mindmap.md, structure.excalidraw, structure.png) to _archive/20261127/<topic>-mindmap/; structure.md stays
- do: move
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/build_structure_studios.py
  what: to _archive/20261127/; its mind-map checks are replaced by build_organization.py --check
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/s01-design.md
  what: Views and Sources name the new builder
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/s02-workbench-ui.md
  what: Views and Sources name the new builder
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.md
  what: Job group, Job name, Task group, Task name in place of Job Type and Task Type
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.md
  what: the same for the Book
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench-design/design_jobs.py
  what: a Book Job with no authored family takes its method's registry family, as the tree does
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench-design/tests/test_design_jobs.py
  what: the Book Job's group is its registry family
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
  what: T15 folder-tree structure, with its guard
changed:
- examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1305_folder_tree_structure.md
---

# Design structure Studios as b17's folder tree

## Prompts

- **13:05** raed this, could you update yours to this folder-tree structure as well?

## Plan details

- Structure and Draw: the naming rules, `Design-〈app〉/` and `DesignMethodBook-〈topic〉/` folder trees with each
  folder's job on hover, and the four-level Job / Task tree: Job group (the method family, optional), Job name,
  Task group (Ideas, Designs, Review), Task name. The Book stops at Job name.
- Examples: the real Design-Example and DesignMethodBook-Example folders, every real Job in one map, the real Studio
  topics, and the live Block.
- b17's builder stays b17's; this one imports it and changes no b17 file.

## Check

- `build_organization.py --check`: 0 problems (six sections each, no table, fresh build, manifests match).
- Headless Chrome screenshots of design-board.html: the Design-〈app〉/ rule tree; the four-level Job / Task rule
  map; the real Jobs under Goal Only (j01, j02) and Internal (j03) with their real Task names.
- `pytest servers/workbench-design/tests`: 68 passed, 298 subtests passed.
- Tools host on 5623 restarted: b12 Studio's s01 views load design-board.html (200); the Book's Jobs show
  Goal Only and Internal. Chrome itself was not connected.

## Summary

s01 and s02 now read as b17's: Folder, Job / Task Organization and Studio Organization, rules then real records,
drawn by b17's code imported, not copied. Job Type and Task Type became Job group and Task group. The mind-map
files and their checker are in `_archive/20261127/`.
