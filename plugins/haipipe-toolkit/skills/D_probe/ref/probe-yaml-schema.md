probe.yaml — Schema
=========================

What this file is
-----------------

`probe.yaml` is the **state of one research thread**, not a result
artifact. It belongs to the research pipeline (D_probe), which is
distinct from the execution pipeline (C_task, owner of tasks/runs):

```
EXECUTION PIPELINE     task/run    →  did this run work? (metrics, runtime.yaml)
RESEARCH PIPELINE      probe  →  does the hypothesis hold? (this yaml)
```

The yaml evolves over the lifetime of the thread:
  pre-run     hypothesis, claim_target, planned arms, aggregation spec
  in-flight   linked run paths (filled as arms get their runs)
  post-run    result block, caveats, claim sentence, evidence refs

It is **steering state**, not a metrics file. Numbers in `result:` are
aggregated *references* to per-run metrics that live under tasks/.

Location: `examples/<project>/probes/<MMDD>_<slug>/probe.yaml`
Owner:    Written by `haipipe-probe-design` (`new`/`link`),
          extended by `haipipe-probe-result` (`aggregate`/`claim`).
          Audited by `haipipe-probe-review`. Read by all.

Sibling files in the same folder:
  probe.yaml             this file (source of truth for the thread)
  review.md                   latest QA report (overwritten)
  CLAIMS_FROM_RESULTS.md      Codex verdict snapshot (overwritten)
  logs/<YYYY-MM-DD>.md        daily captain's-log narrative (append-only)
  reports/ (optional)         other per-probe reports

NO code, no notebooks, no plots in probe folder. Those live in
tasks/ (execution pipeline) and are referenced via `evidence:` field.


ID convention
-------------

```
lightweight, project-scoped source ref:
  P.0601, P.0602, P.0603, ...

  P      = probe layer
  06     = month of creation
  01     = day of creation
  (a 2nd probe the same day appends a letter suffix: P.0601b)
```

Folder name: `probes/<MMDD>_<slug>/`
(e.g. `probes/0601_framing_loss-aversion/`).
File inside: `probe.yaml` (canonical name; never
`<MMDD>_<slug>.yaml`).

YAML `id:` is the canonical source ref (`P.0601`), not `E01` or flat
`P01`. `created_month:` and `created_day:` duplicate the parseable pieces so
tools can sort and allocate without regex-only logic.

Cross-reference style:

```
human prose:        probe P.0601
mixed source lists: P.0601          # avoids collision with D/I/K/W card IDs
commands accept:    P.0601 | 0601 | probes/0601_framing_loss-aversion/
```

Active/archive organization:

```
probes/
  0601_framing_loss-aversion/                 # active
  0602_simplification_plain-language/         # active
  2026-archive/
    0501_social-norm/                         # inactive; name preserved
```

Move inactive, completed, or deprecated probes into
`probes/<YYYY>-archive/`. Preserve the original folder name so historical
records remain auditable while the active workspace stays clean.

Legacy grouped layouts such as
`probes/A_baseline_controls/01_lhm_vs_baseline/` may be read during
migration, but new writes should use the lightweight active/archive
layout above.


Top-level fields
-----------------

| Field           | Type    | When written     | Required |
|-----------------|---------|------------------|----------|
| id              | string  | design new       | yes      |
| created_month   | string  | design new       | yes      |
| created_day     | string  | design new       | yes      |
| slug            | string  | design new       | yes      |
| title           | string  | design new       | yes      |
| hypothesis      | string  | design new       | yes      |
| claim_target    | string  | design new       | yes      |
| resolves_K      | string  | design new       | (opt)    |
| arms            | mapping | design new+link  | yes      |
| aggregation     | mapping | design new       | yes      |
| result          | mapping | result aggregate | (post)   |
| caveats         | list    | review / design  | (post)   |
| claim           | string  | result claim     | (post)   |
| created_at      | ISO8601 | design new       | yes      |
| updated_at      | ISO8601 | any edit         | yes      |


Skeleton (design new writes this)
----------------------------------

