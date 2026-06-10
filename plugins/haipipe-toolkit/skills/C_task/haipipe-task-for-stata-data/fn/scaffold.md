fn-scaffold: Scaffold a data-pipeline task-folder (Stata dialect)
=================================================================

Assembles the cross-year, regression-ready analysis table into
`_WorkSpace/*-Data-Store/`. Output:
`tasks/{G}{NN}_<group>/C{NN}_data_pipeline_<study>/`  (task-folder letter C = data stage).
Read `../haipipe-task-for-stata/ref/stata-dialect.md` for the engine contract.

NOTE: this stage is **cross-year** — the dispatcher takes
`<config> <step> <results_dir>` with NO year argument; `filter_case`
appends all per-year CASES internally.


Step 1 — Identify project + task-group
---------------------------------------

- Auto-detect project from cwd (`examples/Proj*/`).
- AUTO_MODE: infer from cwd or return `status: blocked`. Interactive: ASK task-group. Data work lives in the study group
  (e.g. `R1_Regression_TraitOpioid`) next to its case + reg siblings.
- Confirm the upstream case-pipeline task exists (data consumes its
  Case-Store panels). If not, suggest `/haipipe-task-for-stata-case` first.


Step 2 — Collect metadata
--------------------------

- 2-digit NN: next free in this group.
- task_name: `data_pipeline_<study>` (e.g. `data_pipeline_opioid`).
- **Analysis spec:** cohort + pairing + filter choices that name the run
  (e.g. `1stPairOpioidRx_VisitLBP`). One `configs/<Spec>.do` each.
- Filters: first-visit rule, age/year window, MD/DO restriction,
  review-count threshold, whether policy merge is on.
- `_meta:` block.


Step 3 — Create skeleton
-------------------------

```
C{NN}_data_pipeline_<study>/        # task-folder letter C = data stage ({LNN})
├── C{NN}_data_pipeline_<study>.do  # dispatcher: from ref/dispatcher-do-template.do (<config> <step> <results_dir> <ws_root>; no year)
├── scripts/
│   ├── 1-filter-case/
│   ├── 2-filter-external/
│   ├── 3-full-variables/
│   └── 4-describe/
├── configs/
│   ├── <Spec>.do
│   └── run_data_<Spec>.yaml
├── runs/
│   └── run_data_<Spec>.ps1
├── run_data_steps.ps1              # sequential orchestrator stub
├── sbatch/
├── results/
└── diagram/
```


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to `configs/run_data_<Spec>.yaml`. Fill
`_meta`, set `stata_config: <Spec>`, `spec:`. Filter rules + variable
lists live in `configs/<Spec>.do`.


Step 5 — Run-script
-------------------

Copy `../haipipe-task-for-stata/ref/run-stage-year-template.ps1` to `run_data_steps.ps1`
and fill the sequential chain (the dispatcher call omits the year argument).
Copy `../haipipe-task-for-stata/ref/run-ps1-template.ps1` to `runs/run_data_<Spec>.ps1`,
one THIN entry per spec:
`& "$PSScriptRoot\..\run_data_steps.ps1" -cfg <Spec>`.
Follow the "Script style + server constraints" contract in stata-dialect.md
(ASCII-only, no `pwsh`, one `$stata` line, no ceremony).


Step 5b — Describe / QC run
---------------------------

The data stage already has a `describe` dispatch step (`scripts/4-describe/describe-data.do`).
Ensure it is a proper QC report and ALSO expose it as a describe-only run (see
"Describe / QC run" in `../haipipe-task-for-stata/ref/stata-dialect.md`):
- `describe-data.do` reports: N, distinct benes / npis (`egen tag` — NOT
  `distinct`, which aborts `r(199)` on a clean server), year dist, treatment
  (trait) summary, outcome means, key-control missingness, IV first-stage corr.
  Keep every block `capture`-guarded.
- `runs/run_describe_<Spec>.ps1` — resolves Stata + `ws_root`, runs ONLY the
  `describe` step on the built `ANALYSIS-*.dta` (no rebuild).


Step 6 — Report
----------------

```
status:    ok
summary:   Scaffolded data-pipeline task <NN>_data_pipeline_<study> under {G}{NN}_<group>; spec <Spec>.
artifacts: [paths created]
next:      author dispatcher .do + scripts/{1..4}-* workers (4-describe = QC); CODE_REVIEW.md; then runs/run_data_<Spec>.ps1 (+ run_describe_<Spec>.ps1)
```


MUST NOT
---------

- Place the heavy `ANALYSIS-*.dta` in `results/` — it goes to the Data-Store.
- Add a year axis to the RUNNAME — this stage is cross-year by design.
- Skip the `_meta:` block. Create `README.md`. Use papermill / `.ipynb`.
