fn/workflow-plan — audit + fix + generate plans
=================================================

Called by `/haipipe-task plan`. Runs the full pre-plan sequence:
audit the task folder, fix fixable issues, then generate plans
at two levels: per-script and task-level. Both levels MUST follow
the haipipe-workflow IPO schema.

Schema source of truth:
  ../../B_project/haipipe-workflow/ref/plan-schema.md
  ../../B_project/haipipe-workflow/ref/concepts.md

Generic template (fill in the blanks):
  ../ref/workflow-template.yaml

Type-specific sample (if the specialist has one):
  ../haipipe-task-for-<type>/ref/workflow-plan-sample.yaml


Two-layer plan structure
-------------------------

```
┌────────┬──────────────────────────────────┬────────────────────────────────────┐
│ Layer  │ File                             │ Answers                            │
├────────┼──────────────────────────────────┼────────────────────────────────────┤
│ Task   │ workflow/plan.yaml               │ "What does this task folder do?"   │
│        │                                  │ Full IPO: gates + run + report     │
├────────┼──────────────────────────────────┼────────────────────────────────────┤
│ Script │ workflow/plan-script-<name>.yaml │ "What does this one script do?"    │
│        │                                  │ Full IPO: internal phases/steps    │
└────────┴──────────────────────────────────┴────────────────────────────────────┘
```

Both layers use the SAME schema shape from plan-schema.md:
  Header (name, purpose, skill)
  I: Input (args, files_in)
  P: Phases → Steps (label, type, required, prompt, files_in, files_out)
  O: Output (returns, files_out)

The config layer (configs/<run>.yaml) is an input FILE, not a separate
plan layer. It appears in `input.files_in`.


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
3. Group cells into Phases by logical boundary
4. Within each Phase, each cell becomes a Step
5. Map _WorkSpace references to files_in/files_out

**The per-script plan MUST follow plan-schema.md.** Every step uses
the canonical fields:

  label      "phase:step-name"  (e.g. "train:fit-xgboost")
  type       agent              (always agent for script-internal steps)
  required   true | false
  prompt     what this step computes (one line)
  files_in   files this step reads ([] if none)
  files_out  files this step creates ([] if none)

Do NOT use ad-hoc fields like `id`, `name`, `cell`, `reads`, `does`,
`outputs`. Those are not in the schema.

**Per-script plan format (follows plan-schema.md):**

```yaml
# ─── Header ──────────────────────────────────────────────────────
name: <script-name-kebab>
purpose: "<one-line: what this script does>"
skill: haipipe-task-for-<type>

# ─── I: Input ────────────────────────────────────────────────────
input:
  args:
    config: configs/<run_name>.yaml
    run_trigger: runs/<run_name>.sh
  files_in:
    - <script_name>.py
    - configs/<run_name>.yaml
    - _WorkSpace/...                     # upstream data dependencies

# ─── P: Phases ───────────────────────────────────────────────────
phases:

  - title: <Phase title>
    detail: "<one-line what this phase does>"
    steps:
      - label: "<phase>:<step-name>"
        type: agent
        required: true
        prompt: "<what this step computes>"
        files_in:
          - _WorkSpace/...               # or [] if reads only in-memory
        files_out: []                    # or [results/<run>/<file>]

      - label: "<phase>:<step-name>"
        type: agent
        required: true
        prompt: "<what this step computes>"
        files_in: []
        files_out:
          - results/<run>/<file>

  - title: <Next phase>
    detail: "..."
    steps:
      - label: "..."
        # ...

# ─── O: Output ───────────────────────────────────────────────────
output:
  returns:
    status: ok
    # task-specific return fields
  files_out:
    - results/<run>/<file1>
    - results/<run>/<file2>
```

Write one `workflow/plan-script-<name>.yaml` per script.

Progress:
```
📍 Script plan: workflow/plan-script-<name>.yaml
   phases: N, steps: M, files_in: X, files_out: Y
```

### Step 6 — Generate task-level plan.yaml

The task plan is ALSO a plan-schema.md-compliant IPO. Its phases
are the high-level lifecycle steps (Run, Gate1, Gate2), not the
script-internal phases (those live in the script plan).

**Task plan format (follows plan-schema.md):**

```yaml
# ─── Header ──────────────────────────────────────────────────────
name: <task-name-kebab>
purpose: "<one line: the research question or deliverable>"
skill: haipipe-task-for-<type>
task_folder: <path relative to project root>

# ─── I: Input ────────────────────────────────────────────────────
input:
  args:
    config: configs/<run_name>.yaml
    probe_ref: <if applicable>
  files_in:
    - <script>.py
    - configs/<run_name>.yaml
    - _WorkSpace/...                     # union of all script inputs

# ─── P: Phases ───────────────────────────────────────────────────
phases:

  - title: Run
    detail: "execute <script>.py via papermill"
    steps:
      - label: "run:<script-name>"
        type: agent
        required: true
        prompt: "<what the script does end-to-end>"
        files_in:
          - <script>.py
          - configs/<run_name>.yaml
          - _WorkSpace/...
        files_out:
          - results/<run>/<file1>
          - results/<run>/<file2>
          - notebooks/<run>.ipynb

  - title: Gate1
    detail: "pre-run code quality review"
    steps:
      - label: "gate1:code-review"
        type: agent
        required: true
        agentType: haipipe-task-reviewer-agent
        prompt: "gate 1: review <script>.py for intent-vs-implementation bugs"
        files_in:
          - <script>.py
          - configs/<run_name>.yaml
        files_out:
          - CODE_REVIEW.md
        schema:
          name: VERDICT
          type: object
          required: [verdict]
          properties:
            verdict: { type: string, enum: [pass, warn, fail] }
            issues: { type: array, items: { type: string } }

  - title: Gate2
    detail: "post-run result audit"
    steps:
      - label: "gate2:result-audit"
        type: agent
        required: true
        agentType: haipipe-task-reviewer-agent
        prompt: "gate 2: audit results of <run_name>"
        files_in:
          - results/<run>/*
          - workflow/plan-script-<name>.yaml
        files_out:
          - RUN_AUDIT.md
        schema:
          name: VERDICT
          type: object
          required: [verdict]
          properties:
            verdict: { type: string, enum: [pass, warn, fail] }
            findings: { type: array, items: { type: string } }

# ─── O: Output ───────────────────────────────────────────────────
output:
  returns:
    status: ok
    gate1_verdict: <pass | warn | fail>
    gate2_verdict: <pass | warn | fail>
    headline: "<one-line result summary>"
  files_out:
    - results/<run>/<file1>
    - results/<run>/<file2>
    - notebooks/<run>.ipynb
    - CODE_REVIEW.md
    - RUN_AUDIT.md
```

### Step 7 — Progress report

```
📍 Plan: <task-name>
   task plan: workflow/plan.yaml (N phases, M steps)
   script plans:
     workflow/plan-script-<name>.yaml (X phases, Y steps)
   fixed: Z per-run configs
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
