---
name: haipipe-page-for-brief
description: >-
  The Page Type contract for the BRIEF page, exactly one per application. It defines the intervention opportunity, audience and behavior, success and kill criteria, selected settled Insight Pages, delivery venue, audience-facing promise, and the bounded handoff to Intervention design. Use when starting or retargeting an application, combining legacy Seed/Venue/Pitch decisions, selecting which Task/Insight Pages justify an intervention, or checking what the Intervention page may assume. Trigger: application brief, intervention brief, audience, behavior change, venue promise, selected insights, page-type brief, /haipipe-page-for-brief.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-17"
  summary: "Application uses Brief rather than Opening: one Page owns opportunity, audience, outcome, venue, promise, and the handoff to Intervention."
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "opportunity → audience/behavior → outcome → source insights → venue → promise → Intervention handoff"
---

# /haipipe-page-for-brief · define what intervention is being designed

Load `haipipe-page` first and `haipipe-plugin-pagex` when resolving Insight sources. Load `haipipe-page-for-stage` only when a legacy runtime still presents the Brief as an S page.

This type covers exactly one Brief per application. Declare `page-type: brief`.

`Brief` is intentionally not called `Opening`. Paper owns `page-type: opening`; globally unique keys keep the base resolver deterministic.

## Boundary

```text
Insight Page   what is known, with DIKW trace and evidence limits
Brief          what intervention, for whom, through which venue, and why
Intervention   how selected insights become mechanisms and components
Artifact       the independently reviewable delivery unit
```

Brief selects settled insights but does not reproduce DIKW or investigate raw Task/Discovery evidence.

## Fixed Content outline

```text
### 1 · Opportunity
### 2 · Audience and Behavior
### 3 · Outcome and Kill Criteria
### 4 · Selected Insights
### 5 · Venue
### 6 · Promise
### 7 · Intervention Handoff
```

- **Opportunity** states the problem and why an intervention is warranted now.
- **Audience and Behavior** names the people, context, current behavior, and desired change.
- **Outcome and Kill Criteria** makes success, guardrails, and abandonment conditions observable.
- **Selected Insights** lists PageX bindings to settled Insight Pages, plus one-line relevance and limits. No raw result copy.
- **Venue** pins channel, format, audience constraints, and the venue pack used.
- **Promise** states what this intervention offers this audience without exceeding the selected insights.
- **Intervention Handoff** is the bounded packet the next Page may assume.

## PageX-only evidence boundary

```text
Task/Discovery evidence ─▶ Task/Insights Board ─▶ settled Insight Page
                                                     │
                                                   PageX
                                                     ▼
                                                   Brief
```

Brief owns `pagex/` and no `probe/`. If a required insight is absent or unsettled, add a `missing insight` row with the question and intended Task/Insights Board destination. Do not open a local evidence investigation.

## Retargeting

Keep opportunity, audience, outcome, and source insight identities when still valid. Rewrite venue, promise, and handoff. A heavier venue may require additional settled insights; it does not authorize Brief to settle them.

## Legacy compatibility

Until runtime migration, read legacy Seed, Venue, and Pitch pages as inputs and fold their current decisions into this contract. Do not delete or silently rewrite those pages. The target page is one `S-Brief-0-brief.md` or equivalent Board Page.

## Runtime shape

```text
<BriefPage>/
├── <BriefPage>.md
├── pagex/       selected Insight Page bindings
└── outline/     optional fixed-outline working material
```

Brief owns no Probe, raw evidence, deployable artifact, or venue implementation.

## Closing checks

- One audience, desired behavior, measurable outcome, and kill criterion are visible.
- Every substantive justification resolves to a settled Insight Page.
- Venue and promise fit the audience and evidence limits.
- Missing insights are routed back to Task/Insights Board rather than answered locally.
- Intervention can start from Division 7 without reading legacy Seed/Venue/Pitch pages.

This variant owns no scripts.
