---
name: haipipe-probe-inspect
description: "Read-only specialist of haipipe-probe. Lists probes, prints status, shows arms + linked runs, finds reverse references (which probes reference a given run). The 'what's the state of probes?' query layer. Called by /haipipe-probe orchestrator."
argument-hint: "[list|show|refs|unused] [target]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "1.2.0"
  last_updated: "2026-06-01"
  summary: "Read-only specialist of haipipe-probe."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "1.1.0 (2026-06-01): update probe examples for lightweight `MM-NN_slug` layout."
    - "1.2.0 (2026-06-01): switch probe folder + ref examples to date-based `MMDD` / `P.MMDD`."
---

Skill: haipipe-probe-inspect
==================================

Read-only query layer for probes. Never modifies files.


Commands
--------

```
/haipipe-probe inspect list [project-path]
  Table of all probes in project: ID, title, status, # arms, # runs.

/haipipe-probe inspect show <probe>
  Full view of one probe yaml: claim, arms, results, caveats.

/haipipe-probe inspect refs <run-path>
  Reverse index: which probes reference this run?

/haipipe-probe inspect unused [project-path]
  List runs in the project that are NOT referenced by any probe.
  Useful for finding debug / smoke / exploratory runs that never got promoted.

/haipipe-probe inspect runs [<probe> | project]
  Render the RUN DASHBOARD (see ../ref/probe-run-dashboard-template.txt): per
  arm, the PLANNED runs (run_specs, with seeds) JOINED to the DONE/linked runs,
  so you see proposed-vs-existing grouped by arm + the per-arm fill ratio
  (e.g. treatment 1/3 seeds). `project` form → probes/RUNS.md across all probes.
  Flags exploratory (1 seed/arm, row-bootstrap CI only) vs confirmatory (≥3
  seeds). Proposed rows show the command that materializes them (a to-do list).

/haipipe-probe inspect cycle <probe>
  Render + persist the per-probe CLOSED-LOOP AUDIT to <probe>/CYCLE.md (see
  ../ref/probe-cycle-audit-template.txt): 7 sections — header · stage trail ·
  hypothesis · method (re-runnable) · evidence (checkable) · verdict · produced
  (insight cards grepped from insights/ `sources:`). Click ONE file to audit the
  whole cycle. Derived (regenerate any time); respects insight→probe one-way dep.

/haipipe-probe inspect status [project-path]
  Render the canonical 4-section campaign STATUS TRACKER (see
  ../ref/probe-status-template.txt): (1) arc · (2) probe matrix · (3) active-
  probe stage+artifact ladder · (4) blockers/next. Regenerated from the
  probe.yaml files each call (read-only; stdout). This is ALSO the block to
  emit at the END of any response that advances probe work, so the position is
  always visible. Persisting to probes/STATUS.md is the caller's job (inspect
  never writes).
```


Output — `list`
----------------

```
═══ Probes in Proj-Model-1-ScalingLaw ═══

ID      Title                             Status         Arms  Runs  Claim
──────  ────────────────────────────────  ─────────────  ────  ────  ──────
P.0601   baseline_noise_floor              ✅ confirmed    1     5     "Baseline MAE 24.6 ± 0.2"
P.0602   lhm_vs_baseline                   ⚠️ exploratory  2     2     "LHM-A beats baseline 0.68 (N=1)"
P.0603 event_channels                    ❌ refuted      2     6     "No measurable gain from events"
P.0604 transformer_pilot                 ⏸ pending      1     1     (no aggregate yet)
```


Output — `show <probe>`
---------------------

```
═══ P.0602 — lhm_vs_baseline ═══

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

Linked in 2 probes:
  P.0601 (arm: baseline)  status: ✅ confirmed
  P.0602 (arm: baseline)  status: ✅ confirmed
```


Output — `unused`
------------------

```
═══ Unused runs in Proj-Model-1-ScalingLaw ═══

37 runs total, 14 unused (38%):

tasks/A01_pretraining_clm/01_pretrain_baseline/runs/
  run_smoke_test           (smoke, ok)
  run_debug_oom            (failed, debug)
  run_seed99_one_off       (ok, but never linked to a probe)

tasks/A01_pretraining_clm/02_pretrain_lhm/runs/
  run_lhm_no_event         (exploratory, never linked)
  ...

Hint: unused runs are fine for debug/smoke. Link them to a probe
      if they're part of a comparison; otherwise leave as exploration.
```


Output — `status`  (canonical campaign tracker)
------------------------------------------------

Full format + render rules: ../ref/probe-status-template.txt. The arc is a
LOOP: the probe is the machine hub (judge before insights), and the HUMAN
narrative closes it — `explore` only feeds the human's propose-next decision:
`probe ⇄ task → probe(judge) → insights → explore → NARRATIVE(human: propose next)↺`.
NEVER `paper` (a paper is a downstream application, not part of the loop).

```
╔═ OptTime campaign status ═══════════════════════════════ 2026-06-01 ═╗

① ARC   probe ⇄ task → probe(judge) → insights → explore → NARRATIVE(human)↺
           ▲ HERE: planning probes; no task has run, nothing to judge yet

② PROBE MATRIX  (✅ done · ⏳ active · ⬜ todo)
   ┌───────┬────────┬────────┬─────┬──────┬──────┬─────┬──────┬───────┐
   │ probe │ design │ bridge │ run │ aggr │ revw │claim│fileK │verdict│
   ├───────┼────────┼────────┼─────┼──────┼──────┼─────┼──────┼───────┤
   │ P.B01 │   ✅   │   ⏳   │  ⬜ │  ⬜  │  ⬜  │ ⬜  │  ⬜  │  —    │
   │ P.A01 │   ✅   │   ⬜   │  ⬜ │  ⬜  │  ⬜  │ ⬜  │  ⬜  │  —    │
   │ P.C01 │   ✅   │   ⬜   │  ⬜ │  ⬜  │  ⬜  │ ⬜  │  ⬜  │  —    │
   └───────┴────────┴────────┴─────┴──────┴──────┴─────┴──────┴───────┘

③ ACTIVE PROBE — P.B01 (arm_pool_20to4_bands) — stage + ARTIFACT
   1 design    ✅  probes/B_action_restructure/01_.../probe.yaml
   2 bridge    ⏳  → tasks/B03_method_probes/01_band4/                  NEXT
   3 run       ⬜  → results/<run>/metrics.json (CI-aware)
   4 aggregate ⬜  → probe.yaml result:
   5 review    ⬜  → review.md
   6 claim     ⬜  → probe.yaml claim:
   7 file K    ⬜  → insights/K_knowledge/K*.md (win OR loss)
   8 explore   ⬜  → probes/propose.md

④ BLOCKERS / NEXT
   ⚠️ baseline arm links the v3 eval but it has no metrics.json yet.
   ▶ next: bridge — backfill baseline metrics.json + scaffold band run.
╚══════════════════════════════════════════════════════════════════════╝
```


Disambiguation
---------------

  - No verb → default `list`.
  - <target> looks like a path → assume `refs`.
  - <target> looks like `P.0601`, `0601`, or `probes/0601_<slug>` → assume `show`.


Specialist tail
---------------

```
status:    ok
summary:   "N probes listed / shown / referenced"
artifacts: (stdout only; no file writes)
next:      suggested follow-up depending on what was inspected
```
