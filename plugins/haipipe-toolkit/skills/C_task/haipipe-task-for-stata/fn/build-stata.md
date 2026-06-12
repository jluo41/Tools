fn/build-stata — Author Stata pipeline code
=============================================

Extends `fn/scaffold.md` (which creates the skeleton) into full authoring: write dispatcher branches, worker scripts, configs, and orchestrator logic. This is what the creator agent does during Stage 2 of the lifecycle.


When to call
------------

As Stage 2 of the `/haipipe-task` lifecycle on a Stata task folder.
Also callable standalone: `/haipipe-task-for-stata build <task-folder-path>`

Prerequisite: `fn/plan-stata.md` has been run (plan.yaml exists).


Mode: existing task folder (match-existing)
-------------------------------------------

When building into a task folder that already has authored code (e.g., adding a new cohort config to an existing data-pipeline task):

1. **Read existing patterns first.** Scan the task folder for:
   - Resolve-StataExe function presence (if yes, use it in new files)
   - Config structure (section headers, global naming conventions)
   - Runner structure (thin delegate vs self-orchestrating)
   - Precondition check presence (if yes, replicate in new runners)
   - Manifest/config-snapshot presence (if yes, replicate)
   - STATATMP setup (if yes, replicate in new orchestrators)

2. **Match, do not override.** New files MUST follow the conventions
   already established in the task folder, even if those conventions
   differ from the default templates. Consistency within a task folder
   beats template compliance.

3. **When to deviate.** Only deviate from existing patterns when:
   - The existing pattern has a known bug (document in the file header)
   - The plan explicitly says to refactor
   - The new file is in a different topology


Procedure
---------

### Step 0 — Read the plan

Read `workflow/plan.yaml` and all `workflow/plan-script-*.yaml`.
These define WHAT to build. The plan's phases and steps map to:
- Dispatcher `.do` branches (one `else if` per step)
- Worker `.do` scripts (one file per step in `scripts/`)
- Orchestrator `.ps1` blocks (topic grouping + parallelism)
- Config globals (paths, flags, parameters)

### Step 1 — Author dispatcher (cms/case/data stages)

Read `ref/dispatcher-do-template.do` as the starting template.

For each step in the plan:
1. Add an `else if` branch to the dispatcher
2. The branch calls `do "scripts/<subdir>/<worker>.do" <year>`
3. Add the step's output file to the skip-if-exists map (idempotency)

**Dispatcher contract:**
```stata
args config_file step year results_dir ws_root [source]
// load config
// mkdir dirs
// log open
// skip-if-exists check
// dispatch by step name
// log close
```

For reg stage: NO dispatcher — workers are called directly by .ps1 runners.

### Step 2 — Author worker scripts

For each step, create `scripts/<subdir>/<worker>.do`:

**Worker contract:**
- Receives year as arg (from dispatcher) + globals (from config)
- Reads input from `_WorkSpace/` or prior step's output
- Writes output to `${year_dir}/` or `${temp_dir}/`
- NO SSC except `rangejoin` (the ONE allowed exception — installed on CMS server)
- Uses `egen tag()` for distinct counts (NOT SSC `distinct`)
- 1-2 line header comment, no banners

**Stage-specific patterns:**

cms workers: extract + clean one CMS file type per year
case workers: merge cases with CMS claims within BFAF time windows
data workers: filter + join + derive analysis variables (cross-year)
reg workers: estimate one model specification (OLS/IV/DID)

### Step 3 — Author orchestrator (cms/case/data stages)

Read `ref/run-stage-year-template.ps1` as the starting template.

Build the orchestrator (`run_<stage>_year.ps1`, <=30 lines) with:
1. Param block: `$cfg`, `$year`, `$source` (case only)
2. `$ErrorActionPreference = "Stop"`
3. `$stata` = ONE editable line (no resolver functions)
4. `$dir = $PSScriptRoot` + repo root walk-up for `$ws`
5. Config validation (`if -not Test-Path configs/$cfg.do`)
6. `$wsRoot` + `$resultsDir` as named variables
7. `New-Item` for results dir + log/ subdirectory
8. `$base` + `$tail` for Stata dispatcher args
9. Phase blocks: `Start-Process ... -PassThru` for parallel, `-PassThru -Wait` for sequential
10. Final `Write-Host` done message

**CMS server rules (baked in):**
- NO `Start-Job` (constrained language mode)
- `$stata` = ONE editable line, no Resolve-StataExe function
- Bare `Start-Process ... -PassThru` + `Wait-Process`, no helper functions
- Pure ASCII in .ps1 (no em-dash, no Unicode)

### Step 3b — Author reg runners (reg stage only)

Reg is DISPATCHER-LESS — each `.ps1` runner is self-contained.
Read `ref/run-ps1-reg-template.ps1` as the starting template.

