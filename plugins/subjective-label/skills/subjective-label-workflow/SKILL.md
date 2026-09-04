---
name: subjective-label-workflow
description: >-
  The crossing machine of the subjective-label family: declares the six phase
  names P0-P5 and the seven gates G0-G6, tests Label Handoff validity, decides
  which side is runnable, routes invalidation between sides, and dispatches one
  bounded action to label-building-workflow or label-scanning-workflow. It owns
  no step order, no semantic rule, no item judgment, no executor prediction,
  and no audit verdict. It publishes the family's Phase × Run Map. Use when asking where a labeling job is, whether it may
  cross, why it is blocked, or /subjective-label-workflow.
metadata:
  version: "0.8.0"
  last_updated: "2026-09-01"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
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
its own, it is a step, a gate, or a route. Other files USE these numbers as names;
no file other than this one may DEFINE one or attach a different meaning to it.

## Six phases, two sides

```text
🏗 Building side                 authority artifact
P0 Contract                      config.yaml + corpus/manifest.json + test/sealed/status.json
                                 + register.md + policy/versions/G_00/manifest.yaml
P1 Round × N                     rounds/round_<t>/checkpoint.json
P2 Freeze                        handoff/label-v1.yaml
        ───────────── the crossing: one immutable Label Handoff ─────────────
🔍 Scanning side
P3 Test                          evaluation/summary.md (which cites test/final/lock.json)
P4 Scan                          production/run_<n>/manifest.yaml
P5 Audit                         audit/final_<n>/receipt.json → corpus/final/D_star.jsonl
```

Building mirrors the Application family's Insight lane (scope, loop, export);
Scanning mirrors its Design lane plus an independent verifier (frame, execute,
verify). One artifact never answers both sides' questions.

## Phase × Run Map

This is the workflow-level index required by `haipipe-run`. Phase owns purpose,
authority, gate, and handoff; episode groups; each listed operation may allocate
independently closable Run instances.

| Phase | Folder / Episode | Phase purpose | Allowed Run operations | Cardinality | Gate / authority | Close / handoff |
|---|---|---|---|---:|---|---|
| P0 Contract | contract | establish one fenced job | `corpus-contract` ×1 · `discovery-search` ×D · `guideline-seed` ×1 · `test-reserve` ×1 · `embedding-build` ×1 | D + 4 | G0 · identified human confirms meaning | bound P0 + G0 receipts |
| P1 Round × N | `round_<t>` | learn and test the human meaning | per round: `round-prepare` ×1 · `weak-prelabel` ×W_r · `human-calibration` ×1 · `guideline-learn` ×1 · `round-measure` ×1 · `round-close` ×1 | 5N + sum(W_r) | G1 checkpoint · G2 human STOP | closed checkpoint and G_t/D_t |
| P2 Freeze | freeze | package the stopped Building lineage | `handoff-freeze` ×1 | 1 | exact human FREEZE signature · G3 | valid `handoff/label-v1.yaml` |
| P3 Test | `test_<n>` | qualify one frozen executor route | `test-gold-lock` ×1 · `executor-predict` ×K · `executor-score` ×K · `executor-select` ×1 | 2K + 2 | blind human T* · G4 | `evaluation/summary.md` |
| P4 Scan | `production_<n>` | label the in-scope corpus under the qualified route | `scan-preflight` ×1 · `scan-shard` ×S · `risk-route` ×1 · `human-review` ×1 · `reconcile` ×1 | S + 4 | human risk queue · G5 | terminal candidate + `run_report.md` |
| P5 Audit | `audit_<n>` | verify the candidate and bound final claims | `audit-sample` ×1 · `audit-human-gold` ×1 · `audit-analyze` ×1 · `dstar-materialize` ×1 | 4 | blind audit human · limitation tick · G6 | audited D* and receipt |

```text
expected happy-path Runs = D + sum(W_r) + 5N + 2K + S + 15
```

Treat this total as a plan. Count actual Runs only from allocated Tickets with
valid runtime receipts. Round, Test, Scan, Audit, individual judgments, calls,
and bare human ticks add no umbrella rows.

