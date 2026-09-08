---
name: haipipe-design
description: >-
  Canonical owner of a Design Folder: frame an audience/job/venue, commission
  Run-backed design units, compare verified candidates, and record a person's
  adoption. Delegates unit generation/verification to haipipe-design-unit.
  Use for a Design Folder or DesignBoard; ends at accepted candidates, never
  shipping or measuring.
metadata:
  version: "2.0.0"
  last_updated: "2026-09-07"
  folder_owner: canonical
  folder_kind: design
  primary_face: page
  page_ruling: domain-gate
  legacy_page_type: design
  outline:
    mode: grammar
    source: "Brief + frozen design commissions + version-bound Results"
    shape: "design contract → insight use → principles → unit map → repeated message/unit divisions → rails → render/acceptance"
---

# /haipipe-design · one stable Folder, Run-backed units

A Design Folder is the same work-object altitude as a Task/Page Folder.
It has one Page Face and one Task Face. A **DU is the Result of a generation
Run**, never another phase-owned Folder beneath the DS Folder. A verification
Run produces a verification Result, not a DU.

## Ownership and routing

- This skill owns the stable Folder, both faces, evidence/creative boundaries,
  plugin selection, closure, and adoption.
- `haipipe-design-workflow` owns commissions, the Phase × Run map, dispatch,
  recovery, and gates.
- `haipipe-run` owns identities, pairing, immutable history, and runtime.
- `haipipe-design-unit` is the unit worker with generate/verify operations.
  See `../workflow-phases/haipipe-design-unit/SKILL.md`.
- Page writing uses `haipipe-page` and `haipipe-page-workflow`; Runs and
  Delivery present the existing records and do not own execution or adoption.

Use status, plan, generate/compose, verify/evaluate, revise, render, or adopt/
accept as user verbs. A request concerning just one unit routes to the worker
after its caller supplies a released Ticket. A proposal is not a release.

## Folder and configuration

Use `2-DS-design/DS<NN>-<audience>-<job>-<venue>/` inside its DesignBoard.
Audience × behavior job × primary venue is stable scope. Config changes
within that scope create new Runs, not new Folders. New Pages declare
`folder-kind: design`; no `workflow/phase.yaml` is manufactured.

```text
DS<NN>-<audience>-<job>-<venue>/
  <stem>.md                         Page Face
  outline/                          commissions, release/adoption receipts
  workflow/                         dispatch/round receipts, not duplicate Run states
  scripts/config/                   reusable defaults and frozen per-Run configs
  runs/rNN_design_generate_<slug>.yaml
  runs/rNN_design_verify_<slug>.yaml
  results/<same-Run-stem>/           result.yaml + checks.yaml + runtime.yaml + payload
  delivery/render/                  exact candidate previews and adopted projections
```

Materialize optional lanes only when used. YAML Tickets are agent-readable
execution commissions, not shell programs. The native profile and resolver
are in `haipipe-design-workflow/references/run-profile.md`.

## Page Face

Explain the goal and constraints, authorized sources, useful candidate
differences, review findings, chosen members, and open gaps. The main Page may
curate candidates; the Runs inventory retains all attempts. A sequence/set may
be one jointly commissioned DU; its members remain individually identifiable.

Human adoption lives in one version-bound outline decision receipt, projected
onto the Page. It pins DU manifests/member hashes, independent verification,
current preview, and any required handoff versions. A failed/unselected
candidate stays historical; it is not deleted. A new source marks affected
bindings stale without erasing the earlier person's decision.

## Task Face

Compile each commission before release. Freeze target, config, source roles,
acceptance list, output scope, and iteration budget. Dispatch through the
Ticket to the unit worker; supply only authorized, relevant inputs. Preserve
failed/blocked attempts. Independent verification uses a fresh reviewer.
The caller owns runtime receipts; the worker owns only its Result payload.
Choosing an existing candidate or recording a human decision creates no Run.

## Design-specific boundaries

Keep Board reads → commission grant → cited evidence narrowing. Distinguish
evidence from inspiration, reference material, avoid lists, and intuition.
A signed, contextual Application W handoff is still required for empirical
Design authority; Task RF and raw D/I/K prose do not acquire that authority.
Until Insight has actual Run Results, pin its existing signed handoff as a
versioned input, with no invented Supporting Run id or new PageX lane.
A brief-only creative commission is legal and makes no empirical effect claim.

The generation mode determines needed rationale, novelty and prospect
deliverables; see the worker's modes reference. Forecasts are labeled and
never become measured evidence. Brainstorming a candidate pool does not
commission an experiment. "Arm" remains downstream allocation vocabulary.

## Plugins and closure

Outline is required for commissions and person decisions. Runs is selected
once Tickets exist. Delivery/render supplies current previews before adoption.
Studio is optional. No Task plugin, new PageX lane, or design/DU storage lane
is selected for new work. The old Design plugin is a read-only legacy adapter.

The Folder closes only when commissioned work is terminal, required independent
reviews and human decisions exist, and the Page/projections match those exact
versions. Release and adoption remain person's acts over already-written,
named commissions/results. Do not infer them or add duplicate human ticks.
Stop at accepted candidates; building, sending, allocation, and measurement
belong to downstream Task owners.

## Legacy

Read `references/legacy-board.md` and the workflow's legacy reference only
when inspecting existing `design/DU*/` records or old D0–D5 phases.
After an explicit owner-metadata migration, new commissions in an existing DS
Folder use native Tickets/Results alongside read-only historical units. An old
authoritative phase.yaml cannot be silently bypassed. Never bulk-convert old
results, forge Run receipts, or rewrite old decisions. See `references/migration.md`.
