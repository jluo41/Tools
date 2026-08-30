---
name: subjective-label-workflow
description: >-
  The crossing machine of the subjective-label family: declares the six phase
  names P0-P5 and the seven gates G0-G6, tests Label Handoff validity, decides
  which side is runnable, routes invalidation between sides, and dispatches one
  bounded action to label-building-workflow or label-scanning-workflow. It owns
  no step order, no semantic rule, no item judgment, no executor prediction,
  and no audit verdict. Use when asking where a labeling job is, whether it may
  cross, why it is blocked, or /subjective-label-workflow.
---

# /subjective-label-workflow · the numbers, the gates, the crossing

Load `subjective-label` first. This file is the only place phase numbers and
gate numbers are declared. The side workflows (`label-building-workflow`,
`label-scanning-workflow`) own the order inside a phase; the doors
(`label-building`, `label-scanning`) own the law.

## Terminology law

A **journey phase** is one of P0-P5 and is named by its authority artifact. A
**step** is an action inside a phase and is named by the side workflow that
orders it. A **gate** is an assertion over named existing artifacts. A **route**
is a gate's outcome. If a proposed phase cannot name an authority artifact of
its own, it is a step, a gate, or a route. No file other than this one may
introduce a phase number or a gate number.

## Six phases, two sides

```text
🏗 Building side                 authority artifact
P0 Contract                      config.yaml + corpus/manifest.json + test/sealed/status.json
P1 Round × N                     rounds/round_<t>/checkpoint.json
P2 Freeze                        handoff/label-v1.yaml
        ───────────── the crossing: one immutable Label Handoff ─────────────
🔍 Scanning side
P3 Test                          test/final/lock.json + evaluation/summary.md
P4 Scan                          production/run_<n>/manifest.yaml
P5 Audit                         audit/final_<n>/receipt.json → corpus/final/D_star.jsonl
```

Building mirrors the Application family's Insight lane (scope, loop, export);
Scanning mirrors its Design lane plus an independent verifier (frame, execute,
verify). One artifact never answers both sides' questions.

## Seven gates, one line each

```text
G0 Contract → Round    the five Contract files exist and rehash; sealed ids are outside the development pool
G1 Round close         checkpoint.json closed by the Keeper with every check passing (label-building-workflow §CLOSE)
G2 Round → Freeze      quality floor + stability streak + coverage (no open register cell, or one the human accepted) + risk, on comparable checkpoints; custody valid; human signature on exact G* and D_cal*; handoff written and rehashed
G3 Freeze → Test       handoff valid and current; evaluation/registry.yaml frozen before any protected text release
G4 Test → Scan         test/final/lock.json precedes every prediction run; every run closed before scoring; one route passes every floor, or an explicit human-only route is frozen
G5 Scan → Audit        one terminal disposition per in-scope id, none duplicated or missing; risk queue reconciled; audit design frozen before the auditor sees production labels
G6 Audit → Complete    blind probability audit valid; findings and intervals recorded; protected strata checked; repairs closed; D* manifest links every upstream checksum; any limitation explicitly accepted
```

A gate that depends on prose, elapsed time, model consensus, or an absent file
is not passable. The checklists behind G0-G2 live in `label-building-workflow`,
behind G3-G6 in `label-scanning-workflow`.

## The crossing

The Label Handoff is valid when `status: valid`, no invalidation descendant
exists, and every bound checksum rehashes. Scanning binds the handoff checksum
in each run manifest and never follows `policy/current`. Read
`../../ref/ref-label-handoff.md` for fields.

## Routes between sides

```text
P1 → P1         another round, justified by a named open register cell
P1 → P2         G2 passes
P2 → P3         handoff valid
P3 → HOLD       no executor qualifies and no human-only route is frozen
P3 → P1         scoring exposes a semantic defect; consumed T* becomes development evidence; new lineage
P4 → P5         G5 passes
P5 → P4         rescan under a new production manifest
P5 → P5         repair, then a new audit receipt
P5 → P1         semantic failure; new lineage; downstream claims invalidated
P5 → complete   G6 passes
```

Every backward route appends an invalidation receipt naming the changed
component, the affected scorecards, runs, audits and claims, and the required
new lineage, handoff, test, scorecard, scan or audit. No closed artifact is
rewritten in place.

## Receipt chain

```text
G0 corpus/manifest.json    G1 checkpoint.json        G2 handoff/label-v1.yaml
G3 evaluation/registry.yaml  G4 evaluation/summary.md  G5 production/run_<n>/run_report.md
G6 audit/final_<n>/receipt.json
```

Phase is derived from the highest gate whose artifacts rehash and whose human
ticks exist. `.state.json`, `REPORT.md` and every `view/` file are convenience
views; a view that disagrees with a receipt loses.

## Dispatch

```text
resolve   one corpus snapshot × one target job
derive    the Building frontier from checkpoints, the Scanning frontier from run receipts,
          handoff validity from the crossing
select    the single runnable phase, or the blocking human gate, or HOLD
hand      P0-P2 → label-building-workflow · P3-P5 → label-scanning-workflow
fold      advance only when the owning receipt exists and its gate passes
stop      at a human gate, HOLD, invalidation, step limit, or completed action
```

## Return

Return both frontiers, the bound handoff checksum or its absence, the first
failed gate assertion, the human decision owed, and exactly one next runnable
action with the side workflow that owns it.