## Labeling Run Profile

This phase machine owns the Labeling family extension of `haipipe-run`:

```text
ALLOWED    the 25 operation kinds in ref-run.md, across P0-P5
TARGET     one operation-specific bounded target; episodes are grouping only
TICKET     runs/<RUNNAME>.yaml, authored after its commission and inputs freeze
INPUTS     exact corpus, policy/handoff, registry, executor/wrapper, scope, and design checksums required by the operation
WORKER     the side workflow plus its declared skill, human, Keeper, CLI, API, or runner
RESULT     results/<RUNNAME>/result.yaml pointing to canonical domain artifacts
ACCEPT     the operation gate in ref-run.md; process exit alone never completes a Run
PROMOTION  only round-close, handoff-freeze, executor-select, reconcile, audit-analyze,
           or dstar-materialize may perform their declared phase binding/promotion
REOPEN     a material semantic, target, checksum, route, threshold, scope, or design change mints a new Run
```

P0-P5 may allocate independently closable operations. In particular, bounded
discovery queries, guideline creation, embeddings, each weak prelabeler,
human-calibration work, each executor prediction and score, each production
shard, risk review, and blind audit work may have distinct Runs. Round, Test,
Scan, and Audit remain episodes and add no rows of their own. Bare human
meaning/release/stop/freeze/limitation events are gates, not Runs.

Read `../../ref/ref-run.md` before any Run decision. Use its deterministic
planner for expected counts, and derive actual inventory only from allocated
Ticket/runtime envelopes. Never backfill an artifact-only history as Runs.

## Seven gates, one line each

```text
G0 Contract → Round    the five P0 files above exist and rehash; sealed ids are outside the development pool
G1 Round close         checkpoint.json closed by the Keeper with every check passing (label-building-workflow §CLOSE)
G2 Round → Freeze      quality floor + stability streak of K comparable checkpoints (K = config.yaml consecutive_rounds_k) + coverage (no open register cell, or one the human accepted) + risk; custody valid; the human's STOP signoff recorded in the last checkpoint
G3 Freeze → Test       handoff written by the Keeper, carrying the human's FREEZE signature on exact G* and D_cal*, status valid, every checksum rehashing; evaluation/registry.yaml frozen against that checksum before any protected text release
G4 Test → Scan         test/final/lock.json precedes every candidate prediction attempt; every attempt closes before scoring; one route passes every floor, or an explicit human-only route is frozen
G5 Scan → Audit        one terminal disposition per in-scope id, none duplicated or missing; risk queue reconciled; audit design frozen before the auditor sees production labels
G6 Audit → Complete    blind probability audit valid; findings and intervals recorded; protected strata checked; repairs closed; D* manifest links every upstream checksum; any limitation explicitly accepted
```

A gate that depends on prose, elapsed time, model consensus, or an absent file
is not passable. The checklists behind G0-G2 live in `label-building-workflow`,
behind G3-G6 in `label-scanning-workflow`.

## The crossing

The Label Handoff is valid when `status: valid`, no invalidation descendant
exists, and every bound checksum rehashes. Scanning binds the handoff checksum
in each Run Ticket and never follows `policy/current`. Read
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
component, the affected scorecards, Runs, audits and claims, and the required
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
derive    the Building frontier from checkpoints, the Scanning frontier from gate receipts,
          handoff validity from the crossing
select    the single runnable operation, or the blocking human gate, or HOLD
hand      P0-P2 → label-building-workflow · P3-P5 → label-scanning-workflow
          (each ORDER machine loads its LAW door first; the law is never skipped)
allocate  only when the selected operation has a frozen commission; otherwise
          report the gate without minting a Run
fold      advance only when the owning receipt exists and its gate passes
stop      at a human gate, HOLD, invalidation, step limit, or completed action
```

## Return

Return both frontiers, the bound handoff checksum or its absence, the first
failed gate assertion, the human decision owed, the current Run address or
`none`, actual allocated count, optional planned count with its assumptions,
and exactly one next runnable action with the side workflow that owns it.
