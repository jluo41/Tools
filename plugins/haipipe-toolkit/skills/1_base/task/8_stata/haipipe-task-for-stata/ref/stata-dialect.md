Stata Execution Dialect — shared engine contract
==================================================

This is the **layer-2 execution contract** for Stata jobs, owned by `haipipe-task-for-stata` (this skill's `ref/`).
The parent `/haipipe-task` is the high-level router (default dialect Python + papermill); this document defines the parallel Stata + PowerShell + `.log` dialect that all 4 Stata stages (cms/case/data/reg) share.

The **structure invariants** (the block > job > task > run ladder, four levels since 260829; the RUNNAME spine; one folder per Run with its result/; the light/heavy split) are shared with the Python dialect.
Only the execution engine differs.
Read `../../../haipipe-task/ref/task-folder.md` first for the invariants; this file only describes what swaps out.


Three orthogonal axes
----------------------

```
hierarchy   project → block → job → task   (engine-agnostic; haipipe-task ref/task-folder.md)
engine      Python+papermill   |   Stata+PowerShell  (this file picks the 2nd)
task-type   stata-cms · stata-case · stata-data · stata-reg   (per-stage semantics)
```

"Stata" is an ENGINE, not a task-type.
The four Stata task-types (`stata-cms | stata-case | stata-data | stata-reg`, the values a Task face writes) share this one engine but differ in RUNNAME grammar, output destination, and headline meaning — which is why each is its own stage branch of `haipipe-task-for-stata`.


Stage topology families
------------------------

The four stages split into two TOPOLOGY FAMILIES that determine how runners, orchestrators, and ceremony are organized:

```
ORCHESTRATED (year axis):                SELF-ORCHESTRATING (no year axis):
  cms, case                                data, reg
  ---------------------------              ----------------------------------
  src/run_<stage>_year.ps1 heavyweight     the Run's runner IS the heavyweight:
  runs/<run>/<run>.ps1 = 2 thin lines      its ticket, or the Job runner its two
  (hands config.do to the Job runner)      lines call (no year orchestrator exists)

  No preconditions in runner               Preconditions in runner (config
  (orchestrator checks inputs)             parsing, upstream .dta existence)

  No ceremony in runner                    config_snapshot.do + manifest.json
  (Stata logs are the record)              acceptable (runner IS orchestrator)

  Template: ref/run-ps1-template.ps1       Template: ref/run-data-runner-template.ps1
            ref/run-stage-year-template.ps1           (reg: inline in runner)
```

Rules A5, B2, B3 are SCOPED by topology family -- see each rule for per-family details.
Rules A1-A4, A6-A8, B1, B4-B6 apply equally.


The RUNNAME spine — Stata projection
-------------------------------------

```
Python projection                          Stata projection
────────────────────────────────────────   ─────────────────────────────────────────────
{task}.py              (cell source)    →  {task}.do (dispatcher) + scripts/*.do (lib)
runs/<run>/config.yaml (_meta+params)   →  runs/<run>/config.do   (Stata globals: source of truth)
                                           + runs/<run>/config.yaml (_meta ONLY, optional)
runs/<run>/<run>.sh    (entry)          →  runs/<run>/<run>.ps1   (PowerShell entry)
runs/<run>/run.yaml    (card)           →  runs/<run>/run.yaml    (SAME card, with role:)
notebooks/<run>.ipynb  (record)         →  runs/<run>/result/log/*.txt (Stata logs: the record)
runs/<run>/result/     (light out)      →  runs/<run>/result/     (+ runtime.yaml)
runtime.yaml           (status)         →  runtime.yaml           (SAME flat schema)
```

A reg Run splits its record in two: `result/` keeps only what a reader reviews (RUN-REPORT.md,
`tables/`, `describe/`), and each execution's `log/`, `steps/`, `.done`, `runtime.yaml`,
`config_snapshot.do` and `manifest.json` go to `runs/<run>/passes/pNN-<MMDD>/`.
A Block not yet moved keeps the flat layout: `runs/<run>.ps1`, `scripts/config/<run>.do`
and everything in `results/<run>/`.

Two deliberate departures from the Python mold:

1. **No `notebooks/` folder.** The execution record is the Stata `.log`. `runs/<run>/result/log/<step>[-<year>].txt` is the per-step log (reg: `runs/<run>/passes/pNN-<MMDD>/log/`). The `runtime.yaml` `notebook:` field is repurposed to point at that log dir.

2. **Config is a two-file pair.** Stata cannot read YAML, so the real parameters stay in the Run's `runs/<run>/config.do` (Stata globals), which loads the Task's shared `scripts/config/<cfg>.do`. An optional sibling `runs/<run>/config.yaml` carries ONLY the `_meta:` discipline block (purpose / note / input / output) plus a `stata_config: config.do` pointer. The `.ps1` snapshots BOTH into the Run's record (`result/`; reg: `passes/pNN-<MMDD>/`).


runtime.yaml — controller-owned Run receipt
--------------------------------------------

Every Stata Run requires its receipt `runtime.yaml`; it is never optional, in any layout:
`$OUTPUT_ROOT/<task>/runs/<run>/result/runtime.yaml` (a reg Run: one per execution, in
`runs/<run>/passes/pNN-<MMDD>/runtime.yaml`; a Block not yet moved: `results/<run>/runtime.yaml`).
The Task controller/scaffolder writes planned status before dispatch, running
before execution, and complete only after checking required logs, snapshots,
summary and domain outputs. It uses the same Run identity, config/script/input
paths, timestamps, exit status, Result paths and failure fields as the shared
Task receipt. See `../../../haipipe-task/ref/run-sh-template.sh` for the fields.
Stata keeps per-step logs as its engine evidence; it has no notebook requirement.
The controller cites those logs in the receipt and `notebook` may be null.
Keep this bookkeeping outside thin cms/case Tickets and workers; the parent
controller (in practice the Job runner in src/ that the two-line ticket calls) owns it. Manual server execution returns evidence to that same
controller; pending external execution cannot pass the Run gate.
Legacy logs without a receipt are inspectable, but never silently count as a
complete current Run. Backfilled facts must come from original evidence, and
unknown timestamps or exit status remain explicitly unknown.

Anatomy of a Stata job
-------------------------------

Two shapes. The NESTED shape is what the
production data/reg jobs already use (e.g. OpioidRx R03_Reg_TraitCABG/
C01_data_pipeline_cabg and D01-reg_visitami_leftdigit):

```
jNN_{L}_{kind}_{subject}/           NESTED (current production, 260831)
├── sbatch/                         batchers that SPAN tasks + batch.psd1 declaring
│                                   Mode (sequential|parallel) · Ceiling · CollisionKey
├── src/                            SHARED by every task in this job: lib-*.do,
│   │                               the runner .ps1, config-defaults.do, the
│   │                               dispatcher .do the launcher resolves
│   └── 0-libs/                     the pre-260830 name, now an ordinary subfolder that
│                                   OpioidRx's shared runners still live in
├── tNN_{L}_{kind}_{subject}/       one TASK = one pipeline, directly under the job
│   ├── scripts/                    THE TASK'S OWN CODE (JL 260831)
│   │   ├── run-*-pipeline.do       the spine: the plan, printed not executed
│   │   └── config/                 INSIDE scripts/ — the SHARED cohort .do every
│   │                               Run's config.do loads (a Block not yet moved
│   │                               also keeps each rNN_*.do here)
│   ├── runs/rNN_*/                 one folder per Run, one per run identity:
│   │                               rNN_*.ps1 (two-line ticket) · config.do ·
│   │                               run.yaml (card, role:) · result/ (log/*.txt ·
│   │                               report artifacts · config_snapshot.do ·
│   │                               runtime.yaml); reg adds passes/pNN-<MMDD>/
│   └── tNN_*.md                    the page a reader opens
    └── workflow/ · diagram/ · ISSUES.md   inside each tNN Task

TWO WORDS ON PURPOSE (JL 260831): `src/` is the JOB's shared code, `scripts/` is
the TASK's own. The name alone says the level, so no one walks the path to find out.
```

The FLAT dispatcher shape below is the LEGACY cms/case-stage anatomy (and the
legacy form of data/reg). Read it to understand an old tree; do not scaffold it.
The cms and case stages migrated to the NESTED shape above on 260831.

⚠️ Its job-root `scripts/` is the WORKER LIBRARY and predates the two-word
ruling, so the same word means two different things across the two shapes: here
it is the job's shared step code (which is `src/` in the nested shape), while in
a nested tree `scripts/` is a TASK's own code. That collision is exactly what
the ruling removed, and it is why this shape is not scaffolded any more.

```
{LNN}_{stage}_pipeline/
├── {LNN}_{stage}_pipeline.do  ← single-step DISPATCHER: <config> <step> [<year>] <results_dir> <ws_root>
├── scripts/                   ← the worker library (one .do per step; imported by the dispatcher)
├── configs/
│   ├── <cfg>.do               ← Stata globals (keep-vars, flags; paths built from ${ws_root}) — SOURCE OF TRUTH
│   └── <run>.yaml             ← _meta: block + stata_config: pointer  (NEW under this dialect)
├── run_{stage}_year.ps1       ← intra-run ORCHESTRATOR at task root (about 30 lines plus required checks: phases + parallelism)
├── runs/
│   └── <run>.ps1              ← THIN per-run entry (a few lines); one per run identity; pairs with results/<run>/
├── sbatch/
│   └── <range>.ps1            ← cross-run batcher: loops the runs/ entries (no logic of its own)
├── results/
│   └── <run>/                 ← log/*.txt · summary.txt · runtime.yaml (required)
└── diagram/                   ← doc surface (NEVER README.md); see diagram-ascii
```

The dispatcher `.do`, the worker `scripts/`, and `run_{stage}_year.ps1` live at the job ROOT — they are the flat job's entry + execution machinery (the Stata analog of Python's root `{task}.py` + papermill).
Only the per-step WORKERS go in `scripts/`.
Three ref templates seed them: `run-ps1-template.ps1` (the thin per-run entry), `run-stage-year-template.ps1` (the orchestrator), `dispatcher-do-template.do` (the dispatcher).

