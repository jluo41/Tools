---
name: haipipe-ideation-select
description: >-
  Stage 3 of HAI Ideation: compare tested Idea Cards, preserve rejected and
  deferred history, present an evidence-bound recommendation, record the
  person's idea-and-target decision, and build the pointer-only Paper P0
  handoff. Use when deciding which research idea and journal target to pursue.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.4"
  last_updated: "2026-09-22"
  capability_family: "3_select"
---

# /haipipe-ideation-select · portfolio to human decision

Load `haipipe-ideation`, its receipt contract, the Stage 2 test matrix, every
candidate Idea Card, the linked Venue Fit Cards, and the latest
`projection/paper-ideation-sync.yaml`. This skill owns portfolio comparison,
the sole human decision capture, and the final Paper adapter. It does not
improve weak evidence by scoring it, choose on the user's behalf, or write
Paper prose.

For a durable commission, use the owner-bound Run Specs in
`../haipipe-ideation/references/workflow-runs.md`. This capability's checks
are internal Steps unless separately commissioned under that contract.

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
6. Allocate one distinct Story route per selected card and write the
   pointer-only handoff. Multiple selected Ideas do not become alternatives
   inside one Story.

Before the person decides, write the machine comparison only into the sync
packet's `portfolio_recommendation`. Do not invent a separate durable
recommendation file. Ask `haipipe-paper-ideation` to project that revision into
the same evergreen P0 cockpit through the current Page update boundary. A
working-projection refresh does not publish adopted Page Content or delivery;
the I3 receipt remains the sole selection authority and the sync does not
allocate an `rpNN` Page Run.

## Human receipt

Use the version-3 schema and history/projection mapping in
`../haipipe-ideation/references/receipts.md`. Record reviewed_cards and one
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
passes, load `haipipe-paper-ideation` to project the authoritative I3 receipt
into the existing P0 Page and open distinct Story routes.

Run the shared checker with `--gate select`, then `--gate handoff`. The checker
checks per-card eligibility, target contracts, exact selection/handoff joins
and current sync bindings; only the named person can make
the decision.

## One-off mode

For an inline comparison, return the complete portfolio and recommendation,
then ask for the user's decision. Do not claim a selection until the user has
actually supplied it.
