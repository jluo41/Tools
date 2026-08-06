# Reference: revised lifecycle and state machine

The plugin operates at three nested scales: project lifecycle, Calibration Round, and Human-AI Session.
The scales have different units and closure rules and must not be collapsed into one generic iteration.

## 1. Project lifecycle

```text
/sl-init
    ↓
/sl-round × N
    ↓ four-gate stop + human signoff
freeze G*
    ↓
/sl-evaluate
    ↓ eligible production policy
/sl-complete
    ↓ final corpus audit
complete

/sl-status reads every state without mutation
```

Canonical states:

```text
new
→ initialized
→ calibrating
→ calibration_stopped
→ evaluating
→ evaluated
→ producing
→ auditing
→ complete
```

`hold` is an explicit side state with a reason and owner.
Any semantic change after `calibration_stopped` returns the project to `calibrating` under a new policy lineage and invalidates downstream claims as required.

## 2. Initialization

`/sl-init` performs these responsibilities in order:

1. Validate one corpus snapshot with stable ids and text.
2. Record the vague trait seed and the identified human semantic authority.
3. Establish the H/L/N class schema, seven diagnostic regions, and separate uncertainty field as the default contract.
4. Reserve sealed-test identifiers from a declared sampling frame without exposing their text.
5. Compute stable corpus embeddings for retrieval and cache them by model plus text hash.
6. Create project, policy, round, gold, test, evaluation, production, and audit directories.
7. Draw Round 1 randomly from the eligible development pool, usually about 50 to 60 items as a configurable starting point.

Initialization does not assign gold labels, seven-region truth, or a complete guideline.
Those first semantic artifacts emerge inside Round 1 dialogue.

## 3. Calibration Round

A round begins from one closed state and closes only at a Checkpoint:

```text
G_(t-1) closed + D_(t-1)
        ↓
C_t candidate pool
        ↓
P_t sealed weak-model prelabels
        ↓
B_t frozen human batch
        ↓
one or more Human-AI Sessions
        ↓
Y*_t human final records + G_t draft
        ↓
Checkpoint t
        ↓
D_t cumulative human gold + G_t closed
```

Round 1 is the exception at the front of this sequence:

- it receives the random initialization batch directly;
- it has no prior weak prelabels or valid seven-region selector;
- class labels, region assignments, reasons, and the first policy draft co-emerge through dialogue.

Round 2 onward uses the full candidate and prelabel funnel.

## 4. Later-round selection

Candidate generation produces broad `C_t`, such as about 200 items, before the smaller human batch is chosen.
The selector uses seven-region retrieval, lightweight rankers, diversity, novelty, sparse-region capacity, and a random coverage reserve.
Embeddings and classifiers rank candidates but cannot assign human gold.

Independent weak executors apply `G_(t-1)` to `C_t` and create sealed `P_t`.
Each output contains a class prediction, optional predicted region, confidence, concise structured reason, executor identity, wrapper identity, and seal checksum.

`B_t` combines:

- class and rule disagreement;
- geometry-model mismatch;
- novelty and sparse-region coverage;
- carryover unresolved cases;
- a stratified random consensus audit.

Batch membership and audit probabilities freeze before the Session.

## 5. Human-AI Session

A Session is one resumable conversation inside a round.
For every item:

1. Show the human the item and prior closed policy without weak-model predictions.
2. Save the human-first class, region, uncertainty, evidence, and rejected alternative.
3. Lock the first-pass record.
4. Reveal the sealed prediction comparison.
5. Ask contrast and counterfactual questions.
6. Save the final human record and classify any change as correction, clarification, or concept revision.
7. Draft policy changes and backward-impact candidates without accepting them automatically.

The human may leave an item unresolved with a typed reason.
Unresolved is not a class and never becomes `NONE`.

## 6. Checkpoint

The Checkpoint Keeper validates and closes:

- every item disposition in `B_t`;
- `Y*_t` human evidence;
- cumulative human gold `D_t`;
- accepted policy changes and regression evidence;
- closed `G_t` plus checksums and parent;
- audit and challenge metrics;
- coverage matrix and risk ledger;
- backward-impact ownership;
- next project state.

No new round may use `G_t` or `D_t` before checkpoint closure.
A draft or partially written Session cannot promote itself.

## 7. Round measurements

Two score families close every round:

| family | source | purpose |
|---|---|---|
| audit | probability or weighted sample with a comparable target population | quality trajectory and stopping |
| challenge | adaptively selected disagreement, mismatch, boundary, and novelty cases | policy discovery and diagnosis |

Correction loss compares `P_t` with `Y*_t` per executor.
Policy deltas separate semantic, procedural, casebook, wrapper, and editorial changes.

## 8. Stopping

Stop calibration only when quality, stability, coverage, and risk all pass for configured `K` consecutive comparable checkpoints and the human signs off.
A stable score below the quality floor does not converge.

Calibration stop freezes `G*` plus the cumulative human calibration gold as `D_cal*`,
then closes development. `D_cal*` is not the completed corpus `D*`.
It does not complete the corpus.

## 9. Final evaluation

`/sl-evaluate` requires `calibration_stopped` and a valid sealed-test manifest.
It performs:

1. authorized test-text release after the freeze;
2. blind human labeling under `G*` without executor predictions;
3. final human-gold lock;
4. execution by registered seen and held-out candidates;
5. absolute metrics, guideline uplift, transfer, stability, cost, and failure scorecards;
6. invalidation recording if results are used to modify a scored component.

Public datasets may support separate engine-level external validity.
They cannot replace the project-specific sealed human test.

## 10. Corpus completion

`/sl-complete` selects one frozen production policy from eligible scorecards and the predefined quality-risk-cost rule.
It then:

1. runs a preflight sample;
2. labels the eligible remainder through idempotent attempts;
3. routes disagreement, uncertainty, novelty, failures, and known error strata to the human;
4. reconciles one terminal disposition per item;
5. runs a blind probability audit of machine-accepted labels;
6. repairs or reopens failed strata;
7. writes final provenance shares and bounded reliability claims.

Complete means every in-scope item has a terminal disposition and the final audit passes or has an explicitly accepted limitation.

## 11. Compatibility commands

```text
/sl-iterate  → /sl-round
/sl-validate → /sl-evaluate
/sl-scale    → /sl-complete
```

Aliases announce the canonical command before dispatch.
They do not preserve old panel-consensus, public-kappa, or static-cascade semantics.

## 12. Implementation status

The lifecycle above is the governing contract.
Current libraries provide partial technical primitives but do not yet automate every seal, checkpoint, final-test, production, and audit operation.
Skills must emit an explicit implementation HOLD where a required engine unit has not shipped.
