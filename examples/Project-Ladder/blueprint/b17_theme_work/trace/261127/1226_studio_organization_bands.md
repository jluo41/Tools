---
title: Studio Organization lists the blueprint bands
date: 2026-11-27 12:26
topic: s02-blueprint-structure
aim: 'The blueprint Block''s Studio Organization shows the four bands the Studio page groups by: Block Structure, Job previews, Side pane, Guide.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1226_studio_organization_bands.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
  what: 'BLUEPRINT_BANDS: the four bands; tree, rule map and rows read them'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
  what: expects the four bands, not Block UI
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/blueprint-organization.html
  what: rebuilt
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1226_studio_organization_bands.md
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/blueprint-organization.html
---

# Studio Organization lists the blueprint bands

## Prompts

- **12:26** we hvae the block structure, and block job preview UI. and then Side pane, and then Guide. you need to update this first. right?

## Check

- rebuilt blueprint-organization.html holds the four bands; check_organization.py passes up to the pre-existing work folder hash pin (not this change)

## Summary

Studio Organization of a blueprint Block lists the four Studio bands from one BLUEPRINT_BANDS table.

