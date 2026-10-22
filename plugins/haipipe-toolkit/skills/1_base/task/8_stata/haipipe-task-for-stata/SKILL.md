---
name: haipipe-task-for-stata
description: "Unified Stata-engine job specialist: handles all 4 stages internally (cms/case/data/reg), owns the Stata engine contract, the {LNN} stage-letter alphabet, and stage disambiguation. Also a SERVER CHECK mode for the CMS secure server. Called by /haipipe-task when engine=Stata. Engine = Stata + PowerShell + logs (not Python/papermill)."
argument-hint: "[stage] [project_id] [bNN_<block>/jNN_<job>] [tNN_<task>]  OR  [server-check] [jNN_<job>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.4.0"
  last_updated: "2026-10-21"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-stata (unified Stata engine)
=====================================================

This is the UNIFIED Stata skill -- handles all 4 stages (cms/case/data/reg) internally.
Called by `/haipipe-task` when engine=Stata.
Each stage scaffolds a different pipeline stage; all share one engine contract (`ref/stata-dialect.md`).

Two modes: **BUILD** (scaffold job folders) and **SERVER CHECK** (validate before/after CMS server migration).

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Phase 2: Build, then authors the worker `.do` files).
Always end with the structured return block (status / task_folder / run_name / files).


## Type contract

```yaml
task-type: stata-cms | stata-case | stata-data | stata-reg
skill: haipipe-task-for-stata
does: Builds and runs one stage of the CMS Medicare Stata pipeline (cms extract, case panel, analysis table, or regression) through PowerShell tickets, on synth data locally and on full data on the CMS secure server.
worker: Stata .do files (dispatcher and step workers) in the Task's scripts/, or in the Job's src/ when its Tasks share them, with the Job's shared PowerShell 5.1 runner in src/ (run_cms_year.ps1, run_case_year.ps1, run-data-pipeline.ps1, run-regression-pipeline.ps1)
config: runs/<run>/config.do (Stata globals; it loads the Task's shared scripts/config/<cfg>.do), or scripts/config/<run>.do in a Block not yet moved
ticket: runs/<run>/<run>.ps1, a two-line caller that hands its config.do to the Job's runner in src/; templates ref/run-ps1-template.ps1 (cms, case) with ref/run-stage-year-template.ps1 (the runner), ref/run-data-runner-template.ps1 (data), ref/run-ps1-reg-template.ps1 (reg)
result: runs/<run>/result/ holding runtime.yaml, log/<step>[-<year>].txt and summary.txt (data adds config_snapshot.do and manifest.json); a reg result/ holds only what a reader reviews (RUN-REPORT.md, tables/, describe/), and each execution's log/, steps/, .done, runtime.yaml, config_snapshot.do and manifest.json go to runs/<run>/passes/pNN-<MMDD>/
heavy: the .dta assets in _WorkSpace/1-CMS-Store (cms), 2-Case-Store (case) and <N>-Data-Store (data), on the CMS server for full data; reg has none
roles: [trial, make, describe]
companions: [haipipe-task, haipipe-run, remote-error, haipipe-task-reviewer-agent]
plan_sample: ref/workflow-plan-sample-<stage>.yaml (cms, case, data, reg)
```

`trial` is a synth Run on the laptop (Gate 1), `make` a cms year, case cohort x source x year, data spec
or reg window x family, and `describe` a separately commissioned describe-only Run.


Stage dispatch table
--------------------

```
stage   task-type     {LNN} letter   Output store
-----   -----------   ------------   -----------------------
cms     stata-cms      A              1-CMS-Store   (heavy)
case    stata-case     B              2-Case-Store  (heavy)
data    stata-data     C              *-Data-Store  (heavy)
reg     stata-reg      D              runs/<run>/result/ (LIGHT)
```

The `{LNN}` letter encodes the stage so a job sorts in pipeline order (`A`cms -> `B`case -> `C`data -> `D`reg).
Full definition: the "Job `{LNN}` stage-letter alphabet" section in `ref/stata-dialect.md`.


