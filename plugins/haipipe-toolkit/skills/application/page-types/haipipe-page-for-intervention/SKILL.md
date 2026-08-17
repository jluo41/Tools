---
name: haipipe-page-for-intervention
description: >-
  The Page Type contract for the INTERVENTION page, exactly one per application. It reads an accepted Brief, settled Insight Pages through PageX, and the venue pack, then maps them into a theory of change, intervention principles, message or interaction strategy, venue-appropriate arc, component map, experimental variants, safety rails, and one handoff row per Artifact Page. Use when designing a message, dashboard, checklist, report, or other intervention from existing insights; when repairing component allocation; or when retargeting an application. Trigger: intervention design, message strategy, theory of change, component map, artifact map, variant arms, page-type intervention, /haipipe-page-for-intervention.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-17"
  summary: "Intervention is Application's composition Page: it transforms settled Insight Pages into mechanisms, components, variants, and Artifact handoffs without redoing DIKW."
  outline:
    mode: grammar
    source: "accepted Brief + PageX Insight Pages + venue pack"
    shape: "insight selection → theory of change → principles → strategy/arc → components → variants → safety → Artifact handoff"
---

# /haipipe-page-for-intervention · turn settled insights into a delivery design

Load `haipipe-page`, `haipipe-page-for-brief`, and `haipipe-plugin-pagex` first. Load the selected venue pack before making channel-specific choices.

This type covers exactly one Intervention Page per application. Declare `page-type: intervention`.

The name is intentionally distinct from Board's generic `page-type: design`, which compares candidate artifacts and closes on a selection record. Intervention closes on an accepted delivery architecture.

## Boundary

```text
Brief          opportunity · audience · outcome · venue · promise
Insight Pages  settled knowledge/wisdom and evidence limits
Intervention   mechanism · strategy · components · variants · handoffs
Artifact       concrete copy, interface, section, or delivery unit
```

Intervention performs composition, not research. It may select, decline, combine, and translate insights, but it may not change their evidence status.

## Content grammar

Every Intervention Page must realize these roles; division titles and grouping may follow the venue:

```text
Insight selection       adopted/declined Insight Pages and why
Theory of change        audience action chain, each link insight-anchored
Intervention principles exact design moves derived from K/W rows
Strategy and arc        framing, timing, sequence, interaction or narrative
Component map           one row per independently reviewable Artifact unit
Variants and arms       invariants, experimental variables, comparison logic
Safety and compliance   forbidden moves, uncertainty language, escalation rails
Artifact handoff        the packet each Artifact Page executes
```

Narrative is a conditional role inside Intervention, not its own Application Page Type. SMS may need one move, a checklist a sequence, a dashboard an interaction architecture, and a report a narrative arc.

## Trace and component maps

Each design move must trace:

```text
Insight Page K/W row ─▶ intervention principle ─▶ component ─▶ Artifact unit
```

Write one component row per independently approvable unit:

```text
unit-id | audience job | adopted insight/principle | content move |
venue constraint | invariant | variant | safety rail | Artifact page
```

If two units cannot be accepted independently, keep them in one Artifact Page. If one may pass while the other fails, split them.

## PageX-only evidence boundary

Intervention owns `pagex/` and no `probe/`. A missing premise becomes a `missing insight` request naming the question, required target level, and Task/Insights Board destination. Work pauses only where that premise is load-bearing; unrelated components may continue.

Do not inspect Task `results/`, dispatch Discovery, or copy another Page's probe cards. PageX imports the settled Page contract and its source pointers.

## Retargeting

Reread Brief, load the new venue pack, and preserve only venue-independent principles that still serve the promise. Rewrite strategy, arc, components, variants, safety rails, and Artifact handoffs as required. Existing Artifacts become revision inputs, not authority over the new design.

## Runtime shape

```text
<InterventionPage>/
├── <InterventionPage>.md
├── pagex/       selected Insight Page bindings
├── outline/     strategy, arc, and component-map working surface
└── display/     optional mockups or architecture displays
```

Intervention owns no raw evidence, deployable output, or direct deployment action.

## Closing checks

- Every theory-of-change link and design principle names a settled Insight K/W row.
- Declined insights remain visible with reasons.
- Every component has one audience job, venue constraint, and safety rail.
- Experimental variables are separated from invariants.
- Every Artifact Page has exactly one current handoff row.
- Missing insights route to Task/Insights Board; no local Probe work exists.
- A fresh Artifact agent can execute its row without inventing global strategy.

This variant owns no scripts.
