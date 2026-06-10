Stata Execution Dialect — shared engine contract
==================================================

This is the **layer-2 execution contract** for Stata task-folders, owned by
`haipipe-task-for-stata` (this skill's `ref/`). The parent `/haipipe-task` is
the high-level router (default dialect Python + papermill); this document
defines the parallel Stata + PowerShell + `.log` dialect that the four
all 4 Stata stages (cms/case/data/reg) share.

The **structure invariants** (3-level hierarchy, RUNNAME spine, run↔result
pairing, light/heavy split, diagram-as-doc) are UNCHANGED. Only the
execution engine differs. Read `../../haipipe-task/ref/hierarchy.md` first for
the invariants; this file only describes what swaps out.


Three orthogonal axes
----------------------

```
hierarchy   project → task-group → task-folder       (engine-agnostic; see hierarchy.md)
engine      Python+papermill   |   Stata+PowerShell  (this file picks the 2nd)
task-type   cms · case · data · reg                  (per-specialist semantics)
```

"Stata" is an ENGINE, not a task-type. The four Stata task-types share
this one engine but differ in RUNNAME grammar, output destination, and
headline meaning — which is why each gets its own specialist.


Stage topology families
------------------------

The four stages split into two TOPOLOGY FAMILIES that determine how
runners, orchestrators, and ceremony are organized:

```
ORCHESTRATED (year axis):                SELF-ORCHESTRATING (no year axis):
  cms, case                                data, reg
  ---------------------------              ----------------------------------
  run_<stage>_year.ps1 heavyweight         runs/<run>.ps1 IS the heavyweight
  runs/<run>.ps1 = 2-3 thin lines          (no year orchestrator exists)
  (delegates to orchestrator)

  No preconditions in runner               Preconditions in runner (config
  (orchestrator checks inputs)             parsing, upstream .dta existence)

  No ceremony in runner                    config_snapshot.do + manifest.json
  (Stata logs are the record)              acceptable (runner IS orchestrator)

  Template: ref/run-ps1-template.ps1       Template: ref/run-data-runner-template.ps1
            ref/run-stage-year-template.ps1           (reg: inline in runner)
```

Rules A5, B2, B3 are SCOPED by topology family -- see each rule for
per-family details. Rules A1-A4, A6-A8, B1, B4-B6 apply equally.


The RUNNAME spine — Stata projection
-------------------------------------

```
Python projection                    Stata projection
─────────────────────────────────    ──────────────────────────────────────────────
{task}.py        (cell source)    →   {task}.do        (dispatcher) + scripts/*.do (lib)
configs/<run>.yaml (_meta+params) →   configs/<run>.yaml (_meta ONLY)
                                       + configs/<cfg>.do  (Stata globals — source of truth)
runs/<run>.sh    (entry)          →   runs/<run>.ps1   (PowerShell entry)
notebooks/<run>.ipynb (record)    →   results/<run>/log/*.txt  (Stata logs — the record)
results/<run>/   (light out)      →   results/<run>/   (+ runtime.yaml)
runtime.yaml     (status)         →   runtime.yaml     (SAME flat schema)
```

Two deliberate departures from the Python mold:

1. **No `notebooks/` folder.** The execution record is the Stata `.log`.
   `results/<run>/log/<step>[-<year>].txt` is the per-step log. The
   `runtime.yaml` `notebook:` field is repurposed to point at that log dir.

2. **Config is a two-file pair.** Stata cannot read YAML, so the real
   parameters stay in `configs/<cfg>.do` (Stata globals). A sibling
   `configs/<run>.yaml` carries ONLY the `_meta:` discipline block
   (purpose / note / input / output) plus a `stata_config:` pointer to the
   `.do`. The `.ps1` snapshots BOTH into `results/<run>/`.


runtime.yaml — OPTIONAL task-log integration
---------------------------------------------

Under the Stata dialect the execution record is the per-step Stata log +
`summary.txt`; runners stay THIN and write no bookkeeping (see the script
style contract below). `results/<run>/runtime.yaml` is OPTIONAL — add one
after a run (by hand or tooling, never in the runner hot path) only when the
unified `task-log.md` from `haipipe-task-logging/ref/regen_task_log.py` is
wanted. Flat schema:

```yaml
status:     ok                              # running | ok | failed
started:    2026-02-23T13:52:27-05:00       # ISO 8601
ended:      2026-02-23T17:19:00-05:00
duration:   3h26m
git_sha:    8d8d6d1
host:       jjluo-pc/floyd
exit_code:  0
cmd:        powershell A01_cms_pipeline/runs/run_cms_2015.ps1
config:     configs/run_cms_2015.yaml
notebook:   results/run_cms_2015/log/       # repurposed -> per-step log dir
headline:   Bene_Info-2015 11,783,927 x 121
```


Anatomy of a Stata task-folder
-------------------------------

```
{LNN}_{stage}_pipeline/
├── {LNN}_{stage}_pipeline.do  ← single-step DISPATCHER: <config> <step> [<year>] <results_dir> <ws_root>
├── scripts/                   ← the worker library (one .do per step; imported by the dispatcher)
├── configs/
│   ├── <cfg>.do               ← Stata globals (keep-vars, flags; paths built from ${ws_root}) — SOURCE OF TRUTH
│   └── <run>.yaml             ← _meta: block + stata_config: pointer  (NEW under this dialect)
├── run_{stage}_year.ps1       ← intra-run ORCHESTRATOR at task root (<=30 lines: phases + parallelism)
├── runs/
│   └── <run>.ps1              ← THIN per-run entry (a few lines); one per run identity; pairs with results/<run>/
├── sbatch/
│   └── <range>.ps1            ← cross-run batcher: loops the runs/ entries (no logic of its own)
├── results/
│   └── <run>/                 ← log/*.txt · summary.txt  (runtime.yaml optional)
└── diagram/                   ← doc surface (NEVER README.md); see diagram-ascii
```

The dispatcher `.do`, the worker `scripts/`, and `run_{stage}_year.ps1` live at
the task ROOT — they are the task's entry + execution machinery (the Stata
analog of Python's root `{task}.py` + papermill). Only the per-step WORKERS go
in `scripts/`. Three ref templates seed them:
`run-ps1-template.ps1` (the thin per-run entry), `run-stage-year-template.ps1`
(the orchestrator), `dispatcher-do-template.do` (the dispatcher).

Roles, precisely:

- **dispatcher `.do`** — `do {task}.do <config> <step> [<year>] <results_dir> <ws_root>`.
  Sets `global ws_root` FIRST, loads `configs/<cfg>.do`, sets up dirs, opens a
  per-step log, dispatches to `scripts/<step>.do`, skips if output exists
  (idempotent), closes log. Code paths (`configs/`, `scripts/`) are
  task-folder-relative; the DATA root arrives absolute as `<ws_root>`. The file
  name is FREE — nothing references it by a hardcoded path.
- **`run_{stage}_year.ps1`** — the engine for one run: `$stata` variable at top
  (one editable line), resolves `ws_root` by walking up to `pyproject.toml`,
  runs Stata with the working dir set to `$PSScriptRoot` (the task folder), and
  sequences the dispatcher's steps in dependency-correct phases (within-phase
  parallelism via `Start-Process ... -PassThru | Wait-Process`). <=30 lines —
  see the script style contract below.
