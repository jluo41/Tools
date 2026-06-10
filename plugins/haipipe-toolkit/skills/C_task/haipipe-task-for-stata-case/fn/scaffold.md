fn-scaffold: Scaffold a case-pipeline task-folder (Stata dialect)
=================================================================

Triggers cohort cases + feature panels per (cohort x source x year) into
`_WorkSpace/2-Case-Store/`. Output:
`tasks/{G}{NN}_<group>/B{NN}_case_pipeline_<study>/`  (task-folder letter B = case stage).
Read `../haipipe-task-for-stata/ref/stata-dialect.md` for the engine contract.


Step 1 -- Identify project + task-group
---------------------------------------

- Auto-detect project from cwd (`examples/Proj*/`).
- AUTO_MODE: infer from cwd or return `status: blocked`. Interactive: ASK task-group. Case work usually lives in a study group
  (e.g. `C01_CaseData_TraitOpioid`) alongside its data + reg siblings.
- Confirm the upstream CMS-pipeline task exists (case consumes its
  per-year `Neat-*.dta` + `Bene_Info-*.dta`). If not, suggest
  `/haipipe-task-for-stata-cms` first.


Step 2 -- Collect metadata
--------------------------

- 2-digit NN: next free in this group.
- task_name: `case_pipeline_<study>` (e.g. `case_pipeline_visitlbp`).
- **Cohort list:** which clinical cohorts to trigger (VisitLBP, VisitCancer,
  VisitHeadache, VisitMusc, VisitOsteo, ...). One `configs/<Cohort>.do` each.
- **Source list:** which CMS sources to scaffold runners for.
  Default: `[synth, full]`. Synth = laptop-safe synthetic CMS data.
  Full = real CMS PHI, server-only.
- **Year axis:** default 2015..2020.
- Topic flags: which feature chains to build (pde/claims/lines/outpt;
  opioidrx subchain on/off).
- `_meta:` block.


Step 3 -- Create skeleton
-------------------------

```
B{NN}_case_pipeline_<study>/
|-- case_pipeline.do               dispatcher: <config> <step> <year> <results_dir> <ws_root> <source>
|-- run_case_year.ps1              year orchestrator (topic flags, parallel Stata jobs)
|-- scripts/
|   |-- cases/                     trigger-cases-<script>.do
|   |-- feat/                      bene-*, bfaf-*, shared-* workers
|   +-- d-Case-Describe.do        cross-year QC
|-- configs/
|   |-- <Cohort>.do                SHARED cohort config (ICD codes, topic flags, paths)
|   |-- _source_synth.do           source selector: cms_source=synth
|   |-- _source_full.do            source selector: cms_source=full
|   |-- <Cohort>_synth_<year>.do   PER-RUN config (thin wrapper)
|   +-- <Cohort>_full_<year>.do    PER-RUN config (thin wrapper)
|-- runs/
|   |-- run_case_<Cohort>_synth_<year>.ps1
|   |-- run_case_<Cohort>_full_<year>.ps1
|   +-- run_describe_<Cohort>.ps1
|-- sbatch/
|   |-- run_all_<y0>-<y1>_synth.ps1
|   +-- run_all_<y0>-<y1>_real.ps1
|-- results/
+-- diagram/
```


Step 4 -- Seed source selectors
-------------------------------

Create two source selector files in `configs/`:

`configs/_source_synth.do`:
```stata
// _source_synth.do -- CMS input = SYNTHETIC store (laptop-safe)
global cms_source        "synth"
global cms_asset_name    "cms_synth"
global cms_asset_version "v0002_enrich"
```

`configs/_source_full.do`:
```stata
// _source_full.do -- CMS input = REAL store (server, PHI)
global cms_source        "full"
global cms_asset_name    "cms_full"
global cms_asset_version "v0001_0130"
```

ASK the user for the correct asset versions. The version strings above
are defaults from ProjB; other projects may differ.


Step 5 -- Seed per-run configs
------------------------------

