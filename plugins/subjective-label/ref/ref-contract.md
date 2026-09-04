# Reference: authority, metrics, and claim contract

This reference defines which comparisons support learning, stopping, final evaluation, and corpus-reliability claims.
It applies to the human-grounded subjective-label lifecycle governed by the current Board QA0.

## 1. Authority and deliverables

One identified human is the semantic authority for one subjective trait in one project.
Models may retrieve, pre-label, diagnose, draft, and execute a frozen policy.
Only an inspectable human decision creates human gold or accepts a substantive semantic rule.

Required final deliverables:

| id | deliverable | meaning |
|---|---|---|
| `D*` | complete corpus | terminal class or accepted non-label disposition plus provenance for every in-scope item |
| `G*` | frozen annotation policy | core guideline, boundary rules, ordered procedure, uncertainty policy, compact casebook, and versioned wrappers |
| `T*` | sealed human-gold test | unseen items labeled by the human after `G*` freezes |
| `S*` | executor scorecards | comparable per-model quality, uplift, transfer, stability, cost, and error profiles |
| `A*` | audit trail | round, policy, test, production, repair, and provenance records |

The calibration process also freezes an intermediate `D_cal*`: the cumulative
human-confirmed development gold `D_t` at the stopping checkpoint. `D_cal*` supports
policy traceability and executor development; it is not the completed corpus `D*`.

The two sides exchange one signed Label Handoff rather than sharing mutable
state. It binds the exact corpus snapshot, schema, `G*`, `D_cal*`, sealed-test
manifest checksum, stopping evidence, lineage, and human freeze signature. It
contains no protected test ids or text. Scanning artifacts bind the handoff
checksum; a semantic change creates a new Building lineage and invalidates
affected downstream claims.

## 2. Label, region, and uncertainty

The default subjective-intensity schema is:

```yaml
labels:
  type: ordinal
  values: [high, low, none]
  none_value: none

regions:
  values: [H, L, N, HL, LN, HN, HLN]

uncertainty:
  required: true
```

`HIGH`, `LOW`, and `NONE` form the final class field.
`NONE` means absence of sufficient target-trait evidence.
It never means uncertain, unresolved, abstain, missing context, or model failure.

The seven-region field is diagnostic metadata.
An item in `HN` still receives a final class of `H` or `N` after human adjudication.

Uncertainty is a separate record containing confidence, reason, and review state.
Unresolved is a terminal workflow disposition, not a fourth class.

## 3. Metric families

For categorical tasks, report macro-F1, balanced accuracy, per-class precision and recall, confusion, and a declared agreement statistic.
For ordinal tasks, add quadratic weighted kappa and a distance-sensitive error such as MAE.
For probability or weighted samples, report the sampling design, weights, denominator, and uncertainty interval.

No single kappa value defines convergence.
Model-model agreement measures consistency, not correctness.

## 4. Comparison contexts

| context | comparison | valid use |
|---|---|---|
| `round_correction` | sealed `P_t` versus human `Y*_t` | executor error diagnosis for one round |
| `round_audit` | prior-policy predictions versus human gold on a probability or weighted slice | comparable quality trajectory and stopping |
| `round_challenge` | predictions versus human gold on adaptively selected difficult cases | discovery and policy refinement only |
| `human_test_retest` | one human's blind later label versus their prior final label | intra-rater concept stability |
| `final_absolute` | one frozen executor under `G*` versus human gold on `T*` | final model quality |
| `guideline_uplift` | same executor under `G*` versus a predefined minimal instruction on `T*` | policy contribution beyond model prior knowledge |
| `heldout_transfer` | executor family absent from optimization versus `T*` gold | model-family portability |
| `production_audit` | blind human audit versus machine-accepted production labels | completed-corpus reliability |
| `external_validity` | whole engine on a public dataset's native construct | optional general engine evidence, never project gold |

Audit and challenge observations must never be merged into one unlabeled trajectory.
If the target population, sampling protocol, executor, or semantic construct changes, open a new metric series.

## 5. Stopping contract

Calibration may stop only when all four gates pass for `K` consecutive comparable checkpoints:

```text
quality floor
AND stability plateau
AND class, region, and corpus coverage
AND acceptable unresolved risk
AND human semantic signoff
```

The quality gate uses the declared round-audit context.
The stability gate uses configured `epsilon`, substantive policy-change counts, and new-boundary yield.
A low plateau fails even when improvement is small.

Calibration stop freezes `G*` and `D_cal*`, then opens final evaluation.
It does not mean that all corpus items have been processed or that the corpus is reliable.

## 6. Sealed final-test contract

Reserve test identifiers at project initialization.
Do not inspect their text, embed them, retrieve them, pre-label them, or use them in stopping.
After `G*` freezes, the human labels the test blind to all executor predictions.

The primary final score uses a representative probability sample.
An optional region-enriched diagnostic supplement is reported separately or reweighted.

If any `T*` outcome changes the policy, wrapper, threshold, executor, ensemble, or routing rule, `T*` becomes validation data for that changed system.
A new sealed test is required for a new final claim.

## 7. Production and reliability claims

Production may use one executor, an ensemble, or validated cost-aware routing.
Every automatic label records policy, executor, wrapper, route, threshold, confidence, and audit linkage.
Disagreement, low confidence, novelty, failures, and known shared-error strata route to human review.

The completed corpus is reliable only after a blind probability audit of machine-accepted production labels.
Report the weighted error estimate, interval, protected-stratum results, repair actions, and share of every provenance tier.

All claims are relative to:

- the identified human semantic authority;
- the declared target population;
- the frozen policy and executor versions;
- the stated audit protocol and date.

Do not claim universal or objective construct truth from this one-person project.

## 8. Engine acceptance

An implementation is accepted only when it can run construct-agnostic categorical and ordinal fixtures and preserves all authority fields.
It must reject or HOLD on:

- model consensus presented as human gold;
- uncertainty encoded as `NONE`;
- test access during calibration;
- a checkpoint without human evidence;
- raw challenge loss used as a stopping series;
- unvalidated nearest-neighbor label inheritance;
- final-test tuning without invalidation;
- a corpus reliability claim without final audit and provenance.
