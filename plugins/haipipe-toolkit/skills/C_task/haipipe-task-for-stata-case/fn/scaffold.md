fn-scaffold: Scaffold a case-pipeline task-folder (Stata dialect)
=================================================================

Triggers cohort cases + feature panels per (cohort × year) into
`_WorkSpace/2-Case-Store/`. Output:
`tasks/{G}{NN}_<group>/B{NN}_case_pipeline_<study>/`  (task-folder letter B = case stage).
Read `../haipipe-task-for-stata/ref/stata-dialect.md` for the engine contract.


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
│   ├── feat/                       # bene-*, bfaf-*, shared-* workers
│   └── d-Case-Describe.do          # `describe` QC worker (cross-year, read-only)
├── configs/
│   ├── <Cohort>.do                 # one per cohort: ICD codes, topic flags
│   └── run_case_<Cohort>_<year>.yaml
├── runs/
│   ├── run_case_<Cohort>_<year>.ps1
│   └── run_describe_<Cohort>.ps1   # describe-ONLY QC run (no rebuild)
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

Copy `../haipipe-task-for-stata/ref/run-stage-year-template.ps1` to `run_case_year.ps1`
and fill the topic-chain steps. Copy `../haipipe-task-for-stata/ref/run-ps1-template.ps1`
to `runs/run_case_<Cohort>_<year>.ps1`, one THIN entry per (cohort × year):
`& "$PSScriptRoot\..\run_case_year.ps1" -cfg <Cohort> -year <year>`.
sbatch/ batchers loop the runs/ entries. Follow the "Script style + server
constraints" contract in stata-dialect.md (ASCII-only, no `pwsh`, one `$stata`
line, no ceremony).


Step 5b — Describe / QC run
---------------------------

Add the read-only QC run (see "Describe / QC run" in `../haipipe-task-for-stata/ref/stata-dialect.md`):
- `scripts/d-Case-Describe.do` — loops the `year-*` dirs under `${case_asset_path}`
  and `file write`s `case-describe.txt`: per year #cases, distinct benes / npis
  (via `egen tag` — NOT `distinct`), `visit_type` split, the pde_bn enrichment
  check (rows with >=1 rx), `obs_dt` range. `capture`-guarded; read-only.
- Wire a `describe` branch into the dispatcher (`do "scripts/d-Case-Describe.do" \`year'`).
- `runs/run_describe_<Cohort>.ps1` — resolves Stata + `ws_root`, runs only the
  `describe` step (dummy year; `-source synth|full` picks which case asset).


Step 6 — Report
----------------

```
status:    ok
summary:   Scaffolded case-pipeline task <NN>_case_pipeline_<study> under {G}{NN}_<group>; cohorts <...> × years <...>.
artifacts: [paths created]
next:      author dispatcher .do + scripts/{cases,feat}/ workers + d-Case-Describe.do; CODE_REVIEW.md; then runs/run_case_<Cohort>_<year>.ps1 (+ run_describe_<Cohort>.ps1)
```


MUST NOT
---------

- Place heavy `.dta` panels in `results/` — they go to `_WorkSpace/2-Case-Store/`.
- Skip the `_meta:` block. Create `README.md`. Use papermill / `.ipynb`.
- Symlink another cohort's `configs/` — each cohort owns its `.do`.