Roles, precisely (current places; the flat shape above kept them at the job root):

- **dispatcher `.do`** — `do {task}.do <config> <step> [<year>] <results_dir> <ws_root>`. Sets `global ws_root` FIRST, loads the Run's config (`<config>` is its Task-relative path, `runs/<run>/config.do`; a bare name still means `scripts/config/<name>.do`), sets up dirs, opens a per-step log, dispatches to `scripts/<step>.do`, skips if output exists (idempotent), closes log. Code paths (`runs/`, `scripts/`) are Task-relative; the DATA root arrives absolute as `<ws_root>`. The file name is FREE — nothing references it by a hardcoded path.
- **`src/run_{stage}_year.ps1`** — the Job's engine for one run: takes the Run's config path, finds the Task from it (never from its own folder), `$stata` variable at top (one editable line), resolves `ws_root` by walking up to `pyproject.toml`, runs Stata with the working dir set to the Task folder, and sequences the dispatcher's steps in dependency-correct phases (within-phase parallelism via `Start-Process ... -PassThru | Wait-Process`). about 30 lines plus required checks — see the script style contract below.
- **`runs/<run>/<run>.ps1`** — the RUNNAME entry, THIN: one comment line + one call that hands the Run's config to the Job's runner (`& "$PSScriptRoot\..\..\..\src\run_<stage>_year.ps1" "$PSScriptRoot\config.do"`). One Run folder per run identity so run ↔ `result/` pairing stays 1:1.
- **`sbatch/`** — fans across runs: `foreach ($r in "r01_<stage>_2015","r02_<stage>_2016") { & "$PSScriptRoot\..\runs\$r\$r.ps1" }`. No logic of its own.


