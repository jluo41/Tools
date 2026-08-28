---
name: haipipe-page-for-design
description: >-
  The Page Type contract for an Application DESIGN PAGE on the DesignBoard, machine key `page-type: design`. This page lives in `<DesignBoard>/2-DS-design/DS<NN>-<slug>/`, one page per audience x behavior job x primary venue. A DesignBoard may own many Design Pages; each serves one audience × behavior job × primary venue, consumes the Brief and settled InsightBoard Design Handoffs through PageX, then authors principles, a message/unit map, repeated message divisions, variants, rails, and a per-division acceptance row. The Page ENDS AT ACCEPTED: it never ships and never measures. Use for SMS/email/dashboard/checklist/report/message design, audience-specific strategy, message sequences, interaction components, or retargeting. Trigger: design page, message strategy, audience job, message map, message divisions, component map, variants, accept a unit, page-type design, /haipipe-page-for-design.
metadata:
  version: "0.6.1"
  last_updated: "2026-08-24"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
  outline:
    mode: grammar
    source: "accepted Brief + PageX Insight handoffs + venue pack"
    shape: "design contract → insight use → principles → unit map → repeated message/unit divisions → rails → render/acceptance"
---

# /haipipe-page-for-design · design one audience/job delivery system

Load `haipipe-page`, `haipipe-page-for-brief`, `haipipe-plugin-pagex`, and the selected venue pack. Declare `page-type: design`. This page lives in `<DesignBoard>/2-DS-design/DS<NN>-<slug>/`, one page per audience x behavior job x primary venue.

The key was `page-type: intervention` until 260820, with "Design Page" as a separate user-facing word. JL retired the double naming: one concept carries one word, because two names for one page is what made readers ask whether Design and Artifact were the same thing.

A DesignBoard may own many Design Pages. The default grain is:

```text
one audience or recipient class × one behavior job × one primary venue
```

Split when two designs can be accepted, retargeted, or reopened independently.

## Boundary

```text
Brief          DesignBoard scope, promise, Design roster
direction/     the card: stance · thesis · wager · and `grant:`, which NAMES
               InsightBoard pages inside the board's `reads:`
Principle      because <W>, do <move>, within <rail> · exists only when PROMOTED
               (reused by two or more Design pages, or adjudicating two boards
               in conflict) · then it is the warrant those pages cite
Design Page    message roles, content, rails, render, acceptance · each division
               warrants from its CARD's stance, or from a promoted principle;
               its prose never re-derives a finding from a W/D/I/K page
─────────────────────────────────────────────────────────────────────────────
NOT this Page  building it · shipping it · running the experiment · collecting data
```

**Warrant and grant are different things, and 0.5.0 conflated them.** A WARRANT says why a division may exist; since the 260824 demotion it rides inline on the card's `stance:` by default, and moves onto a P page only when promotion earns one. A GRANT says what an arm-agent may quote while composing, and it must name InsightBoard pages by path, because an agent cannot be handed a rule and asked to quote a rate. An exploration card is the clearest case: it exists to resolve a named uncertainty, and that uncertainty lives on a K row no principle restates. The chain reads `board reads:` ⊇ `card grant` ⊇ `unit evidence.md`, and it governs the grant only.

Design performs composition, not evidence settlement. It owns `pagex/` and no `probe/`. Since 0.5.0 it owns TWO plugins of its own (JL 260824): `direction/` (haipipe-plugin-direction), the strategy cards proposed before any artifact and released only by a person; and `design/` (haipipe-plugin-design), the artifact units, one per released card, written by one arm-agent each. Every unit-citing division carries a `stance:` taken verbatim from its card, and a division without a stance is illegal. The wager terms (expected effect, falsification line) live on the card only; the page and the unit cite, never restate.

**This Page ends at ACCEPTED (JL 260820).** Deciding that an exact version may go is a design judgment and belongs here. Building it, shipping it, running the A/B, and collecting what came back are separate work owned by the task layer. A Design Page has no deploy record and no round folder.