Stage disambiguation
--------------------

The bare keyword `stata` (or a `.do` file) signals this skill; the accompanying **stage word** picks the internal branch:

```
+------------+-----------------------------------------------------------------+
| stata-cms  | cms . cms-pipeline . neat . bene_info . extract claims .         |
|            | elixhauser . raw cms . per year                                  |
| stata-case | case-pipeline . trigger cases . cohort . visit . bfaf .          |
|            | opioidrx . case panel . cohort x year                            |
| stata-data | data-pipeline . analysis table . filter case . filter external . |
|            | full variables . ANALYSIS-*.dta . cross-year                     |
| stata-reg  | reg . regression . ols . iv . instrument . estimate .             |
|            | coef table . two-part . lpm . logit . first-stage                |
+------------+-----------------------------------------------------------------+
```

Cascade:
  (1) EXPLICIT -- stage given as a positional (`cms`/`case`/`data`/`reg`) -> use it.
  (2) KEYWORD-INFERRED -- first stage keyword in the args wins.
        AUTO        -> accept; log "inferred stata stage '<kw>': <stage>"
        interactive -> propose; one-line confirm.
  (3) STILL UNKNOWN -- `stata` present but no stage word:
        AUTO        -> status: blocked, reason: "stata engine but stage unknown
                      (pass cms/case/data/reg, or a stage keyword)."
        interactive -> ASK which of the four stages.


Stage: cms
----------

**What this scaffolds:**

```text
work/bNN_<block>/
├── board.md
└── jNN_<job>/
    ├── src/                         run_cms_year.ps1 (the shared runner), libraries, config-defaults.do
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── draft/
        ├── workflow/                plan.yaml + report.yaml
        ├── scripts/<worker>.do
        ├── scripts/config/<cfg>.do  the Task's shared globals; every Run's config.do loads them
        └── runs/rNN_<run>/          one folder per Run
            ├── rNN_<run>.ps1        two lines: hands config.do to src/run_cms_year.ps1
            ├── config.do            this Run's globals: loads cms_production.do, pins data_year
            ├── run.yaml             its card: run, kind, role, status
            └── result/              runtime.yaml, log/<step>-<year>.txt, summary.txt

Result: $OUTPUT_ROOT/tNN_<task>/runs/rNN_<run>/result/ (OUTPUT_ROOT is the Job unless a consumer resolves it)
Task scripts/ (or Job src/ when the Tasks share them): dispatcher .do + extraction workers.
A Block not yet moved keeps runs/rNN_<run>.ps1, scripts/config/rNN_<run>.do and results/rNN_<run>/.
```

- **RUNNAME grammar:** `rNN_cms_<year>` (one per year, 2015..2020).
- **Steps:** `pde . carrier_claim . carrier_line . outpatient . bene_year . summary`.
- **Heavy outputs:** `_WorkSpace/1-CMS-Store/cms_full/<asset>/year-<year>/`.
- **Headline:** `Bene_Info-<year>` row x col counts.


Stage: case
-----------

**What this scaffolds:**

```text
work/bNN_<block>/
├── board.md
└── jNN_<job>/
    ├── src/                         run_case_year.ps1 (the shared runner), _source_{synth|full}.do, libraries
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── draft/
        ├── workflow/                plan.yaml + report.yaml
        ├── scripts/<worker>.do
        ├── scripts/config/<cfg>.do  the Task's shared globals; every Run's config.do loads them
        └── runs/rNN_<run>/          one folder per Run
            ├── rNN_<run>.ps1        two lines: hands config.do to src/run_case_year.ps1
            ├── config.do            loads the source selector, then the cohort config; pins the year
            ├── run.yaml             its card: run, kind, role, status
            └── result/              runtime.yaml, log/<step>-<year>.txt, summary.txt

Result: $OUTPUT_ROOT/tNN_<task>/runs/rNN_<run>/result/
Task scripts/: case_pipeline.do, cases/, feat/, describe worker.
Config chain: source selector -> shared cohort config -> the Run's runs/rNN_<run>/config.do.
A Block not yet moved keeps runs/rNN_<run>.ps1, scripts/config/rNN_<run>.do and results/rNN_<run>/.
```