Script style + server constraints — the review contract
---------------------------------------------------------

The CMS secure server is the binding constraint: **Windows PowerShell 5.1 only** (no `pwsh`; installs blocked), clean Stata (no SSC), isolated (no network), and every file is hand-read + hand-copied there by the researcher.
Audience is human AND machine.
Style reference: `cms_results_v0316/code` (the `_cms-server` snapshot under `_WorkSpace/0-CMS-Store/CMS-Analysis-Results/`).
The `haipipe-task-reviewer-agent` enforces these points before any hand-copy.

Server-runnability (hard blockers):

```
A1  No `pwsh`, no PS7-only syntax (&&, ||, ternary, ??). Child calls are
    `& $script` (preferred, same session) or `powershell -File`.
A2  ASCII-only .ps1/.do. PS 5.1 reads ANSI: an em-dash or box-drawing char
    mis-decodes (em-dash byte 0x94 = closing smart-quote) -> string truncates
    -> "Unexpected token" parse error. If non-ASCII is truly unavoidable,
    save UTF-8 WITH BOM.
A3  No installs, no network: no winget / pip / ssc install anywhere.
A4  No SSC commands in .do, ONE exception: `rangejoin`. No `distinct`
    (use egen tag() + count); otherwise built-ins only; capture-guard
    optional variables.



A5  Stata exe resolution -- two accepted patterns, either OK for ANY stage:
    (a) HARDCODED: $stata = "C:\...\StataMP-64.exe" (one editable line;
        another machine edits that line).
    (b) RESOLVER: Resolve-StataExe function (~10 lines, checks
        $env:HAIPIPE_STATA then scans Program Files).
    The reviewer accepts either. $env:HAIPIPE_STATA always overrides.
A6  Output paths from the ABSOLUTE _WorkSpace (pyproject.toml walk-up).
    Never a relative "_WorkSpace", never ..\.. depth counting. Genuinely
    fixed raw inputs (G:\CMS\DATA) stay absolute in the config.
A7  Run from the tNN Task folder; runs/<run>/config.do, scripts/config/ and
    scripts/ relative; nothing hardcodes the folder's own name.
A8  Dead %TEMP% on the server. (a) NEVER run a .do via the editor's "Do"
    button -- it stages to %TEMP%\pNNNN.do and fails (`command E is
    unrecognized` r(199)); launch ONLY via the .ps1 (Start-Process $stata
    /e do <dispatcher>). (b) `preserve`/`tempfile` write to %TEMP% too:
    stage intermediates with explicit `save "${temp_dir}/.."` + `use`
    (the v0316 trigger pattern), or set $env:STATATMP to a writable in-repo
    dir. (c) Python build steps (external-data) set $env:PYTHONUTF8="1" --
    Windows cp1252 default crashes read_text()/print() on UTF-8 files.
```

