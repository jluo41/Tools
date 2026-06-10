---
name: haipipe-task-for-stata
description: "Unified Stata-engine task-folder build specialist. Handles all 4 stages internally (cms/case/data/reg). Owns the Stata engine contract, the {LNN} stage-letter alphabet, and stage disambiguation. Called by /haipipe-task when engine=Stata; direct invocation works for any Stata-dialect scaffold. Engine = Stata + PowerShell + logs (NOT Python/papermill)."
argument-hint: "[stage] [project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-06-10"
  summary: "Unified Stata skill — handles cms/case/data/reg internally."
  changelog:
    - "1.0.0 (2026-05-31): baseline."
    - "1.1.0 (2026-06-08): add metadata; workflow lifecycle compatible."
    - "1.2.0 (2026-06-09): unwrap prose; fix agent names to haipipe-task-{creator,reviewer}-agent; add lifecycle paragraph."
    - "2.0.0 (2026-06-10): unified — absorb all 4 child specialists (cms/case/data/reg) into one skill; no child delegation."
---

Skill: haipipe-task-for-stata  (unified Stata engine)
=====================================================

This is the UNIFIED Stata skill -- handles all 4 stages (cms/case/data/reg) internally. Called by `/haipipe-task` when engine=Stata. Each stage scaffolds a different pipeline phase; all share one engine contract (`ref/stata-dialect.md`).

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
    +-- run_cms_year.ps1                         orchestrator (~15 lines)
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
    +-- scripts/
    |   +-- 1-filter-case/
    |   +-- 2-filter-external/
    |   +-- 3-full-variables/
    |   +-- 4-describe/d-Data-Describe.do
    +-- configs/
    |   +-- <Spec>.do
    +-- runs/
    |   +-- run_data_<Spec>.ps1
    |   +-- run_describe_<Spec>.ps1
    +-- results/
    +-- diagram/
```

- **RUNNAME grammar:** `run_data_<Spec>` (cross-year, NO year axis).
- **Steps:** `filter_case -> filter_external -> full_variables -> describe -> summary`.
- **Numbered subdirs** under scripts/ for sequential chain.
- **Heavy outputs:** `_WorkSpace/*-Data-Store/<asset>/` -> `ANALYSIS-CMS-Filter.dta`.


Stage: reg
----------

**What this scaffolds:**

```
tasks/{G}{NN}_<group>/
+-- D{NN}_reg_<condition>_<pairing>/
    +-- scripts/
    |   +-- run-{N}-{family}-{spec}.do           numbered workers (1-10 across OLS/IV/DID)
    +-- configs/
    |   +-- <Cohort>_<Pairing>.do                shared config (no dispatcher)
    +-- runs/
    |   +-- run_reg_<window>_<family>.ps1         calls workers directly (DISPATCHER-LESS)
    +-- results/
    |   +-- run_reg_<window>_<family>/
    |       +-- tables/                          .tex + .csv coef tables
    |       +-- log/                             Stata .log transcripts
    +-- diagram/
```

- **RUNNAME grammar:** `run_reg_<window>_<family>` (window x estimator-family grid).
- **DISPATCHER-LESS:** .ps1 runners call worker .do scripts directly.
- **Output is LIGHT:** coef tables (.tex/.csv) in results/, NOT _WorkSpace/.
- **Env vars** (`HAIPIPE_WS_ROOT`, `HAIPIPE_REG_WINDOW`, `HAIPIPE_RES_DIR`) cross the Stata `clear all` boundary.


Routing protocol
----------------

Step 0: Read `ref/stata-dialect.md` (the engine contract) -- the three CWD/location-independence rules (Stata auto-detect, run-from-`$PSScriptRoot`, `ws_root`-anchored output) and the `{LNN}` alphabet.

Step 1: Detect AUTO_MODE (same triggers as `/haipipe-task`: `--auto`, env, or parent passed `--auto`).

Step 2: Resolve stage via the cascade above.

Step 3: Verify ancestors exist (project -> group), mirroring `/haipipe-task` Step 3b. If a `--project-id` / `--group` is given and missing, scaffold via `/haipipe-task` (project / task-group) first; else ASK / block.

Step 4: Branch internally by stage -- read `ref/config-seed-<stage>.do` (the Stata config template) and run the stage-specific scaffold from `fn/scaffold.md`. The `.do` file is what Stata reads; the companion `ref/config-meta-<stage>.yaml` carries `_meta:` discipline for the workflow layer.


Shared engine assets
--------------------

```
ref/stata-dialect.md            engine contract + {LNN} alphabet + script style/server constraints
ref/run-ps1-template.ps1        THIN per-run entry in runs/ (a few lines; delegates to the orchestrator)
ref/run-stage-year-template.ps1 intra-run ORCHESTRATOR (~15 lines; $stata var; $PSScriptRoot CWD; phases)
ref/dispatcher-do-template.do   DISPATCHER (5-arg: <config> <step> <year> <results_dir> <ws_root>)
```

Three portability rules (DO NOT re-derive per task -- the templates already bake them):
  1. Stata exe = ONE editable `$stata` line at the top of the orchestrator (no resolver functions).
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
ref/config-seed-reg.do                Stata config template for reg stage (regression config)
ref/config-seed-run.do                thin per-run .do wrapper (case only — loads source + cohort + year)
ref/config-meta-cms.yaml              _meta: discipline template for CMS (workflow layer reads this)
ref/config-meta-case.yaml             _meta: discipline template for case
ref/config-meta-data.yaml             _meta: discipline template for data
ref/config-meta-reg.yaml              _meta: discipline template for reg
ref/workflow-plan-sample-cms.yaml     IPO phases for CMS stage
ref/workflow-plan-sample-case.yaml    IPO phases for case stage
ref/workflow-plan-sample-data.yaml    IPO phases for data stage
ref/workflow-plan-sample-reg.yaml     IPO phases for reg stage
```


Workflow plan
-------------

When `/haipipe-task plan` targets an existing task-folder of this type, the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample-<stage>.yaml     <- script-level phases for this stage
../haipipe-task/ref/workflow-template.yaml  <- task-level template (Run/Gate1/Gate2)
```

Schema source of truth:
  B_project/haipipe-workflow/ref/plan-schema.md


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences -- which stage was chosen + what was scaffolded
artifacts: [paths created]
next:      author dispatcher .do + scripts/ workers (incl. a `describe` step + run_describe_*.ps1 QC run); haipipe-task-reviewer-agent before hand-copy; then runs/<run>.ps1 (or sbatch/)
```
