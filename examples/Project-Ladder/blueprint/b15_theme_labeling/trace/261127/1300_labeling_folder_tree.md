---
title: Labeling structure as folder trees
date: 2026-11-27 13:00
topic: s01-labeling-ladder
aim: Each labeling Block Structure topic shows Folder, Job / Task Organization and Studio Organization as the same folder tree b17 uses, drawn by b17's own tree_html, not a copy.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/1300_labeling_folder_tree.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/build.py
  what: Add folder-rules, jobs-rules, studio-rules trees via b17 tree_html
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/model.json
  what: Folder names for each Block's Job and Tasks
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/structure.css
  what: Map b17 tree colours onto the shared page variables
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/itemization.html
  what: Regenerated
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/guideline.html
  what: Regenerated
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/scale.html
  what: Regenerated
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/studio-views.json
  what: Structure tabs Folder, Job / Task Organization, Studio Organization
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/studio-views.json
  what: Same three Structure tabs
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/studio-views.json
  what: Same three Structure tabs
---

# Labeling structure as folder trees

## Prompts

- **12:40** b17_theme_work, read this, how do you want to design the job/task like the folder tree
- **13:00** for you s01 could you update yours to this folder-tree structure as well?

## Check

- build.py --check passes (3 Studios, 12 views). Each structure page serves 200; its folder-rules, jobs-rules and studio-rules sections read as trees with level words. The Studio page lists Folder, Job / Task Organization and Studio Organization. Chrome was not connected, so the page was checked by its served HTML only.

## Summary

The three labeling Block Structure topics (s01 to s03) now open on Folder, Job / Task Organization and Studio Organization, drawn as folder trees by b17's own tree_html and tree CSS, imported, not copied. Draw keeps the shared mind maps. The trees are naming rules: no real labeling Job folders exist yet.