Readability (every file is hand-checked before copy):

```
B1  Header = 1-2 comment lines (what + args/usage). No banner blocks, no
    ===/--- separator walls, no ASCII-art in code, no "// CHANGE (n)" patch
    markers, no commented-out alternatives left behind.
B2  Size budget (scoped by topology):
    ORCHESTRATED (cms/case): orchestrator about 30 lines plus required checks; runs/ entry 2-3
      lines (comment + call orchestrator -- thin dispatch only).
    SELF-ORCHESTRATING (data/reg): the Run's runner IS the orchestrator, no fixed
      limit but stays focused (data: ~60-105 lines; reg: ~30-40 lines).
      Shared helper (run_data_steps.ps1) <= ~45 lines.
    All: sbatch <= ~10 lines (longer if parameterized); worker .do = one step.
B3  Ceremony (scoped by topology):
    ORCHESTRATED (cms/case): no ceremony in runners -- Stata logs +
      summary.txt are the record.
    SELF-ORCHESTRATING (data/reg): runners MAY include config_snapshot.do,
      manifest.json, and precondition checks (verify upstream .dta exist).
      Acceptable because the runner IS the orchestrator. Keep in numbered
      sections for readability. Do NOT add ceremony to shared helpers or workers.
B4  .do dispatch ladders: multi-line braces (next section), aligned step names.
B5  Orchestrator reads as: variable block ($stata, $dir, $ws, $base, $tail),
    then the action lines. Input -> step -> output traceable in one screen.
B6  Comment budget: ref TEMPLATES carry a ~4-line header (contract + what to
    EDIT) and one short note per decision point (phase blocks, $stata, $tail);
    scaffolded INSTANCES trim to a 1-2 line header + the phase labels.
```

