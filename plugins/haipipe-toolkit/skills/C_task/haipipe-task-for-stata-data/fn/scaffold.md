fn-scaffold: Scaffold a data-pipeline task-folder (Stata dialect)
=================================================================

Assembles the cross-year, regression-ready analysis table into
`_WorkSpace/*-Data-Store/`. Output:
`tasks/{G}{NN}_<group>/{NN}_data_pipeline_<study>/`.
Read `../haipipe-task/ref/stata-dialect.md` for the engine contract.

NOTE: this stage is **cross-year** — the dispatcher takes
`<config> <step> <results_dir>` with NO year argument; `filter_case`
appends all per-year CASES internally.


Step 1 — Identify project + task-group
---------------------------------------

- Auto-detect project from cwd (`examples/Proj*/`).
- ASK task-group. Data work lives in the study group
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
{NN}_data_pipeline_<study>/
├── {NN}_data_pipeline_<study>.do   # dispatcher stub: <config> <step> <results_dir>  (no year)
├── stata/
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

Copy `../haipipe-task/ref/run-ps1-template.ps1` to
`runs/run_data_<Spec>.ps1`. Set `$CFG = "<Spec>"`,
`$RUNNAME = "run_data_<Spec>"`, the `$REQUIRED` Case-Store + trait/policy
precondition list, and point at `run_data_steps.ps1`. The dispatcher call
inside the orchestrator omits the year argument.


Step 6 — Report
----------------

```
status:    ok
summary:   Scaffolded data-pipeline task <NN>_data_pipeline_<study> under {G}{NN}_<group>; spec <Spec>.
artifacts: [paths created]
next:      author dispatcher .do + stata/{1..4}-* workers; CODE_REVIEW.md; then runs/run_data_<Spec>.ps1
```


MUST NOT
---------

- Place the heavy `ANALYSIS-*.dta` in `results/` — it goes to the Data-Store.
- Add a year axis to the RUNNAME — this stage is cross-year by design.
- Skip the `_meta:` block. Create `README.md`. Use papermill / `.ipynb`.