Build each runner (`runs/run_reg_<RUNNAME>.ps1`) with:
1. `$ErrorActionPreference = "Stop"`
2. `$TASK_DIR = Split-Path -Parent $PSScriptRoot`
3. Repo root walk-up via `pyproject.toml`
4. `Resolve-StataExe` function (auto-detects edition + version)
5. `$env:HAIPIPE_WS_ROOT` = `Join-Path $WS_ROOT "_WorkSpace"`
6. `$env:HAIPIPE_RUN_CONFIG` = `"<RUNNAME>"` (matches per-run config stem)
7. `$workers = @(...)` — list of worker .do filenames for this estimator family
8. `Push-Location $TASK_DIR` + `foreach ($w in $workers) { & $stata /e do "scripts/$w" }`

**Reg runner rules:**
- Resolve-StataExe IS allowed (auto-detects; matches data-stage pattern)
- Direct `& $stata /e do` — NOT `Start-Process` (sequential workers)
- Each worker reads its own config via `$env:HAIPIPE_RUN_CONFIG`
- STATATMP: only needed if any worker uses `preserve` (add if so)

### Step 4 — Author configs

**Shared config** (`configs/<Cohort>.do`):
- All globals that don't change per run
- ICD codes, BFAF windows, topic flags, output paths
- Uses `${ws_root}` and `${cms_source}` (set by source selector / dispatcher)

**Source selectors** (case stage only):
- `configs/_source_synth.do`: sets `cms_source`, `cms_asset_name`, `cms_asset_version` for synth
- `configs/_source_full.do`: same for full/real

**Per-run configs** (thin wrappers):
- `configs/<Cohort>_{synth|full}_{year}.do`: loads source selector + shared config + pins year
- Generated from `ref/config-seed-run.do`

**Reg configs** (two-layer chain, from `ref/config-seed-reg.do` + `ref/config-seed-reg-run.do`):
- Shared: `configs/<Cohort>_<Pairing>.do` — data path + version + res_root
- Shared synth: `configs/<Cohort>_<Pairing>_synth.do` — same but synth data version
- Per-run: `configs/run_reg_<RUNNAME>.do` — loads shared config + pins `outcome_bfaf_window` + `res_dir`
- DID per-run: same + adds `global file_policy "${ws_root}/0-External-Store/Policy/Policy-State-Year.dta"`
- Controls, outcomes, treatment, instruments live in worker .do scripts (NOT config) because different workers within the same run have different RHS.

### Step 5 — Author thin runners + sbatch

**cms/case/data thin runners** (`runs/run_<stage>_<RUNNAME>.ps1`):
- 2 lines: comment + call to orchestrator with args
- From `ref/run-ps1-template.ps1`

**Reg runners** (`runs/run_reg_<RUNNAME>.ps1`):
- Self-contained (~30-38 lines): from `ref/run-ps1-reg-template.ps1`
- NOT thin delegates — each runner IS its own orchestrator

**Sbatch batchers** (`sbatch/run_all_*.ps1` or `sbatch/run-<cohort>-<est>-all.ps1`):
- Reg: per-estimator and per-source batchers using `& powershell -File`
- cms/case/data: multi-year batchers

**Describe runner** (`runs/run_describe_<Cohort>.ps1`):
- Standalone (doesn't go through orchestrator)
- Has its own Stata exe resolution + STATATMP
- Calls dispatcher with `describe` step

### Step 6 — Author describe/QC script

Stages cms/case/data ship a mandatory describe step:
- `scripts/d-<Stage>-Describe.do` (or `scripts/d-Case-Describe.do`)
- Walks output directory, counts rows per file
- Uses ONLY built-in Stata (`egen tag`, `summarize`, `tabulate`)
- NO SSC (`distinct`, `ftools`, etc.)
- Writes human-readable report to results/

Reg stage: describe is OPTIONAL. Stata logs + .tex coefficient tables are self-documenting. Skip unless the plan explicitly requests a describe step.

### Step 7 — Validate

Run `fn/audit-stata.md` on the authored code:
- Four-sister alignment
- Three-layer config consistency
- STATATMP present
- No SSC in describe scripts
- Pure ASCII in .ps1

### Step 8 — Report

```
🔨 Build: <task_name>
   dispatcher: <name>.do (<N> step branches)
   workers: <M> scripts in scripts/
   orchestrator: <name>.ps1 (<K> topic blocks)
   configs: <L> (shared + per-run + source selectors)
   runners: <P> thin entries + <Q> sbatch
   describe: scripts/d-<Stage>-Describe.do
```


MUST NOT
--------

- Use papermill, .ipynb, or Python — this is Stata + PowerShell
- Use SSC packages in describe scripts
- Use `Start-Job` in orchestrator (CMS server incompatible)
- Write heavy .dta to results/ (they go to _WorkSpace/)
- Skip STATATMP in orchestrator
- Use non-ASCII in .ps1 files
- Add comment banners, ASCII art, or box-drawing to .ps1
- Skip exit code checking after Start-Process


Return contract
---------------

```yaml
status: ok | blocked | failed
files_created: [list of all authored files]
files_modified: [list of edited existing files]
audit_result: { from fn/audit-stata.md }
next: "Run fn/execute-stata.md (mode A: local synth first)"
```