Illustration of the current shape (OpioidRx `b02_A_cms_pipeline/j02_A1_cms_pipeline`), trimmed.
For new work start from the ref templates: canonical Task paths, config-owned year,
resolved output root, and child ExitCode checks are required (`ref/run-stage-year-template.ps1`):

```powershell
# src/run_cms_year.ps1 (the Job's runner): one year: 4 extracts in parallel, then bene_year + summary
param([Parameter(Mandatory)][string]$ConfigPath)

$stata = "C:\Program Files\Stata18\StataMP-64.exe"
$cfg   = (Resolve-Path $ConfigPath).Path
$run   = Split-Path -Leaf (Split-Path -Parent $cfg)
$dir   = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $cfg))
$ws    = $dir; while ($ws -and -not (Test-Path "$ws\pyproject.toml")) { $ws = Split-Path $ws }
$year  = [regex]::Match((Get-Content $cfg -Raw), 'global\s+data_year\s+(\d{4})').Groups[1].Value
$base  = "do scripts/run_cms_pipeline.do runs/$run/config.do"
$tail  = "`"$dir\runs\$run\result`" `"$ws\_WorkSpace`""

$jobs = "pde","carrier_claim","carrier_line","outpatient" |
        ForEach-Object { Start-Process $stata "/e $base $_ $year $tail" -WorkingDirectory $dir -PassThru }
$jobs | Wait-Process
Start-Process $stata "/e $base bene_year $year $tail" -WorkingDirectory $dir -PassThru -Wait
Start-Process $stata "/e $base summary   $year $tail" -WorkingDirectory $dir -PassThru -Wait
Write-Host "Year $year done."
```

```powershell
# t01_A_cms_Pde/runs/r01_A_cms_Pde_2015/r01_A_cms_Pde_2015.ps1 (thin ticket; one Run folder per year)
& "$PSScriptRoot\..\..\..\src\run_cms_year.ps1" "$PSScriptRoot\config.do"
```

```powershell
# sbatch/by_year/01_2015.ps1 (batcher; loops the Run folders' tickets)
foreach ($r in "r01_A_cms_Pde_2015","r02_A_cms_Pde_2016") { & "$PSScriptRoot\..\t01_A_cms_Pde\runs\$r\$r.ps1" }
```


Brace style — every `if` body on its own line
----------------------------------------------

**Every `if` in a `.do` uses multi-line braces, never a one-liner.** The condition line opens `{`, the body sits on its OWN indented line, and `}` is alone on the next line, even for a single-command branch. This covers the dispatcher's `step → worker` ladder, every `if/else if` chain, and every `capture` / `_rc` guard.

This is a READABILITY and edit-safety rule, not a runnability blocker, and the distinction matters when you read existing code: the one-line form RUNS. The server-proven snapshot `Report-From-CMS-Server/v0827_Code0827/` carries 43 one-line `if`s, three of them exactly `if _rc == 0 global file_policy "\`_polalt'"`. Do not "fix" those on the belief that they are broken; write new code in the brace form because a brace form is never in doubt, never traps when someone later wraps the body with `///`, and shows the branch in a diff.

Ruled by JL on 260829, on reading the `capture quietly describe, varlist` guard added for `[C01-05]`.

```stata
// GOOD
else if "`step'" == "claims_erase" {
    do "scripts/feat/_old/shared-claims-erase.do" `year'
}

// AVOID — one-liners (and braceless `else if … local …`) read poorly and make
// diffs and edits error-prone
else if "`step'" == "claims_erase" { do "scripts/feat/_old/shared-claims-erase.do" `year' }
else if "`step'" == "bene_year"    local out_file "${out_bene_beneobsdt_year}"
```

The same shape for a `capture` guard, which is where this came up:

```stata
// GOOD
capture quietly describe, varlist
if _rc == 0 {
    local vars_before "`r(varlist)'"
}

