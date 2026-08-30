---
name: label-building-workflow
description: >-
  The ORDER machine of the Building side of the subjective-label family: drives
  P0 Contract, the P1 Round loop (PREPARE, JUDGE, LEARN, CLOSE), and P2 Freeze
  as round units on disk, owns item-level resume and round receipts, and hands
  the crossing back to subjective-label-workflow. It owns no law: authority,
  human gates and forbidden acts live in label-building. Use when running or
  resuming a calibration round, opening a round card, resuming a Session,
  closing a checkpoint, or /label-building-workflow.
metadata:
  version: "0.5.0"
  last_updated: "2026-08-30"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /label-building-workflow · one round at a time, resumable per item

Load `subjective-label` (family), `subjective-label-workflow` (phase numbers,
gates G0-G2) and `label-building` (the law) first. This file says only in what
ORDER the Building side runs, what it resumes, and which receipt each step
writes. A rule about who may decide is never written here.

## The unit this machine produces

One round is one folder, `rounds/round_<t>/`, with the anatomy in
`../../ref/ref-assets.md` §3: a `card.md` (the wager), `README.md` (identity),
`manifest.yaml` (the compiled batch), `evidence.md` (what the round may read),
`prospect.md` (the forecast), the canonical event files, `checkpoint.json` (the
close), and `view/` (rendered, never authority). Every step below names the
file it leaves behind.

## P0 Contract · order

```text
1 validate   corpus ids, text, target population, checksum   → corpus/manifest.json
2 declare    trait seed, human authority, class/region/       → config.yaml
             uncertainty/unresolved schemas
3 reserve    Test Custodian draws sealed ids, hides them      → test/sealed/status.json
4 scaffold   policy/versions/G_00 (the seed guideline),       → register.md (seven cells,
             gold/cumulative.jsonl (empty), register.md          all `open`)
5 cache      embed every eligible item once                   → cache/embeddings/
```

G0 (family workflow) is tested on the five P0 files it names; `cache/embeddings/`
is provenance, not a gate input. Contract runs once; a rerun with a changed
corpus checksum is a new job, not a resume.

## P1 Round · order

```text
CARD      round card proposed → a person releases it            card.md
PREPARE   pool → batch → seal                                   manifest.yaml · candidate_pool.jsonl
                                                                human_batch.jsonl · prelabels/<executor>.jsonl
PROSPECT  forecast written before the first item is shown       prospect.md
JUDGE     per item: show → first record → lock → reveal → final sessions/ (append-only events)
                                                                human_final.jsonl
LEARN     propose patches → backward impact → measure           policy_draft/ · metrics.json
                                                                coverage.json · risk_ledger.jsonl
CLOSE     Checkpoint Keeper verifies → promotes → routes        checkpoint.json · README.md closed:
                                                                policy/versions/G_<t>/ · gold/cumulative.jsonl
                                                                register.md cells settled · view/
```

### CARD

`card.md` is the folder's first file. It names the register cell(s) the round
targets, the two arms (challenge n, audit n), the seed, and the expected
finding. Round 1's card names no cell: its arm is one random development draw.
Nothing else may exist in the folder while `state: proposed`. A person flips
it to `released:`; the machine never does.

### PREPARE

1. Round 1: draw the declared random sample from the development pool.
   Later rounds: retrieve a candidate pool around the targeted cells, novelty,
   sparse coverage, risk, and unresolved items, with a selection reason per row.
2. Compose the batch from the card's arms; freeze membership, role, stratum,
   inclusion probability, seed, and blind-access state in `human_batch.jsonl`.
3. Run each registered weak executor independently under `G_(t-1)`; write its
   sealed `prelabels/<executor>.jsonl` before any human-first event. Round 1
   has no prelabels.
4. Write `evidence.md`: the checksums of `G_(t-1)`, `D_(t-1)`, the pool, and
   the custody status; never a sealed-test id.

### PROSPECT

Before the first item is shown, write what the round expects: disagreement
count per targeted cell, the rule the evidence is expected to force, and the
audit-arm metric it should move. `result.md` at CLOSE is scored against it.

### JUDGE

Per item, in this order, each step its own appended event in `sessions/`:

```text
show      item text + G_(t-1) cheatsheet; no prelabel, no selection reason that reveals one
first     class · region · uncertainty · evidence · rejected alternative
lock      immutable; a locked event is never replayed
reveal    sealed comparisons, structured, only after lock
final     the human's final decision + change type
          (correction · clarification · concept revision · unresolved)
```

Resume rule: the open item is the first batch row with no `final` event; a
row with `lock` and no `final` resumes at `reveal`. A dead chat changes nothing
on disk.

### LEARN

1. From accepted human evidence, draft the smallest general patch into
   `policy_draft/`, typed semantic / procedural / casebook / wrapper / editorial.
2. Compute backward impact: every prior gold row the patch would flip, into
   `policy_draft/regression.jsonl`.
3. Present each substantive patch with its impact for the human's ruling.
4. Measure: audit-arm metrics separately from challenge-arm metrics, coverage
   per register cell, risk rows; write `metrics.json`, `coverage.json`,
   `risk_ledger.jsonl`.

### CLOSE

The Checkpoint Keeper, in order: completeness (every batch row has a typed
disposition), blinding (every seal precedes its first event), leakage (no
sealed id in the round), regression (accepted patches applied, flipped rows
recorded), coverage, risk, checksums. Then it promotes `D_t` and `G_t`,
writes `checkpoint.json`, appends `closed:` to `README.md`, settles the
targeted `register.md` cells, renders `view/judgments.md`, `view/rules.md`,
`view/result.md` (prospect vs actual, one line per gate), and records the
route: `another round`, `freeze`, or `HOLD`. A round with an unmet check does
not close; it stays `judged` with the failing check named.

## P2 Freeze · order

```text
1 test G2    family workflow asserts the stopping conjunction on the streak
2 rehash     Label Handoff Keeper rehashes G* and D_cal*
3 custody    Test Custodian confirms protected ids never entered a round
4 sign       the human's signature naming exact checksums and lineage
5 write      handoff/label-v1.yaml, once, with its receipt block
6 return     to subjective-label-workflow, which owns the crossing
```

If step 1 fails, the route is `another round` with the failing gate named. If
the Keeper or Custodian is absent, `label-building` §Ends at the handoff rules
`HOLD`; this machine stops at step 2 with the frontier preserved.

## Receipts this machine writes

```text
card.md released:        the person's release of the batch (before PREPARE)
sessions/ events         item-level, append-only, the resume source
checkpoint.json          the round receipt; the only artifact that promotes gold and policy
README.md closed:        keeper · date · route
handoff/label-v1.yaml    the P2 receipt: written once by the Label Handoff Keeper,
                         its validity tested by the family crossing at G3
```

## Return

Return the round id and its `state:`, the open step and open item if any, the
files written this run, the register cells still open, the checkpoint route,
and exactly one next runnable step.