## Content grammar

Every Design Page realizes these roles; venue decides the exact titles and repeated unit form:

```text
Design contract       audience · behavior job · context · primary venue · success condition
Principle Use Map     adopted/declined P pages and applicability reasons
Design moves          how each adopted P<n> lands in THIS venue
Message/Unit map      ordered roles, trigger/timing, job, invariant, allowed variable
R<n> unit divisions   one message, touchpoint, panel, checklist block, or report section per division
Cross-unit rails      coherence, escalation, prohibited moves, uncertainty language
Render                the exact visible version of the system
```

Each repeated unit division carries:

```text
unit id · recipient moment · audience job · Insight/Handoff refs · design move
exact content or interaction · declared variants · safety rail · next trigger
accepted: <reviewer> <YYMMDD> · handoff <W-id>@v<N> · render v<N>
```

A division may instead close by RAISING what it lacks (haipipe-design-workflow's EMIT edge, 260827): `emitted: <YYMMDD> · <BR00 need id> · <what was missing>` — a terminal equal in rank to `accepted:`, whose need row on BR00 births the register question need-first. A division carries exactly one of the two terminals, never both.

Do not create empty Narrative or Display divisions. Use one division per jointly reviewed message/unit.

## Acceptance is per division, not per page

`page-type: artifact` was retired on 260820. It held six Content roles and five of them already existed inside a unit division; the only genuine difference was where a reviewer's name and date got written. A whole Page Type to relocate one signature is not a Page Type.

```text
RETIRED · a second Page                 CURRENT · a row on the division
─────────────────────────               ───────────────────────────────────
3-artifacts/A01-<unit>/A01.md           R4 · abtest arm
  page-type: artifact                     accepted: JL 260818
  Acceptance: reviewer/date/versions      handoff W01@v1 · render v5
```

One division may be accepted while a sibling is mid-revision, which is the case the retired type existed for. The Page's own `state:` line reports the system; each division's row reports the unit. A changed handoff, content edit, venue constraint, or re-render clears the affected division's `accepted:` row and only that row.

Renders live in this page's own `render/` plugin, not in a board-level folder. A render is derived from a division and is what a human reads before writing the `accepted:` row, so it exists BEFORE acceptance rather than after it.

## PageX-only input boundary

```text
Brief Page ───────────── PageX ─┐
settled Insight Handoff ─ PageX ─┼─▶ Design Page
accepted prior Design ─── PageX ─┘
```

PageX binds exact files and scopes, and it crosses boards unchanged because it binds by path: a DesignBoard page borrows a settled Design Handoff, through its principle, the same way it borrows a local file. Write the path in the source board's CURRENT layout, which `ref/partition.md` decides: `.../1-F-full/FW01-<slug>/FW01-<slug>.md#5` on a partition-major board, `.../4-W-wisdom/W01-<slug>/W01-<slug>.md#5` on a rung-major one. A board that is restructured moves every one of these, so a relayout is a cross-board edit and not a local one. The Insight Use Map records why they apply here. Never inspect Task `results/`, dispatch Discovery, or copy an Insight Page's Probe cards.

## Runtime shape

```text
<application-root>/<DesignTopic>-DesignBoard/2-DS-design/DS<NN>-<audience>-<job>/
├── DS<NN>-<audience>-<job>.md    the page, named for its own folder
├── direction/       strategy cards · haipipe-plugin-direction
├── design/          artifact units · haipipe-plugin-design
├── render/          the unit as the recipient sees it · read BEFORE accepting
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
- Every accepted division names reviewer, date, handoff version, and render version.
- A changed input cleared the affected division's acceptance and left its siblings alone.
- Missing premises route to an InsightBoard Insight Page; no local Probe exists.
- No deployment record, shipment log, or measurement round appears on the Page.

This variant owns no scripts.
