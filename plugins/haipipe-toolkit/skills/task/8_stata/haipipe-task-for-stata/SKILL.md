---
name: haipipe-task-for-stata
description: "Unified Stata-engine job specialist: handles all 4 stages internally (cms/case/data/reg), owns the Stata engine contract, the {LNN} stage-letter alphabet, and stage disambiguation. Also a SERVER CHECK mode for the CMS secure server. Called by /haipipe-task when engine=Stata. Engine = Stata + PowerShell + logs (not Python/papermill)."
argument-hint: "[stage] [project_id] [group] [task-name]  OR  [server-check] [job]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.3.0"
  last_updated: "2026-08-29"
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


Stage dispatch table
--------------------

```
stage   task-type     {LNN} letter   Output store
-----   -----------   ------------   -----------------------
cms     stata-cms      A              1-CMS-Store   (heavy)
case    stata-case     B              2-Case-Store  (heavy)
data    stata-data     C              *-Data-Store  (heavy)
reg     stata-reg      D              results/      (LIGHT)
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
tasks/bNN_<block>/
├── board.md
└── jNN_<job>/
    ├── src/                         shared libraries + config-defaults.do
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── outline/
        ├── workflow/                plan.yaml + report.yaml
        ├── scripts/<worker>.do
        ├── scripts/config/rNN_<run>.do   + optional YAML metadata wrapper
        └── runs/rNN_<run>.ps1

Generated: $OUTPUT_ROOT/tNN_<task>/results/rNN_<run>/
           per-step logs under the same Result/log/
Task scripts/: dispatcher .do + run_cms_year.ps1 + extraction workers.
```

- **RUNNAME grammar:** `rNN_cms_<year>` (one per year, 2015..2020).
- **Steps:** `pde . carrier_claim . carrier_line . outpatient . bene_year . summary`.
- **Heavy outputs:** `_WorkSpace/1-CMS-Store/cms_full/<asset>/year-<year>/`.
- **Headline:** `Bene_Info-<year>` row x col counts.


Stage: case
-----------

**What this scaffolds:**

```text
tasks/bNN_<block>/
├── board.md
└── jNN_<job>/
    ├── src/                         shared libraries + config-defaults.do
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── outline/
        ├── workflow/                plan.yaml + report.yaml
        ├── scripts/<worker>.do
        ├── scripts/config/rNN_<run>.do   + optional YAML metadata wrapper
        └── runs/rNN_<run>.ps1

Generated: $OUTPUT_ROOT/tNN_<task>/results/rNN_<run>/
           per-step logs under the same Result/log/
Task scripts/: case_pipeline.do, run_case_year.ps1, cases/, feat/, describe worker.
Config chain: source selector -> shared cohort config -> rNN per-run wrapper.
```

- **RUNNAME grammar:** `rNN_case_<Cohort>_{synth|full}_<year>` (cohort x source x year).
- **Source dimension:** synth (laptop-safe) vs full (CMS server only). Each has `_source_{synth|full}.do` selector. Output tagged by `${cms_source}` to avoid collision.
- **Three-layer config:** (1) source selector, (2) shared cohort .do, (3) thin per-run wrapper.
- **Steps:** `cases`; `bene_year + enrollment` (parallel); `pde chain`; `claims chain`; `lines chain`; `outpt chain`; `summary`.
- **Heavy outputs:** `_WorkSpace/2-Case-Store/case_<cohort>_<source>/<asset>/year-<year>/`.


Stage: data
-----------

**What this scaffolds:**

```text
tasks/bNN_<block>/
├── board.md
└── jNN_<job>/
    ├── src/                         shared libraries + config-defaults.do
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── outline/
        ├── workflow/                plan.yaml + report.yaml
        ├── scripts/<worker>.do
        ├── scripts/config/rNN_<run>.do   + optional YAML metadata wrapper
        └── runs/rNN_<run>.ps1

Generated: $OUTPUT_ROOT/tNN_<task>/results/rNN_<run>/
           per-step logs under the same Result/log/
Task scripts/: data_pipeline.do, run_data_steps.ps1, numbered filter/derive/describe workers.
Each synth/real spec has an independent rNN config/Ticket pair; no year axis.
```

- **RUNNAME grammar:** `rNN_data_<Spec>` (cross-year, NO year axis).
- **SELF-ORCHESTRATING topology:** NO year orchestrator -- `runs/*.ps1` IS the orchestrator.
- **Source dimension:** synth vs real via paired configs (`v001_base_synth` / `v001_base_real`).
- **Steps:** `filter_case -> filter_external -> full_variables -> describe -> summary`.
- **Numbered subdirs** under scripts/ for sequential chain.
- **Heavy outputs:** `_WorkSpace/*-Data-Store/<asset>/` -> `ANALYSIS-CMS-Filter.dta`.
- **Traceability:** config_snapshot.do + manifest.json in results/ (per B3 self-orchestrating).


Stage: reg
----------

**What this scaffolds:**

```text
tasks/bNN_<block>/
├── board.md
└── jNN_<job>/
    ├── src/                         shared libraries + config-defaults.do
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── outline/
        ├── workflow/                plan.yaml + report.yaml
        ├── scripts/<worker>.do
        ├── scripts/config/rNN_<run>.do   + optional YAML metadata wrapper
        └── runs/rNN_<run>.ps1

Generated: $OUTPUT_ROOT/tNN_<task>/results/rNN_<run>/
           per-step logs under the same Result/log/
Task scripts/: estimation workers; config chain shared cohort/pairing -> rNN wrapper.
Each window/family/source variant has an independent rNN Ticket; no dispatcher.
```

