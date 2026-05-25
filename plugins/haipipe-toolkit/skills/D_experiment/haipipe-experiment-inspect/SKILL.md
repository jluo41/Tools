---
name: haipipe-experiment-inspect
description: "Read-only specialist of haipipe-experiment. Lists experiments, prints status, shows arms + linked runs, finds reverse references (which experiments reference a given run). The 'what's the state of experiments?' query layer. Called by /haipipe-experiment orchestrator."
argument-hint: [list|show|refs|unused] [target]
allowed-tools: Bash, Read, Grep, Glob, Skill
---

Skill: haipipe-experiment-inspect
==================================

Read-only query layer for experiments. Never modifies files.


Commands
--------

```
/haipipe-experiment inspect list [project-path]
  Table of all experiments in project: ID, title, status, # arms, # runs.

/haipipe-experiment inspect show <ID>
  Full view of one experiment yaml: claim, arms, results, caveats.

/haipipe-experiment inspect refs <run-path>
  Reverse index: which experiments reference this run?

/haipipe-experiment inspect unused [project-path]
  List runs in the project that are NOT referenced by any experiment.
  Useful for finding debug / smoke / exploratory runs that never got promoted.

/haipipe-experiment inspect status [project-path]
  Counts: # experiments by status (confirmed / inconclusive / refuted / pending).
```


Output — `list`
----------------

```
═══ Experiments in Proj-Model-1-ScalingLaw ═══

ID    Title                             Status         Arms  Runs  Claim
────  ────────────────────────────────  ─────────────  ────  ────  ──────
E01   baseline_noise_floor              ✅ confirmed    1     5     "Baseline MAE 24.6 ± 0.2"
E02   lhm_vs_baseline                   ⚠️ exploratory  2     2     "LHM-A beats baseline 0.68 (N=1)"
E03   event_channels                    ❌ refuted      2     6     "No measurable gain from events"
E04   transformer_pilot                 ⏸ pending      1     1     (no aggregate yet)
```


Output — `show <ID>`
---------------------

```
═══ E02 — lhm_vs_baseline ═══

hypothesis:    LHM-A in test-id MAE lower than baseline by ≥ 0.5 mg/dL
claim_target:  "LHM-A architecture improves CGM forecasting by X mg/dL ..."

arms:
  baseline (3 runs)
    ✅ tasks/A01_pretraining_clm/01_pretrain_baseline/runs/run_seed42_baseline
    ✅ tasks/A01_pretraining_clm/01_pretrain_baseline/runs/run_seed7_baseline
    ✅ tasks/A01_pretraining_clm/01_pretrain_baseline/runs/run_seed13_baseline
  lhm (3 runs)
    ✅ tasks/A01_pretraining_clm/02_pretrain_lhm/runs/run_seed42_lhm
    ✅ tasks/A01_pretraining_clm/02_pretrain_lhm/runs/run_seed7_lhm
    ✅ tasks/A01_pretraining_clm/02_pretrain_lhm/runs/run_seed13_lhm

aggregation: mean_std_paired_t on MAE_test_id

result:
  baseline_mean: 24.60 ± 0.18
  lhm_mean:      23.92 ± 0.21
  delta:        -0.68
  p_value:       0.018
  sign_test:     3/3 negative
  status:        confirmed

caveats:
  - Same AIData v3, same schedule ✅
  - LHM has 1.2× params — partial confound ⚠️

claim:
  "LHM-A beats baseline by 0.68 ± 0.27 MAE on test-id
   (paired-t p=0.018, N=3 seeds; sign 3/3). Confound: +20% params."
```


Output — `refs <run-path>`
---------------------------

```
═══ References to run_seed42_baseline ═══

Linked in 2 experiments:
  E01 (arm: baseline)  status: ✅ confirmed
  E02 (arm: baseline)  status: ✅ confirmed
```


Output — `unused`
------------------

```
═══ Unused runs in Proj-Model-1-ScalingLaw ═══

37 runs total, 14 unused (38%):

tasks/A01_pretraining_clm/01_pretrain_baseline/runs/
  run_smoke_test           (smoke, ok)
  run_debug_oom            (failed, debug)
  run_seed99_one_off       (ok, but never linked to expmt)

tasks/A01_pretraining_clm/02_pretrain_lhm/runs/
  run_lhm_no_event         (exploratory, never linked)
  ...

Hint: unused runs are fine for debug/smoke. Link them to an experiment
      if they're part of a comparison; otherwise leave as exploration.
```


Disambiguation
---------------

  - No verb → default `list`.
  - <ID> looks like a path → assume `refs`.
  - <ID> looks like E\d+ → assume `show`.


Specialist tail
---------------

```
status:    ok
summary:   "N experiments listed / shown / referenced"
artifacts: (stdout only; no file writes)
next:      suggested follow-up depending on what was inspected
```
