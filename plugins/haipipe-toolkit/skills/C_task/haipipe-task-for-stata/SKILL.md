---
name: haipipe-task-for-stata
description: "Unified Stata-engine task-folder build specialist. Handles all 4 stages internally (cms/case/data/reg). Owns the Stata engine contract, the {LNN} stage-letter alphabet, and stage disambiguation. Also provides SERVER CHECK mode — three-gate migration checklist for the CMS secure server. Called by /haipipe-task when engine=Stata; direct invocation works for any Stata-dialect scaffold. Engine = Stata + PowerShell + logs (NOT Python/papermill)."
argument-hint: "[stage] [project_id] [group] [task-name]  OR  [server-check] [task-folder]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.4.0"
  last_updated: "2026-06-10"
  summary: "Unified Stata skill — topology-aware templates + contract aligned with production."
  changelog:
    - "1.0.0 (2026-05-31): baseline."
    - "1.1.0 (2026-06-08): add metadata; workflow lifecycle compatible."
    - "1.2.0 (2026-06-09): unwrap prose; fix agent names to haipipe-task-{creator,reviewer}-agent; add lifecycle paragraph."
    - "2.0.0 (2026-06-10): unified — absorb all 4 child specialists (cms/case/data/reg) into one skill; no child delegation."
    - "2.1.0 (2026-06-10): absorb cms-server-checklist from 0_utils; add server check mode with three-gate protocol."
    - "2.2.0 (2026-06-10): fix 6 issues — rewrite 4 plan samples to match real pipeline phases; remove SSC from build-stata; fix scaffold config extension; update orchestrator template to working version (<=30 lines); fix ~15-><=30 budget; remove helper function references from build-stata."
    - "2.3.0 (2026-06-10): align templates+contract with production — add topology families (orchestrated vs self-orchestrating) to dialect; soften A5 (accept Resolve-StataExe); scope B2/B3 by topology; expand config-seed-data to production size (~80 globals); add run-data-runner-template.ps1; data-stage synth/real source dimension; STATATMP in orchestrator template; match-existing mode in build-stata."
    - "2.4.0 (2026-06-10): align reg stage to D01 ground truth — add run-ps1-reg-template.ps1 + config-seed-reg-run.do; rewrite config-seed-reg.do (data path only, controls in workers); fix RUNNAME to include cohort+pairing+source; document DID policy as reg-stage concern (not C-stage); make describe optional for reg; add Step 3b to build-stata (reg runner authoring); fix workflow-plan-sample-reg.yaml (DID policy phase, correct skill name)."
---

Skill: haipipe-task-for-stata  (unified Stata engine)
=====================================================

This is the UNIFIED Stata skill -- handles all 4 stages (cms/case/data/reg) internally. Called by `/haipipe-task` when engine=Stata. Each stage scaffolds a different pipeline phase; all share one engine contract (`ref/stata-dialect.md`).

Two modes: **BUILD** (scaffold task folders) and **SERVER CHECK** (validate before/after CMS server migration).

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Stage 2: Build, then authors the worker `.do` files). Always end with the structured return block (status / task_folder / run_name / files).


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

The `{LNN}` letter encodes the stage so a task-folder sorts in pipeline order (`A`cms -> `B`case -> `C`data -> `D`reg). Full definition: the "Task-folder `{LNN}` stage-letter alphabet" section in `ref/stata-dialect.md`.


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

```
tasks/{G}{NN}_<group>/
+-- A{NN}_cms_pipeline/                          <- task-folder letter A = cms stage ({LNN})
    +-- A{NN}_cms_pipeline.do                    dispatcher: <config> <step> <year> <results_dir> <ws_root>
    +-- scripts/                                 worker .do per step (b-*-All.do, c-Bene-Year.do, d-Year-Summary.do)
    +-- configs/
    |   +-- cms_production.do                    Stata globals (keep-vars, flags; paths from ${ws_root}) -- source of truth
    |   +-- run_cms_<year>.yaml                  _meta: block + stata_config: pointer
    +-- run_cms_year.ps1                         orchestrator (<=30 lines)
    +-- runs/
    |   +-- run_cms_<year>.ps1                   THIN per-year entry
    +-- sbatch/
    |   +-- run_cms_<y0>-<y1>.ps1                multi-year batcher
    +-- results/
    +-- diagram/
```

