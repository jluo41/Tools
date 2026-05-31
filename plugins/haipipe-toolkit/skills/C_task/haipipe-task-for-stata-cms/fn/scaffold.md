fn-scaffold: Scaffold a CMS-pipeline task-folder (Stata dialect)
================================================================

Extracts + enriches raw CMS claims per year into `_WorkSpace/1-CMS-Store/`.
Output: `tasks/{G}{NN}_<group>/{NN}_cms_pipeline/`.
Read `../haipipe-task/ref/stata-dialect.md` for the engine contract.


Step 1 — Identify project + task-group
---------------------------------------

- Auto-detect project from cwd (`examples/Proj*/`).
- ASK task-group if not given. CMS is the upstream-most stage; it usually
  lives in its own group (e.g. `D3_CMS-pipeline`). The project-local
  letter convention (cms/case/data/reg) applies — see stata-dialect.md.
  Scaffold a new group via `../haipipe-task/fn/task-group.md` if needed.


Step 2 — Collect metadata
--------------------------

- 2-digit NN: next free in this group (no gaps).
- task_name: `cms_pipeline` (or `<source>_cms_pipeline`).
- **Year axis:** which years get a run (default 2015..2020 → one
  `run_cms_<year>` each).
- Asset name + version (the `1-CMS-Store/cms_full/<asset>/` folder).
- `_meta:` block (purpose / note / input / output).


Step 3 — Create skeleton
-------------------------

```
{NN}_cms_pipeline/
├── {NN}_cms_pipeline.do        # dispatcher stub: args <config> <step> <year> <results_dir>
├── stata/                      # empty; workers authored later (b-*-All.do, c-Bene-Year.do, d-Year-Summary.do)
├── configs/
│   ├── cms_production.do       # stub: raw_cms path, keep-vars, skip_existing, run_* flags
│   └── run_cms_<year>.yaml     # from ref/config-seed.yaml, one per year
├── runs/
│   └── run_cms_<year>.ps1      # from ../haipipe-task/ref/run-ps1-template.ps1
├── run_cms_year.ps1            # orchestrator stub (phase1 4 extracts ∥; phase2 bene_year; phase3 summary)
├── sbatch/
├── results/
└── diagram/
```


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to `configs/run_cms_<year>.yaml`. Fill `_meta`,
set `stata_config: cms_production`, set `year:`. The real Stata globals
(raw paths, keep-vars, flags) live in `configs/cms_production.do`.


Step 5 — Run-script
-------------------

Copy `../haipipe-task/ref/run-ps1-template.ps1` to `runs/run_cms_<year>.ps1`.
Set `$CFG = "cms_production"`, the `$YEAR`/`$RUNNAME`, the `$REQUIRED`
raw-input precondition list, and point the orchestrator call at
`run_cms_year.ps1`.


Step 6 — Report
----------------

```
status:    ok
summary:   Scaffolded CMS-pipeline task <NN>_cms_pipeline under {G}{NN}_<group>; years <...>.
artifacts: [paths created]
next:      author dispatcher .do + stata/ workers; produce CODE_REVIEW.md; then runs/run_cms_<year>.ps1
```


MUST NOT
---------

- Place heavy `.dta` assets in `results/` — they go to `_WorkSpace/1-CMS-Store/`.
- Skip the `_meta:` block in `<run>.yaml`.
- Create `README.md` (doc surface is `diagram/`).
- Use papermill / `.ipynb` — this is the Stata dialect.
