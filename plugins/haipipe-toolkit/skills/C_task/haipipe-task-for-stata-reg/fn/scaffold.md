fn-scaffold: Scaffold a reg-pipeline task-folder (Stata dialect)
================================================================

Runs the estimation grid (OLS / IV / DID) on the data-stage analysis
table, writing LIGHT coefficient tables into `results/<RUNNAME>/`.
Output: `tasks/{G}{NN}_<group>/D{NN}_reg_<condition>_<pairing>/`
(task-folder letter D = reg stage).
Read `../haipipe-task-for-stata/ref/stata-dialect.md` for the engine contract.

KEY DIFFERENCE from cms/case/data: the primary output is LIGHT (coef
tables in-repo under `results/`), not a heavy `.dta` in `_WorkSpace/`.


Topic-split layout (recommended)
---------------------------------

One folder per condition (topic). The condition and pairing are encoded
in the folder name. The grid axes WITHIN the folder are
**window x estimator-family**:

  RUNNAME = run_reg_<window>_<family>
  window  = {af14d, af7d, ...}
  family  = {ols, iv, did, ols_windows}


Step 1 -- Identify project + task-group
---------------------------------------

- Auto-detect project from cwd (`examples/Proj*/`).
- ASK task-group. Reg work lives in the study group
  (e.g. `R1_Regression_TraitOpioid`) next to its case + data siblings.
- Confirm the upstream data-pipeline task exists (reg consumes its
  `ANALYSIS-*.dta`). If not, suggest `/haipipe-task-for-stata-data` first.


Step 2 -- Collect metadata (the grid)
-------------------------------------

- 2-digit NN: next free in this group.
- task_name: `reg_<condition>_<pairing>` (e.g. `reg_visitlbp_1stpair`).
- **The estimation grid** (topic-split):
  - Windows     (e.g. af14d, af7d)
  - Families    (ols, iv, did, ols_windows)
  - Workers per family:
    - OLS: run-1 progressive, run-2 lpm-logit, run-3 twopart, run-5 traitform
    - IV:  run-6 main, run-7 grid, run-8 overid
    - DID: run-9 staggered TWFE, run-10 Callaway-Sant'Anna
    - ols_windows: run-4 (loops all windows internally, window-agnostic)
- `_meta:` block per RUNNAME.
- Shared Stata config (.do): data path, data version, cohort name.


Step 3 -- Create skeleton
-------------------------

```
D{NN}_reg_<condition>_<pairing>/
+-- configs/
|   +-- <Cohort>.do                          shared Stata globals (data path)
+-- scripts/                                 worker .do files (SHARED)
|   +-- run-{N}-*-<family>-<variant>.do      numbered 1-10
+-- runs/
|   +-- run_reg_<window>_<family>.ps1        thin launcher (one per RUNNAME)
+-- sbatch/
|   +-- run-all.ps1                          fan-out all runs
+-- results/
|   +-- run_reg_<window>_<family>/           per-run output
|       +-- log/
|       +-- tables/
+-- diagram/
```


Step 4 -- Shared config (.do)
-----------------------------

Create `configs/<Cohort>.do` with shared Stata globals (data path, data
version, cohort name, res_root). Stata dialect uses `.do` for configs,
not `.yaml` -- Stata cannot parse YAML. Per-run parameters (window,
res_dir) pass via env vars in the `.ps1` runner.


Step 5 -- Run-script (reg runtime contract)
-------------------------------------------

Reg is **dispatcher-less** -- each `runs/<RUNNAME>.ps1` calls worker
`scripts/*.do` DIRECTLY (no dispatcher, no year axis).

Three env vars cross the `clear all` boundary:

  $env:HAIPIPE_WS_ROOT     absolute _WorkSpace path
  $env:HAIPIPE_REG_WINDOW  outcome BFAF window (af14d, af7d, ...)
  $env:HAIPIPE_RES_DIR     absolute per-run results dir

Each `.ps1`:

- resolves the absolute `_WorkSpace` (walk up to `pyproject.toml`)
  and exports as `$env:HAIPIPE_WS_ROOT`;
- sets `$env:HAIPIPE_REG_WINDOW` to the window for this run;
- sets `$env:HAIPIPE_RES_DIR` to `$TASK_DIR\results\<RUNNAME>`;
- runs Stata from the task folder via Push-Location / Pop-Location;
- calls workers directly: `& $stata /e do "scripts/<worker>.do"`.

Each worker `.do` reads env vars after `clear all`:

```stata
if "${data_file}" == "" {
    global ws_root : environment HAIPIPE_WS_ROOT
    if "${ws_root}" == "" global ws_root "_WorkSpace"
    do "configs/<Cohort>.do"
}
global res_dir : environment HAIPIPE_RES_DIR
if "${res_dir}" == "" global res_dir "results/${outcome_bfaf_window}"
```

A `.ps1` may loop a worker family (e.g. run-1..5 for OLS). The special
`run_reg_ols_windows.ps1` does NOT set HAIPIPE_REG_WINDOW (worker 4
loops all windows internally).

NO path hardcodes the folder name -- renamable by `mv`.


Step 5b -- Describe / QC run
-----------------------------

Reg's "describe" is a **coefficient-sanity** report. A
`runs/run_describe.ps1` that runs `scripts/d-Reg-Describe.do`
(read-only) which parses per-run logs and writes `reg-describe.txt`:
per cell the trait coef / SE / N (first-stage F for IV), FLAGS any cell
that failed to estimate. Built-ins only; `capture`-guarded.


Step 6 -- Report
----------------

```
status:    ok
summary:   Scaffolded reg task D{NN}_reg_<cond>_<pair> with <N> runs (window x family grid).
artifacts: [paths created]
next:      author worker .do files; CODE_REVIEW.md (IV validity / spec / clustering); then runs/*.ps1
```


MUST NOT
---------

- Send coefficient tables to `_WorkSpace/` -- reg output is LIGHT,
  in-repo under `results/<RUNNAME>/`.
- Skip the `_meta:` block. Create `README.md`. Use papermill / `.ipynb`.
- Collapse the WHOLE grid (all windows/families) into one run.
  Keep runs at the window x estimator-family grain so results stay
  legible. (Grouping a worker family in one .ps1 is fine; collapsing
  distinct windows or estimator families into a single run is not.)