- **RUNNAME grammar:** `rNN_case_<Cohort>_{synth|full}_<year>` (cohort x source x year).
- **Source dimension:** synth (laptop-safe) vs full (CMS server only). Each has `_source_{synth|full}.do` selector. Output tagged by `${cms_source}` to avoid collision.
- **Three-layer config:** (1) source selector, (2) shared cohort .do, (3) the Run's thin `runs/<run>/config.do`.
- **Steps:** `cases`; `bene_year + enrollment` (parallel); `pde chain`; `claims chain`; `lines chain`; `outpt chain`; `summary`.
- **Heavy outputs:** `_WorkSpace/2-Case-Store/case_<cohort>_<source>/<asset>/year-<year>/`.


Stage: data
-----------

**What this scaffolds:**

```text
work/bNN_<block>/
├── board.md
└── jNN_<job>/
    ├── src/                         run-data-pipeline.ps1 (the shared runner, when the Job has one), libraries
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── draft/
        ├── workflow/                plan.yaml + report.yaml
        ├── scripts/<worker>.do
        ├── scripts/config/<cfg>.do  the Task's shared globals; every Run's config.do loads them
        └── runs/rNN_<run>/          one folder per Run
            ├── rNN_<run>.ps1        self-orchestrating, or two lines into src/0-libs/run-data-pipeline.ps1
            ├── config.do            this spec's globals: case asset, version, year range
            ├── run.yaml             its card: run, kind, role, status
            └── result/              runtime.yaml, log/, summary.txt, config_snapshot.do, manifest.json

Result: $OUTPUT_ROOT/tNN_<task>/runs/rNN_<run>/result/
Task scripts/: data_pipeline.do, run_data_steps.ps1, numbered filter/derive/describe workers.
Each synth/real spec is its own Run folder (ticket + config.do + run.yaml); no year axis.
A Block not yet moved keeps runs/rNN_<run>.ps1, scripts/config/rNN_<run>.do and results/rNN_<run>/.
```

- **RUNNAME grammar:** `rNN_data_<Spec>` (cross-year, NO year axis).
- **SELF-ORCHESTRATING topology:** NO year orchestrator -- the Run's ticket `runs/<run>/<run>.ps1` (or the Job runner its two lines call) IS the orchestrator.
- **Source dimension:** synth vs real via paired configs (`v001_base_synth` / `v001_base_real`).
- **Steps:** `filter_case -> filter_external -> full_variables -> describe -> summary`.
- **Numbered subdirs** under scripts/ for sequential chain.
- **Heavy outputs:** `_WorkSpace/*-Data-Store/<asset>/` -> `ANALYSIS-CMS-Filter.dta`.
- **Traceability:** config_snapshot.do + manifest.json in the Run's `result/` (per B3 self-orchestrating).


Stage: reg
----------

**What this scaffolds:**

```text
work/bNN_<block>/
├── board.md
└── jNN_<job>/
    ├── src/                         0-libs/run-regression-pipeline.ps1 (the shared runner), cohort config
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── draft/
        ├── workflow/                plan.yaml + report.yaml
        ├── scripts/<worker>.do
        ├── scripts/config/<cfg>.do  the Task's shared globals; every Run's config.do loads them
        └── runs/rNN_<run>/          one folder per Run
            ├── rNN_<run>.ps1        two lines into src/0-libs/run-regression-pipeline.ps1
            ├── config.do            loads the cohort/pairing config; pins window, run_name, res_dir
            ├── run.yaml             its card: run, kind, role, status
            ├── result/              only what a reader reviews: RUN-REPORT.md, tables/, describe/
            └── passes/pNN-<MMDD>/   one per execution: log/, steps/, .done, runtime.yaml,
                                     config_snapshot.do, manifest.json (stays on the server)

Result: $OUTPUT_ROOT/tNN_<task>/runs/rNN_<run>/result/ (receipt: passes/pNN-<MMDD>/runtime.yaml)
Task scripts/: estimation workers; config chain shared cohort/pairing -> the Run's config.do.
Each window/family/source variant is its own Run folder; no dispatcher.
A Block not yet moved keeps runs/rNN_<run>.ps1, scripts/config/rNN_<run>.do and results/rNN_<run>/ (one folder, no passes/).
```