For each (cohort x source x year), create a thin per-run `.do` config
in `configs/`. The naming convention mirrors the RUNNAME:

  RUNNAME: `run_case_<Cohort>_{synth|full}_<year>`
  config:  `configs/<Cohort>_{synth|full}_<year>.do`
  runner:  `runs/run_case_<Cohort>_{synth|full}_<year>.ps1`
  results: `results/run_case_<Cohort>_{synth|full}_<year>/`

Each per-run config is a thin wrapper (3 lines) that loads the source
selector + shared cohort config + pins the year. Use `ref/config-seed-run.do`
as template:

```stata
// Per-run config: <Cohort> <source> <year>
// Matched to: runs/run_case_<Cohort>_<source>_<year>.ps1
do configs/_source_<source>.do
do configs/<Cohort>.do
global data_year <year>
```

This ensures the four-sister convention holds: every RUNNAME has a
matching config file in `configs/`, a runner in `runs/`, and (after
execution) a results folder in `results/`.

The shared `<Cohort>.do` remains the single source of truth for ICD
codes, topic flags, and path templates. The per-run `.do` just selects
which source + year to use.

IMPORTANT: the audit/plan workflow checks four-sister alignment by
scanning `configs/` for stems that match `runs/` stems (minus the
`run_case_` prefix). A missing per-run config is flagged as FIXABLE.
The fix is to generate the thin wrapper automatically.


Step 6 -- Seed YAML meta configs (optional)
--------------------------------------------

Optionally, also create `configs/run_case_<Cohort>_<source>_<year>.yaml`
with a `_meta:` block from `ref/config-seed.yaml`. This carries
structured metadata (purpose, input, output) that the workflow layer
reads. The `.do` config is what Stata loads; the `.yaml` is what the
haipipe-task workflow layer reads.

If only one format is created, prefer the `.do` (Stata needs it).
The `.yaml` is a bonus for workflow tooling.


Step 7 -- Run-script
--------------------

Copy `../haipipe-task-for-stata/ref/run-ps1-template.ps1` to thin
per-run entries in `runs/`. Each is 2 lines:

```powershell
# <Cohort> case pipeline - <source> <year>
& "$PSScriptRoot\..\run_case_year.ps1" -cfg <Cohort> -year <year> -source <source>
```

sbatch/ batchers loop the runs/ entries per source:

`sbatch/run_all_<y0>-<y1>_synth.ps1`:
```powershell
# Run all years for <Cohort> - synth (laptop-safe)
Get-ChildItem "$PSScriptRoot\..\runs\run_case_<Cohort>_synth_*.ps1" | Sort-Object Name | ForEach-Object { & $_.FullName }
```

Follow the "Script style + server constraints" contract in
stata-dialect.md (ASCII-only, no `pwsh`, one `$stata` line).


Step 7b -- Describe / QC run
-----------------------------

Add the read-only QC run (see "Describe / QC run" in
`../haipipe-task-for-stata/ref/stata-dialect.md`):
- `scripts/d-Case-Describe.do`
- Wire a `describe` branch into the dispatcher.
- `runs/run_describe_<Cohort>.ps1` -- resolves Stata + `ws_root`, runs
  only the `describe` step (`-source synth|full` picks which case asset).


Step 8 -- Report
-----------------

```
status:    ok
summary:   Scaffolded case-pipeline B{NN}_case_pipeline_<study>;
           cohorts <...> x sources [synth, full] x years <...>.
           Per-run configs: N, runners: N, source selectors: 2.
artifacts: [paths created]
next:      author dispatcher .do + scripts/{cases,feat}/ workers;
           run haipipe-task-reviewer-agent; then hand-copy to server.
```


MUST NOT
--------

- Place heavy `.dta` panels in `results/` -- they go to `_WorkSpace/2-Case-Store/`.
- Skip the per-run config. Every RUNNAME must have a matching `.do` in `configs/`.
- Use `pwsh` in any `.ps1`. Use `powershell` or the fallback pattern.
- Include non-ASCII characters (em-dashes, box-drawing) in `.ps1` files.
- Symlink another cohort's `configs/` -- each cohort owns its `.do`.