- **`runs/<run>.ps1`** — the RUNNAME entry, THIN: one comment line + one call
  into the orchestrator with this run's parameters
  (`& "$PSScriptRoot\..\run_<stage>_year.ps1" -cfg <cfg> -year <year>`).
  One file per run identity so run ↔ `results/<run>/` pairing stays 1:1.
- **`sbatch/`** — fans across runs: `foreach ($y in 2015..2020) { & "$PSScriptRoot\..\runs\run_<stage>_$y.ps1" }`.
  No logic of its own.


Script style + server constraints — the review contract
---------------------------------------------------------

The CMS secure server is the binding constraint: **Windows PowerShell 5.1 only**
(no `pwsh`; installs blocked), clean Stata (no SSC), isolated (no network), and
every file is hand-read + hand-copied there by the researcher. Audience is
human AND machine. Style reference: `cms_results_v0316/code` (the `_cms-server`
snapshot under `_WorkSpace/0-CMS-Store/CMS-Analysis-Results/`). The
`haipipe-task-reviewer-agent` enforces these points before any hand-copy.

Server-runnability (hard blockers):

```
A1  No `pwsh`, no PS7-only syntax (&&, ||, ternary, ??). Child calls are
    `& $script` (preferred, same session) or `powershell -File`.
A2  ASCII-only .ps1/.do. PS 5.1 reads ANSI: an em-dash or box-drawing char
    mis-decodes (em-dash byte 0x94 = closing smart-quote) -> string truncates
    -> "Unexpected token" parse error. If non-ASCII is truly unavoidable,
    save UTF-8 WITH BOM.
A3  No installs, no network: no winget / pip / ssc install anywhere.
A4  No SSC commands in .do: no `distinct` (use egen tag() + count); built-ins
    only; capture-guard optional variables.
A5  Stata exe resolution -- two accepted patterns (scoped by topology):
    (a) HARDCODED (server-optimized): $stata = "C:\...\StataMP-64.exe"
        Another machine edits that one line. Preferred for cms-stage.
    (b) RESOLVER (multi-machine): Resolve-StataExe function (~10 lines,
        checks $env:HAIPIPE_STATA then scans Program Files). Standard for
        data/reg/case-stage runners that also run on laptop during dev.
    The reviewer accepts either. On the CMS server the user can always
    override via $env:HAIPIPE_STATA.
A6  Output paths from the ABSOLUTE _WorkSpace (pyproject.toml walk-up).
    Never a relative "_WorkSpace", never ..\.. depth counting. Genuinely
    fixed raw inputs (G:\CMS\DATA) stay absolute in the config.
A7  Run from the task folder ($PSScriptRoot); configs/ + scripts/ relative;
    nothing hardcodes the folder's own name.
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
    ORCHESTRATED (cms/case): orchestrator <= ~30 lines; runs/ entry 2-3
      lines (comment + call orchestrator -- thin dispatch only).
    SELF-ORCHESTRATING (data/reg): runs/ IS the orchestrator, no fixed
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

The settled good example (ProjB `A01_cms_pipeline`):

```powershell
# run_cms_year.ps1 (orchestrator, task root)
# one year: 4 extracts in parallel, then bene_year + summary
param([string]$cfg = "cms_production", [string]$year = "2015")

