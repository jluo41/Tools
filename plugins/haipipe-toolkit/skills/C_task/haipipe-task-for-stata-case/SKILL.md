---
name: haipipe-task-for-stata-case
description: "Stata-dialect case-pipeline task-folder build specialist. Scaffolds {NN}_case_pipeline_<study>/ task-folders that trigger cohort cases (per cohort × year) from CMS-Store into _WorkSpace/2-Case-Store as CASES + BFAF feature panels. Called by /haipipe-task orchestrator when task-type=stata-case. Direct invocation works for scoped scaffolding. Shares the Stata engine in ../haipipe-task-for-stata/ref/stata-dialect.md."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.3.0"
  last_updated: "2026-06-09"
  summary: "Stata case-pipeline task-folder builder."
  changelog:
    - "1.0.0 (2026-05-31): baseline."
    - "1.1.0 (2026-06-08): add metadata; workflow lifecycle compatible."
    - "1.2.0 (2026-06-08): add synth/full source dimension to RUNNAME grammar; per-run .do configs; _source_{synth|full}.do selectors."
    - "1.3.0 (2026-06-09): unwrap prose; fix agent names to haipipe-task-{creator,reviewer}-agent; add lifecycle paragraph."
---

Skill: haipipe-task-for-stata-case
==================================

Scaffolds a **case-pipeline task-folder** (Stata dialect) — triggers cases for a clinical cohort (e.g. VisitLBP, VisitCancer) at every service event, then attaches bene/PDE/claims/lines/outpatient feature panels (`BFAF-*`). Runs per (cohort × source × year); consumes the per-year CMS-Store slices plus External-Store crosswalks (NDC→opioid, ICD→pain).

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Stage 2: Build, then authors the worker `.do` files). Always end with the structured return block (status / task_folder / run_name / files).

**Source dimension (synth vs full):** CMS data exists in two environments:
- `synth` — synthetic CMS data, laptop-safe, for pipeline development
- `full` — real CMS PHI, runs ONLY on the isolated CMS secure server

Each source has its own `_source_{synth|full}.do` selector that sets `cms_source`, `cms_asset_name`, and `cms_asset_version`. Case output is tagged by `${cms_source}` (e.g. `case_lbp_synth` vs `case_lbp_full`) so outputs never collide. Every (source × year) pair gets its own runner AND its own config in `configs/`.

Engine: **Stata + PowerShell + logs**. Read `../haipipe-task-for-stata/ref/stata-dialect.md` first. This skill scaffolds the task-folder; worker `.do` logic is authored separately.


Position in the Stata sub-family
--------------------------------

```
/haipipe-task-for-stata-cms         1-CMS-Store, per year
/haipipe-task-for-stata-case    ◀── you are here   (2-Case-Store, cohort × year)
/haipipe-task-for-stata-data        analysis table  (*-Data-Store, cross-year)
/haipipe-task-for-stata-reg         estimation      (coef tables → results/, LIGHT)
```


What this scaffolds
-------------------

```
tasks/{G}{NN}_<group>/                                  ← group
└── B{NN}_case_pipeline_<study>/                         ← task-folder letter B = case stage
    ├── case_pipeline.do                                 dispatcher: <config> <step> <year> <results_dir> <ws_root> <source>
    ├── run_case_year.ps1                                year orchestrator (topic flags, parallel Stata jobs)
    ├── scripts/
    │   ├── cases/                                       trigger-cases-<script>.do
    │   ├── feat/                                        bene-* / bfaf-* / shared-* workers
    │   └── d-Case-Describe.do                           cross-year QC
    ├── configs/
    │   ├── <Cohort>.do                                  SHARED: ICD codes, topic flags, paths
    │   ├── _source_synth.do                             source selector: cms_source=synth
    │   ├── _source_full.do                              source selector: cms_source=full
    │   ├── <Cohort>_synth_<year>.do                     PER-RUN: loads selector + shared config + pins year
    │   └── <Cohort>_full_<year>.do                      PER-RUN: same for full
    ├── runs/
    │   ├── run_case_<Cohort>_synth_<year>.ps1           THIN wrapper: calls run_case_year.ps1 -source synth
    │   ├── run_case_<Cohort>_full_<year>.ps1            THIN wrapper: calls run_case_year.ps1 -source full
    │   └── run_describe_<Cohort>.ps1                    describe-only QC
    ├── sbatch/
    │   ├── run_all_<y0>-<y1>_synth.ps1                  all synth years (loops runs/)
    │   └── run_all_<y0>-<y1>_real.ps1                   all full years
    ├── results/
    │   ├── run_case_<Cohort>_synth_<year>/              log/ + summary.txt + manifest.json
    │   └── run_case_<Cohort>_full_<year>/               (same, from CMS server)
    └── diagram/
```

- **RUNNAME grammar:** `run_case_<Cohort>_{synth|full}_<year>` (cohort × source × year).
- **Four-sister convention:** every RUNNAME has a matched triple:
  `configs/<Cohort>_{synth|full}_<year>.do` + `runs/run_case_<Cohort>_{synth|full}_<year>.ps1` + `results/run_case_<Cohort>_{synth|full}_<year>/`
- **Config architecture (3 layers):**
  1. `_source_{synth|full}.do` — sets `cms_source`, `cms_asset_name`, `cms_asset_version`
  2. `<Cohort>.do` — shared cohort definition (ICD codes, topic flags, paths via `${ws_root}`)
  3. `<Cohort>_{synth|full}_<year>.do` — thin per-run wrapper that loads (1) + (2) + pins year
- **Steps (topic chains):** `cases`; `bene_year + enrollment` (parallel);
  `shared_pde -> {pde_bene, pde_npi, pde_bn} -> *_opioidrx`;
  `shared_claims -> claims_bene`; `shared_lines -> {lines_npi, lines_bn}`;
  `shared_outpt -> {outpt_bene, outpt_npi, outpt_bn}`; `summary`.
- **Inputs:** `1-CMS-Store/{cms_synth|cms_full}/<ver>/year-<year>/`
  + `0-External-Store/` NDC-opioid & ICD-pain crosswalks.
- **Heavy outputs:** `_WorkSpace/2-Case-Store/case_<cohort>_{synth|full}/<asset>/year-<year>/`.
- **Output tagging:** `${cms_source}` in the case_asset_name prevents synth/full collision.


Commands
--------

```
/haipipe-task-for-stata-case                          ASK project / group / name / cohorts
/haipipe-task-for-stata-case <project> <group> <name>  scaffold direct
```


Scaffold flow
-------------

See `fn/scaffold.md`. Summary: identify project+group → collect `_meta` + cohort list + source list + year axis → create skeleton → seed source selectors (`_source_synth.do`, `_source_full.do`) → seed per-run `.do` configs from `ref/config-seed-run.do` for each (cohort × source × year) → copy `runs/<run>.ps1` → emit return contract.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded
artifacts: [paths created]
next:      author dispatcher .do + scripts/{cases,feat}/ workers; run haipipe-task-reviewer-agent before hand-copy
```


Workflow plan
--------------

When `/haipipe-task plan` targets an existing task-folder of this type, the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     <- script-level phases for this type
../haipipe-task/ref/workflow-template.yaml  <- task-level template (Run/Gate1/Gate2)
```

Schema source of truth:
  B_project/haipipe-workflow/ref/plan-schema.md