- **RUNNAME grammar:** `rNN_reg_<cohort>_<pairing>_{synth_}?<window>_<family>` (cohort x pairing x source x window x estimator-family grid).
- **DISPATCHER-LESS:** the runner calls worker .do scripts directly via `& $stata /e do "scripts/$w"`.
- **Output is LIGHT:** coef tables (.tex/.csv) in the Run's `result/`, logs in its `passes/pNN-<MMDD>/`, NOT _WorkSpace/.
- **Config dispatch:** `$env:HAIPIPE_RUN_CONFIG` (the Run's config, relative to the Task: `runs/<run>/config.do`) -> shared .do chain. Env vars: `HAIPIPE_WS_ROOT`, `HAIPIPE_RUN_CONFIG`, `HAIPIPE_RUN_RESULT` (result/), `HAIPIPE_PASS_DIR` (passes/pNN-<MMDD>/).
- **Two-layer config:** (1) shared `<Cohort>_<Pairing>.do` (data path + version), (2) the Run's thin `runs/<run>/config.do` (pins `outcome_bfaf_window` + `res_dir`; DID adds `file_policy`).
- **synth/full dimension:** separate shared configs (`<Cohort>_<Pairing>_synth.do` loads synth data version).
- **DID policy:** DID scripts merge `Policy-State-Year.dta` themselves (NOT baked into ANALYSIS-CMS-Filter.dta). Policy is a reg-stage concern -- C-stage should set `use_policy 0`.
- **Describe:** optional for reg -- Stata logs + .tex tables are self-documenting. No mandatory `d-Reg-Describe.do`.
- **Runner template:** `ref/run-ps1-reg-template.ps1` (self-contained, NOT the thin `ref/run-ps1-template.ps1`). In current practice its body is the Job's `src/0-libs/run-regression-pipeline.ps1` and each Run's ticket is the two-line caller `& "$PSScriptRoot\..\..\..\src\0-libs\run-regression-pipeline.ps1" "$PSScriptRoot\config.do"`.


Server check mode
-----------------

When invoked with "server check", "pre-flight", "cms server checklist", or "before hand-copy", this skill runs in CHECK mode instead of BUILD mode.

This is the OUTBOUND leg only: everything done BEFORE the code reaches the server.
When an error comes BACK from a run, hand off to `remote-error` (in `skills/0_utils/`, because that loop is engine-neutral), which owns the return leg: reason, fix the canonical, name the lines, land the lesson in the issue register.
It reads this folder's `ref/cms-server-checklist.md` through its own `ref/profile-cms-stata.md`, so the gate numbering and the issue-ID grammar stay identical across the two.

Three gates -- each catches different failure modes:

```
  Gate 1: LOCAL SYNTH RUN     run with synth config on laptop   (logic, wiring, paths)
  Gate 2: SERVER PRE-FLIGHT   machine checks before shipping    (encoding, PS 5.1, SSC, TEMP)
  Gate 3: FIRST REAL-DATA RUN after first server run            (filters, sample sizes, IV, signs)
```

Full checklist with all items, machine commands, and workflow: `ref/cms-server-checklist.md`

Execution:

```
Step 1 — Read ref/cms-server-checklist.md
Step 2 — Glob the job folder for .ps1, .do files
Step 3 — Run applicable gate checks:
         Gate 1: if synth results exist, check L1-L10
         Gate 2: always -- byte-scan, grep, parse-check (B1-F6)
         Gate 3: if user pastes server output, check R1-R10
Step 4 — Write SERVER_CHECK.md in the job folder (verdict + file list)
```

Return:

```
status: ok | blocked
verdict: pass | warn | fail
gates: {gate1: pass|skip, gate2: pass|warn|fail, gate3: pass|pending}
deliverable: SERVER_CHECK.md
files_to_copy: [list]
issues: [list of {id, gate, severity, file, line, detail}]
```


Dispatch table (scope → fn/)
-----------------------------

```
Scope              fn/ file                  When
────────────────── ───────────────────────── ──────────────────────────────
scaffold (new)     fn/scaffold.md             new job folder creation
audit (existing)   fn/audit-stata.md          /haipipe-task audit (or auto)
plan (existing)    fn/plan-stata.md           /haipipe-task plan
build (existing)   fn/build-stata.md          /haipipe-task build
execute            fn/execute-stata.md        /haipipe-task execute
report (existing)  fn/report-stata.md         /haipipe-task report
```

For an EXISTING job folder, the full lifecycle is:
  audit → plan → build → execute → report
Each stage reads its fn/ file.
For explicit commands (`plan`, `audit`, etc.), run ONLY that step.

For a NEW job folder, only `fn/scaffold.md` runs.


Routing protocol
----------------

Step 0: Read `ref/stata-dialect.md` (the engine contract) -- the three CWD/location-independence rules (Stata auto-detect, run-from-`$PSScriptRoot`, `ws_root`-anchored output) and the `{LNN}` alphabet.

Step 1: Detect AUTO_MODE (same triggers as `/haipipe-task`: `--auto`, env, or parent passed `--auto`).

Step 2: Resolve stage via the cascade above.

Step 3: Verify ancestors exist (project -> group), mirroring `/haipipe-task` Step 3b.
If a `--project-id` / `--group` is given and missing, scaffold via `/haipipe-task` (project / block) first; else ASK / block.

Step 4: Branch by scope:
  - NEW job folder → read `fn/scaffold.md`, execute
  - EXISTING job folder → dispatch to lifecycle fn/:
    (a) `fn/audit-stata.md` — Stata-aware pre-flight (extends generic four-sister)
    (b) `fn/plan-stata.md` — generate IPO plan.yaml + plan-script-*.yaml using `ref/workflow-plan-sample-<stage>.yaml`
    (c) `fn/build-stata.md` — author .do/.ps1 code (extends scaffold into full authoring)
    (d) `fn/execute-stata.md` — two-mode: local synth or CMS server hand-copy
    (e) `fn/report-stata.md` — generate report.yaml mirroring plan (binds runtime.yaml to original Stata logs and Results)
  - SERVER CHECK → read `ref/cms-server-checklist.md`, execute gate checks


Shared engine assets
--------------------

```
ref/stata-dialect.md            engine contract + {LNN} alphabet + script style/server constraints
ref/cms-server-checklist.md     three-gate migration checklist (synth run / pre-flight / real-data validation)
                                + the issue register and how an issue is named
ref/ndc-drug-features.md        NDC drug-type feature pattern: tier 1 (class flags) vs tier 2 (named drugs) + coverage
ref/run-ps1-template.ps1        THIN ticket for ORCHESTRATED stages (cms/case): the two-line caller, in either layout
ref/run-data-runner-template.ps1 SELF-ORCHESTRATING ticket for data-stage (preconditions + delegate)
ref/run-stage-year-template.ps1 the Job's per-year RUNNER in src/ for ORCHESTRATED stages: takes the Run's
                                config path, finds the Task from it (about 30 lines plus required checks)
ref/dispatcher-do-template.do   DISPATCHER (5-arg: <config> <step> <year> <results_dir> <ws_root>;
                                <config> = the Run's config relative to the Task, runs/<run>/config.do)
```

Three portability rules (DO NOT re-derive per task -- the templates already bake them):
  1. Stata exe = ONE resolvable location: hardcoded `$stata` line (cms-stage) OR
     `Resolve-StataExe` function (data/reg/case-stage). See rule A5 in stata-dialect.md.
  2. Run from the tNN Task folder, found from the Run's own path in both layouts (a ticket in `runs/` is flat and
     its Task is the parent; a ticket in `runs/<run>/` has its Task two levels up); code paths stay relative; folder name is free.
  3. Anchor the DATA root absolute via `ws_root` (config builds paths from `${ws_root}`, never literal `_WorkSpace`).

