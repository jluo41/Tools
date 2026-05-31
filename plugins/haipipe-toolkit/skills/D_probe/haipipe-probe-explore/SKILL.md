---
name: haipipe-probe-explore
description: "Coverage and propose specialist of haipipe-probe. Maps what's been explored across (arch × data × training) axes, identifies gaps, and proposes the next valuable probes or runs to fill them. The 'what should we try next?' brain of the research methodology layer."
argument-hint: "[coverage|propose] [project-path]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
---

Skill: haipipe-probe-explore
==================================

The active research-design assistant. Reads all probes + runs in a
project, infers the design-space axes, marks coverage, and proposes
the most informative next probe.

**Agent embodiment.** This is the D_probe **advancer** — dispatchable as the
`probe-explorer-agent` subagent_type (e.g. by `haipipe-probe-loop` after a
`partial`/`no` claim verdict, to propose supplementary probes). This skill is
the canonical logic home; the agent is a thin pointer (`skills/D_probe/agents/advancers/`).


Commands
--------

```
/haipipe-probe explore coverage [project-path]
  Build coverage map across detected axes. Show ✅/—/⚠️ per cell.

/haipipe-probe explore propose [project-path] [--budget HOURS]
  Suggest next 3-5 probes based on:
    - Gaps in coverage
    - Unconfirmed single-seed runs (need N≥3 paired)
    - High-value missing baselines
    - User's stated open questions (from paper narrative or claim_target)

/haipipe-probe explore axes [project-path]
  Inspect what axes are detected. Allow user to add/remove/rename axes.
```


Axis detection (heuristic)
---------------------------

The skill auto-detects design-space axes by scanning all probes +
runs in the project:

```
1. arch       distinct architectures (from runtime.yaml or config keys)
2. data       distinct AIData versions / data slices
3. training   distinct seeds / schedules / LRs (signal: > 2 values across runs)
4. evaluation distinct splits / metrics / horizons
```

Axes with only one value are dropped from the coverage map (uninformative).

User can extend via /explore axes (e.g., add "preprocessing" or
"augmentation").


Coverage map output
--------------------

```
═══ Coverage — Proj-Model-1-ScalingLaw ═══

axes detected: arch × data × seed-count

           data_v1    data_v2    data_v3
─────────────────────────────────────────
baseline     ✅(5)      ✅(3)      ✅(5)       N = seeds covered
LHM-A          —          —        ⚠️(1)       single-seed only
LHM-B          —          —          —
Transformer  ⚠️(1)        —          —
─────────────────────────────────────────

cells: ✅=N≥3 paired | ⚠️=N=1 (needs confirm) | —=no runs
total: 4 archs × 3 data = 12 cells; 3 confirmed, 2 exploratory, 7 untouched

probes covering this design space:
  P.A01 baseline_noise_floor       (covers baseline x all data)
  P.A02 lhm_vs_baseline            (covers baseline + LHM-A x data_v3)
  P.C01 transformer_pilot          (covers Transformer x data_v1, single-seed)
```


Propose output
---------------

```
═══ Suggested next probes — Proj-Model-1-ScalingLaw ═══

Priority 1 — confirm exploratory cells:
  P.C02  Transformer noise-floor   paired N=3 on data_v1
       Why: existing single-seed result (MAE 24.2) is in baseline noise range
       Cost: ~12 GPU-hours (3 seeds x 4h)
       Adds: cell (Transformer, data_v1) → ✅

  P.A03  LHM-A confirm             paired N=3 on data_v3
       Why: P.A02 used N=1 LHM, claim is exploratory
       Cost: ~10 GPU-hours
       Adds: cell (LHM-A, data_v3) → ✅, upgrades P.A02 claim

Priority 2 — fill obvious gaps:
  P.B01  LHM-A OOD test            data_v1, paired N=3
       Why: does LHM-A win generalize across data versions?
       Cost: ~12 GPU-hours
       Adds: cell (LHM-A, data_v1) → ✅

Priority 3 — speculative:
  P.A04  LHM-B baseline            data_v3, paired N=3
       Why: LHM family extension; only worth if P.A03 confirms LHM-A win
       Defer until P.A03.
```


Workflow — `coverage`
----------------------

```
Step 1: Load all probes/*/*/probe.yaml in project.
Step 2: Scan all runs across tasks/ (recursive); extract design-space
        signals from configs and runtime.yaml.
Step 3: Group runs by (arch × data); count seeds per cell.
Step 4: Classify each cell: ✅ (N≥3), ⚠️ (N=1-2), — (none).
Step 5: Render table + list which probe covers which cells.
```


Workflow — `propose`
---------------------

```
Step 1: Coverage map (as above).
Step 2: For each ⚠️ cell, propose a "confirm" probe (N=3 paired).
Step 3: For — cells adjacent to ✅ cells, propose a "fill" probe.
Step 4: LLM ranks proposals by:
        - Information value (does it answer an open question?)
        - Cost (GPU-hours estimate)
        - Risk (likelihood of definitive result)
Step 5: Output ranked list with rationale.
```


Disambiguation
---------------

  - No verb → default `coverage`.
  - No project path → default to cwd's project root.
  - Axes ambiguous → ask user to confirm or use /explore axes first.


Risk profile
-------------

READ-ONLY. Produces a report (stdout or `--out`). Does not scaffold
or modify probes. Suggested proposals are textual — user runs
`/haipipe-probe design new` to actually create them.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "Coverage: 3 confirmed, 2 exploratory, 7 untouched. 4 proposals ranked."
artifacts: [coverage report path or stdout]
next:      /haipipe-probe design new transformer_noise_floor (for top-priority proposal)
```
