## 0.4.6 · 2026-09-20

- Remove retired Design Adopt declarations and coverage; retain Commission, Generate, and Verify.
- Align failure routes and Verify closure with the Design owner; Delivery projects the passed candidate.
- Count C Commission decisions, N Generate Runs, and J Verify Runs, including held decisions.

## 0.4.5 · 2026-09-20

- State directly that a Workflow is a list of Run Specs and Routes connect
  the listed Specs.
- Synchronize the Design schema, matrix, and example Cells with the live
  Goal/Design/Insight/Run/Delivery Workspace roster.
- Correct stale Workspace coordinates in the skill coverage and Run catalog.

## 0.4.4 · 2026-09-15

- Make Workflow Definition the directed graph of Run Specs and spec-owned
  Routes; Workflow Table rows are Run Specs rather than Phase/Cycle rows.
- Keep the plural `workspace_roster` and one coordinate-keyed Cell per
  Run Spec × Workspace, with Cells limited to skill, presentation, and
  interaction bindings. Gates and Routes remain on the Run Spec.
- Define Run Type, Run Spec, Run Instance, internal Step, and Workspace
  boundaries; make Human Actions a derived queue of instances needing a human
  actor or gate.
- Make the row/instance boundary explicit: Steps and Versions stay inside one
  Run, while multiple actual Runs under a parameterized Spec stay in Runs
  Overview rather than becoming duplicate Workflow Table rows.
- Update the Design graph to `Design.commission → N Design.generate →
  J Design.verify → Design.adopt`, with count `1 + N + J + 1` and a stable
  `runtime` Workspace id behind the optional UI label `Run`.

## 0.4.3 · 2026-09-15

- Make Workflow × Workspace the canonical grammar: one plugin/work object
  declares a plural Workspace roster of member Workspaces, a domain Workflow
  declares Phase/Cycle rows, and each row/Workspace intersection is a
  coordinate-keyed Cell.
- Move skill, Run, L3, gate, route, and source/projection bindings into Cells;
  point Runs Overview, Human Actions, and Skill Coverage to owning Cell
  coordinates while keeping projections and actual Run inventory separate.
- Add a worked Design matrix for Plan/Create/Review/Run/Delivery and preserve
  the `N_generate + J_verify` actual Run count.
- Clarify that one Plugin/work object declares a plural `workspace_roster` of
  member Workspaces; Cell `workspace_id` references one member Workspace.

## 0.4.2 · 2026-09-08

- Update the Page CONTENT example to Paragraph Writing with Cn.Pm targets and paragraph cardinality; remove the retired DRAFT phase from that example.

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