All `.ps1`/`.do` follow the **"Script style + server constraints"** contract in `ref/stata-dialect.md` -- CMS server is Windows PowerShell 5.1 only (no `pwsh`), ASCII-only files, 1-2 line headers, no ceremony, thin `runs/` + `sbatch/`.
`haipipe-task-reviewer-agent` enforces it before any hand-copy to the server (the researcher hand-reads every file).

cms/case/data Tasks include a read-only **describe / QC Step** (`describe` dispatch -> `scripts/d-<Stage>-Describe.do`) inside the variant Run.
Create a separate describe-only Run folder `runs/rNN_describe_<...>/` (its `run.yaml` says `role: describe`) only for an independently requested describe-only goal. Reg describe remains optional.
Built-ins only -- NO SSC (`egen tag` for distinct counts, never `distinct`).
See the "Describe / QC Step" section in `ref/stata-dialect.md`.


Per-stage ref files
-------------------

```
ref/config-seed-cms.do                Stata config template for CMS stage
ref/config-seed-case.do               Stata config template for case stage (shared cohort)
ref/config-seed-data.do               Stata config template for data stage (analysis spec)
ref/config-seed-reg.do                Stata config template for reg stage (shared: data path + version)
ref/config-seed-reg-run.do            a reg Run's runs/<run>/config.do (pins window + res_dir; DID adds file_policy)
ref/run-ps1-reg-template.ps1          self-contained reg runner (Resolve-StataExe + HAIPIPE_RUN_CONFIG + worker list)
ref/config-seed-run.do                a case Run's runs/<run>/config.do (loads source + cohort + year)
ref/workflow-plan-sample-cms.yaml     Run Spec with internal steps for CMS stage
ref/workflow-plan-sample-case.yaml    Run Spec with internal steps for case stage
ref/workflow-plan-sample-data.yaml    Run Spec with internal steps for data stage
ref/workflow-plan-sample-reg.yaml     Run Spec with internal steps for reg stage
```