$stata = "C:\Program Files\Stata18\StataMP-64.exe"
$dir   = $PSScriptRoot
$ws    = $dir; while ($ws -and -not (Test-Path "$ws\pyproject.toml")) { $ws = Split-Path $ws }
$base  = "do 01_cms_pipeline.do $cfg"
$tail  = "`"$dir\results\run_cms_$year`" `"$ws\_WorkSpace`""

$jobs = "pde","carrier_claim","carrier_line","outpatient" |
        ForEach-Object { Start-Process $stata "/e $base $_ $year $tail" -WorkingDirectory $dir -PassThru }
$jobs | Wait-Process
Start-Process $stata "/e $base bene_year $year $tail" -WorkingDirectory $dir -PassThru -Wait
Start-Process $stata "/e $base summary   $year $tail" -WorkingDirectory $dir -PassThru -Wait
Write-Host "Year $year done."
```

```powershell
# runs/run_cms_2015.ps1 (thin per-run entry; one per year)
& "$PSScriptRoot\..\run_cms_year.ps1" -cfg cms_production -year 2015
```

```powershell
# sbatch/run_cms_2015-2020.ps1 (batcher; loops the runs/ entries)
foreach ($y in 2015..2020) { & "$PSScriptRoot\..\runs\run_cms_$y.ps1" }
```


Dispatcher coding style (multi-line braces)
--------------------------------------------

The dispatcher's `step → worker` ladder (and any `if/else if` chain) uses ONE
house style: **multi-line braces, never one-liners.** Each branch opens `{` on
the condition line, the body sits on its OWN indented line, and `}` is alone on
the next line — even for a single-command branch:

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

Section labels (`// PDE`, `// CLAIMS`, …) above a group of branches are fine and
encouraged — a full-line `//` comment between a `}` and the next `else if` is
tolerated by Stata (verified) and does not break brace matching. The
`dispatcher-do-template.do` already encodes this style; keep generated and
hand-edited dispatchers consistent with it.


Idempotency
-----------

Every worker `.do` (or the dispatcher's skip block) does
`capture confirm file <output>.dta` and SKIPs if present. Re-running a
finished pipeline is cheap; to recompute, delete the specific `.dta`.
Steps with no persistent output (`shared_*`, `describe`, `summary`,
`*_erase`) always run.


Describe / QC run (every stage ships one)
------------------------------------------

Beyond its build steps, every Stata task SHIPS a read-only **describe** run that
emits a human-readable QC report so a reviewer can confirm the output is correct
without opening Stata. Two pieces:

- **`describe` dispatch step** → `scripts/d-<Stage>-Describe.do`. Walks the
  stage's asset and `file write`s a report into `${results_dir}` (e.g.
  `case-describe.txt`). No persistent data output, so it is NOT in the skip list
  — it always runs.
