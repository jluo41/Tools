---
name: label-evaluate
description: "Perform sealed final evaluation after calibration stops: freeze G*, authorize release of protected test items, collect blind human H/L/N gold, close registered executor predictions, and produce absolute, baseline-uplift, held-out-family, class, region, stability, and cost scorecards. Use for /label-evaluate or final guideline/model evaluation."
---

# Evaluate the frozen guideline and executors

Estimate how well registered weak executors implement the frozen human construct on a
test set that did not influence guideline development.

## Read first

Read:

- `../../../ref/ref-contract.md`
- `../../../ref/ref-schema.md`
- `../../../ref/ref-stages.md`
- `../../../ref/ref-assets.md`
- `../../../ref/ref-architecture.md`
- `../../../ref/ref-datasets.md`
- `../../../ref/ref-output-style.md`

## Preconditions

Require:

- passed stopping gates and explicit human signoff;
- frozen `G*` and cumulative calibration-gold `D_cal*` checksums;
- a valid sealed-test reservation and access log;
- no evidence that protected ids or labels entered calibration;
- a preregistered candidate registry, minimal-instruction baseline, metrics, repeats,
  selection rule, and at least one held-out model family when required.

If leakage occurred, mark the test invalid and require a new protected sample. Never hide
or waive invalidation.

## Protocol

1. **Freeze evaluation.** Close the registry with model/version, family, role, wrapper,
   decoding, policy checksum, repeat rule, metric definitions, quality floors, and
   protected claims.
2. **Authorize release.** The Test Custodian releases only the allowed test items after
   verifying `G*` freeze. Preserve access events and item counts.
3. **Create human gold.** The human labels test items blind to all candidate predictions.
   The Strong Calibration Agent may apply the frozen guideline and ask for consistency,
   but cannot edit `G*`. Record first and final human events, region, uncertainty,
   rationale, and consistency review in `T*`.
4. **Close executor predictions.** Run registered candidates independently while `T*`
   labels remain hidden. Store append-only predictions and structured reasons. Close all
   runs before opening gold for scoring.
5. **Score.** Produce absolute headline metrics with intervals; per-class, per-region,
   and protected-stratum results; confusion and error analysis; repeated-run stability;
   latency and cost; uplift over minimal instruction; and held-out-family performance.
6. **Select or reject.** Apply the preregistered rule. A candidate that fails a required
   floor is not production-qualified, even if it is cheapest or best among failures.
7. **Render and close.** Write immutable scorecards and evaluation summary, update state,
   and preserve prediction/gold separation in provenance.

Do not tune `G*`, wrappers, thresholds, or candidate selection against `T*`. If the result
reveals a semantic defect, reopen calibration under a new version and reserve a new test
for any future confirmatory claim. The consumed test becomes diagnostic evidence only.

## Optional external validation

Run external datasets only as a separately registered external-validity analysis after
or alongside the project evaluation. Preserve native labels, justify mappings, and label
every result `external`. Never use a public human-agreement value as the project's
convergence criterion or autonomy license.

## Result

Return `G*`, `T*`, registry and run checksums; validity status; human-gold count; each
executor scorecard; baseline uplift; held-out-family result; selected production
candidate or no-qualified-candidate; limitations; and next valid action.

If custody, blind human recording, sealed execution, or scorecard computation is not
implemented, emit `HOLD` without opening protected data or producing placeholder scores.