Workflow lifecycle
------------------

When `/haipipe-task` targets an EXISTING job of this type, it runs the Stata lifecycle via the fn/ dispatch table above.
Each fn/ procedure reads its ref/ inputs:

```
fn/audit-stata.md    reads: (job folder .do/.ps1 files)
fn/plan-stata.md     reads: ref/workflow-plan-sample-<stage>.yaml
                            ../../haipipe-task/ref/workflow-template.yaml
                            ../../../project/haipipe-run/ref/plan-schema.md
fn/build-stata.md    reads: ref/config-seed-<stage>.do (+ ref/config-seed-reg-run.do for reg)
                            ref/dispatcher-do-template.do (cms/case/data)
                            ref/run-ps1-template.ps1 (cms/case) OR ref/run-ps1-reg-template.ps1 (reg)
                            ref/run-stage-year-template.ps1 (cms/case)
fn/execute-stata.md  reads: ref/cms-server-checklist.md (server mode)
fn/report-stata.md   reads: workflow/plan.yaml + runs/*/result/ (cms/case/data: result/log/*.txt;
                            reg: runs/*/passes/pNN-<MMDD>/log/*.txt)
```

This closes the gap where the old skill only had `fn/scaffold.md` (new task creation) but no procedures for the plan/audit/build/execute/report lifecycle on existing job folders.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences -- which stage was chosen + what was scaffolded
artifacts: [paths created]
next:      author dispatcher .do + scripts/ workers (incl. a `describe` step; separate describe Run only when requested); haipipe-task-reviewer-agent before hand-copy; then runs/<run>/<run>.ps1 (or sbatch/)
```
