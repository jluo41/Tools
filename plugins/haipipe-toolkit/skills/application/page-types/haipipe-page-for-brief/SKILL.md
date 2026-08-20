---
name: haipipe-page-for-brief
description: >-
  The Page Type contract for the one BRIEF Page of an Application Board. It fixes the opportunity, audience set, behavior/outcome, venue scope, promise, Insight Need Map, optional core PageX inputs, and roster/handoff for Application-local Insight and Design Pages. Use when starting or retargeting an Application, deciding what must be understood before design, folding legacy Seed/Venue/Pitch decisions, or checking which Insight/Design work the Application authorizes. Trigger: application brief, intervention brief, audience roster, behavior change, venue scope, insight need map, design roster, page-type brief, /haipipe-page-for-brief.
metadata:
  version: "0.2.0"
  last_updated: "2026-08-20"
  summary: "One Brief frames the Application and releases local Insight needs before audience/job Design Pages begin."
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "opportunity → audience set → behavior/outcome → venue scope → promise → Insight Need Map → Design roster/handoff"
---

# /haipipe-page-for-brief · define what this Application must understand and design

Load `haipipe-page` first and `haipipe-plugin-pagex` when resolving already accepted core inputs. Load `haipipe-page-for-stage` only for a legacy runtime.

Declare `page-type: brief`. One Brief exists per Application.

## Boundary

```text
Brief          why this Application exists and which insight/design work it authorizes
Insight Page   Task-backed D→I→K→W for one Brief need
Design Page    one audience × behavior job × primary venue
Artifact       exact projection or independently promoted unit
```

Brief frames evidence needs; it does not perform DIKW or prescribe the answers local Insight Pages must reach.

## Fixed Content outline

```text
### 1 · Opportunity
### 2 · Audience Set and Behavior
### 3 · Outcome and Kill Criteria
### 4 · Venue Scope
### 5 · Promise
### 6 · Insight Need Map
### 7 · Core PageX Inputs
### 8 · Insight and Design Handoff
```

- **Opportunity** bounds the problem and why an Application is warranted now.
- **Audience Set and Behavior** names the people, contexts, current actions, and desired changes; one audience need not own the whole Board.
- **Outcome and Kill Criteria** makes success, guardrails, and abandonment observable.
- **Venue Scope** pins one or more allowed delivery channels without designing their messages.
- **Promise** states the ceiling the Application may offer.
- **Insight Need Map** gives each required understanding a stable id, question, target DIKW level, affected audience/job, and blocked Aim.
- **Core PageX Inputs** binds already accepted Pages that apply across the Application. A candidate is not a binding.
- **Insight and Design Handoff** releases local Insight Pages and the initial Design Page roster.

## Runtime shape

```text
<application-root>/0-brief/A00-brief/
├── A00-brief.md
└── pagex/       accepted core Page inputs only
```

Brief owns no `probe/`. An unsettled need releases or resumes an Application-local `page-type: insight` Page under `1-insights/`.

## Closing checks

- Opportunity, audience set, behavior, outcome, kill criteria, and venue scope are visible.
- Every load-bearing premise is either an accepted PageX input or a named Insight Need.
- No Insight Need contains a preferred answer.
- Every planned Design Page names one audience, behavior job, and primary venue.
- A fresh Insight or Design agent can start from Division 8 without reading legacy stages.

This variant owns no scripts.