- **`runs/run_describe_<...>.ps1`** — a describe-ONLY run: same thin shape as
  any runs/ entry, runs just the `describe` step on the already-built asset (no
  rebuild). For per-year stages the year arg is a dummy; the worker loops the
  `year-*` dirs it finds under the asset path.

⚠️ **No SSC dependencies in describe** (it must run on a clean CMS server). Use
built-ins: `egen tag()` + `count` for distinct counts — NEVER `distinct` (SSC;
aborts `r(199)`). Use `summarize` / `tabulate` / `ds` + `egen rowtotal` for the
rest, all `capture`-guarded so a missing optional variable is skipped, not fatal.

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


Runtime portability — three CWD/location-independence rules
------------------------------------------------------------

A Stata task must run identically on a laptop and on the secure server,
launched from anywhere, regardless of the folder's own name. Three rules
(all baked into the ref templates — do NOT re-derive them per task):

1. **Stata exe = one resolvable location.** Either a hardcoded line
   (`$stata = "C:\...\StataMP-64.exe"` -- cms-stage server pattern) or a
   `Resolve-StataExe` function (~10 lines, checks `$env:HAIPIPE_STATA` then
   scans Program Files -- data/reg/case pattern for multi-machine dev).
   See rule A5 for when each is preferred.

2. **Run from the task folder; keep code paths relative.** The orchestrator
   sets the Stata working dir to `$PSScriptRoot` (the task root) and calls the
   dispatcher by bare name; the dispatcher loads `configs/<cfg>.do` and
   `scripts/<step>.do` relative to that. NO path hardcodes the folder name, so
   the folder can be renamed with a pure `mv`.

3. **Anchor the DATA root absolute via `ws_root`.** The per-run `.ps1` walks up
   to the `pyproject.toml` marker, forms `<repo>/_WorkSpace`, and passes it as
   `-wsRoot`. The dispatcher sets `global ws_root` and the config builds ALL
   output paths from `${ws_root}` (e.g. `global output_root "${ws_root}"`).
   NEVER write a relative `_WorkSpace` in the config — outputs would land
   wherever the CWD happens to be (a classic bug: 50+ GB/year under the task
   folder).

Inputs that are genuinely fixed (e.g. real CMS at `G:\CMS\DATA`) stay absolute
in the config; only the *repo-relative* `_WorkSpace` data root is resolved this
way.

### reg-stage exception — dispatcher-less, env-var ws_root

The **reg** stage has NO central dispatcher and NO `run_<stage>_year.ps1`
orchestrator (there is no year axis). Each `runs/<run>.ps1` calls its estimation
`scripts/run-*.do` **directly**, and each `.do` opens with `clear all`. So rules
2–3 take a reg-specific form:

- **ws_root via ENV var, not a `do` arg.** `clear all` would drop a `global`
  (and is hostile to threading args), so the `.ps1` exports
  `$env:HAIPIPE_WS_ROOT = "<repo>/_WorkSpace"` and the `.do` reads it AFTER
  `clear all`:
  ```stata
  global ws_root : environment HAIPIPE_WS_ROOT
  if "${ws_root}" == "" global ws_root "_WorkSpace"   // fallback for direct GUI runs
  ```
- **Run from the task folder via `Push-Location`.** A direct `& $stata /e do
  "scripts/..."` cannot take `-WorkingDirectory`, so wrap it:
  `Push-Location $TASK_DIR; try { & $stata /e do "scripts/<run>.do" } finally { Pop-Location }`.
- **Output is task-relative `results/`** (LIGHT coef tables) — `global log_file
  "results/<run>.log"`, `capture mkdir "results"`. No folder-name prefix.
- **Grouped vs per-cell runs.** Each estimator family may be one `.ps1` that
  loops several worker `.do` (e.g. `ols` → run-1..5, `iv` → run-6..8), or one
  `.ps1` per cell — the author's call; both keep results task-relative.


Light vs heavy (unchanged from the invariants)
-----------------------------------------------

