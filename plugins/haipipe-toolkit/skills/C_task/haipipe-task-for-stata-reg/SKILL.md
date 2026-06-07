---
name: haipipe-task-for-stata-reg
description: "Stata-dialect reg-pipeline task-folder build specialist. Scaffolds {NN}_reg_pipeline_<study>/ task-folders that estimate trait→outcome models (OLS / IV / LPM / logit / two-part) over a condition × pairing × trait × estimator grid, writing LIGHT coefficient tables (.tex/.csv) into results/. Called by /haipipe-task orchestrator when task-type=stata-reg. Direct invocation works for scoped scaffolding. Shares the Stata engine in ../haipipe-task-for-stata/ref/stata-dialect.md."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-task-for-stata-reg
=================================

Scaffolds a **reg-pipeline task-folder** (Stata dialect) — runs the
estimation grid on the analysis table from the data stage: OLS
(progressive / LPM-logit / two-part / windows / trait-form) and IV
(main / grid / over-id). This is the **findings** stage.

⚠️ Output asymmetry: unlike cms/case/data, the reg stage's PRIMARY output
is **LIGHT** — coefficient tables (`.tex`/`.csv`/`.txt`) that belong
in-repo under `results/<run>/`, NOT in `_WorkSpace/`. Re-runs are cheap
and you WANT many (one per spec cell), so the grid fans out wide.

Engine: **Stata + PowerShell + logs**. Read
`../haipipe-task-for-stata/ref/stata-dialect.md` first. This skill scaffolds the
task-folder; worker `.do` logic is authored separately.


Position in the Stata sub-family
--------------------------------

```
/haipipe-task-for-stata-cms         1-CMS-Store, per year
/haipipe-task-for-stata-case        2-Case-Store, cohort × year
/haipipe-task-for-stata-data        *-Data-Store, cross-year analysis table
/haipipe-task-for-stata-reg     ◀── you are here   (coef tables → results/, LIGHT)
```


What this scaffolds
-------------------

```
tasks/{G}{NN}_<group>/                              ← group (e.g. R1_Regression_TraitOpioid)
└── D{NN}_reg_pipeline_<study>/                      ← task-folder letter D = reg stage ({LNN})
    ├── scripts/
    │   └── <Condition>_<Pairing>/                   per-spec worker .do files:
    │       ├── run-1-..._-ols-progressive.do          run-2 ols-lpm-logit · run-3 ols-twopart
    │       ├── run-4-..._-ols-windows.do              run-5 ols-traitform
    │       └── run-6-..._-iv-main.do                  run-7 iv-grid · run-8 iv-overid
    ├── configs/                                     (optional .do shared estimation settings)
    │   └── run_reg_<Condition>_<Pairing>_<Trait>.yaml   _meta: block
    ├── runs/
    │   └── <Condition>_<Pairing>/
    │       ├── run-<Condition>_<Pairing>_<Trait>-ols.ps1
    │       └── run-<Condition>_<Pairing>_<Trait>-iv.ps1
    ├── sbatch/
    │   ├── run-<Trait>-all.ps1                      one trait, all conditions/pairings
    │   ├── run-<Condition>_<Pairing>-all.ps1        one spec, all traits
    │   └── run-all.ps1                              full grid
    ├── results/
    │   └── run_reg_<Condition>_<Pairing>_<Trait>/   log/ · *.tex / *.csv (THE output)
    └── diagram/
```

- **RUNNAME grammar:** `run_reg_<Condition>_<Pairing>_<Trait>[-ols|-iv]`
  (condition × pairing × trait × estimator). Runs are organized in
  per-spec subfolders under `runs/`.
- **Estimators:** OLS progressive · LPM/logit · two-part · windows ·
  trait-form; IV main · grid · over-id.
- **Inputs:** the data stage's `ANALYSIS-*.dta` + IV definitions.
- **Output (LIGHT, in-repo):** coefficient tables `.tex`/`.csv` + logs
  under `results/<run>/`.
- **Headline:** key β · SE · N (and first-stage F for IV).


Commands
--------

```
/haipipe-task-for-stata-reg                          ASK project / group / name / grid
/haipipe-task-for-stata-reg <project> <group> <name>  scaffold direct
```


Scaffold flow
-------------

See `fn/scaffold.md`. Summary: identify project+group → collect `_meta` +
the (condition × pairing × trait × estimator) grid → create skeleton
(runs/ + scripts/ organized in per-spec subfolders) → seed `<run>.yaml`
from `ref/config-seed.yaml` → copy per-estimator `runs/.../<run>.ps1` →
emit return contract.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded
artifacts: [paths created]
next:      author the per-spec estimation .do files; run stata-script-reviewer-agent before hand-copy (esp. IV/spec checks)
```
