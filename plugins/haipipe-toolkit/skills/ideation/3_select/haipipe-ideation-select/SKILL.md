---
name: haipipe-ideation-select
description: >-
  Stage 3 of HAI Ideation: compare tested Idea Cards, preserve rejected and
  deferred history, present an evidence-bound recommendation, record the
  person's idea-and-target decision, and build the pointer-only Paper P0
  handoff. Use when deciding which research idea and journal target to pursue.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.0"
  last_updated: "2026-09-08"
  capability_family: "3_select"
---

# /haipipe-ideation-select · portfolio to human decision

Load `haipipe-ideation`, its receipt contract, the Stage 2 test matrix, every
candidate Idea Card, the linked Venue Fit Cards, and the latest
`projection/paper-ideation-sync.yaml`. This skill owns portfolio comparison,
the sole human decision capture, and the final Paper adapter. It does not
improve weak evidence by scoring it, choose on the user's behalf, or write
Paper prose.

## Comparison surface

Present every admitted candidate, including candidates recommended for
deferral or abandonment:

| Axis | Required reading |
|---|---|
| scientific delta | claim-level remaining novelty after closest work |
| identification | separate credibility and fatal assumptions |
| feasibility | data access, pilot/waiver, cost, clock, ethics |
| publication fit | best current target/category, desk risk, fallback |
| repair burden | evidence or design work needed before execution |
| downside | likely referee rejection and failure interpretation |

Do not compute a composite score that hides an off-fit, unverified claim, or
fatal assumption. An optional comparison order is a review aid only.

## Decision protocol

1. Verify that every candidate's test states resolve to canonical evidence or
   an explicit HOLD.
2. Give a machine recommendation for each: `proceed`,
   `proceed-with-caution`, `defer`, or `abandon`, with the decisive reasons.
3. Present a small portfolio view: strongest scientific candidate, lowest-risk
   executable candidate, ambitious venue route, realistic route, and fallback
   when those roles are supported. These are roles, not automatic rankings.
4. Ask the person to select none, one, or several Ideas and, for every
   selected Idea, one intended target and article category. Record accepted
   conditions for `PROCEED WITH CAUTION`.
5. Preserve every nonselected card as deferred or eliminated with its reason;
   never delete it or reuse its stable id.
6. Allocate one distinct Story route per selected card and write the
   pointer-only handoff. Multiple selected Ideas do not become alternatives
   inside one Story.

Before the person decides, write the machine comparison only into the sync
packet's `portfolio_recommendation`. Do not invent a separate durable
recommendation file. Ask `haipipe-paper-ideation` to project that revision into
the same evergreen P0 cockpit.

## Human receipt

The receipt records:

```yaml
version: 2
kind: ideation-selection
ideation_task: bNN.jNN.tNN
direction_card: cards/direction.yaml
decision: select | defer | abandon
selection_posture: proceed | proceed-with-caution | not-applicable
selected_cards: [cards/i01_idea.yaml]
story_routes:
  - card: cards/i01_idea.yaml
    story_role: Story-A
    story_path: "path or planned path"
target_routes:
  - card: cards/i01_idea.yaml
    target: "journal"
    category: "article type"
    venue_contract: "path"
by: "person:<identifier>"
at: "ISO-8601"
accepted_risks: []
assertions:
  evidence_complete: true | false
  novelty_reviewed: true | false
  feasibility_receipt_or_waiver: true | false
  venue_fit_reviewed: true | false
  target_selected: true | false
reason: "bounded decision rationale"
```

A missing name/date, unresolved target/category, stale Venue contract, or
machine-only recommendation keeps the receipt open.

This receipt is the single selection authority. Paper P0 may display its
verdict, target, and `went to` values, but Page approval or CHECK cannot create
or replace them.

## Paper handoff

Write `handoff/paper-ideation.yaml` using the shared receipt schema. Carry
only IDs, statuses, interpretations, paths, the latest sync packet/revision,
exact target/category, accepted conditions, and hard limits. Do not copy
Result text, Bib entries, raw data, or venue rules. After the handoff gate
passes, load `haipipe-paper-ideation` to project the authoritative I3 receipt
into the existing P0 Page and open distinct Story routes.

Run the shared checker with `--gate select`, then `--gate handoff`. The checker
can establish that the receipt and paths exist; only the named person can make
the decision.

## One-off mode

For an inline comparison, return the complete portfolio and recommendation,
then ask for the user's decision. Do not claim a selection until the user has
actually supplied it.
