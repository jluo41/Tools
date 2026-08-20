---
name: haipipe-page-for-intervention
description: >-
  The Page Type contract for an Application DESIGN PAGE, using the globally unique machine key `page-type: intervention`. An Application may own many Design Pages; each serves one audience × behavior job × primary venue, consumes the Brief and settled local/external Insight Design Handoffs through PageX, then authors principles, a message/unit map, repeated message divisions, variants, rails, and an accepted visible projection. Use for SMS/email/dashboard/checklist/report/message design, audience-specific strategy, message sequences, interaction components, or retargeting. Trigger: application design page, intervention design, message strategy, audience job, message map, message divisions, component map, variants, page-type intervention, /haipipe-page-for-intervention.
metadata:
  version: "0.2.0"
  last_updated: "2026-08-20"
  summary: "Many Design Pages per Application; each turns settled Insight handoffs into one audience/job/venue message system."
  outline:
    mode: grammar
    source: "accepted Brief + PageX Insight handoffs + venue pack"
    shape: "design contract → insight use → principles → unit map → repeated message/unit divisions → rails → render/acceptance"
---

# /haipipe-page-for-intervention · design one audience/job delivery system

Load `haipipe-page`, `haipipe-page-for-brief`, `haipipe-plugin-pagex`, and the selected venue pack. In user-facing prose call this a **Design Page**; declare `page-type: intervention` for deterministic global resolution.

An Application may own many Design Pages. The default grain is:

```text
one audience or recipient class × one behavior job × one primary venue
```

Split when two designs can be accepted, retargeted, or reopened independently.

## Boundary

```text
Brief          Application scope, need map, promise, Design roster
Insight Page   settled K/W + Design Handoff under source boundaries
Design Page    applicability, principles, message roles, content, render, acceptance
Artifact Page  optional promotion for one independently accepted/deployed unit
```

Design performs composition, not evidence settlement. It owns `pagex/` and no `probe/`.

## Content grammar

Every Design Page realizes these roles; venue decides the exact titles and repeated unit form:

```text
Design contract       audience · behavior job · context · primary venue · success condition
Insight Use Map       adopted/constraining/declined handoffs and applicability reasons
Design principles     because <H/K/W>, do <move>, within <rail>
Message/Unit map      ordered roles, trigger/timing, job, invariant, allowed variable
R<n> unit divisions   one message, touchpoint, panel, checklist block, or report section per division
Cross-unit rails      coherence, escalation, prohibited moves, uncertainty language
Render and acceptance exact visible version reviewed as one system
```

Each repeated unit division carries:

```text
unit id · recipient moment · audience job · Insight/Handoff refs · design move
exact content or interaction · declared variants · safety rail · next trigger
```

Do not create empty Narrative or Display divisions. Use one division per jointly reviewed message/unit. Promote a unit to an Artifact Page only when it can pass/fail/deploy while its neighbors do not.

## PageX-only input boundary

```text
Brief Page ───────────── PageX ─┐
settled Insight Handoff ─ PageX ─┼─▶ Design Page
accepted prior Design ─── PageX ─┘
```

PageX binds exact files/scopes. The Insight Use Map records why they apply here. Never inspect Task `results/`, dispatch Discovery, or copy an Insight Page's Probe cards.

## Runtime shape

```text
<application-root>/2-design/D<NN>-<audience>-<job>/
├── D<NN>-<audience>-<job>.md
├── pagex/
├── outline/
└── display/
```

## Closing checks

- The Page names one audience, behavior job, context, and primary venue.
- Every load-bearing design principle reaches a settled Insight Design Handoff.
- Declined and constraining insights remain visible with reasons.
- Every unit has one audience job, trigger/timing, design move, and safety rail.
- Experimental variables are separated from invariants.
- The exact visible system has a version-bound human acceptance.
- Missing premises route to a local Insight Page; no local Probe exists.
- A promoted Artifact can execute its handoff without inventing global strategy.

This variant owns no scripts.
