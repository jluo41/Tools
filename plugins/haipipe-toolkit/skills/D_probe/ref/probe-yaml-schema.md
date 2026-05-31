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

Location: `examples/<project>/probes/<GROUP>_<group_slug>/<NN>_<slug>/probe.yaml`
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
grouped, project-scoped source ref:
  P.A01, P.A02, P.B01, ...

  P      = probe layer
  A/B/C  = probe group / series
  01     = sequence number within the group
```

Folder name: `probes/<GROUP>_<group_slug>/<NN>_<slug>/`
(e.g. `probes/A_baseline_controls/01_lhm_vs_baseline/`).
File inside: `probe.yaml` (canonical name; never `<NN>_<slug>.yaml`).

YAML `id:` is the canonical source ref (`P.A01`), not `E01` or flat
`P01`. `group:` and `local_id:` duplicate the parseable pieces so tools
can sort and allocate without regex-only logic.

Cross-reference style:

```
human prose:        probe P.A01
mixed source lists: P.A01            # avoids collision with D/I/K/W card IDs
commands accept:    P.A01 | A01 | A/01_lhm_vs_baseline | probes/A_baseline_controls/01_lhm_vs_baseline/
```

`probes/INDEX.md` may define the group registry:

```yaml
groups:
  A: baseline_controls
  B: generalization
  C: architecture_family
```

The letter is stable; the title can be renamed as the research thread
gets clearer.


Top-level fields
-----------------

| Field           | Type    | When written     | Required |
|-----------------|---------|------------------|----------|
| id              | string  | design new       | yes      |
| group           | string  | design new       | yes      |
| group_title     | string  | design new       | yes      |
| local_id        | string  | design new       | yes      |
| slug            | string  | design new       | yes      |
| title           | string  | design new       | yes      |
| hypothesis      | string  | design new       | yes      |
| claim_target    | string  | design new       | yes      |
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
id: P.A01
group: A
group_title: baseline_controls
local_id: "01"
slug: lhm_vs_baseline
title: LHM-A architecture beats baseline on test-id
created_at: 2026-05-24T18:00:00-04:00
updated_at: 2026-05-24T18:00:00-04:00

# ── INTENT (pre-run, user/Claude writes) ────────────────────────────
hypothesis: |
  LHM-A test-id MAE lower than baseline by ≥ 0.5 mg/dL,
  paired-t p<0.05 at N=3.

claim_target: |
  "LHM-A architecture improves CGM forecasting by X mg/dL on test-id
   (N=3 seeds, paired-t p=Y)."

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
- id matches folder group + local_id (`P.<GROUP><NN>`)
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
