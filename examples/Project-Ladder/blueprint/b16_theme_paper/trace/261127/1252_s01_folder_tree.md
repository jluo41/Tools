---
title: s01 Idea Block Jobs and Tasks as a folder tree
date: 2026-11-27 12:52
topic: s01-idea-block-structure
aim: s01's Jobs & Tasks view reads like the Folder view, using b17's shared tree_html; Job and Task are folders, groups are labels.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/trace/261127/1252_s01_folder_tree.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/structure/organization.json
  what: levels become Job group, Job folder, Task group, Task folder
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/delivery/page-spec/build_organization_maps.py
  what: a topic marked folder-tree renders with b17 tree_html
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/structure/jobs.html
  what: rebuilt by the builder, never by hand
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/delivery/page-spec/check_block_structures.py
  what: accept the folder-tree levels for s01
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/s01-idea-block-structure.md
  what: one decision line for the folder tree
---

## Prompts

- "for you s01 could you update yours to this folder-tree structure as well?"
- "check its s01, update yours accofdingly. go"

## Changed

- delivery/page-spec/build_idea_organization.py: new (off the first plan; replaces editing build_organization_maps.py). Builds structure/idea-organization.html with b17's tree_html: folder-rules, jobs-rules, studio-rules, and the j01_calibration / j02_missingness example.
- s01 studio-views.json: Structure, Draw, Examples open those sections by fragment, as b17's s01 does; Skills kept.
- s01 face: title "s01 · Block Structure: Idea"; a Folder trees section.
- check_block_structures.py: Structure/Draw may open structure/*-organization.html.
- organization.json and jobs.html left as they were (the earlier map).

## Check

- check_block_structures.py: 2 problems, the same s01/s02 "map is stale" as before the change.
- Chrome on 5623: #jobs and #folder-rules render as folder trees.

## Summary

s01 now shows its Folder, Job / Task and Studio organization as folder trees like b17's s01, drawn by b17's shared tree_html; Jobs and Tasks are folders, groups are labels.