- **RUNNAME grammar:** `rNN_reg_<cohort>_<pairing>_{synth_}?<window>_<family>` (cohort x pairing x source x window x estimator-family grid).
- **DISPATCHER-LESS:** .ps1 runners call worker .do scripts directly via `& $stata /e do "scripts/$w"`.
- **Output is LIGHT:** coef tables (.tex/.csv) + logs in results/, NOT _WorkSpace/.
- **Config dispatch:** `$env:HAIPIPE_RUN_CONFIG` -> per-run .do -> shared .do chain. Env vars: `HAIPIPE_WS_ROOT` + `HAIPIPE_RUN_CONFIG`.
- **Two-layer config:** (1) shared `<Cohort>_<Pairing>.do` (data path + version), (2) per-run thin wrapper (pins `outcome_bfaf_window` + `res_dir`; DID adds `file_policy`).
- **synth/full dimension:** separate shared configs (`<Cohort>_<Pairing>_synth.do` loads synth data version).
- **DID policy:** DID scripts merge `Policy-State-Year.dta` themselves (NOT baked into ANALYSIS-CMS-Filter.dta). Policy is a reg-stage concern -- C-stage should set `use_policy 0`.
- **Describe:** optional for reg -- Stata logs + .tex tables are self-documenting. No mandatory `d-Reg-Describe.do`.
- **Runner template:** `ref/run-ps1-reg-template.ps1` (self-contained, NOT the thin `ref/run-ps1-template.ps1`).


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
ref/run-ps1-template.ps1        THIN per-run entry for ORCHESTRATED stages (cms/case)
ref/run-data-runner-template.ps1 SELF-ORCHESTRATING per-run entry for data-stage (preconditions + delegate)
ref/run-stage-year-template.ps1 intra-run ORCHESTRATOR for ORCHESTRATED stages (about 30 lines plus required checks; internal step groups)
ref/dispatcher-do-template.do   DISPATCHER (5-arg: <config> <step> <year> <results_dir> <ws_root>)
```

Three portability rules (DO NOT re-derive per task -- the templates already bake them):
  1. Stata exe = ONE resolvable location: hardcoded `$stata` line (cms-stage) OR
     `Resolve-StataExe` function (data/reg/case-stage). See rule A5 in stata-dialect.md.
  2. Run from the tNN Task folder (resolve from the script location); code paths stay relative; folder name is free.
  3. Anchor the DATA root absolute via `ws_root` (config builds paths from `${ws_root}`, never literal `_WorkSpace`).

All `.ps1`/`.do` follow the **"Script style + server constraints"** contract in `ref/stata-dialect.md` -- CMS server is Windows PowerShell 5.1 only (no `pwsh`), ASCII-only files, 1-2 line headers, no ceremony, thin `runs/` + `sbatch/`.
`haipipe-task-reviewer-agent` enforces it before any hand-copy to the server (the researcher hand-reads every file).

cms/case/data Tasks include a read-only **describe / QC Step** (`describe` dispatch -> `scripts/d-<Stage>-Describe.do`) inside the variant Run.
Create a separate `runs/rNN_describe_<...>.ps1` only for an independently requested describe-only goal. Reg describe remains optional.
Built-ins only -- NO SSC (`egen tag` for distinct counts, never `distinct`).
See the "Describe / QC Step" section in `ref/stata-dialect.md`.


Per-stage ref files
-------------------

```
ref/config-seed-cms.do                Stata config template for CMS stage
ref/config-seed-case.do               Stata config template for case stage (shared cohort)
ref/config-seed-data.do               Stata config template for data stage (analysis spec)
ref/config-seed-reg.do                Stata config template for reg stage (shared: data path + version)
ref/config-seed-reg-run.do            thin per-run .do wrapper for reg (pins window + res_dir; DID adds file_policy)
ref/run-ps1-reg-template.ps1          self-contained reg runner (Resolve-StataExe + HAIPIPE_RUN_CONFIG + worker list)
ref/config-seed-run.do                thin per-run .do wrapper (case only — loads source + cohort + year)
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
                            ../../haipipe-workflow/ref/plan-schema.md
fn/build-stata.md    reads: ref/config-seed-<stage>.do (+ ref/config-seed-reg-run.do for reg)
                            ref/dispatcher-do-template.do (cms/case/data)
                            ref/run-ps1-template.ps1 (cms/case) OR ref/run-ps1-reg-template.ps1 (reg)
                            ref/run-stage-year-template.ps1 (cms/case)
fn/execute-stata.md  reads: ref/cms-server-checklist.md (server mode)
fn/report-stata.md   reads: workflow/plan.yaml + results/*/log/*.txt
```

This closes the gap where the old skill only had `fn/scaffold.md` (new task creation) but no procedures for the plan/audit/build/execute/report lifecycle on existing job folders.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences -- which stage was chosen + what was scaffolded
artifacts: [paths created]
next:      author dispatcher .do + scripts/ workers (incl. a `describe` step; separate describe Run only when requested); haipipe-task-reviewer-agent before hand-copy; then runs/<run>.ps1 (or sbatch/)
```
