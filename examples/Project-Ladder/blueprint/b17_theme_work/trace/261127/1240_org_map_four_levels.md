---
title: org map four levels
date: 2026-11-27 12:40
work: [s01]
aim: "s01's Job / Task Organization map shows its four levels (Job group, Job name, Task group, Task name) at once: the shared mind map opens every level instead of starting with all but the first closed."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1240_org_map_four_levels.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
    what: "the rule map (Structure › Job / Task Organization) draws the shared mind map open (organization_map fold=False); the map's columns narrow on these pages so the four levels fit a Studio frame"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/ (work, blueprint, cowork, discovery -organization.html)
    what: rebuilt by build_organization.py
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1240_org_map_four_levels.md
  - examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
  - examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/ (work, blueprint, cowork, discovery -organization.html, rebuilt)
---

# org map four levels

## Prompts

- **12:38** [Image #45] I think this is not correct. the mind map should be four layer JobGroup -> JobName -> TaskGroup -> TaskName,

## Check

- Cause: the shared mind map (hai-mindmap) draws the root and the first level as cards and the deeper levels as a numbered list under each card, closed until "show"; and its fixed 250px and 230px columns pushed that list past the right edge of a 592px Studio frame.
- 5623's b17 Studio (Chrome), s01 › Structure › Job / Task Organization: Work Block → 〈Job group〉 → 1.1 〈Job name〉 → 1.1.1 〈Task group〉 → 1.1.1.1 〈Task name〉, all shown at once; the last word ends at 581px inside the 592px frame.
- The real Job examples (Examples view) and the Studio map keep starting folded with Open all, as check_organization.py asks; the shared skill is unchanged.
- check_organization.py: only the earlier "work: Folder changed" (the pinned hash of b01_example_work's real tree, open with its owner).

## Summary

The Job / Task Organization rule map shows its four levels at once and fits the Studio frame.