- 💾 HEAVY (`.dta` data assets) → `_WorkSpace/{1-CMS,2-Case,...}-Store/`.
  Out-of-repo. NEVER under `results/`.
- 📊 LIGHT (logs, summary.txt, runtime.yaml, coef tables `.tex`/`.csv`,
  `diagram.txt`) → in-repo under `results/<run>/`.

The **reg** stage is the exception that proves the rule: its *primary*
output (coefficient tables) is LIGHT and belongs in `results/`. The
cms/case/data stages produce HEAVY `.dta` assets and keep only pointers +
logs in `results/`.


Pre-hand-copy review (agent, not in-script plumbing)
-----------------------------------------------------

There is NO in-script review gate — runners stay thin (rule B3). Instead,
run `haipipe-task-reviewer-agent` on the task-folder BEFORE hand-copying
files to the server. It checks the contract above (structure S, runnability
A, readability B, pipeline correctness C) plus a machine pre-flight
(PS 5.1 parse-check, non-ASCII byte scan, grep gate for pwsh/ssc/distinct),
and writes `CODE_REVIEW.md` + the hand-port file list. For Stata this
matters MORE than for Python — silent merge / keep-var / sample-definition
bugs run clean and produce numbers.

Author convention: the dispatcher `.do` carries a 1-2 line header comment
(args + step list) — that is the whole "intent block" under this dialect.


Project-local letter convention (cms/case/data/reg)
----------------------------------------------------

The skill's default group letters (A=training, B=eval, C=display,
D=data, E=individual, F=agent, X=algo) describe the ML/CGM world. The
CMS/Stata project uses a DIFFERENT, domain-native pipeline ontology that
mirrors `CMS-Stata-Project`'s cms → case → data → reg pipelines:

```
stage   meaning                              produces                  output store
─────   ──────────────────────────────────  ────────────────────────  ─────────────────────
cms     extract+enrich raw CMS, per year     Neat-*.dta, Bene_Info     1-CMS-Store   (heavy)
case    trigger cases on a cohort, per year  CASES / BFAF panels       2-Case-Store  (heavy)
data    assemble cross-year analysis table   ANALYSIS-CMS-Filter.dta   *-Data-Store  (heavy)
reg     estimate (OLS / IV / LPM / 2-part)   coef tables (.tex/.csv)   results/      (LIGHT)
```

This is an ACCEPTED project-local override. Document it in the project's
`diagram/` so an auditor reading `tasks/{letter}{NN}_*/` is not confused
by the letter mismatch with the default convention. `regen_task_log.py`'s
`LETTER_TO_TYPE` map (keyed on the GROUP letter, `parent[:1]`) is approximate
for these folders; the type hint it prints is cosmetic and does not affect
correctness.

### Task-folder `{LNN}` stage-letter alphabet

Stata task-FOLDERS use `{L}{NN}_{stage}_pipeline[_<study>]`, where the leading
letter `L` encodes the pipeline STAGE (so alphabetical sort = pipeline order),
and `NN` is a stable study/cohort id (or a within-stage sequence where no study
axis exists):

```
L   stage   produces                  store
──  ─────   ────────────────────────  ─────────────────────
A   cms     Neat-*.dta, Bene_Info     1-CMS-Store   (heavy)
B   case    CASES / BFAF panels       2-Case-Store  (heavy)
C   data    ANALYSIS-*.dta            *-Data-Store  (heavy)
D   reg     coef tables (.tex/.csv)   results/      (LIGHT)
```

So `B01/C01/D01` = one study's case→data→reg folders; the disease-agnostic
`cms` stage (run once, reused) sits alone with `NN` as a plain sequence
(`A01`, `A02`). These task-folder letters reuse `A/B/C/D` (which mean
training/eval/display/data at the GROUP level) — no functional clash, since
they live at a different hierarchy level and the logging map keys on the
GROUP letter. Note it in the project `diagram/` so it reads clearly.


RUNNAME grammar by stage (see each specialist for detail)
----------------------------------------------------------

```
cms    run_cms_<year>                                  axis: year
case   run_case_<Cohort>_<year>                        axes: cohort × year
data   run_data_<Spec>                                 axis: analysis-spec (no year — cross-year)
reg    run_reg_<Condition>_<Pairing>_<Trait>[-ols|-iv] axes: condition × pairing × trait × estimator
```
