fn/plan-stata — Generate Stata-specific IPO plans
===================================================

Called by `/haipipe-task plan` when the task-folder is Stata-engine.
Generates plan.yaml + plan-script-*.yaml in plan-schema.md format,
using the stage-specific samples in `ref/workflow-plan-sample-<stage>.yaml`.


When to call
------------

Automatically when `/haipipe-task plan` targets an existing Stata task folder.
Also callable standalone: `/haipipe-task-for-stata plan <task-folder-path>`


Procedure
---------

### Step 0 — Read references

Read (in order):
1. `ref/stata-dialect.md` — engine contract
2. `B_project/haipipe-workflow/ref/plan-schema.md` — canonical IPO shape
3. `../haipipe-task/ref/workflow-template.yaml` — task-level template (Run/Gate1/Gate2)

### Step 1 — Detect stage

Infer stage from the task folder content (NOT from group letter):
- Has `scripts/cases/trigger-cases-*.do` → case
- Has `scripts/b-*-All.do` or Step names `pde carrier_claim` → cms
- Has `scripts/1-filter-case/` numbered subdirs → data
- Has `scripts/run-{N}-{family}-*.do` worker pattern → reg
- Has `case_pipeline.do` → case
- Has `data_pipeline.do` → data
- Has no dispatcher but `scripts/run-*.do` → reg

### Step 2 — Discover run matrix

Scan configs/ and runs/ to build the run matrix:

**cms:** `run_cms_<year>` — one per year
**case:** `run_case_<Cohort>_{synth|full}_<year>` — cohort × source × year
**data:** `run_data_<Spec>` — one per spec (cross-year)
**reg:** `run_reg_<window>_<family>` — window × estimator grid

Also discover:
- Shared configs vs per-run configs
- Source selectors (`_source_synth.do`, `_source_full.do`)
- Describe/QC runs (`run_describe_*.ps1`)
- Sbatch batchers (`sbatch/run_all_*.ps1`)

### Step 3 — Generate plan-script-*.yaml (per-script plans)

For EACH main script (dispatcher .do + orchestrator .ps1 + describe .do):

1. Read the script file fully
2. Identify phases from the dispatcher step branches / orchestrator blocks
3. Use `ref/workflow-plan-sample-<stage>.yaml` as the starting template
4. Fill in concrete values (cohort name, paths, file names, topic flags)
5. Write `workflow/plan-script-<name>.yaml`

**IPO format** (every plan-script MUST have this structure):

```yaml
# --- Preview -----------------------------------------------------------
# <script> — <one-line purpose>
#
# I: <inputs, one per line>
#
# +-- emoji P1: <Phase title>
# |   +-- S1: <step>
# |   +-- S2: <step>           -> <output>
# |
# +-- emoji P2: ...
#
# O: <outputs>
# -------------------------------------------------------------------

name: <script-name-kebab>
purpose: "<one line>"
skill: haipipe-task-for-stata

input:
  args: { config: ..., year: ..., source: ... }
  files_in: [...]

phases:
  - title: "<Phase>"
    detail: "<what>"
    steps:
      - label: "<phase>:<step>"
        type: agent
        required: true
        prompt: "<what step does>"
        files_in: [...]
        files_out: [...]

output:
  returns: { status: ok }
  files_out: [...]
```

**Stage-specific phase mappings:**

```
cms:   Setup → Extract (pde/carrier/outpt parallel) → Bene → Summary
case:  Setup → TriggerCases → BENE → PDE → Claims → Lines → Outpt → Summary
data:  Setup → FilterCase → FilterExternal → FullVariables → Describe
reg:   Setup → Estimate (per-family workers) → Collect → Describe
```

### Step 4 — Generate task-level plan.yaml

Roll up all script plans into a task-level plan.yaml:

```yaml
# --- Preview (task-level roll-up) ----------------------------------------
# <task_name> — <purpose>
#
# I: <_WorkSpace inputs>
#
# +-- emoji P1: <main phase>     [<orchestrator>.ps1]
# |   <brief step summary>
# |
# +-- emoji P2: QC               [run_describe_*.ps1]
# |
# O: <_WorkSpace outputs> + results/
# -------------------------------------------------------------------

name: <task-name>
purpose: "<one line>"
type: stata-<stage>
task_folder: <path>

input:
  files_in: [union of all script inputs]

scripts:
  - plan: workflow/plan-script-<name>.yaml
    phase: P1
    run_trigger: runs/<run>.ps1

phases:
  - title: "<Main Phase>"
    emoji: "emoji"
    scripts: [<list>]
    ordering: "<serial|parallel|per-year>"
    runs: { synth: [...], full: [...] }
    status: "<complete|pending>"

  - title: "QC"
    emoji: "📋"
    scripts: [<describe>]

output:
  files_out: [union of all script outputs]
```

**Key Stata differences from generic template:**
- NO `Gate1`/`Gate2` phases in plan.yaml — Stata tasks use `CODE_REVIEW.md`
  and `SERVER_CHECK.md` as pre-flight artifacts, not agent gates in the plan.
  The reviewer agent is called OUTSIDE the plan lifecycle.
- Phases reflect the PIPELINE topology (cases → bene → pde → ...), not the
  generic Run/Gate pattern.
- Per-year × per-source run matrix documented in the `runs:` field.
- _WorkSpace I/O explicitly tracked (heavy input from CMS-Store, heavy output
  to Case-Store, light output to results/).

### Step 5 — Validate

Check each generated plan against plan-schema.md:
- Header has name, purpose, skill
- Input has files_in
- Each phase has title + steps with labels
- Each step has label in `<phase>:<step>` format
- Output has files_out
- Preview tree comment at top matches the phases

### Step 6 — Report

```
📍 Plan: <task_name>
   stage: <detected>
   task plan: workflow/plan.yaml (<N> phases, <M> scripts)
   script plans:
     workflow/plan-script-<name>.yaml (<X> steps)
     ...
```


Return contract
---------------

```yaml
status: ok | blocked
plan_path: workflow/plan.yaml
script_plans: [workflow/plan-script-*.yaml]
stage: <cms|case|data|reg>
phases: N
scripts: M
```
