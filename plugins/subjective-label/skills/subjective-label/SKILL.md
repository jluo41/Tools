---
name: subjective-label
description: "Human-grounded workflow for labeling a large text corpus on a vague subjective trait while jointly refining H/L/N gold labels, seven diagnostic regions, a human-and-machine-readable guideline, sealed-test model scorecards, and production provenance. Use for subjective annotation projects, calibration rounds, guideline optimization, final evaluation, corpus completion, or /subjective-label."
---

# Subjective Label router

Route the request to the smallest canonical command that can advance the project.

## Canonical commands

The five workflow members live in `../page-workflows/`.

| command | responsibility |
|---|---|
| `/label-init` | initialize corpus, seal final-test ids, embed the development pool, run random Round 1, and close the first checkpoint |
| `/label-round` | run or resume one later calibration round from candidate retrieval through checkpoint |
| `/label-evaluate` | freeze `G*`, create blind human gold on the sealed test, and score registered executors |
| `/label-complete` | run a validated production policy over the remaining corpus, reconcile outcomes, and perform final audit |
| `/label-status` | inspect current state, evidence, holds, and next valid action without writing |

Legacy names (retired 2026-08-15, the router resolves them; no alias skills exist):

- `/sl-init` → `/label-init`; `/sl-status` → `/label-status`
- `/sl-round` and `/sl-iterate` → `/label-round`
- `/sl-evaluate` and `/sl-validate` → `/label-evaluate`
- `/sl-complete` and `/sl-scale` → `/label-complete`

Explain the changed semantics when a legacy name is used. Do not reproduce the legacy
panel-majority, public-dataset convergence, or k-NN inheritance workflow.

Knowledge commands remain available when installed: `lesson`, `feedback`, and `digest`.

## Core contract

Treat one identified human as the semantic authority. Use the strong calibration agent
to elicit, contrast, record, and generalize that person's judgment. Use weak language
models as independent executors whose sealed outputs diagnose guideline clarity; never
treat their consensus as gold.

Maintain these outputs:

- cumulative human-confirmed calibration gold `D_t`, frozen as `D_cal*` at stopping;
- completed corpus `D*` only after validated production, reconciliation, and audit;
- versioned structured guideline `G_t` and eventually `G*`;
- seven diagnostic regions H, L, N, HL, LN, HN, and HLN, separate from uncertainty;
- complete Session, checkpoint, test, scorecard, production, and provenance records.

The canonical round is:

```text
closed G_(t-1)
  → candidate pool C_t
  → sealed weak prelabels P_t
  → human batch B_t
  → blind Human-AI Session
  → human final Y*_t + guideline draft
  → checkpoint
  → closed D_t + G_t
```

Round 1 is random and has no model prelabels or inherited regions. Later rounds combine
targeted challenge items with a stratified random sample of consensus items to detect
shared model error.

## Required references

Before routing a mutating command, read the command skill and the references it names.
The authority and lifecycle sources are:

- `../../ref/ref-contract.md`
- `../../ref/ref-stages.md`
- `../../ref/ref-assets.md`
- `../../ref/ref-architecture.md`

## Safety and implementation truth

Inspect the actual project state and available implementation before writing. Never
claim a phase ran because its conceptual contract exists. When a required engine,
custodian, schema writer, or verifier is absent, write no substitute evidence; return a
structured `HOLD` with the missing capability, preserved state, and next implementation
action.
