---
title: org rule as tree
date: 2026-11-27 12:50
work: [s01]
aim: "s01's Structure › Job / Task Organization draws its rule as a folder tree, like Structure › Folder: Work Block, then 〈Job group〉, 〈Job name〉, 〈Task group〉, 〈Task name〉 one under another, each level's name small and grey after it; no mind map there, nothing cut at the frame's edge."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1250_org_rule_as_tree.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
    what: rule_sections draws the Job / Task rule with tree_html (roles = the level names) instead of the mind map; the 1240 column overrides go
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/ (work, blueprint, cowork, discovery -organization.html)
    what: rebuilt by build_organization.py
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1250_org_rule_as_tree.md
  - examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
  - examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/ (work, blueprint, cowork, discovery -organization.html, rebuilt)
---

# org rule as tree

## Prompts

- **12:48** [Image #47] could you make this to be the folder tree as well?

## Check

- 5623's b17 Studio (Chrome), s01 › Structure › Job / Task Organization: ▼ Work Block › 〈Job group〉 job group · optional › 〈Job name〉 Job name › 〈Task group〉 Task group · optional › 〈Task name〉 Task name, one under another with the Folder tab's lines; the page is 592px wide in a 592px frame, nothing cut.
- This replaces trace 1240's open mind map and its column overrides (removed); Examples and Studio Organization keep the mind map, as check_organization.py asks.
- check_organization.py: only the earlier "work: Folder changed" (pinned hash of b01_example_work's real tree).

## Summary

Job / Task Organization's rule is a folder tree like Folder's: four levels one under another, each level named small after it.
