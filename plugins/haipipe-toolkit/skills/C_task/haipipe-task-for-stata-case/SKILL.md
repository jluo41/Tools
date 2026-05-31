---
name: haipipe-task-for-stata-case
description: "Stata-dialect case-pipeline task-folder build specialist. Scaffolds {NN}_case_pipeline_<study>/ task-folders that trigger cohort cases (per cohort × year) from CMS-Store into _WorkSpace/2-Case-Store as CASES + BFAF feature panels. Called by /haipipe-task orchestrator when task-type=stata-case. Direct invocation works for scoped scaffolding. Shares the Stata engine in ../haipipe-task/ref/stata-dialect.md."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-task-for-stata-case
==================================

Scaffolds a **case-pipeline task-folder** (Stata dialect) — triggers cases
for a clinical cohort (e.g. VisitLBP, VisitCancer) at every service
event, then attaches bene/PDE/claims/lines/outpatient feature panels
(`BFAF-*`). Runs per (cohort × year); consumes the per-year CMS-Store
slices plus External-Store crosswalks (NDC→opioid, ICD→pain).

Engine: **Stata + PowerShell + logs**. Read
`../haipipe-task/ref/stata-dialect.md` first. This skill scaffolds the
task-folder; worker `.do` logic is authored separately.


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
tasks/{G}{NN}_<group>/                              ← group (e.g. R1_Regression_TraitOpioid)
└── {NN}_case_pipeline_<study>/
    ├── {NN}_case_pipeline_<study>.do                dispatcher: <config> <step> <year> <results_dir>
    ├── stata/
    │   ├── cases/                                   trigger-cases-<script>.do (one per cohort)
    │   └── feat/                                    bene-* / bfaf-* / shared-* feature workers
    ├── configs/
    │   ├── <Cohort>.do                              per-cohort: ICD codes, topic flags (VisitLBP.do, ...)
    │   └── run_case_<Cohort>_<year>.yaml            _meta: block + stata_config: pointer
    ├── runs/
    │   └── run_case_<Cohort>_<year>.ps1             from ../haipipe-task/ref/run-ps1-template.ps1
    ├── run_case_year.ps1                            intra-run orchestrator (topic chains, parallel)
    ├── sbatch/
    │   ├── run_case_<Cohort>_<y0>-<y1>.ps1          one cohort, all years
    │   └── run_case_all_<y0>-<y1>.ps1               all cohorts, all years
    ├── results/                                     log/ · runtime.yaml · summary.txt (heavy → _WorkSpace)
    └── diagram/
```

- **RUNNAME grammar:** `run_case_<Cohort>_<year>`  (cohort × year).
- **Steps (topic chains):** `cases · bene_year · enrollment · summary`;
  `shared_pde → {pde_bene, pde_npi, pde_bn} → *_opioidrx`;
  `shared_claims → claims_bene`; `shared_lines → {lines_npi, lines_bn}`;
  `shared_outpt → {outpt_bene, outpt_npi, outpt_bn}`; `*_erase`.
- **Inputs:** `1-CMS-Store/.../year-<year>/{BCarrierLine,Outpatient,BCarrierClaim,Bene_Info}-Neat-<year>.dta`
  + `0-External-Store/` NDC-opioid & ICD-pain crosswalks.
- **Heavy outputs:** `_WorkSpace/2-Case-Store/case_<cohort>/<asset>/year-<year>/`.
- **Headline:** triggered case count for the cohort × year.


Commands
--------

```
/haipipe-task-for-stata-case                          ASK project / group / name / cohorts
/haipipe-task-for-stata-case <project> <group> <name>  scaffold direct
```


Scaffold flow
-------------

See `fn/scaffold.md`. Summary: identify project+group → collect `_meta` +
cohort list + year axis → create skeleton → seed one `<run>.yaml` per
(cohort × year) from `ref/config-seed.yaml` → copy `runs/<run>.ps1` →
emit return contract.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded
artifacts: [paths created]
next:      author dispatcher .do + stata/{cases,feat}/ workers; run the Run Script Reviewer agent
```
