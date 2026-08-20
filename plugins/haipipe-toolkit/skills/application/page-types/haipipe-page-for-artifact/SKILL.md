---
name: haipipe-page-for-artifact
description: >-
  The Page Type contract for an OPTIONAL promoted Application Artifact: one delivery unit that can be accepted, rejected, versioned, or deployed independently from neighboring units on its Design Page. Most SMS sets, email sequences, dashboards, checklists, and reports remain projections of one accepted Design Page; promote only when the independent accept/reject test passes. Use when a message, dashboard card, panel, checklist block, report section, or experimental arm needs its own acceptance/deployment lifecycle. Trigger: promote application artifact, independent message unit, artifact acceptance, deployable unit, stale render, page-type artifact, /haipipe-page-for-artifact.
metadata:
  version: "0.2.0"
  last_updated: "2026-08-20"
  summary: "Artifact is projection-first and Page-optional; promote only an independently accepted/deployed unit."
  outline:
    mode: resolved
    source: "accepted Design Page unit handoff + venue pack"
    shape: "unit contract → authored content/variants → trace → render → acceptance"
---

# /haipipe-page-for-artifact · promote one independently governed delivery unit

Load `haipipe-page`, `haipipe-page-for-intervention`, and the pinned venue pack. Load Display, Word, or another output plugin only when required.

Declare:

```yaml
page-type: artifact
artifact-kind: sms | push | reminder | email | checklist | dashboard | ui-card | report | other
artifact-unit: <stable unit id>
design-page: <owning Design Page>
```

## Admission rule

Default to a projection of the Design Page. Promote to an Artifact Page only when this sentence is true:

```text
This unit may be accepted, rejected, revised, versioned, or deployed while a neighboring unit is not.
```

Variants reviewed as one comparison stay divisions in the same owning Page.

## Boundary

```text
Design Page     owns audience/job strategy, system order, principles, and unit handoff
Artifact Page   owns one promoted unit's concrete content, render, and acceptance
Deploy          ships accepted versions and records external state
Insight Page    evaluates deployment data after Task execution
```

## Required Content roles

```text
Unit contract       Design Page, unit id, audience job, venue constraints, rails
Authored content    exact copy, interface, interaction, or section
Variants/arms       when jointly reviewed under one invariant
Trace               content move → Design principle → Insight Handoff
Render/preview      exact visible version
Acceptance          reviewer/date + design-handoff version + render version
```

## Runtime shape

```text
<application-root>/3-artifacts/A<NN>-<unit>/
├── A<NN>-<unit>.md
├── pagex/        owning Design Page and bounded trace
├── display/
└── word/         optional
```

## Closing checks

- The unit passes the independent accept/reject/deploy test.
- It executes exactly one current Design Page handoff.
- Every substantive move traces through Design to a settled Insight Handoff.
- Venue constraints and safety rails pass on the visible render.
- Acceptance names reviewer, date, Design handoff version, and render version.
- A changed handoff, content division, constraint, or render reopens acceptance.
- No evidence investigation or global strategy rewrite leaked into the Page.

This variant owns no scripts.
