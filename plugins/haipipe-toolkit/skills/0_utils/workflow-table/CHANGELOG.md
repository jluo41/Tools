# Changelog · workflow-table

## 0.4.1 · 2026-09-05

- Fix the Tables-family boundary to name the Board Table row grain explicitly:
  one Board Page/Page Folder, with Tasks and runtime evidence summarized below
  that owner.

## 0.4.0 · 2026-09-04

- Define the Tables family as a two-lens projection: a plan lens plus an
  observed display lens, with the owning workflow/Page/Task/Outline remaining
  authoritative.
- Name `Task Tables` as the current task-folder sibling and reserve `Board
  Tables` as a future Board/Folder projection rather than conflating it with
  the existing Folder inventory.

## 0.3.0 · 2026-09-01

- Remove the obsolete `skill-inspect` dependency and make Skill Coverage own
  workflow-local inventory and static quality assessment.
- Absorb the five ownership classes and compact quality questions into
  `ref/skill-coverage.md`; retain `field-test` as the separate behavior-proof
  skill.
- Require all workflow references and quality evidence to resolve through
  Workflow Table's own coverage rules.

## 0.2.0 · 2026-09-01

- Make Skill Coverage a default workflow-report projection, with one row per
  participating skill and source-backed status, version, `SKILL.md` line count,
  quality/completeness, and field-test evidence.
- Make Workflow Table's Skill Coverage the inventory/static-quality view and
  keep `field-test` as the behavior-proof sibling.
- Add a workspace-level Run Catalogue reference that distinguishes Run types
  from concrete Runs Overview instances.
- Extend the normalized schema, audit order, validation gates, and invocation
  metadata for the four synchronized views.
- Record provenance for observed, user-declared, derived, and unresolved
  coverage facts; distinguish the bundled Run Catalogue reference from a live
  workspace catalogue; and make compact phase status source-backed.
- Render the default surfaces in the reader-facing order Workflow Table → Runs
  Overview → Human Actions → Skill Coverage, with Skill Coverage last as the
  meta/audit projection.

## 0.1.0 · 2026-09-01

- Add a cross-workflow contract for one row per executable Phase/Cycle.
- Separate authoritative L3 Task/Page content changes from L4 Run activity.
- Define synchronized Workflow Table, Runs Overview, and Human Actions
  surfaces with distinct row grains.
- Add a normalized declaration shape, rendering projections, and audit rules.