- **RUNNAME grammar:** `run_cms_<year>` (one per year, 2015..2020).
- **Steps:** `pde . carrier_claim . carrier_line . outpatient . bene_year . summary`.
- **Heavy outputs:** `_WorkSpace/1-CMS-Store/cms_full/<asset>/year-<year>/`.
- **Headline:** `Bene_Info-<year>` row x col counts.


Stage: case
-----------

**What this scaffolds:**

```
tasks/{G}{NN}_<group>/
+-- B{NN}_case_pipeline_<study>/
    +-- case_pipeline.do                         dispatcher: <config> <step> <year> <results_dir> <ws_root> <source>
    +-- run_case_year.ps1                        year orchestrator (topic flags, parallel Stata jobs)
    +-- scripts/
    |   +-- cases/                               trigger-cases-<script>.do
    |   +-- feat/                                bene-* / bfaf-* / shared-* workers
    |   +-- d-Case-Describe.do                   cross-year QC
    +-- configs/
    |   +-- <Cohort>.do                          SHARED: ICD codes, topic flags, paths
    |   +-- _source_synth.do                     source selector: cms_source=synth
    |   +-- _source_full.do                      source selector: cms_source=full
    |   +-- <Cohort>_synth_<year>.do             PER-RUN: loads selector + shared config + pins year
    |   +-- <Cohort>_full_<year>.do              PER-RUN: same for full
    +-- runs/
    |   +-- run_case_<Cohort>_synth_<year>.ps1
    |   +-- run_case_<Cohort>_full_<year>.ps1
    |   +-- run_describe_<Cohort>.ps1
    +-- sbatch/
    +-- results/
    +-- diagram/
```

- **RUNNAME grammar:** `run_case_<Cohort>_{synth|full}_<year>` (cohort x source x year).
- **Source dimension:** synth (laptop-safe) vs full (CMS server only). Each has `_source_{synth|full}.do` selector. Output tagged by `${cms_source}` to avoid collision.
- **Three-layer config:** (1) source selector, (2) shared cohort .do, (3) thin per-run wrapper.
- **Steps:** `cases`; `bene_year + enrollment` (parallel); `pde chain`; `claims chain`; `lines chain`; `outpt chain`; `summary`.
- **Heavy outputs:** `_WorkSpace/2-Case-Store/case_<cohort>_<source>/<asset>/year-<year>/`.


Stage: data
-----------

**What this scaffolds:**

```
tasks/{G}{NN}_<group>/
+-- C{NN}_data_pipeline_<study>/
    +-- data_pipeline.do                         dispatcher (NO year argument -- cross-year)
    +-- run_data_steps.ps1                       shared helper: sequential step runner
    +-- scripts/
    |   +-- 1-filter-case/
    |   +-- 2-filter-external/
    |   +-- 3-full-variables/
    |   +-- 4-describe/d-Data-Describe.do
    |   +-- d-Data-Summary.do
    +-- configs/
    |   +-- <Spec>.do                            synth config (laptop-safe)
    |   +-- <Spec>_real.do                       real config (CMS server); version TODO-tagged
    +-- runs/
    |   +-- run_data_<Spec>.ps1                  SELF-ORCHESTRATING (ref/run-data-runner-template.ps1)
    |   +-- run_data_<Spec>_real.ps1
    |   +-- run_describe_<Spec>.ps1
    +-- sbatch/
    |   +-- run_data_all.ps1                     batcher (-mode synth|real|all)
    +-- results/
    |   +-- run_data_<Spec>/
    |       +-- log/ config_snapshot.do manifest.json summary.txt
    +-- diagram/
```

