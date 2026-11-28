---
title: studio rule as tree
date: 2026-11-27 12:55
work: [s01]
aim: "s01's Structure › Studio Organization draws its rule as a folder tree, as Folder and Job / Task Organization do: the Block, then its Studio topics (or, for the blueprint Block, its bands) one under another, the level's name small after each."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1255_studio_rule_as_tree.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
    what: "rule_sections draws the Studio rule with tree_html instead of the mind map (its level 'Studio band' for the blueprint Block); tree_html keeps only the part of a level's name the line lacks (no '〈Job name〉 Job name', but '〈Job group〉 optional')"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/ (work, blueprint, cowork, discovery -organization.html)
    what: rebuilt by build_organization.py
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1255_studio_rule_as_tree.md
  - examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
  - examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/ (work, blueprint, cowork, discovery -organization.html, rebuilt)
---

# studio rule as tree

## Prompts

- **12:54** I think for the studio org, we can use teh folder tree as well.

## Check

- 5623's b17 Studio (Chrome), s01 › Structure: Studio Organization reads "▼ Work Block › 〈Studio topic〉" as a folder tree, 592px in a 592px frame; Job / Task Organization reads "Work Block › 〈Job group〉 optional › 〈Job name〉 › 〈Task group〉 optional › 〈Task name〉".
- The four Block types, read from the rebuilt pages: blueprint's Studio tree lists its five bands, each "Studio band"; cowork's Job tree "〈Job group〉 optional › j00_people Job name › 〈Request or coordination job〉 Job name"; discovery's "〈Inquiry name〉 Job / inquiry group › 〈Research question〉 Task / research topic".
- Examples keep the folded mind map, as check_organization.py asks; its only failure is the earlier "work: Folder changed" (pinned hash of b01_example_work's real tree).

## Summary

Structure's three tabs (Folder, Job / Task Organization, Studio Organization) are all folder trees.