// AVOID — runs, but the branch is invisible in a diff and cannot take a `///` wrap
capture quietly describe, varlist
if _rc == 0 local vars_before "`r(varlist)'"
```

Section labels (`// PDE`, `// CLAIMS`, …) above a group of branches are fine and encouraged — a full-line `//` comment between a `}` and the next `else if` is tolerated by Stata (verified) and does not break brace matching.
The `dispatcher-do-template.do` already encodes this style; keep generated and hand-edited dispatchers consistent with it.


Idempotency
-----------

Every worker `.do` (or the dispatcher's skip block) does `capture confirm file <output>.dta` and SKIPs if present.
Re-running a finished pipeline is cheap; to recompute, delete the specific `.dta`.
Steps with no persistent output (`shared_*`, `describe`, `summary`, `*_erase`) always run.


Describe / QC Step
------------------------------------------

cms/case/data include a read-only **describe Step** within the variant Run; reg adds it when requested. It emits human-readable QC evidence.
A separate describe-only Run needs its own explicit goal and Ticket:

- **`describe` dispatch step** → `scripts/d-<Stage>-Describe.do`. Walks the stage's asset and `file write`s a report into `${results_dir}` (e.g. `case-describe.txt`). No persistent data output, so it is NOT in the skip list — it always runs.
- **Optional `runs/rNN_describe_<...>/`** — a separately commissioned describe-only Run folder (its `run.yaml` says `role: describe`): same thin two-line ticket as any Run, runs just the `describe` step on the already-built asset (no rebuild). For per-year stages the year arg is a dummy; the worker loops the `year-*` dirs it finds under the asset path.

⚠️ **No SSC dependencies in describe** (it must run on a clean CMS server).
Use built-ins: `egen tag()` + `count` for distinct counts — NEVER `distinct` (SSC; aborts `r(199)`).
Use `summarize` / `tabulate` / `ds` + `egen rowtotal` for the rest, all `capture`-guarded so a missing optional variable is skipped, not fatal.

What each stage's describe reports (illustrative):
```
cms   per year: Neat panel inventory + row counts, Bene_Info rows, claim
      service-date ranges (sanity: dates are %td and within the year).
case  per year: #cases, distinct benes / npis, visit_type split, the BN
      enrichment check (pde_bn rows with >=1 rx), obs_dt range.
data  analysis table: N, distinct benes/npis, year dist, treatment (trait)
      summary, outcome means, key-control missingness, IV first-stage corr.
reg   coefficient sanity: trait coef + SE + N per spec from the logs
      (did every cell estimate; any dropped / collinear / no-obs).
```


Current path rule: launch from the tNN Task root, load the Run's
`runs/<run>/config.do` (a Block not yet moved: `scripts/config/rNN_*.do`), and
call `scripts/<dispatcher>.do` / `scripts/<worker>.do`. A runner, Task-local
under scripts/ or shared under Job src/, finds the Task from the Run's own path,
never from its own folder: a ticket whose folder is `runs/` is flat and its Task
is that folder's parent; any other ticket sits in `runs/<run>/` and its Task is
its folder's grandparent (from a config: `runs/<run>/config.do` and
`scripts/config/<run>.do` both sit two levels below the Task). The caller
resolves RESULT_STORE, then Job store declaration, then Job root; every light
output uses `$OUTPUT_ROOT/<task>/runs/<run>/result/` (reg logs and receipts:
`runs/<run>/passes/pNN-<MMDD>/`). Older snippets elsewhere describe older entry
locations only and must be translated through this rule.

Runtime portability — three CWD/location-independence rules
------------------------------------------------------------

A Stata task must run identically on a laptop and on the secure server, launched from anywhere, regardless of the folder's own name.
Three rules (all baked into the ref templates — do NOT re-derive them per task):

1. **Stata exe = one resolvable location.** Either a hardcoded line (`$stata = "C:\...\StataMP-64.exe"` -- cms-stage server pattern) or a `Resolve-StataExe` function (~10 lines, checks `$env:HAIPIPE_STATA` then scans Program Files -- data/reg/case pattern for multi-machine dev). See rule A5 for when each is preferred.

