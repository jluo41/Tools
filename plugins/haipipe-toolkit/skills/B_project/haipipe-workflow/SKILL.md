---
name: haipipe-workflow
description: "IPO workflow designer + builder + reporter. The basic orchestration unit of haipipe-toolkit. Every skill (task, probe, insight, narrative) is a specific workflow with its own IPO. This skill defines the shared shape: Input → Phases[Steps] → Output, the lifecycle (Plan → Execute → Report), file tracking per step, and the boundary rule for sub-workflows. Trigger: workflow, plan workflow, design workflow, IPO, phases, build workflow, run workflow, report, /haipipe-workflow."
argument-hint: "[function] [workflow-name-or-path] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow
metadata:
  version: "2.1.0"
  last_updated: "2026-06-08"
  summary: "IPO workflow designer + builder + reporter — the basic orchestration unit."
  changelog:
    - "1.0.0 (2026-06-08): initial skill — plan/build/run/inspect/template."
    - "2.0.0 (2026-06-08): add lifecycle (Plan/Execute/Report), file tracking, template vs specific, sub-workflow boundary rule."
    - "2.1.0 (2026-06-08): restore 4-step lifecycle (Plan/Build/Execute/Report); build generates .workflow.js from plan."
---

Skill: haipipe-workflow (orchestrator)
======================================

The **basic orchestration unit** of haipipe-toolkit.

Every haipipe skill (task, probe, insight, narrative) IS a workflow —
a specific one with its own domain phases and steps. This skill defines
the shared shape they all follow.

```
     ┌─────────┐     ┌───────────────────────────────────┐     ┌──────────┐
     │  INPUT   │ ──▶ │  PHASES                           │ ──▶ │  OUTPUT  │
     │  (args)  │     │  P1 [S1,S2,..] → P2 [S1,..] → …  │     │ (return) │
     │  (files) │     │  each step: files_in → files_out   │     │ (files)  │
     └─────────┘     └───────────────────────────────────┘     └──────────┘
```


Two things this skill provides
-------------------------------

**1. The shape** (vocabulary + structure)

```
I = Input       args + files the workflow starts with
P = Phase       coarse-grained chunk (NOT "Process" — that's the whole middle)
S = Step        atomic action in a phase (NOT "Stage" — that's the 6-stage pipeline)
O = Output      return value + files the workflow produced
```

Every Step tracks `files_in` (what it reads) and `files_out` (what it creates).

**2. The lifecycle** (how every workflow runs)

```
PLAN  ──▶  BUILD  ──▶  EXECUTE  ──▶  REPORT
```

| Act | What | Output |
|-----|------|--------|
| **Plan** | Design the IPO. Iterate rounds until frozen. | `plan.yaml` |
| **Build** | Generate executable script from frozen plan. | `.workflow.js` |
| **Execute** | Run the script via Workflow engine (or manually). | Raw results per step |
| **Report** | Mirror the plan with what actually happened. | `report.yaml` |

```
plan.yaml ──(build)──▶ .workflow.js ──(execute)──▶ results ──(report)──▶ report.yaml
 (human)                (machine)                  (raw)                  (structured)
```


Template vs Specific
---------------------

This skill defines **templates** — abstract shapes with placeholders.
Each domain skill (task, probe, ...) fills in the blanks to make a
**specific** workflow with concrete files, concrete steps, concrete prompts.

```
TEMPLATE (this skill):                SPECIFIC (e.g. haipipe-task):
  Phase: "Author"                      Phase: "Author"
  Step: "write script"                 Step: "write build_lbp.py"
  files_in: [template]                 files_in: [ref/source_fn_template.py]
  files_out: [<TASK>.py]               files_out: [tasks/A01_.../build_lbp.py]
```


How skills relate to this
--------------------------

```
haipipe-workflow     ← the PATTERN (IPO + lifecycle + file tracking)
    │
    ├── haipipe-task         ← a SPECIFIC workflow (own phases, own steps)
    │     └── haipipe-task-for-data   ← a more specific workflow
    │
    ├── haipipe-probe        ← a SPECIFIC workflow
    │     └── calls haipipe-task as sub-workflow (sees only I/O)
    │
    ├── haipipe-insight      ← a SPECIFIC workflow
    │     └── reads probe outputs
    │
    └── haipipe-narrative    ← a SPECIFIC workflow
          └── calls haipipe-probe as sub-workflow (sees only I/O)
```

Each skill:
- **Owns** its own Phases and Steps (full internal IPO)
- **Declares** only I and O when calling a sub-workflow
- **Hides** its internal Phases from its caller


Commands
--------

```
/haipipe-workflow plan     <name>          design IPO interactively → plan.yaml
/haipipe-workflow build    <plan-path>     generate .workflow.js from frozen plan
/haipipe-workflow execute  <script-path>   run .workflow.js via Workflow engine
/haipipe-workflow report   <plan+results>  generate report.yaml mirroring the plan
/haipipe-workflow inspect  <path>          read + summarize existing workflow's IPO
/haipipe-workflow template                 dump starter plan.yaml template
/haipipe-workflow "<natural language>"     infer, dispatch
```

---


Function: plan
--------------

