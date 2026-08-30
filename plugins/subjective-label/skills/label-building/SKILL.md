---
name: label-building
description: >-
  The Building-side door of the subjective-label family: establish one human's
  meaning for one vague target over one corpus, reserve a sealed final test,
  run resumable calibration rounds that select attention, seal weak-model
  guesses, collect human-first judgments, learn rules, and close checkpoints,
  then freeze G* and D_cal* into a signed Label Handoff. Use for new labeling
  jobs, calibration, human annotation sessions, boundary discovery, guideline
  revision, stopping decisions, freeze, or /label-building.
---

# /label-building · build one meaning and freeze it

`subjective-label` is the family umbrella. This sibling door owns the laws and
verbs of the Building side, symmetric to `/label-scanning`. It ends at a
signed Label Handoff and never evaluates executors or scans the remaining
corpus.

## Authority

One identified human decides class, region, semantic rules, concept revisions,
stopping signoff, and accepted risk. The strong calibration agent controls the
interaction order and records inspectable human input; it cannot create gold or
accept its own rule proposal.

Weak executors are independent diagnostic readers. Their sealed predictions may
select challenge cases and expose guideline failures after the human-first lock.
Agreement is a sampling stratum, never gold.

## The Building side

```text
P0 Contract (scope)
      ↓
P1 Round (calibrate) ↺
      ↓ stopping gates pass
P2 Freeze (sign)  ──▶ Label Handoff ──▶ Label Scanning
```

`Contract`, `Round`, and `Freeze` are journey phases because each has an
authority artifact: the closed config plus corpus manifest, one closed
checkpoint, and `handoff/label-v1.yaml`. Freeze opens no new content authority:
it signs and packages artifacts that are already closed.

## Contract

The Contract authority is the closed job configuration plus corpus manifest.
Before any semantic development:

1. validate stable ids, text, target population, and corpus checksum;
2. record the vague trait seed and identified human authority;
3. declare class, region, uncertainty, and unresolved schemas;
4. reserve final-test identifiers through the Test Custodian without exposing
   their ids or text to development agents;
5. create the canonical artifact scaffold and retrieval cache provenance.

The contract creates no gold and makes no claim that the guideline is mature.

## One calibration round

A round is one resumable unit from a closed `G_(t-1)`/`D_(t-1)` to one closed
checkpoint. The verbs below are steps, not journey phases:

```text
PREPARE   pick attention → seal independent weak predictions
JUDGE     human-first decision → immutable lock → reveal → final decision
LEARN     propose minimal rules → resolve backward impact → measure evidence
CLOSE     checkpoint D_t/G_t → another round, freeze, or HOLD
```

### PREPARE

- Round 1 draws a declared random development sample and has no prelabels or
  inherited regions.
- Later rounds retrieve a broad candidate pool around all seven regions,
  novelty, sparse coverage, risk, and unresolved cases.
- Freeze a human batch containing challenge cases plus a probability or weighted
  consensus-audit arm.
- Run registered weak executors independently under the prior closed policy and
  seal their predictions before any human-first event.

### JUDGE

For every item, show item text and the prior closed policy without weak outputs;
record human-first class, region, uncertainty, evidence, and rejected alternative;
lock that event; then reveal structured comparisons when useful and record the
human's final decision. Classify a change as correction, clarification, concept
revision, or unresolved. Unresolved is never `NONE`.

Calibration Sessions are item-resumable. Never replay a completed human-first
event or reopen a seal merely because a chat ended.

### LEARN

Turn accepted human evidence into the smallest general policy change. Separate
semantic, procedural, casebook, wrapper, and editorial edits. Show the human
every substantive rule and affected prior label; the human accepts, rejects, or
narrows it. Report representative audit evidence separately from adaptively
selected challenge evidence.

### CLOSE

The Checkpoint Keeper verifies completeness, blinding, leakage, regression,
coverage, risk, and checksums. Only a closed checkpoint promotes cumulative
human gold and a policy version. Route to:

```text
another round   a declared gap remains worth the human cost
freeze          quality, stability, coverage, risk, and human signoff all pass
HOLD            evidence, implementation, or human authority is missing
```

"Another round?" is a route, never a phase.

## Freeze

The Label Handoff Keeper rehashes the exact `G*` and `D_cal*`, confirms
sealed-test custody with the Test Custodian, records the human's signature
naming those checksums and the lineage, and writes `handoff/label-v1.yaml`
once. That signature is a second, later human tick: the stopping signoff
recorded at CLOSE approves stopping, it does not sign the handoff. Read `../../ref/ref-label-handoff.md` for the fields and the creation
gate. A handoff is valid only when every stopping gate passed for the configured
consecutive comparable checkpoints and the signature names the exact lineage.

## Human gates

```text
meaning       the human confirms the target and schema            (P0)
item          the human creates each first/final judgment          (P1)
rule          the human accepts each substantive semantic patch    (P1)
freeze        the human signs the exact G* and D_cal* checksums    (P2)
```

A batch-selection charter may pre-authorize mechanical sampling classes for one
bounded run. It cannot pre-authorize item labels, semantic rules, or freeze.

## Verbs

```text
enter | status      resolve the Building frontier from closed artifacts
start | contract    establish or resume P0 without creating gold
round               run or resume exactly one P1 round
prepare             pick the batch and seal predictions for the open round
judge | label       resume item-level human-first Sessions
learn | rules       propose and adjudicate policy changes
checkpoint | next   close the round and record its route
freeze              run P2: test G2 and record the human-signed Label Handoff
reopen              open a new policy lineage and invalidate downstream claims
workflow | run      ask the family workflow to drive the Building frontier
```

## Ends at the handoff

This door writes no `T*` gold, executor scorecard, production label, or audit
claim. If a selector, sealed runner, Session recorder, Checkpoint Keeper, Test
Custodian, or Label Handoff Keeper is missing, stop at the last closed artifact
and return a structured `HOLD`.
