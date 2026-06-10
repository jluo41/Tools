---
name: haipipe-task-for-stata-reg
description: "Stata-dialect reg-pipeline task-folder build specialist. Scaffolds D{NN}_reg_<condition>_<pairing>/ task-folders that estimate trait->outcome models (OLS / IV / DID) over a window x estimator-family grid, writing LIGHT coefficient tables (.tex/.csv) into results/. Called by /haipipe-task orchestrator when task-type=stata-reg. Direct invocation works for scoped scaffolding. Shares the Stata engine in ../haipipe-task-for-stata/ref/stata-dialect.md."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.2.0"
  last_updated: "2026-06-09"
  summary: "Stata reg-pipeline task-folder builder."
  changelog:
    - "1.0.0 (2026-05-31): baseline."
    - "1.1.0 (2026-06-08): add metadata; workflow lifecycle compatible."
    - "1.2.0 (2026-06-09): unwrap prose; fix agent names to haipipe-task-{creator,reviewer}-agent; add lifecycle paragraph."
---

Skill: haipipe-task-for-stata-reg
=================================

Scaffolds a **reg-pipeline task-folder** (Stata dialect) — runs the estimation grid on the analysis table from the data stage: OLS (progressive / LPM-logit / two-part / windows / trait-form), IV (main / grid / over-id), and DID (staggered TWFE / Callaway-Sant'Anna). This is the **findings** stage.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Stage 2: Build, then authors the worker `.do` files). Always end with the structured return block (status / task_folder / run_name / files).

Output asymmetry: unlike cms/case/data, the reg stage's PRIMARY output is **LIGHT** — coefficient tables (`.tex`/`.csv`/`.txt`) that belong in-repo under `results/<run>/`, NOT in `_WorkSpace/`. Re-runs are cheap and you WANT many (one per run cell), so the grid fans out wide.

Engine: **Stata + PowerShell + logs**. Read `../haipipe-task-for-stata/ref/stata-dialect.md` first. This skill scaffolds the task-folder; worker `.do` logic is authored separately.


Position in the Stata sub-family
--------------------------------

```
/haipipe-task-for-stata-cms         1-CMS-Store, per year
/haipipe-task-for-stata-case        2-Case-Store, cohort x year
/haipipe-task-for-stata-data        *-Data-Store, cross-year analysis table
/haipipe-task-for-stata-reg     <-- you are here   (coef tables -> results/, LIGHT)
```


Three-sisters pattern (RUNNAME spine)
-------------------------------------

Reg follows the same **haipipe-task** convention as all other task types, adapted for Stata (no notebooks). Each RUNNAME appears in three sisters:

```
configs/<RUNNAME>.yaml     frozen config with _meta: block
runs/<RUNNAME>.ps1         thin PS1 launcher (sets env vars, calls workers)
results/<RUNNAME>/         per-run output (log/ + tables/)
```

Workers in `scripts/` are SHARED across runs — they are estimation code, not runs themselves. A run calls a subset of workers.


What this scaffolds (topic-split layout)
----------------------------------------

When one condition per folder (recommended), the condition and pairing are encoded in the folder name. The grid axes WITHIN the folder are **window x estimator-family**:

```
tasks/{G}{NN}_<group>/
  D{NN}_reg_<condition>_<pairing>/
  +-- configs/
  |   +-- <Cohort>.do                            shared Stata globals (data path)
  +-- scripts/                                    worker .do files (SHARED)
  |   +-- run-{N}-*-<family>-<variant>.do         numbered 1-10, all estimators
  +-- runs/
  |   +-- run_reg_<window>_<family>.ps1            thin launcher (one per RUNNAME)
  +-- sbatch/
  |   +-- run-all.ps1                              fan-out all runs
  +-- results/
  |   +-- run_reg_<window>_<family>/               per-run output folder
  |       +-- log/                                 Stata logs (.txt)
  |       +-- tables/                              coef tables (.tex/.csv)
  +-- diagram/
```

**Stata dialect config convention:** Reg uses `.do` for configs (not `.yaml`). Stata cannot parse YAML. The shared `configs/<Cohort>.do` sets data globals; per-run parameters pass via env vars in the `.ps1` runner. The `.ps1` header comment carries the run purpose.

- **RUNNAME grammar (topic-split):** `run_reg_<window>_<family>`
  where window = {af14d, af7d, ...} and family = {ols, iv, did, ols_windows}.
- **Worker numbering:** run-1..5 = OLS family, run-6..8 = IV family,
  run-9..10 = DID family.
- **Estimators:** OLS progressive / LPM-logit / two-part / windows /
  trait-form; IV main / grid / over-id; DID staggered TWFE /
  Callaway-Sant'Anna.
- **Inputs:** the data stage's `ANALYSIS-*.dta` + IV definitions.
- **Output (LIGHT, in-repo):** coefficient tables `.tex`/`.csv` + logs
  under `results/<RUNNAME>/`.
- **Headline:** key coef / SE / N (and first-stage F for IV).


Env vars crossing the `clear all` boundary
-------------------------------------------

Workers start with `clear all` which wipes all Stata globals. Data must pass through **environment variables** set by the `.ps1` runner:

```
HAIPIPE_WS_ROOT      absolute _WorkSpace path (for data input)
HAIPIPE_REG_WINDOW   outcome BFAF window (af14d, af7d, ...)
HAIPIPE_RES_DIR      absolute per-run results dir (for log + table output)
```

Each worker reads these after `clear all`:
```stata
if "${data_file}" == "" {
    global ws_root : environment HAIPIPE_WS_ROOT
    if "${ws_root}" == "" global ws_root "_WorkSpace"
    do "configs/<Cohort>.do"
}
global res_dir : environment HAIPIPE_RES_DIR
if "${res_dir}" == "" global res_dir "results/${outcome_bfaf_window}"
```


Commands
--------

```
/haipipe-task-for-stata-reg                          ASK project / group / name / grid
/haipipe-task-for-stata-reg <project> <group> <name>  scaffold direct
```


Scaffold flow
-------------

See `fn/scaffold.md`. Summary: identify project+group -> collect `_meta` + the window x estimator-family grid -> create skeleton (flat scripts/, runs/, configs/) -> seed per-run `<RUNNAME>.yaml` from `ref/config-seed.yaml` -> create per-run `<RUNNAME>.ps1` -> emit return contract.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded
artifacts: [paths created]
next:      author the worker .do files; run haipipe-task-reviewer-agent before hand-copy
```


Workflow plan
--------------

When `/haipipe-task plan` targets an existing task-folder of this type, the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     <- script-level phases for this type
../haipipe-task/ref/workflow-template.yaml  <- task-level template (Run/Gate1/Gate2)
```

Schema source of truth:
  B_project/haipipe-workflow/ref/plan-schema.md
