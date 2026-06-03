fn-scaffold: Scaffold a case-pipeline task-folder (Stata dialect)
=================================================================

Triggers cohort cases + feature panels per (cohort × year) into
`_WorkSpace/2-Case-Store/`. Output:
`tasks/{G}{NN}_<group>/B{NN}_case_pipeline_<study>/`  (task-folder letter B = case stage).
Read `../haipipe-task/ref/stata-dialect.md` for the engine contract.


Step 1 — Identify project + task-group
---------------------------------------

- Auto-detect project from cwd (`examples/Proj*/`).
- ASK task-group. Case work usually lives in a study group
  (e.g. `R1_Regression_TraitOpioid`) alongside its data + reg siblings.
- Confirm the upstream CMS-pipeline task exists (case consumes its
  per-year `Neat-*.dta` + `Bene_Info-*.dta`). If not, suggest
  `/haipipe-task-for-stata-cms` first.


Step 2 — Collect metadata
--------------------------

- 2-digit NN: next free in this group.
- task_name: `case_pipeline_<study>` (e.g. `case_pipeline_opioid`).
- **Cohort list:** which clinical cohorts to trigger (VisitLBP, VisitCancer,
  VisitHeadache, VisitMusc, VisitOsteo, ...). One `configs/<Cohort>.do` each.
- **Year axis:** default 2015..2020.
- Topic flags: which feature chains to build (pde/claims/lines/outpt;
  opioidrx subchain on/off).
- `_meta:` block.


Step 3 — Create skeleton
-------------------------

```
B{NN}_case_pipeline_<study>/        # task-folder letter B = case stage ({LNN})
├── B{NN}_case_pipeline_<study>.do  # dispatcher: from ref/dispatcher-do-template.do (<config> <step> <year> <results_dir> <ws_root>)
├── scripts/
│   ├── cases/                      # trigger-cases-<script>.do
│   └── feat/                       # bene-*, bfaf-*, shared-* workers
├── configs/
│   ├── <Cohort>.do                 # one per cohort: ICD codes, topic flags
│   └── run_case_<Cohort>_<year>.yaml
├── runs/
│   └── run_case_<Cohort>_<year>.ps1
├── run_case_year.ps1               # orchestrator stub
├── sbatch/
├── results/
└── diagram/
```


Step 4 — Seed config
---------------------

For each (cohort × year), copy `ref/config-seed.yaml` to
`configs/run_case_<Cohort>_<year>.yaml`. Fill `_meta`, set
`stata_config: <Cohort>`, `cohort:`, `year:`. ICD codes + topic flags
live in `configs/<Cohort>.do`.


Step 5 — Run-script
-------------------

Copy `../haipipe-task/ref/run-ps1-template.ps1` to
`runs/run_case_<Cohort>_<year>.ps1`. Set `$CFG = "<Cohort>"`,
`$RUNNAME = "run_case_<Cohort>_<year>"`, the `$REQUIRED` CMS-Store +
External-Store precondition list, and point at `run_case_year.ps1`.


Step 6 — Report
----------------

```
status:    ok
summary:   Scaffolded case-pipeline task <NN>_case_pipeline_<study> under {G}{NN}_<group>; cohorts <...> × years <...>.
artifacts: [paths created]
next:      author dispatcher .do + scripts/{cases,feat}/ workers; CODE_REVIEW.md; then runs/run_case_<Cohort>_<year>.ps1
```


MUST NOT
---------

- Place heavy `.dta` panels in `results/` — they go to `_WorkSpace/2-Case-Store/`.
- Skip the `_meta:` block. Create `README.md`. Use papermill / `.ipynb`.
- Symlink another cohort's `configs/` — each cohort owns its `.do`.
