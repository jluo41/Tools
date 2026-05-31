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
{task}.py        (cell source)    →   {task}.do        (dispatcher) + stata/*.do (lib)
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
{NN}_{stage}_pipeline/
├── {NN}_{stage}_pipeline.do   ← single-step DISPATCHER: args <config> <step> [<year>] <results_dir>
├── stata/                     ← the worker library (one .do per step; imported by the dispatcher)
├── configs/
│   ├── <cfg>.do               ← Stata globals (raw paths, keep-vars, flags) — SOURCE OF TRUTH
│   └── <run>.yaml             ← _meta: block + stata_config: pointer  (NEW under this dialect)
├── runs/
│   └── <run>.ps1              ← per-run ENTRY (from run-ps1-template.ps1); writes runtime.yaml
├── run_{stage}_year.ps1       ← intra-run ORCHESTRATOR at task root (step parallelism + phases)
├── sbatch/                    ← cross-run batchers (multi-year / multi-cohort / multi-trait)
├── results/
│   └── <run>/                 ← log/*.txt · config_snapshot.do · summary.txt · runtime.yaml
└── diagram/                   ← doc surface (NEVER README.md); see diagram-ascii
```

Roles, precisely:

- **dispatcher `.do`** — `do {task}.do <config> <step> [<year>] <results_dir>`.
  Loads `configs/<cfg>.do`, sets up dirs, opens a per-step log, dispatches
  to `stata/<step>.do`, skips if output exists (idempotent), closes log.
- **`run_{stage}_year.ps1`** — internal helper; runs the dispatcher's steps
  in dependency-correct phases (often with within-phase parallelism via
  `Start-Process ... -PassThru | Wait-Process`). Called by the per-run `.ps1`.
- **`runs/<run>.ps1`** — the RUNNAME entry. Precondition-checks inputs,
  snapshots config, writes runtime.yaml, calls the orchestrator, finalizes.
- **`sbatch/`** — fan a single per-run `.ps1` across years / cohorts / traits.


Idempotency
-----------

Every worker `.do` (or the dispatcher's skip block) does
`capture confirm file <output>.dta` and SKIPs if present. Re-running a
finished pipeline is cheap; to recompute, delete the specific `.dta`.
Steps with no persistent output (`shared_*`, `describe`, `summary`,
`*_erase`) always run.


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
`LETTER_TO_TYPE` map is approximate for these folders; the type hint it
prints is cosmetic and does not affect correctness.


RUNNAME grammar by stage (see each specialist for detail)
----------------------------------------------------------

```
cms    run_cms_<year>                                  axis: year
case   run_case_<Cohort>_<year>                        axes: cohort × year
data   run_data_<Spec>                                 axis: analysis-spec (no year — cross-year)
reg    run_reg_<Condition>_<Pairing>_<Trait>[-ols|-iv] axes: condition × pairing × trait × estimator
```