```yaml
id: P.0601
created_month: "06"
created_day: "01"
slug: framing_loss-aversion
title: Loss-aversion framing improves message acceptance
created_at: 2026-06-01T18:00:00-04:00
updated_at: 2026-06-01T18:00:00-04:00

# ── INTENT (pre-run, user/Claude writes) ────────────────────────────
hypothesis: |
  LHM-A test-id MAE lower than baseline by ≥ 0.5 mg/dL,
  paired-t p<0.05 at N=3.

claim_target: |
  "LHM-A architecture improves CGM forecasting by X mg/dL on test-id
   (N=3 seeds, paired-t p=Y)."

# resolves_K (optional, pre-registration): the KNOWLEDGE topic this probe
# will settle, declared at design time BEFORE the result is known. Names the
# K slot the archive reserves — so the answer is recorded whether the probe
# lands `confirmed` (the belief) or `refuted` (its negation). Front-loading
# only the TOPIC (not the verdict) is what kills the file-drawer bias; the
# verdict, plus any I/W cards, stay emergent (discovered by `explore`).
resolves_K: |
  Whether LHM-A architecture beats the baseline forecaster (scope: test-id MAE).

# ── DESIGN (arms = what to run + which runs support each side) ──────
arms:
  baseline:
    task_type: training
    run_specs:
      - name: run_seed42_baseline
        seed: 42
        params: {}
    runs: []              # filled by `design link` after materialization
  lhm:
    task_type: training
    run_specs:
      - name: run_seed42_lhm
        seed: 42
        params: {}
    runs: []

aggregation:
  metric:     MAE_test_id              # which metric to compare
  statistic:  mean_std_paired_t        # mean_std | mean_std_paired_t | sign_test
  baseline_arm: baseline               # for paired-t direction
  treatment_arm: lhm
  noise_floor: 0.3                     # |Δ| below this counts as null

# ── RESULT (filled by `result aggregate`) ───────────────────────────
result:
  status: pending                      # pending|confirmed|inconclusive|refuted
  # baseline_mean, baseline_std, treatment_mean, treatment_std,
  # delta, p_value, sign_test  ← filled after aggregate

# ── CAVEATS (review-checklist driven) ───────────────────────────────
caveats: []

# ── CLAIM (filled by `result claim`) ────────────────────────────────
claim: ""
```


arms field — populated after `link`
-----------------------------------

```yaml
arms:
  baseline:
    task_type: training
    run_specs:
      - name: run_seed42_baseline
        seed: 42
        params: {arch: baseline}
      - name: run_seed7_baseline
        seed: 7
        params: {arch: baseline}
      - name: run_seed13_baseline
        seed: 13
        params: {arch: baseline}
    runs:
      - tasks/A01_pretraining_clm/01_pretrain_baseline/runs/run_seed42_baseline
      - tasks/A01_pretraining_clm/01_pretrain_baseline/runs/run_seed7_baseline
      - tasks/A01_pretraining_clm/01_pretrain_baseline/runs/run_seed13_baseline
  lhm:
    task_type: training
    run_specs:
      - name: run_seed42_lhm
        seed: 42
        params: {arch: lhm}
      - name: run_seed7_lhm
        seed: 7
        params: {arch: lhm}
      - name: run_seed13_lhm
        seed: 13
        params: {arch: lhm}
    runs:
      - tasks/A01_pretraining_clm/02_pretrain_lhm/runs/run_seed42_lhm
      - tasks/A01_pretraining_clm/02_pretrain_lhm/runs/run_seed7_lhm
      - tasks/A01_pretraining_clm/02_pretrain_lhm/runs/run_seed13_lhm
```

Paths are project-relative. Each path in `runs:` must contain
`results/<NAME>/runtime.yaml`. The old shorthand form
`arms.<arm>: [run-path, ...]` may be read during migration, but new writes
must use the object form above so `bridge` has pre-run specs to materialize.


result field — populated by `aggregate`
----------------------------------------

```yaml
result:
  status: confirmed
  baseline_mean:  24.60
  baseline_std:   0.18
  treatment_mean: 23.92
  treatment_std:  0.21
  delta:          -0.68
  p_value:        0.018
  sign_test:      "3/3 seeds show negative Δ"
  N:              3
  excluded_seeds: []         # if outlier-excluded analysis run, list excluded
  aggregated_at:  2026-05-24T19:30:00-04:00
```

When the comparison is interval-based (bootstrap / off-policy eval) rather
than (or in addition to) a t-test, the result block carries the CI on Δ.
All CI fields are OPTIONAL — a plain paired-t result omits them:

