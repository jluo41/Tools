---
name: label-round
description: "Run or resume one human-grounded calibration round after G_1: retrieve a broad seven-region candidate pool, obtain sealed independent weak-LM prelabels, compose a challenge-plus-consensus-audit human batch, conduct blind human adjudication, optimize the guideline without changing human meaning, close D_t/G_t, and evaluate stopping. Use for /label-round, the next batch, or guideline refinement."
---

# Run one calibration round

Advance exactly one round from the latest closed checkpoint. Preserve phase boundaries
so interrupted work can resume without regenerating selections or exposing sealed data.

## Read first

Read:

- `../../../ref/ref-contract.md`
- `../../../ref/ref-schema.md`
- `../../../ref/ref-stages.md`
- `../../../ref/ref-assets.md`
- `../../../ref/ref-architecture.md`
- `../../../ref/ref-embeddings.md`
- `../../../ref/ref-output-style.md`

Read project `config.yaml`, `.state.json`, latest closed policy, cumulative human gold,
prior round manifests, coverage, risk ledger, and implementation holds.

## Preconditions

Require a closed `G_(t-1)` and `D_(t-1)`, no conflicting open round, an unexposed final
test, and inspectable provenance. Resume the recorded open phase when one exists. If the
project has no Round 1 checkpoint, route to `/label-init`.

## Phase A — candidate pool `C_t`

1. Use human-confirmed examples and the closed guideline to retrieve candidates around
   all seven regions.
2. Add novelty, under-covered neighborhoods, metadata strata, and unresolved-risk
   candidates.
3. Deduplicate and exclude prior human gold, invalid records, and sealed-test ids.
4. Freeze a broad pool, commonly around 200 items, with retrieval provenance and region
   hypotheses. Easy H/L/N regions may receive larger pools than scarce boundaries.

Candidate ranking may use embedding features, a transparent classifier, or an MLP. Its
scores select attention; they are neither final labels nor gold confidence.

## Phase B — sealed weak prelabels `P_t`

Run each registered weak executor independently with exactly `G_(t-1)` and its frozen
wrapper. Record H/L/N prediction, region hypothesis, confidence, structured reason
codes, quoted evidence, uncertainty, model/version, and run checksum.

Close and seal all predictions before human-first access. Request inspectable structured
reasons, not hidden chain-of-thought. Model agreement does not create gold.

## Phase C — human batch `B_t`

Compose and freeze the human batch from two arms:

- **challenge:** disagreement, low confidence, policy mismatch, boundary ambiguity,
  novelty, under-coverage, or risk;
- **consensus audit:** a stratified random sample of apparently easy consensus items,
  including H/L/N and relevant corpus strata.

Record arm, stratum, seed, inclusion probability, source candidate, and selection reason.
Do not show predictions or reasons to the human before the human-first event.

## Phase D — Human-AI Session

For each item:

1. obtain the human's initial H/L/N label, seven-region placement, uncertainty, evidence,
   and rationale while weak outputs remain hidden;
2. record the human-first event immutably;
3. when useful, reveal summarized model outputs and structured reasons;
4. let the Strong Calibration Agent ask targeted contrasts, identify inconsistency, and
   propose guideline language;
5. obtain the human's final judgment and classify any change as correction,
   clarification, concept revision, or unresolved;
6. record backward-impact candidates for earlier gold and policy rules.

One round may contain multiple resumable chat Sessions. The round ends only at a
checkpoint, not when a chat window closes.

## Phase E — guideline optimization

Use the strong agent to aggregate executor failure patterns and propose minimal edits to
definitions, boundaries, procedure, uncertainty rules, generalized casebook, or
model-specific wrappers. Optimize executor usability subject to semantic constraints:

- human judgments and explicit boundary decisions are hard constraints;
- examples are generalized when possible and retained verbatim only for an auditable
  purpose;
- wrapper-only repairs are separated from semantic changes;
- every material edit identifies affected prior gold and regression cases;
- no edit is accepted merely because it raises weak-model agreement.

The human accepts, rejects, or revises semantic edits.

## Phase F — checkpoint and stopping

Run schema, completeness, blinding, leakage, contradiction, regression, and checksum
checks. Close `D_t` and `G_t` only after human confirmation.

Report audit and challenge metrics separately. Evaluate stopping as a conjunction:

- quality floor passes on comparable representative audit evidence;
- improvement is below configured `epsilon` for `K` consecutive comparable rounds;
- H/L/N, seven regions, corpus strata, and important neighborhoods meet coverage minima;
- unresolved and critical-risk rates are below limits;
- the human signs off that the articulated construct is stable.

All-data-labeled is an additional stop condition only when every terminal disposition is
valid and risk/audit requirements still pass. A plateau alone never proves quality.

## Result

Return the round id, `C_t/P_t/B_t` checksums, human decisions, consensus shared-error
findings, policy diff, `D_t/G_t`, audit/challenge metrics, stopping-gate result, holds,
and the next valid action.

If a required selector, sealed executor runner, Session recorder, checkpoint keeper, or
metric implementation is absent, emit `HOLD` at that phase and preserve all closed
artifacts. Do not emulate the phase with majority voting or untracked files.
