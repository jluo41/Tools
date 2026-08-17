---
name: haipipe-page-for-artifact
description: >-
  The Page Type contract for one independently reviewable APPLICATION ARTIFACT unit, such as a message set, email, checklist block, dashboard card, interaction panel, report section, or audience segment with experimental arms. It executes one current Intervention handoff under a pinned venue, carries the concrete authored content and render/version acceptance record, and reopens when that handoff or render changes. Use when creating, revising, reviewing, or retargeting deployable application content. Trigger: application artifact, SMS copy, email unit, dashboard card, checklist block, report section, message arms, page-type artifact, /haipipe-page-for-artifact.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-17"
  summary: "One Artifact Page owns one independently approvable delivery unit; variants reviewed together stay as divisions, and changed handoffs/renders reopen acceptance."
  outline:
    mode: resolved
    source: "Intervention handoff + venue pack"
    shape: "unit contract → authored content/variants → trace → render → acceptance"
---

# /haipipe-page-for-artifact · execute one intervention unit

Load `haipipe-page`, `haipipe-page-for-intervention`, and the pinned venue pack first. Load Display, Word, or another output plugin only when the venue requires it.

Declare:

```yaml
page-type: artifact
artifact-kind: sms | push | reminder | email | checklist | dashboard | ui-card | report | other
artifact-unit: <stable unit id>
```

One Page equals one unit that can be accepted while a neighboring unit is rejected. Variants or arms reviewed as one comparison remain Content divisions inside that Page.

## Boundary

```text
Intervention   owns global strategy and the current unit handoff
Artifact       owns concrete content, local trace, render, and acceptance
Deploy         ships accepted artifacts and records external state
Task/Insight   evaluates resulting data after deployment
```

Artifact does not select global insights, redesign the theory of change, or settle evidence.

## Resolved Content outline

Resolve the exact divisions from `artifact-kind`, but every Artifact Page must carry:

```text
Unit contract       audience job, handoff row, venue constraints, safety rails
Authored content    the concrete message, component, interaction, or section
Variants/arms       when applicable, comparable divisions under one invariant
Trace               content move → Intervention principle → Insight Page
Render/preview      the exact version a person reviews
Acceptance          accepted/rejected/held record bound to version and handoff
```

Do not create empty Narrative or Display divisions for venues that do not need them. Venue packs refine the shape without changing the closing rule.

## Source boundary

Artifact reads its Intervention handoff, not Task/Discovery folders. It may follow the handoff's PageX trace during audit, but it owns no `probe/` and cannot repair a missing insight locally.

When content needs an unsupported proposition, route to Intervention. Intervention decides whether to remove the move or request a new Insight Page.

## Version and reopening

Acceptance binds to both:

```text
handoff-version  the Intervention row executed
render-version   the exact visible artifact accepted
```

A changed handoff, authored division, venue constraint, or render reopens the Page. Deployment never treats an earlier acceptance as approval of a different version.

## Runtime shape

```text
<ArtifactPage>/
├── <ArtifactPage>.md
├── outline/      optional unit outline
├── display/      previews, mockups, panels, or rendered assets
├── word/         optional document projection
└── pagex/        bounded trace to Brief/Intervention; normally no direct Insight import
```

The deployable projection may live under `0-artifacts/`, but the Page records which source and version produced it. Hand edits to a projection must be reconciled back to the authored Page before acceptance.

## Closing checks

- The Page grain passes the independent accept/reject test.
- Content executes exactly one current Intervention handoff.
- Every substantive move traces through Intervention to a settled Insight Page.
- Variants change declared variables and preserve declared invariants.
- Venue constraints and safety rails are testable on the visible render.
- Acceptance names reviewer, date, handoff version, and render version.
- No raw evidence investigation, global strategy rewrite, or deploy action leaked into the Page.

This variant owns no scripts.
