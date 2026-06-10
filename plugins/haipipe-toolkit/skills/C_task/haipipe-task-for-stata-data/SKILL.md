---
name: haipipe-task-for-stata-data
description: "Stata-dialect data-pipeline task-folder build specialist. Scaffolds {NN}_data_pipeline_<study>/ task-folders that assemble the cross-year regression-ready analysis table (filter cases → merge physician traits + policy → derive vars → ANALYSIS-*.dta) from Case-Store into _WorkSpace/*-Data-Store. Called by /haipipe-task orchestrator when task-type=stata-data. Direct invocation works for scoped scaffolding. Shares the Stata engine in ../haipipe-task-for-stata/ref/stata-dialect.md."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.2.0"
  last_updated: "2026-06-09"
  summary: "Stata data-pipeline task-folder builder."
  changelog:
    - "1.0.0 (2026-05-31): baseline."
    - "1.1.0 (2026-06-08): add metadata; workflow lifecycle compatible."
    - "1.2.0 (2026-06-09): unwrap prose; fix agent names to haipipe-task-{creator,reviewer}-agent; add lifecycle paragraph."
---

Skill: haipipe-task-for-stata-data
==================================

Scaffolds a **data-pipeline task-folder** (Stata dialect) — assembles the single, cross-year, regression-ready analysis table. Appends per-year CASES, applies first-visit + age/year filters, merges physician personality traits + (optional) policy, applies MD/DO + review-count filters, derives variables, and writes `ANALYSIS-CMS-Filter.dta`.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Stage 2: Build, then authors the worker `.do` files). Always end with the structured return block (status / task_folder / run_name / files).

Unlike cms/case, this stage is **cross-year** (no year axis — it appends all years) and produces ONE analysis asset per spec.

Engine: **Stata + PowerShell + logs**. Read `../haipipe-task-for-stata/ref/stata-dialect.md` first. This skill scaffolds the task-folder; worker `.do` logic is authored separately.


Position in the Stata sub-family
--------------------------------

```
/haipipe-task-for-stata-cms         1-CMS-Store, per year
/haipipe-task-for-stata-case        2-Case-Store, cohort × year
/haipipe-task-for-stata-data    ◀── you are here   (*-Data-Store, cross-year)
/haipipe-task-for-stata-reg         estimation      (coef tables → results/, LIGHT)
```


What this scaffolds
-------------------

```
tasks/{G}{NN}_<group>/                              ← group (e.g. R1_Regression_TraitOpioid)
└── C{NN}_data_pipeline_<study>/                     ← task-folder letter C = data stage ({LNN})
    ├── C{NN}_data_pipeline_<study>.do               dispatcher: <config> <step> <results_dir> <ws_root>  (NO year)
    ├── scripts/
    │   ├── 1-filter-case/                           filter-case.do
    │   ├── 2-filter-external/                       filter-external.do (physician traits, policy)
    │   ├── 3-full-variables/                        full-variables.do (derive + write ANALYSIS-*.dta)
    │   └── 4-describe/                              describe-data.do
    ├── configs/
    │   ├── <Spec>.do                                analysis spec: cohort, pairing, filters, var lists; paths from ${ws_root}
    │   └── run_data_<Spec>.yaml                     _meta: block + stata_config: pointer
    ├── run_data_steps.ps1                           orchestrator (~15 lines) from ../haipipe-task-for-stata/ref/run-stage-year-template.ps1 ($stata var; drop -year; sequential chain)
    ├── runs/
    │   └── run_data_<Spec>.ps1                      THIN entry from ../haipipe-task-for-stata/ref/run-ps1-template.ps1
    ├── sbatch/
    ├── results/                                     log/ · summary.txt (heavy → _WorkSpace)
    └── diagram/
```

- **RUNNAME grammar:** `run_data_<Spec>`  (analysis-spec; e.g.
  `run_data_1stPairOpioidRx_VisitLBP`). **No year** — cross-year append.
- **Steps (sequential chain):** `filter_case → filter_external →
  full_variables → describe → summary`.
- **Inputs:** `2-Case-Store/.../year-*/` CASES + BFAF panels (all years) +
  physician-trait + policy assets.
- **Heavy output:** `${data_output_file}` (`ANALYSIS-CMS-Filter.dta`) in
  the Data-Store.
- **Headline:** analysis-table N rows / N physicians after filters.


Commands
--------

```
/haipipe-task-for-stata-data                          ASK project / group / name / spec
/haipipe-task-for-stata-data <project> <group> <name>  scaffold direct
```


Scaffold flow
-------------

See `fn/scaffold.md`. Summary: identify project+group → collect `_meta` + analysis spec → create skeleton → seed `<run>.yaml` from `ref/config-seed.yaml` → copy `runs/<run>.ps1` → emit return contract.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded
artifacts: [paths created]
next:      author dispatcher .do + scripts/{1..4}-* workers; run haipipe-task-reviewer-agent before hand-copy
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
