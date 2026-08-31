# Paper Board: Cross-event normalization for CGM prediction

paper-id: Paper-CGM-CrossEventNormalization
page-type: paper-board
state: 🟡 INTAKE
owner: research team
spine: establish whether provenance-aware cross-event normalization makes heterogeneous diabetes events useful to CGM prediction.
close: the paper has a checked Narrative and checked Sections, or the direction is explicitly held with its reason recorded.
target-venue: ICLR (provisional)
target-venue-status: not yet bound to a shared Venue Page
current-journey: P0 Ideation

## Topic

CGM prediction receives events from food, exercise, medication, and insulin
records, but those event families use different identifiers, quantities, units,
and denominators.
This paper direction tests whether a common five-slot packet and a separate
`IDENTITY` / `QUANTITY` evaluation make those events more useful to a CGM model.
The source sessions provide a strong hypothesis and a starting set of artifacts,
but the novelty and downstream payoff are still open.

## Pipeline

```text
🧠 ideation  ──▶  🌱 seed  ──▶  🗺 roadmap  ──▶  📥 collection
                                             │
                                             ▼
                                  🧭 ICLR narrative
                                             │
                                             ▼
                                      📄 sections
```

The current board stops at Ideation.
Tasks and Discovery pages will own execution and evidence receipts after the
Seed is minted.

## Purpose

This board is the durable paper-level spine for a proposed study of clinical
event normalization and CGM prediction.
It records the research direction, the evidence gates, and the route toward an
ICLR Narrative without turning session-reported probes into established claims.
The board does not execute tasks or advance a gate without a human decision.

## Page graph

```text
SD00 ideation  [current]
  -> SD01 seed       [not minted]
  -> SD02 roadmap    [not minted]
  -> SD03 collection [not minted]
  -> NA01 narrative for ICLR [not minted]
  -> sections and desk room   [not minted]
```

## Current state

- The direct paper-story source is `Raw-FoodForm` session `beae21bc-6d8b-4b68-a516-34d761f44573`.
- The upstream normalization and benchmark source is `CGM-Raw-Page-Workflow` session `19088662-a806-4498-971f-9b5b9d15ab7e`.
- The four event-normalization families and their benchmark artifacts are
  synced locally under `_WorkSpace/0-RawDataStore/0-EventNorm/`.
- The working method hypothesis is a common five-slot event packet plus an
  `IDENTITY` / `QUANTITY` evaluation split.
- The current paper state is Ideation.
  No Seed proposition has been human-ticked or evidence-closed.

## Proposed contribution, not yet licensed

The candidate contribution is a cross-event normalization protocol that makes
event identity, quantity, denominator, source, and confidence explicit, then
tests whether this representation makes heterogeneous events usable in CGM
prediction.

The strongest proposed result is the downstream payoff experiment.
The current source session reports a large gap between the physiological CGM
response to an extra-large meal and the response predicted from the existing
event channel.
That gap is a probe and not a board-level result until the rerun lands with an
exact task, split, model, metric, and QA receipt.

## Gates

- G0: open.
  The idea has a human request to build the ICLR paper, but claim-level novelty
  receipts and a decisive pilot are not yet recorded.
- G1-G7: not applicable yet because the Seed and later Pages do not exist.

## Pages

### A1-SD-story · venue-free story
SD00-ideation.md

## Files

- `A1-SD-story/SD00-ideation/SD00-ideation.md` - current direction and idea record.
- `../README.md` - project intake summary and source paths.
- `_WorkSpace/0-RawDataStore/0-EventNorm/` - local event-normalization contracts,
  examples, corpora, and benchmark runs.
- `examples/Proj1-CGM-RawData/diagram/01-DataBoard-260818/` - local DataBoard
  and source analysis.

## Human decisions required later

- Confirm the claim-level novelty delta for the `IDENTITY` / `QUANTITY` split.
- Decide whether the decisive downstream experiment supports an ICLR-level
  method claim or a narrower benchmark paper.
- Confirm the releasable benchmark boundary for WellDoc-derived vocabulary and
  patient data.
- Bind the ICLR Venue Page and create the ICLR Narrative only after the Seed
  gate is satisfied.

## Lifecycle receipts

- OUTLINE: drafted from the two named Claude Code sessions and local artifacts.
- PROBE: open; no independent novelty or pilot QA receipt yet.
- EVIDENCE: open; source session values remain session-reported.
- DRAFT: current board and ideation page created.
- CHECK: open; human confirmation is still required before the Seed gate.

## Log

- 2026-08-24 - Created the local paper scaffold from the requested ICLR
  direction using the current `haipipe-paper` P0 Ideation contract.