2. **Run from the task folder; keep code paths relative.** The runner sets the Stata working dir to the Task folder (found from the Run's path, per the rule above) and calls the dispatcher by its Task-relative path; the dispatcher loads the Run's `runs/<run>/config.do` and `scripts/<step>.do` relative to that. NO path hardcodes the folder name, so the folder can be renamed with a pure `mv`.

3. **Anchor the DATA root absolute via `ws_root`.** The per-run `.ps1` walks up to the `pyproject.toml` marker, forms `<repo>/_WorkSpace`, and passes it as `-wsRoot`. The dispatcher sets `global ws_root` and the config builds ALL output paths from `${ws_root}` (e.g. `global output_root "${ws_root}"`). NEVER write a relative `_WorkSpace` in the config — outputs would land wherever the CWD happens to be (a classic bug: 50+ GB/year under the task folder).

Inputs that are genuinely fixed (e.g. real CMS at `G:\CMS\DATA`) stay absolute in the config; only the *repo-relative* `_WorkSpace` data root is resolved this way.

### reg-stage exception — dispatcher-less, env-var ws_root

The **reg** stage has NO central dispatcher and NO `run_<stage>_year.ps1` orchestrator (there is no year axis).
Each reg Run's runner (its self-contained ticket `runs/<run>/<run>.ps1`, or the Job's `src/0-libs/run-regression-pipeline.ps1` that its two lines call) calls its estimation `scripts/run-*.do` **directly**, and each `.do` opens with `clear all`.
So rules 2–3 take a reg-specific form:

- **ws_root via ENV var, not a `do` arg.** `clear all` would drop a `global` (and is hostile to threading args), so the `.ps1` exports `$env:HAIPIPE_WS_ROOT = "<repo>/_WorkSpace"` and the `.do` reads it AFTER `clear all`:
  ```stata
  global ws_root : environment HAIPIPE_WS_ROOT
  if "${ws_root}" == "" global ws_root "_WorkSpace"   // fallback for direct GUI runs
  ```
- **Run from the task folder via `Push-Location`.** A direct `& $stata /e do "scripts/..."` cannot take `-WorkingDirectory`, so wrap it: `Push-Location $TASK_DIR; try { & $stata /e do "scripts/<run>.do" } finally { Pop-Location }`.
- **Output goes to the Run folder** (LIGHT coef tables) — tables under `${res_dir}` (`runs/<run>/result/`, from `HAIPIPE_RUN_RESULT`), logs under `${pass_dir}/log/` (`runs/<run>/passes/pNN-<MMDD>/`, from `HAIPIPE_PASS_DIR`), e.g. `global log_file "${pass_dir}/log/<worker>.log"`, `capture mkdir "${pass_dir}/log"`. No folder-name prefix.
- **Grouped vs per-cell runs.** Each estimator family may be one Run that loops several worker `.do` (e.g. `ols` → run-1..5, `iv` → run-6..8), or one Run per cell — the author's call; both keep each Run's Result in its own Run folder.


Light vs heavy (unchanged from the invariants)
-----------------------------------------------

- 💾 HEAVY (`.dta` data assets) → `_WorkSpace/{1-CMS,2-Case,...}-Store/`.
  Out-of-repo. NEVER under a Run's `result/` (or `passes/`).
- 📊 LIGHT (logs, summary.txt, runtime.yaml, coef tables `.tex`/`.csv`,
  `diagram.txt`) → in-repo under `runs/<run>/result/` (reg: tables in `result/`,
  logs and runtime.yaml in `passes/pNN-<MMDD>/`).

The **reg** stage is the exception that proves the rule: its *primary* output (coefficient tables) is LIGHT and belongs in `result/`.
The cms/case/data stages produce HEAVY `.dta` assets and keep only pointers + logs in `result/`.


Pre-hand-copy review (agent, not in-script plumbing)
-----------------------------------------------------

