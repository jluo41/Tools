---
name: select
part-of: hai-ideation
description: >-
  Stage 3 of HAI Ideation: compare tested Idea Cards, preserve rejected and
  deferred history, present an evidence-bound recommendation, record the
  person's idea-and-target decision, and build the pointer-only Paper P0
  handoff. Use when deciding which research idea and journal target to pursue.
metadata:
  version: "0.1.5"
  last_updated: "2026-10-26"
  capability_family: "3_select"
---

# /hai-ideation select · portfolio to human decision

Load `hai-ideation`, its receipt contract, the Stage 2 test matrix, every
candidate Idea Card, the linked Venue Fit Cards, and the latest
`projection/paper-ideation-sync.yaml`. This skill owns portfolio comparison,
the sole human decision capture, and the final Paper adapter. It does not
improve weak evidence by scoring it, choose on the user's behalf, or write
Paper prose.

For a durable commission, use the owner-bound Run Specs in
`../../references/workflow-runs.md`. This capability's checks
are internal Steps unless separately commissioned under that contract.

## New durable layout

Read `../../references/idea-block.md`. A direction is a Block; each admitted
idea is a Job with one canonical Card. Its Tasks are evaluation/development
questions, and skills are methods within them. A new Job may remain unbound
to Paper through selection. Existing multi-card Task portfolios keep their
original paths and gates.

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
5. Record explicit defer/abandon answers with their reasons. Keep unanswered
   cards open; absence from selected_cards is not a disposition;
   never delete it or reuse its stable id.
6. For each selected Idea Job, record its destination `paper_block` and
   `story_path` and write the pointer-only handoff. Normally each Job gets
   its own Paper Block. The Paper owner creates/binds it after the gate.
   Existing Paper-local portfolios keep their distinct Story routes. An
   explicit split/merge preserves all contributing Jobs and decisions.

Before the person decides, write the machine comparison only into the sync
packet's `portfolio_recommendation`. Do not invent a separate durable
recommendation file. Only when a Paper is already bound or explicitly
requested, ask `hai-paper-ideation` to project that revision into
the same evergreen P0 cockpit through the current Page update boundary. A
working-projection refresh does not publish adopted Page Content or delivery;
the I3 receipt remains the sole selection authority and the sync does not
allocate an `rpNN` Page Run.

## Human receipt

Use the version-3 schema and history/projection mapping in
`../../references/receipts.md`. Record reviewed_cards and one
candidate row per reviewed card. Ask for any missing disposition; unanswered
cards stay open. Selected rows each own their posture, risks, five assertions,
exact target/category/contract version, and Story route. Compatibility lists
are derived from those rows.

Only explicit answers may become human dispositions. Save an immutable
selection snapshot and an identical current workflow/selection.yaml view,
then refresh Card/Venue Fit projections from that snapshot. A missing person,
date, target, stale contract, unaccepted risk or projection mismatch keeps the
affected decision open. Old decisions remain readable and are never silently
rewritten.

## Paper handoff

Write `handoff/paper-ideation.yaml` using the shared receipt schema. Carry
only IDs, statuses, interpretations, paths, the latest sync packet/revision,
exact target/category, accepted conditions, and hard limits. Do not copy
Result text, Bib entries, raw data, or venue rules. After the handoff gate
passes, load `hai-paper-ideation` to project the authoritative I3 receipt
into the destination Paper and open its Story route. A new Idea Job
   does not need an existing P0 Page to pass selection; its exact I2 revision,
   scientific gates and explicit human receipt are still required.

Run the shared checker with `--gate select`, then `--gate handoff`. The checker
checks per-card eligibility, target contracts, exact selection/handoff joins
and current sync bindings; only the named person can make
the decision.

## One-off mode

For an inline comparison, return the complete portfolio and recommendation,
then ask for the user's decision. Do not claim a selection until the user has
actually supplied it.
