---
title: s01 structure look
date: 2026-11-27 12:25
work: [s01]
aim: "s01 Work Block Structure reads as one plain tree: no stage pill on a Studio fold, one frame around a view (not two), tree items without a box each, the naming key and each folder's purpose as hovers instead of a line of text."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1225_s01_structure_look.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
    what: a Studio fold shows no stage pill (its stage stays in the face); an iframe inside left tabs has no border of its own
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
    what: tree items lose their boxes; the naming key and each folder's purpose become hovers
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/tests/test_focus_studio.py
    what: "its Studio row test asserts no stage pill (it asserted one, from the older one-word rule of 261029)"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/ (work, blueprint, cowork, discovery -organization.html)
    what: rebuilt by build_organization.py
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1225_s01_structure_look.md
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  - plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/tests/test_focus_studio.py
  - examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
  - examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/ (work, blueprint, cowork, discovery -organization.html, rebuilt)
---

# s01 structure look

## Prompts

- **12:20** How do you think about the s01? [Image #44] how do you think about this?
- **12:24** okay, got it, plesae go ahead and update them .

## Check

- 5623's b17 Studio (Chrome): s01's fold bar has no "shaping" pill; Structure › Folder sits in one frame (the iframe inside the left tabs has no border, 0px); the tree has no box per item, names in ink and the Block root in accent; no "Fixed name" line.
- Hovers (Chrome): bNN_〈block〉/ "the Block: one piece of work and all it holds", board.md, jNN_〈job〉/ and the rest carry their purpose; the section's hover is the naming key. Only the rule tree has them; a real Block's tree (Examples) stays as read.
- Tests: workbench page, side_pane, studio, home 242 passed, 1 skipped (test_focus_studio's row test now asserts no stage pill).
- check_organization.py: fails "work: Folder changed" on the pinned hash in organization_by_block_type.md. The pinned section is the real b01_example_work tree, which gained files (t13, result/ files, example.csv) not this change; the hash is the b17 session's to re-pin, told by message.
- 5623 and 5602 restarted, both 200.

## Summary

s01's Folder reads as one plain tree in one frame: no stage pill on any Studio fold, no box per item, the naming key and each folder's purpose as hovers.
