fn/workflow-plan — generate plan.yaml from task folder state
=============================================================

Called by `/haipipe-task` after audit, when workflow/plan.yaml is
missing or stale. Reads the task folder's current state (scripts,
configs, runs, results) and generates a plan.yaml.


When to call
------------

Automatically after `fn/workflow-audit` reports `workflow_exists: false`
or plan is stale. Also callable standalone:

```
/haipipe-task plan <task-folder-path>
```


Procedure
---------

### Step 1 — Read audit results

From `fn/workflow-audit`, get:
- `type` — detected task type
- `run_names` — all discovered run names
- `sisters` — four-sister status per name
- `shared_configs` — which configs are shared

### Step 2 — Read the type template

Load the workflow template for this task type:

```
type=data     → haipipe-task-for-data/ref/workflow-template.yaml (if exists)
type=stata    → haipipe-task-for-stata/ref/workflow-template.yaml (if exists)
type=external → haipipe-data-external (or fallback to generic)
fallback      → haipipe-task/ref/workflow-template.yaml
```

The template provides the typical Phase structure for this type.

### Step 3 — Infer Phases and Steps from task state

Read the actual task folder and infer the IPO:

**Input (I):**
- Collect all `files_in` from configs/ and scripts/
- Trace upstream dependencies from `_WorkSpace/` references in configs
- Record the config file(s)

**Phases (P) with Steps (S):**
- Each run name becomes a Step (or group of steps)
- Ordering: infer from file dependencies
  - If S2 reads a file that S1 creates → S1 before S2
  - If sbatch/run_build_all.sh exists, read its ordering
- Group steps into Phases by logical boundary
  - Build phase: steps that create data
  - Validate phase: steps that check/audit data

**Per Step, fill in:**
- `label`: from run name (`S1: build ZIP-county xwalk`)
- `type`: agent (most steps) or skill (if calls sub-workflow)
- `required`: true unless clearly optional
- `run_trigger`: matched runs/<NAME>.sh
- `files_in`: read from script imports + config references
- `files_out`: read from script outputs + results/<NAME>/ contents

**Output (O):**
- Union of all step files_out
- Key output files from `_WorkSpace/` (heavy) + results/ (light)

### Step 4 — Generate per-run configs (if shared config detected)

When audit found `shared_configs`, split into per-run configs:

```
FROM: configs/external_physician.yaml (shared)
TO:   configs/run_build_physician.yaml
      configs/run_build_xwalk.yaml
      configs/run_build_cleanse.yaml
```

Each per-run config:
1. Inherits all params from the shared config
2. Adds `_meta:` block specific to this run:
   ```yaml
   _meta:
     purpose: "Build ZIP-county modal crosswalk from Census+NBER sources"
     input: "Census 2020 ZCTA, NBER SSA-FIPS"
     output: "zip_county_xwalk.dta (one row per ZIP5)"
   ```
3. Optionally adds step-specific params (subset of shared config)

The shared config is kept as a reference but is no longer the config
of record for any run.

### Step 5 — Write plan.yaml

Write `workflow/plan.yaml` to the task folder. Use the format from
`skills/flow/haipipe-workflow/ref/plan-schema.md`.

### Step 6 — Progress report

```
📍 plan generated: A01_build_physician/workflow/plan.yaml
   type: external
   phases: 2 (Build, Validate)
   steps: 5 (3 required + 1 required + 1 optional)
   files tracked: 8 in, 12 out
   per-run configs: 3 generated from shared config
```


Return contract
---------------

```yaml
status: ok | blocked
plan_path: workflow/plan.yaml
phases: 2
steps: 5
configs_generated: [run_build_physician.yaml, run_build_xwalk.yaml, run_build_cleanse.yaml]
issues_fixed: [missing_config x3]
issues_remaining: [stale_result: run_build_roberta]
```
