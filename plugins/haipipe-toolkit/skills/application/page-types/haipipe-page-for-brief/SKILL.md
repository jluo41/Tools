---
name: haipipe-page-for-brief
description: >-
  The Page Type contract for the one BRIEF Page that heads a DesignBoard. It fixes the opportunity, audience set, behavior/outcome, venue scope, promise, the insight needs this Application raises, optional core PageX inputs, and the Design Page roster. The data inventory it used to carry moved to the InsightBoard's Meta Page on 260820. Use when starting or retargeting an Application, deciding what must be understood before design, folding legacy Seed/Venue/Pitch decisions, or checking which Design work the Application authorizes. Trigger: application brief, design brief, audience roster, behavior change, venue scope, insight needs, design roster, page-type brief, /haipipe-page-for-brief.
metadata:
  version: "0.3.0"
  last_updated: "2026-08-20"
  summary: "Heads the DesignBoard: delivery framing plus the needs it raises; the source inventory and insight roster moved to haipipe-page-for-meta."
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "opportunity → audience set → behavior/outcome → venue scope → promise → insight needs raised → core PageX inputs → Design roster"
---

# /haipipe-page-for-brief · define what this Application is building, and for whom

Load `haipipe-page` first and `haipipe-plugin-pagex` when resolving already accepted core inputs.

Declare `page-type: brief`. One Brief exists per DesignBoard.

## What moved out on 260820

This Page used to carry eight divisions serving two different readers: 1-5 said what we are building, 6-7 said what data we have and what we must understand. JL split the Application into two boards, and the Brief split on its own seam.

```text
STAYS HERE · delivery framing        MOVED · haipipe-page-for-meta
─────────────────────────────        ──────────────────────────────────────
opportunity · audience · outcome     the source inventory, grain, population,
venue scope · promise                window, freshness, known limits
the needs this board RAISES          the roster of which Insight Page ANSWERS each
```

The Brief still raises needs, because a need is a delivery-side statement of what design cannot proceed without. It no longer tracks their answers; the rung question registers (`MT01`-`MT04`) do, so each row has one writer.

## Boundary

```text
Brief          why this Application exists and which design work it authorizes
Meta Page      what data exists, on the InsightBoard
Insight Page   Task-backed D→I→K→W for one raised need, on the InsightBoard
Design Page    one audience × behavior job × primary venue, on this board
```

Brief frames needs; it does not perform DIKW and does not prescribe the answers Insight Pages must reach. It owns no `probe/`.

## Fixed Content outline

```text
### 1 · Opportunity
### 2 · Audience Set and Behavior
### 3 · Outcome and Kill Criteria
### 4 · Venue Scope
### 5 · Promise
### 6 · Insight Needs Raised
### 7 · Core PageX Inputs
### 8 · Design Roster and Handoff
```

- **Opportunity** bounds the problem and why an Application is warranted now.
- **Audience Set and Behavior** names the people, contexts, current actions, and desired changes; one audience need not own the whole board.
- **Outcome and Kill Criteria** makes success, guardrails, and abandonment observable.
- **Venue Scope** pins one or more allowed delivery channels without designing their messages.
- **Promise** states the ceiling the Application may offer.
- **Insight Needs Raised** gives each required understanding a stable id, a one-line question, a target DIKW level, the affected audience/job, and the blocked Aim. It carries no answer and no preferred result. The matching question register records which page took each id, and the board rollup lives on the wisdom register's Queue.
- **Core PageX Inputs** binds already accepted Pages that apply across the board. A candidate is not a binding.
- **Design Roster and Handoff** releases the initial Design Page roster, one row per audience × behavior job × primary venue.

## Runtime shape

```text
<application-root>/<DesignTopic>-DesignBoard/0-BR-brief/BR00-brief/
├── BR00-brief.md
└── pagex/       accepted core Page inputs only
```

## Closing checks

- Opportunity, audience set, behavior, outcome, kill criteria, and venue scope are visible.
- Every load-bearing premise is either an accepted PageX input or a raised Insight Need.
- No Insight Need contains a preferred answer.
- Every raised need has a stable id a question register can key on (`QD`/`QI`/`QK`/`QW`).
- Every planned Design Page names one audience, behavior job, and primary venue.
- No source inventory, grain table, or freshness row remains on this Page.
- A fresh Insight or Design agent can start from Division 8 without reading legacy stages.

This variant owns no scripts.