- **RUNNAME grammar:** `run_data_<Spec>` (cross-year, NO year axis).
- **SELF-ORCHESTRATING topology:** NO year orchestrator -- `runs/*.ps1` IS the orchestrator.
- **Source dimension:** synth vs real via paired configs (`v001_base_synth` / `v001_base_real`).
- **Steps:** `filter_case -> filter_external -> full_variables -> describe -> summary`.
- **Numbered subdirs** under scripts/ for sequential chain.
- **Heavy outputs:** `_WorkSpace/*-Data-Store/<asset>/` -> `ANALYSIS-CMS-Filter.dta`.
- **Traceability:** config_snapshot.do + manifest.json in results/ (per B3 self-orchestrating).


Stage: reg
----------

**What this scaffolds:**

```
tasks/{G}{NN}_<group>/
+-- D{NN}_reg_<condition>_<pairing>/
    +-- scripts/
    |   +-- run-{N}-<Cohort>_<Pairing>_<Trait>-{family}-{spec}.do   numbered workers
    +-- configs/
    |   +-- <Cohort>_<Pairing>.do                shared config (data path + version)
    |   +-- <Cohort>_<Pairing>_synth.do          shared config, synth variant
    |   +-- run_reg_<RUNNAME>.do                 per-run thin wrapper (pins window + res_dir)
    +-- runs/
    |   +-- run_reg_<RUNNAME>.ps1                self-contained (Resolve-StataExe + worker list)
    +-- sbatch/
    |   +-- run-<cohort>-<estimator>-all.ps1     per-estimator batcher
    |   +-- run-<cohort>_synth-all.ps1           synth batcher
    +-- results/
    |   +-- run_reg_<RUNNAME>/
    |       +-- tables/                          .tex + .csv coef tables (main-table script only)
    |       +-- log/                             Stata .log transcripts
    +-- diagram/
```

- **RUNNAME grammar:** `run_reg_<cohort>_<pairing>_{synth_}?<window>_<family>` (cohort x pairing x source x window x estimator-family grid).
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
Step 2 — Glob the task folder for .ps1, .do files
Step 3 — Run applicable gate checks:
         Gate 1: if synth results exist, check L1-L10
         Gate 2: always -- byte-scan, grep, parse-check (B1-F6)
         Gate 3: if user pastes server output, check R1-R10
