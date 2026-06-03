Stata Execution Dialect — shared engine contract
==================================================

This is the **layer-2 execution contract** for Stata task-folders. The
skill's default dialect is Python + papermill + `.ipynb`; this document
defines the parallel Stata + PowerShell + `.log` dialect that the four
`haipipe-task-for-stata-*` specialists share.

The **structure invariants** (3-level hierarchy, RUNNAME spine, run↔result
pairing, light/heavy split, diagram-as-doc) are UNCHANGED. Only the
execution engine differs. Read `hierarchy.md` first for the invariants;
this file only describes what swaps out.


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


runtime.yaml — the integration point
-------------------------------------

The `.ps1` runner MUST emit `results/<run>/runtime.yaml` in the flat
key:value schema that `haipipe-task-logging/ref/regen_task_log.py` parses.
That script is engine-agnostic — it only globs `results/*/runtime.yaml` —
so emitting this gives a unified `task-log.md` across Python AND Stata
tasks for free. (The existing `manifest.json` may stay as a Stata-native
extra, or be retired.)

```yaml
status:     ok                              # running | ok | failed
started:    2026-02-23T13:52:27-05:00       # ISO 8601
ended:      2026-02-23T17:19:00-05:00
duration:   3h26m
git_sha:    8d8d6d1
host:       jjluo-pc/floyd
exit_code:  0
cmd:        pwsh A01_cms_pipeline/runs/run_cms_2015.ps1
config:     configs/run_cms_2015.yaml
notebook:   results/run_cms_2015/log/       # repurposed → per-step log dir
headline:   Bene_Info-2015 · 11,783,927 × 121
```

Write it twice: once at launch with `status: running` (atomically, via a
`.tmp` + move), then overwrite at finalize with the terminal status,
duration, exit_code, and headline. See `run-ps1-template.ps1`.


Anatomy of a Stata task-folder
-------------------------------

```
{LNN}_{stage}_pipeline/
├── {LNN}_{stage}_pipeline.do  ← single-step DISPATCHER: <config> <step> [<year>] <results_dir> <ws_root>
├── scripts/                   ← the worker library (one .do per step; imported by the dispatcher)
├── configs/
│   ├── <cfg>.do               ← Stata globals (keep-vars, flags; paths built from ${ws_root}) — SOURCE OF TRUTH
│   └── <run>.yaml             ← _meta: block + stata_config: pointer  (NEW under this dialect)
├── runs/
│   └── <run>.ps1              ← per-run ENTRY (from run-ps1-template.ps1); resolves ws_root; writes runtime.yaml
├── run_{stage}_year.ps1       ← intra-run ORCHESTRATOR at task root (resolves Stata; step parallelism + phases)
├── sbatch/                    ← cross-run batchers (multi-year / multi-cohort / multi-trait)
├── results/
│   └── <run>/                 ← log/*.txt · config_snapshot.do · summary.txt · runtime.yaml
└── diagram/                   ← doc surface (NEVER README.md); see diagram-ascii
```

The dispatcher `.do`, the worker `scripts/`, and `run_{stage}_year.ps1` live at
the task ROOT — they are the task's entry + execution machinery (the Stata
analog of Python's root `{task}.py` + papermill). Only the per-step WORKERS go
in `scripts/`. Three ref templates seed them:
`run-ps1-template.ps1` (the per-run entry), `run-stage-year-template.ps1`
(the orchestrator), `dispatcher-do-template.do` (the dispatcher).

Roles, precisely:

- **dispatcher `.do`** — `do {task}.do <config> <step> [<year>] <results_dir> <ws_root>`.
  Sets `global ws_root` FIRST, loads `configs/<cfg>.do`, sets up dirs, opens a
  per-step log, dispatches to `scripts/<step>.do`, skips if output exists
  (idempotent), closes log. Code paths (`configs/`, `scripts/`) are
  task-folder-relative; the DATA root arrives absolute as `<ws_root>`. The file
  name is FREE — nothing references it by a hardcoded path.
- **`run_{stage}_year.ps1`** — internal helper; resolves the Stata exe
  (`Resolve-StataExe`, any installed version), runs Stata with the working dir
  set to `$PSScriptRoot` (the task folder), and runs the dispatcher's steps in
  dependency-correct phases (within-phase parallelism via
  `Start-Process ... -PassThru | Wait-Process`). Called by the per-run `.ps1`;
  receives `-wsRoot` and passes it through.
- **`runs/<run>.ps1`** — the RUNNAME entry. Resolves the absolute `ws_root`
  (walk up to `pyproject.toml`), precondition-checks inputs, snapshots config,
  writes runtime.yaml, calls the orchestrator, finalizes.
- **`sbatch/`** — fan a single per-run `.ps1` across years / cohorts / traits.


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
- **`runs/run_describe_<...>.ps1`** — a describe-ONLY run: `Resolve-StataExe` +
  `ws_root`, then runs just the `describe` step on the already-built asset (no
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

1. **Resolve Stata, never hardcode a version.** The orchestrator uses
   `Resolve-StataExe`: honor `$env:HAIPIPE_STATA`, else newest
   `C:\Program Files\Stata*\StataMP-64.exe` (then SE/BE/base). This survives
   the common local-17 vs server-18 split with no per-machine edit.

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


Pre-flight code-review gate (ported)
-------------------------------------

The bash `run-sh-template.sh` blocks launch until a fresh `CODE_REVIEW.md`
exists. `run-ps1-template.ps1` ports the same gate to PowerShell. For
Stata this is arguably MORE valuable — silent merge / keep-var / horizon /
sample-definition bugs run clean and produce numbers. Skip mechanisms
mirror the bash gate: `_meta.skip_review: true` in `<run>.yaml`, or
`$env:HAIPIPE_SKIP_REVIEW = "1"` at launch.

Author convention: the dispatcher `.do` SHOULD carry a top-of-file
`Intent` comment block (what each step measures, where outputs land).


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
