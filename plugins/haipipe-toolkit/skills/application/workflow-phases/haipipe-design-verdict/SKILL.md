---
name: haipipe-design-verdict
description: >-
  DesignBoard workflow phase D3 and Folder contract for independent reflection
  on a landed Unit: mechanical compliance, cold-read stance fidelity, novelty,
  and prospect guardrails. Trigger: design verdict, judge a unit, reflect,
  prospect check, D3, /haipipe-design-verdict.
metadata:
  version: "1.0.3"
  last_updated: "2026-08-31"
  workflow: haipipe-design-workflow
  phase: D3
  folder_kind: design-verdict
  primary_face: task
  page_ruling: none
---

# /haipipe-design-verdict · judge the unit independently

Load `haipipe-folder`, the Design door/workflow, and
`haipipe-plugin-design`. The judge is never the D2 designer.

## Position

D3 reads a complete landed unit. GD3 judges realization; GD4 judges the
prospect where the posture owes one. Failure returns the same thread to D2 or
the person kills the card.

## Folder Kind

Verdict is a review state over one Unit, not a second artifact lane. Its visible
record is the unit's `judged:` line plus named findings in the parent Design
Folder's `outline/<DesignFolder-stem>-log.md`.
It is the third current identity of the same stable DU Folder:
`folder-kind: design-verdict`. The card and unit material remain in place.

## Input

The landed card carrying its recorded release/grant, complete unit, declared acceptance list, venue rails,
fielded/template set for novelty checks, and prospect requirements.

## Page Face

A reader sees verdict, reviewer, date, checks performed, unresolved findings,
and the exact unit/card versions judged. The face distinguishes mechanical
failure, stance-fidelity judgment, and prospect failure.

## Task Face

A fresh reviewer checks grant containment, file/spec completeness, rails,
stance fidelity, and posture-specific novelty/ideation rules. When applicable,
check walkthrough, mechanism, predicted effect with uncertainty, failure
conditions, grant-only citations, and forecast typing. Never repair the unit.

## Plugins

- `design` required; verdict state stays on the unit it judges;
- `render` forbidden: D4 owns the first recipient projection; D3 cold-reads
  the unit's source content against venue rails;
- no private verdict, probe, or code plugin.

## Gate and Closure

GD3 passes on a named independent `judged:` record with no blocking finding.
GD4 also passes for every non-pool unit whose prospect satisfies all guardrails.
Pool units are explicitly exempt from GD4, not silently missing it. A failed
verdict records the return edge and restores `folder-kind: design-unit`; a
passing verdict leaves `design-verdict` current while the parent D4 Folder
decides the division.

## Handoff

Hand D4 the judged unit, exact card/handoff/unit versions, verdict findings,
and the exact division it is ready to populate. D3 cannot name a render
version: D4 creates the first render after this handoff.

## Files

- Verdict token: the `judged:` line inside `<unit>/README.md`
- Phase identity/history: `<unit>/workflow/phase.yaml`
- Receipt/findings: `<DesignFolder>/outline/<DesignFolder-stem>-log.md`