Step 4 — Write SERVER_CHECK.md in the task folder (verdict + file list)
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
scaffold (new)     fn/scaffold.md             new task folder creation
audit (existing)   fn/audit-stata.md          /haipipe-task audit (or auto)
plan (existing)    fn/plan-stata.md           /haipipe-task plan
build (existing)   fn/build-stata.md          /haipipe-task build
execute            fn/execute-stata.md        /haipipe-task execute
report (existing)  fn/report-stata.md         /haipipe-task report
```

For an EXISTING task folder, the full lifecycle is:
  audit → plan → build → execute → report
Each stage reads its fn/ file. For explicit commands (`plan`, `audit`, etc.),
run ONLY that step.

For a NEW task folder, only `fn/scaffold.md` runs.


Routing protocol
----------------

Step 0: Read `ref/stata-dialect.md` (the engine contract) -- the three CWD/location-independence rules (Stata auto-detect, run-from-`$PSScriptRoot`, `ws_root`-anchored output) and the `{LNN}` alphabet.

Step 1: Detect AUTO_MODE (same triggers as `/haipipe-task`: `--auto`, env, or parent passed `--auto`).

Step 2: Resolve stage via the cascade above.

Step 3: Verify ancestors exist (project -> group), mirroring `/haipipe-task` Step 3b. If a `--project-id` / `--group` is given and missing, scaffold via `/haipipe-task` (project / task-group) first; else ASK / block.

Step 4: Branch by scope:
  - NEW task folder → read `fn/scaffold.md`, execute
  - EXISTING task folder → dispatch to lifecycle fn/:
    (a) `fn/audit-stata.md` — Stata-aware pre-flight (extends generic four-sister)
    (b) `fn/plan-stata.md` — generate IPO plan.yaml + plan-script-*.yaml using `ref/workflow-plan-sample-<stage>.yaml`
    (c) `fn/build-stata.md` — author .do/.ps1 code (extends scaffold into full authoring)
    (d) `fn/execute-stata.md` — two-mode: local synth or CMS server hand-copy
    (e) `fn/report-stata.md` — generate report.yaml mirroring plan (reads Stata logs, not runtime.yaml)
  - SERVER CHECK → read `ref/cms-server-checklist.md`, execute gate checks


Shared engine assets
--------------------

```
ref/stata-dialect.md            engine contract + {LNN} alphabet + script style/server constraints
ref/cms-server-checklist.md     three-gate migration checklist (synth run / pre-flight / real-data validation)
ref/run-ps1-template.ps1        THIN per-run entry for ORCHESTRATED stages (cms/case)
ref/run-data-runner-template.ps1 SELF-ORCHESTRATING per-run entry for data-stage (preconditions + delegate)
ref/run-stage-year-template.ps1 intra-run ORCHESTRATOR for ORCHESTRATED stages (<=30 lines; phases)
ref/dispatcher-do-template.do   DISPATCHER (5-arg: <config> <step> <year> <results_dir> <ws_root>)
```

Three portability rules (DO NOT re-derive per task -- the templates already bake them):
  1. Stata exe = ONE resolvable location: hardcoded `$stata` line (cms-stage) OR
     `Resolve-StataExe` function (data/reg/case-stage). See rule A5 in stata-dialect.md.
  2. Run from the task folder (`$PSScriptRoot`); code paths stay relative; folder name is free.
  3. Anchor the DATA root absolute via `ws_root` (config builds paths from `${ws_root}`, never literal `_WorkSpace`).

All `.ps1`/`.do` follow the **"Script style + server constraints"** contract in `ref/stata-dialect.md` -- CMS server is Windows PowerShell 5.1 only (no `pwsh`), ASCII-only files, 1-2 line headers, no ceremony, thin `runs/` + `sbatch/`. `haipipe-task-reviewer-agent` enforces it before any hand-copy to the server (the researcher hand-reads every file).

Every Stata task ALSO ships a read-only **describe / QC run** (`describe` dispatch step -> `scripts/d-<Stage>-Describe.do`, + `runs/run_describe_<...>.ps1`) that writes a human-readable correctness report to `results/`. Built-ins only -- NO SSC (`egen tag` for distinct counts, never `distinct`). See the "Describe / QC run" section in `ref/stata-dialect.md`.


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
ref/workflow-plan-sample-cms.yaml     IPO phases for CMS stage
ref/workflow-plan-sample-case.yaml    IPO phases for case stage
ref/workflow-plan-sample-data.yaml    IPO phases for data stage
ref/workflow-plan-sample-reg.yaml     IPO phases for reg stage
```


Workflow lifecycle
------------------

When `/haipipe-task` targets an EXISTING task-folder of this type, it runs
the Stata lifecycle via the fn/ dispatch table above. Each fn/ procedure
reads its ref/ inputs:

```
fn/audit-stata.md    reads: (task folder .do/.ps1 files)
fn/plan-stata.md     reads: ref/workflow-plan-sample-<stage>.yaml
                            ../haipipe-task/ref/workflow-template.yaml
                            B_project/haipipe-workflow/ref/plan-schema.md
fn/build-stata.md    reads: ref/config-seed-<stage>.do (+ ref/config-seed-reg-run.do for reg)
                            ref/dispatcher-do-template.do (cms/case/data)
                            ref/run-ps1-template.ps1 (cms/case) OR ref/run-ps1-reg-template.ps1 (reg)
                            ref/run-stage-year-template.ps1 (cms/case)
fn/execute-stata.md  reads: ref/cms-server-checklist.md (server mode)
fn/report-stata.md   reads: workflow/plan.yaml + results/*/log/*.txt
```

This closes the gap where the old skill only had `fn/scaffold.md` (new
task creation) but no procedures for the plan/audit/build/execute/report
lifecycle on existing task folders.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences -- which stage was chosen + what was scaffolded
artifacts: [paths created]
next:      author dispatcher .do + scripts/ workers (incl. a `describe` step + run_describe_*.ps1 QC run); haipipe-task-reviewer-agent before hand-copy; then runs/<run>.ps1 (or sbatch/)
```
