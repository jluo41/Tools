metrics.json — Schema
======================

Location: `results/<NAME>/metrics.json` (flat job) · `results/<task>/<NAME>/metrics.json` (nested job)
Owner:    Written by the task's `*.py` / `*.do` at finalize. May be edited by
          re-running the task; never hand-edited.
Status:   Source-of-truth for the measured NUMBERS of ONE run. `runtime.yaml`
          records machine facts about the run; `metrics.json` records what it
          measured. It is the file every later reader — a cross-run comparison,
          a report, a QA digest — resolves a number out of, by KEY. Keys are
          therefore a contract: name them stably.


Two value shapes
----------------

A metric key maps to EITHER a bare scalar (the default, unchanged) OR a nested
object carrying an interval. Both are valid; a reader picks behavior by shape.

```json
{
  "mae":   23.92,
  "rmse":  31.40,

  "V_DR_age_routed": {
    "point":     0.4826,
    "ci_lower":  -0.0052,
    "ci_upper":   0.0512,
    "ci_method": "bootstrap_paired",
    "N":          24845
  }
}
```

| Form             | When to use                                              |
|------------------|----------------------------------------------------------|
| bare scalar      | point-estimate metrics (MAE, RMSE, AUROC) — default      |
| nested `{point}` | any metric that has an interval (bootstrap / analytic CI)|


Nested-metric fields
---------------------

| Field      | Type   | Required | Meaning                                            |
|------------|--------|----------|----------------------------------------------------|
| point      | float  | yes      | the point estimate (what a scalar form would hold) |
| ci_lower   | float  | opt      | lower bound of the interval (same units as point)  |
| ci_upper   | float  | opt      | upper bound of the interval                        |
| ci_method  | string | opt      | bootstrap_paired \| percentile \| bca \| analytic_t |
| N          | int    | opt      | sample size the estimate + interval were built on  |
| se         | float  | opt      | standard error, if reported instead of/with the CI |


Extraction contract (how a reader resolves a metric key)
--------------------------------------------------------

```
value = metrics[<metric_key>]
  - value is a number              → use it directly (legacy/scalar path)
  - value is an object with `point` → use value.point as the estimate;
                                       also carry ci_lower/ci_upper/N if present
  - value is an object WITHOUT `point` → WARN: malformed metric; treat as missing
  - key absent                     → FAIL: name the run path + the missing key
```

This keeps every existing scalar `metrics.json` working untouched while giving
off-policy / bootstrapped metrics a canonical slot for their interval, so the
interval SURVIVES to the reader instead of being flattened to a bare point
(which would let a Δ inside the noise band be read as real).


Per-split / per-arm nesting
---------------------------

Both forms may be nested one level under a split name or an arm name. A reader
descends one level when the metric key is dotted (`split.metric` or
`arm.metric`), else reads the top level.

```json
{
  "by_split": {
    "val":     { "mae": 23.10 },
    "test_id": { "mae": 23.92 }
  },
  "per_arm": {
    "greedy":     { "V_DR": { "point": 0.4457, "ci_lower": -0.0401, "ci_upper": 0.0139, "N": 24845 } },
    "age_routed": { "V_DR": { "point": 0.4826, "ci_lower": -0.0052, "ci_upper": 0.0512, "N": 24845 } }
  }
}
```


Display-only evals
------------------

A task whose only output is plots/tables (nothing will ever aggregate a number
out of it) still writes a `metrics.json` stub, so the run↔result pairing holds
and the contract fails fast for genuine omissions:

```json
{ "note": "display-only", "_meta": { "purpose": "figure generation; no aggregatable metric" } }
```


The optional `summary` object
------------------------------

Consumed by run-sh-template.sh and runtime-yaml-schema.md's headline
extraction — emit it if you want a scannable one-liner in runtime.yaml:

```json
{ "auroc": 0.87, "summary": { "headline": "AUROC 0.87 (test), n=82,025" } }
```

Only `summary.headline` (a string) is read by the shipped tooling; other
`summary.*` keys are free-form.


Backward compatibility
-----------------------

- Existing files with only bare scalars are fully valid — no migration needed.
- The nested `{point, ci_*, N}` form is purely additive: a scalar reader that
  predates this schema sees an object and should warn, not crash. Downstream
  readers are expected to handle both shapes.
