fn/workflow-plan — audit + fix + generate plans
=================================================

Called by `/haipipe-task plan`. Runs the full pre-plan sequence:
audit the task folder, fix fixable issues, then generate plans
at two levels: per-script (detailed I/P[S]/O) and task-level
(roll-up).


Three-layer plan structure
---------------------------

```
┌────────┬──────────────────────────────────┬────────────────────────────────────┐
│ Layer  │ File                             │ Answers                            │
├────────┼──────────────────────────────────┼────────────────────────────────────┤
│ Task   │ workflow/plan.yaml               │ "What does this task folder do?"   │
│        │                                  │ Roll-up of all scripts + phases    │
├────────┼──────────────────────────────────┼────────────────────────────────────┤
│ Script │ workflow/plan-script-<name>.yaml │ "What does this one script do?"    │
│        │                                  │ Detailed I/P[S]/O + run trigger    │
├────────┼──────────────────────────────────┼────────────────────────────────────┤
│ Run    │ configs/<run>.yaml               │ "What config for this execution?"  │
│        │ results/<run>/config_snapshot    │ Frozen params + _meta              │
└────────┴──────────────────────────────────┴────────────────────────────────────┘
```

The script plan is the key new layer. Each `.py` (or `.do`) gets its own
plan file that maps the script's internal steps — what it reads, what each
cell/section does, what it produces. Self-contained and independently useful.

The task plan references the script plans and adds the big picture (phases,
ordering, _WorkSpace I/O summary).


When to call
------------

```
/haipipe-task plan <task-folder-path>
```


Procedure
---------

### Step 1 — Run audit first

Execute `fn/workflow-audit.md` on the task folder (the full 6-step
procedure). Collect: type, run_names, sisters, shared_configs, issues.

Report the audit results to the user (the audit progress block).

### Step 2 — Fix: generate per-run configs

When audit found `shared_configs` (one config serving multiple runs),
generate a per-run config for each run that's missing one.

Each per-run config:
1. Inherits all params from the shared config
2. Adds `_meta:` block specific to this run (read the script to fill
   accurate purpose/input/output)
3. The shared config is kept as reference

Progress:
```
🔧 Fix: created N per-run configs from shared <name>.yaml
```

### Step 3 — Fix: generate missing run script counterparts

If a run has `.sh` but no `.ps1` (or vice versa), generate the
missing counterpart.

### Step 4 — Fix: notebook naming

Flag mismatches but do NOT rename existing notebooks.

### Step 5 — Generate per-script plans

For EACH main `.py` (or `.do`) script in the task folder, generate
a `workflow/plan-script-<name>.yaml`.

**How to read a script's internal structure:**
1. Read the full script file
2. Identify cells/sections (marked by `# %%` for papermill .py,
   or section comments for .do)
3. Group cells into Phases by logical boundary:
   - Setup phase: config loading, path resolution, imports
   - Data-specific phases: each distinct analysis chunk
   - Summary/output phase: final tables, wrap-up
4. Within each Phase, each cell becomes a Step:
   - What data it loads (reads)
   - What transformation it applies (does)
   - What it produces (outputs: files, figures, variables)
5. Map _WorkSpace references to roles

The IPO pattern is the SAME at script level as at task level:
  I → P1[S1,S2] → P2[S3,S4] → P3[...] → O

**Per-script plan format:**

```yaml
# --- Preview -----------------------------------------------------------
# <script_name>.py — <one-line purpose>
#
# I: <input files, one per line with role>
#
# +-- P1: <Phase title>
# |   +-- S1: <step name>
# |   +-- S2: <step name>           -> <output>
# |
# +-- P2: <Phase title>
# |   +-- S3: <step name>
# |   |       -> <output>
# |   +-- S4: <step name>
# |           -> <output>
# |
# +-- P3: ...
#
# O: <output files>
# -------------------------------------------------------------------

script: <script_name>.py
config: configs/<run_name>.yaml
run_trigger: runs/<run_name>.sh

inputs:
  - path: _WorkSpace/...
    role: "<what this file is>"
  - path: _WorkSpace/...
    role: "..."

steps:
  - id: S1
    name: "<step name>"
    cell: "<cell marker or line range>"
    reads: [<files or variables from prior steps>]
    does: "<one line: what this step computes>"
    outputs: []                         # empty if no file produced
  - id: S2
    name: "<step name>"
    reads: [<files>]
    does: "<what>"
    outputs: [trait_dictionary.csv]      # relative to results/<run>/
  # ... one entry per logical step

outputs:
  - path: results/<run>/<file>
    role: "<what this output is>"
    from_step: S2
  - path: results/<run>/figures/<file>.png
    role: "<what this figure shows>"
    from_step: S5
```

Write one `workflow/plan-script-<name>.yaml` per script.

Progress:
```
📍 Script plan: workflow/plan-script-explore_physician.yaml
   steps: 10, inputs: 5 _WorkSpace files, outputs: 9 result files
```

### Step 6 — Generate task-level plan.yaml

The task plan rolls up the script plans:

```yaml
# --- Preview (roll-up tree) --- ...

name: <task-name>
purpose: "<one line>"
skill: <detected type skill>
task_folder: <path>

input:
  files_in: [union of all script inputs]

scripts:
  - plan: workflow/plan-script-<name1>.yaml
    phase: P1
    run_trigger: runs/<run1>.sh
  - plan: workflow/plan-script-<name2>.yaml
    phase: P1
    run_trigger: runs/<run2>.sh

phases:
  - title: <Phase>
    scripts: [<name1>, <name2>]
    ordering: <sequential | parallel | independent>

output:
  files_out: [union of all script outputs]
```

The task plan does NOT duplicate the script-level steps — it references
the script plans. To see internal steps, read the script plan.

### Step 7 — Progress report

```
📍 Plan: B01_explore_physician
   task plan: workflow/plan.yaml (1 phase, 2 scripts)
   script plans:
     workflow/plan-script-explore_physician.yaml (10 steps)
     workflow/plan-script-show_final_physician.yaml (3 steps)
   fixed: 2 per-run configs
```


Return contract
---------------

```yaml
status: ok | blocked
plan_path: workflow/plan.yaml
script_plans: [workflow/plan-script-*.yaml]
type: <detected>
phases: N
scripts: M
configs_generated: [list]
issues_fixed: [list]
issues_remaining: [list]
```