There is NO in-script review gate — runners stay thin (rule B3).
Instead, run `haipipe-task-reviewer-agent` on the job BEFORE hand-copying files to the server.
It checks the contract above (structure S, runnability A, readability B, pipeline correctness C) plus a machine pre-flight (PS 5.1 parse-check, non-ASCII byte scan, grep gate for pwsh/ssc/distinct), and writes `CODE_REVIEW.md` + the hand-port file list.
For Stata this matters MORE than for Python — silent merge / keep-var / sample-definition bugs run clean and produce numbers.

Author convention: the dispatcher `.do` carries a 1-2 line header comment (args + step list) — that is the whole "intent block" under this dialect.


Project-local letter convention (cms/case/data/reg)
----------------------------------------------------

Historical letter-only names below describe existing trees; current hierarchy prefixes are bNN/jNN/tNN/rNN for all domains.
Do not scaffold the historical names below. Stage/cohort names belong in suffixes.
The CMS/Stata project uses a DIFFERENT, domain-native pipeline ontology that mirrors `CMS-Stata-Project`'s cms → case → data → reg pipelines:

```
stage   meaning                              produces                  output store
─────   ──────────────────────────────────  ────────────────────────  ─────────────────────
cms     extract+enrich raw CMS, per year     Neat-*.dta, Bene_Info     1-CMS-Store   (heavy)
case    trigger cases on a cohort, per year  CASES / BFAF panels       2-Case-Store  (heavy)
data    assemble cross-year analysis table   ANALYSIS-CMS-Filter.dta   *-Data-Store  (heavy)
reg     estimate (OLS / IV / LPM / 2-part)   coef tables (.tex/.csv)   runs/<run>/result/ (LIGHT)
```

This stage table is the pipeline ONTOLOGY, not the BLOCK letter scheme: it
surfaces as the `{LNN}` JOB-level alphabet below. The actual BLOCK letters
stay project-specific as always (OpioidRx uses A=external/cms, B=case-data,
R=one regression topic per block — a third scheme, and the project's own
scheme wins).
Document it in the project's `README.md` so an auditor reading `work/{letter}{NN}_*/` is not confused by the letter mismatch with the default convention.
`regen_task_log.py`'s `LETTER_TO_TYPE` map (keyed on the GROUP letter, `parent[:1]`) is approximate for these folders; the type hint it prints is cosmetic and does not affect correctness.

### Job `{LNN}` stage-letter alphabet

Legacy Stata jobs used `{L}{NN}_{stage}_pipeline[_<study>]`, where the leading letter `L` encodes the pipeline STAGE (so alphabetical sort = pipeline order), and `NN` is a stable study/cohort id (or a within-stage sequence where no study axis exists):

```
L   stage   produces                  store
──  ─────   ────────────────────────  ─────────────────────
A   cms     Neat-*.dta, Bene_Info     1-CMS-Store   (heavy)
B   case    CASES / BFAF panels       2-Case-Store  (heavy)
C   data    ANALYSIS-*.dta            *-Data-Store  (heavy)
D   reg     coef tables (.tex/.csv)   runs/<run>/result/ (LIGHT)
```

So `B01/C01/D01` = one study's case→data→reg folders; the disease-agnostic `cms` stage (run once, reused) sits alone with `NN` as a plain sequence (`A01`, `A02`).
These job letters reuse `A/B/C/D` (which mean training/eval/display/data at the BLOCK level) — no functional clash, since they live at a different hierarchy level and the logging map keys on the BLOCK letter.
Note it in the project `README.md` so it reads clearly.


RUNNAME grammar by stage (stages unified in this skill since 2.0.0; SKILL.md carries the authoritative grammars)
----------------------------------------------------------

```
cms    rNN_cms_<year>                                        axis: year
case   rNN_case_<Cohort>_{synth|full}_<year>                 axes: cohort × source × year
data   rNN_data_<Spec>                                       axis: analysis-spec (no year — cross-year)
reg    rNN_reg_<cohort>_<pairing>_{synth_}?<window>_<family> axes: cohort × pairing × source × window × family
```
