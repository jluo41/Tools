fn-scaffold: Scaffold a CMS-pipeline task-folder (Stata dialect)
================================================================

Extracts + enriches raw CMS claims per year into `_WorkSpace/1-CMS-Store/`.
Output: `tasks/{G}{NN}_<group>/A{NN}_cms_pipeline/`  (task-folder letter A = cms stage; see {LNN} alphabet in stata-dialect.md).
Read `../haipipe-task-for-stata/ref/stata-dialect.md` for the engine contract.


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
A{NN}_cms_pipeline/
├── A{NN}_cms_pipeline.do       # dispatcher: from ref/dispatcher-do-template.do (<config> <step> <year> <results_dir> <ws_root>)
├── scripts/                    # empty; workers authored later (b-*-All.do, c-Bene-Year.do, d-Year-Summary.do)
├── configs/
│   ├── cms_production.do       # stub: keep-vars, skip_existing, run_* flags; paths built from ${ws_root}
│   └── run_cms_<year>.yaml     # from ref/config-seed.yaml, one per year
├── run_cms_year.ps1            # orchestrator (~15 lines): from ../haipipe-task-for-stata/ref/run-stage-year-template.ps1 (phase1 4 extracts ∥; phase2 bene_year; phase3 summary)
├── runs/
│   └── run_cms_<year>.ps1      # THIN per-year entry: from ../haipipe-task-for-stata/ref/run-ps1-template.ps1
├── sbatch/                     # run_cms_<y0>-<y1>.ps1: loops the runs/ entries
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

Copy `../haipipe-task-for-stata/ref/run-stage-year-template.ps1` to `run_cms_year.ps1`
and fill the step names (4 extracts in parallel → bene_year → summary).
Copy `../haipipe-task-for-stata/ref/run-ps1-template.ps1` to `runs/run_cms_<year>.ps1`,
one THIN entry per year:
`& "$PSScriptRoot\..\run_cms_year.ps1" -cfg cms_production -year <year>`.
Add `sbatch/run_cms_<y0>-<y1>.ps1` looping the runs/ entries. Follow the
"Script style + server constraints" contract in stata-dialect.md: ASCII-only,
no `pwsh`, `$stata` is one editable line, no relative `_WorkSpace`.


Step 5b — Describe / QC run
---------------------------

Add the read-only QC run (see "Describe / QC run" in `../haipipe-task-for-stata/ref/stata-dialect.md`):
- `scripts/d-Cms-Describe.do` — loops the `year-*` dirs under `${cms_asset_path}`
  and `file write`s `cms-describe.txt`: per year the Neat panel inventory + row
  counts, Bene_Info rows, and claim service-date ranges (sanity: dates are `%td`
  and within the year). Built-ins only (no `distinct`); `capture`-guarded.
- Wire a `describe` branch into the dispatcher; add `runs/run_describe_cms.ps1`
  (resolves Stata + `ws_root`, runs only the `describe` step — no rebuild).


Step 6 — Report
----------------

```
status:    ok
summary:   Scaffolded CMS-pipeline task A<NN>_cms_pipeline under {G}{NN}_<group>; years <...>.
artifacts: [paths created]
next:      author dispatcher .do + scripts/ workers + d-Cms-Describe.do; stata-script-reviewer-agent before hand-copy; then runs/run_cms_<year>.ps1 (+ run_describe_cms.ps1)
```


MUST NOT
---------

- Place heavy `.dta` assets in `results/` — they go to `_WorkSpace/1-CMS-Store/`.
- Skip the `_meta:` block in `<run>.yaml`.
- Create `README.md` (doc surface is `diagram/`).
- Use papermill / `.ipynb` — this is the Stata dialect.