Design a specific workflow's IPO. Iterate until frozen.

### Round 1 — Name + Purpose + Input
- What is this workflow called?
- What is its purpose (one line)?
- What are the input args (fields, types)?
- What files does it start with (files_in)?

### Round 2 — Phases and Steps
For each Phase:
- **title**: short name (PascalCase)
- **detail**: one-line explanation
- **steps**: for each Step:
  - **label**: concrete display name
  - **type**: `agent` | `skill` | `workflow`
  - **required**: true | false (optional steps)
  - **prompt**: what the agent does (for type=agent)
  - **calls** + **sub_I** + **sub_O**: for type=skill/workflow
  - **files_in**: which files this step reads
  - **files_out**: which files this step creates
  - **schema**: structured output contract (optional)

### Round 3 — Output
- What does the workflow return?
- What is the complete list of files_out (union of all step files_out)?

### Freeze
Write `plan.yaml` to the target directory. The plan is now the contract.

### Dispatch table

| What to read | Ref doc |
|-------------|---------|
| IPO concepts, lifecycle, file tracking | `ref/concepts.md` |
| plan.yaml full schema + examples | `ref/plan-schema.md` |
| Claude Workflow API | `ref/workflow-api.md` |


Function: build
----------------

Generate a `.workflow.js` script from the frozen `plan.yaml`.

1. Read `plan.yaml` — the frozen IPO contract.
2. Read `ref/workflow-api.md` — the Workflow engine API.
3. Read `ref/template.workflow.js` — the starter skeleton.
4. Map plan → script:
   - `meta.name` ← plan name
   - `meta.description` ← plan purpose
   - `meta.phases[]` ← plan phases (title + detail)
   - `args` parsing ← plan input contract
   - Schema constants ← plan step schemas (CAPS_SNAKE_CASE)
   - Per-phase body: `phase('Title')` + `agent()` calls per step
   - Sub-workflow steps → `agent()` with skill prompt + schema
   - Optional steps → `if` guards
   - File tracking → comments or log() calls per step
   - `return` ← plan output contract
5. Write `<target-dir>/<name>.workflow.js`.

The generated `.js` is the machine-executable form of the plan.
The plan is what you read and edit; the `.js` is what the Workflow
engine runs. You should rarely need to edit the `.js` directly.


Function: execute
------------------

Run the `.workflow.js` via the Workflow engine.

1. Resolve path to `.workflow.js` (from build output or explicit path).
2. Confirm with user (Workflow tool requires explicit opt-in).
3. Run: `Workflow({ scriptPath: "<resolved>" }, args)`.
4. Collect raw results per step.

Execution modes (the `.js` is always generated, but execution varies):

```
Mode              How it runs                      When to use
─────────────────────────────────────────────────────────────────
Workflow engine   Workflow({ scriptPath })          full automation, resumable
Subagent          Agent() per step, manual chain    a few steps, want to watch
Manual            human runs each step              CMS server, GPU jobs
```

For manual mode (e.g. edit-local-run-server), the plan.yaml still
serves as the checklist — the human follows the phases/steps and
records results that feed into the report.


Function: report
-----------------

Generate report.yaml mirroring the plan structure.

1. Read plan.yaml (the contract).
2. Read execution results (per step).
3. For each Phase, for each Step, fill in:
   - `status`: done | skipped | failed
   - `files_in`: files actually read
   - `files_out`: files actually created
   - `output`: structured result (if any)
   - `reason`: why skipped (if skipped)
   - `note`: any observations
   - `sub_report_summary`: one-line from sub-workflow (if type=skill)
4. Write summary: phases completed, steps done/skipped/failed, all files created.


Function: inspect
-----------------

Read any existing workflow (plan.yaml, .workflow.js, or SKILL.md) and
produce a human-readable IPO summary:

```
Workflow: build-lbp-data-pipeline
Purpose:  Scaffold SourceFn + RecordFn task for LBP cohort
Skill:    haipipe-task-for-data

INPUT
  args: { type: data, name: run_lbp, group: A01_pretraining }
  files_in: [ref/source_fn_template.py, ref/record_fn_template.py]

PHASES
  P1 Load      steps=1  files: 2 in, 0 out
  P2 Author    steps=3  files: 1 in → build_lbp.py, config, run script
  P3 Validate  steps=2  files: build_lbp.py → (dry_run.log optional)
  P4 Review    steps=1  files: build_lbp.py + config → CODE_REVIEW.md

OUTPUT
  returns: { status, folder, files_created, verdict }
  files_out: [build_lbp.py, run_lbp.yaml, run_lbp.sh, CODE_REVIEW.md]
```


Function: template
------------------

Dump a starter `plan.yaml` with all fields annotated. Quick start for
designing a new specific workflow.


Routing logic
-------------

```
keyword                → function
────────────────────────────────────
plan, design           → plan
build, generate        → build
execute, run           → execute
report, results        → report
inspect, read, summary → inspect
template, starter      → template
(ambiguous)            → ask
```


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "plan written to <path>" | "executed 4/4 phases" | "report generated"
artifacts: [plan.yaml, report.yaml, ...]
next:      suggested next step
```
