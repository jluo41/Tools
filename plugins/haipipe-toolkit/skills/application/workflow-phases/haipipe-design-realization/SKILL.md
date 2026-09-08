---
name: haipipe-design-realization
description: >-
  Read-only compatibility owner for the historical D2 design-unit Folder
  identity. Resolves old phase.yaml records; new generation uses the
  haipipe-design-unit worker and never creates mutable DU Folders.
metadata:
  version: "1.0.0"
  last_updated: "2026-09-07"
  workflow: haipipe-design-workflow
  phase: D2
  folder_kind: design-unit
  primary_face: task
  page_ruling: none
---

# /haipipe-design-realization · read a legacy D2 record

## Position

Historical D2 between old release and verdict gates. New work uses the native
Design workflow, not this phase.

## Folder Kind

Existing design/DU folders may declare current.folder-kind: design-unit.
This adapter preserves readable identity without inventing Run history.

## Input

The existing card, unit files, phase record and exact historical references.

## Page Face

Read original README, spec, evidence, content and conditional provenance.
Do not replace historical labels with new runtime claims.

## Task Face

Report recorded state and missing/stale files. To revise, return exact content
references for a new native generation Ticket. Do not change the old phase.

## Plugins

Legacy design is read-only. New Runs belong to the parent Design Folder.

## Gate and Closure

Report what the historical GD2 receipt establishes; do not confer a new
passing state, independent review or human adoption.

## Handoff

New commissioned work routes to haipipe-design-unit through the native
haipipe-design-workflow; the old record stays unchanged.

## Files

Old schema: `../haipipe-design-unit/references/legacy-phase.md`.
New worker: `../haipipe-design-unit/SKILL.md`.