```yaml
result:
  status: confirmed
  baseline_mean:  0.4761          # e.g. V_DR of the baseline policy
  treatment_mean: 0.4826          # V_DR of the treatment policy
  delta:          0.0069          # treatment − baseline (native metric units)
  delta_ci_lower: -0.0052         # 95% CI on Δ — lower bound
  delta_ci_upper:  0.0190         # 95% CI on Δ — upper bound
  ci_method:      bootstrap_paired  # paired_t | bootstrap_paired | percentile | bca
  n_bootstrap_samples: 1000       # if ci_method is a bootstrap
  N:              24845           # sample size the estimate was built on
  p_value:        null            # may be null when CI is the primary inference
  aggregated_at:  2026-06-01T00:30:00-04:00
```

status from a CI: `confirmed` if the Δ CI excludes 0 in the claim direction;
`inconclusive` if the CI straddles 0 OR |Δ| < noise_floor; `refuted` if the
CI excludes 0 in the OPPOSITE direction.

Optional secondary results (per-split or per-metric):

```yaml
  by_split:
    val:     {delta: -0.42, p_value: 0.041}
    test_id: {delta: -0.68, p_value: 0.018}
    test_od: {delta: -0.31, p_value: 0.087}
```


statistic enum values
----------------------

| value                 | computes                                          |
|-----------------------|---------------------------------------------------|
| mean_std              | per-arm mean ± std (no comparison)                |
| mean_std_paired_t     | + paired-t between baseline_arm and treatment_arm |
| sign_test             | counts of same-sign Δ across seeds                |
| mean_std_paired_t_+_sign | both                                           |
| mean_std_paired_t_+_ci | paired-t PLUS a CI on Δ (fills delta_ci_lower/upper + ci_method) |
| bootstrap_paired_ci   | paired bootstrap CI on Δ as the primary inference (p_value may be null) |


status enum
------------

| status         | meaning                                                |
|----------------|--------------------------------------------------------|
| pending        | aggregate not yet run (missing or failed runs)         |
| confirmed      | p < 0.05 AND |Δ| > noise_floor AND direction matches  |
| exploratory    | N < 3 (single-seed claim, treat as pilot)              |
| inconclusive   | p >= 0.05 OR |Δ| < noise_floor                         |
| refuted        | p < 0.05 AND |Δ| > noise_floor AND direction OPPOSITE |


caveats — list of strings
--------------------------

```yaml
caveats:
  - "Same AIData v3, same training schedule ✅"
  - "LHM-A has 1.2× params vs baseline — partial scale confound ⚠️"
  - "Single dataset split per seed; held-out test-id only ⚠️"
```

Each item: one sentence. Emoji at end indicates strength:
  ✅ = clean (no confound), ⚠️ = mild confound, ❌ = severe confound.

`review` skill enforces: every detected confound (per checklist) must
appear here, OR review fails.


claim — final 1-2 sentences
----------------------------

LLM-composed after aggregate + caveats:

```yaml
claim: |
  LHM-A architecture beats baseline by 0.68 ± 0.27 MAE on test-id
  (paired-t p=0.018, N=3 seeds; sign test 3/3 negative).
  Confound: +20% params; needs param-matched re-test for full confirmation.
```

Format guideline:
```
<Treatment> <direction> <Baseline> by <Δ ± std> on <metric/split>
(stats: <test> p=<X>, N=<seeds>; <confidence test>). <key caveat>.
```


Validation rules (review enforces)
-----------------------------------

```
- id matches folder date `created_month`+`created_day` (`P.<MMDD>`)
- arms has ≥1 arm and each arm has `runs:` before aggregation
- aggregation.metric is non-empty
- if result.status == confirmed:
    - result.N >= 3
    - result.p_value < 0.05
    - direction matches claim_target
    - all caveats with severity ⚠️/❌ are present in caveats list
- claim is non-empty if result.status in {confirmed, refuted}
```


Atomic write
-------------

Write to `probe.yaml.tmp` in the probe folder, then `mv` to `probe.yaml`.
Same atomicity rule as runtime.yaml.
Comments and field order should be preserved across edits where possible
(use a yaml library that preserves comments, or write the file as a
formatted string).
