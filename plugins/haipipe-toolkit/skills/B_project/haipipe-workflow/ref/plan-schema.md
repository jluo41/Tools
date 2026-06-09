plan.yaml — workflow design document
=====================================

The plan is the human-readable blueprint of a workflow's IPO contract.
`/haipipe-workflow plan` produces it; `/haipipe-workflow build` consumes
it; `/haipipe-workflow report` echoes it with results.

The skill defines **templates** (abstract shapes with placeholders).
A specific workflow instance fills in every field with concrete values.


Plan schema
============

```yaml
# ─── Header ──────────────────────────────────────────────────────
name: build-lbp-data-pipeline           # kebab-case
purpose: "Scaffold a SourceFn + RecordFn task for the LBP cohort"
skill: haipipe-task-for-data             # which skill owns this workflow

# ─── I: Input ────────────────────────────────────────────────────
input:
  args:
    type: data
    name: run_lbp
    group: A01_pretraining
    purpose: "LBP cohort data pipeline"
  files_in:                              # files the workflow starts with
    - ref/source_fn_template.py
    - ref/record_fn_template.py
    - examples/ProjA/tasks/A01_pretraining/   # target task-group

# ─── P: Phases ───────────────────────────────────────────────────
phases:

  - title: Load
    detail: "read templates and task-group structure"
    steps:
      - label: "read template"
        type: agent                      # agent | skill | workflow
        required: true
        prompt: "Read ref/source_fn_template.py and task-group structure"
        files_in:
          - ref/source_fn_template.py
          - ref/record_fn_template.py
        files_out: []                    # no files created, just reads

  - title: Author
    detail: "write scripts and configs"
    steps:
      - label: "write build_lbp.py"
        type: agent
        required: true
        prompt: "Create build_lbp.py with SourceFn + RecordFn"
        files_in:
          - ref/source_fn_template.py    # template to follow
        files_out:
          - tasks/A01_.../build_lbp.py   # script to create
        schema:
          name: AUTHORED
          type: object
          required: [status, file_path]
          properties:
            status: { type: string, enum: [ok, blocked, failed] }
            file_path: { type: string }
            lines: { type: number }

      - label: "fill config"
        type: agent
        required: true
        prompt: "Fill configs/run_lbp.yaml with pipeline parameters"
        files_in:
          - ref/config_template.yaml
        files_out:
          - tasks/A01_.../configs/run_lbp.yaml

      - label: "write run script"
        type: agent
        required: true
        prompt: "Create runs/run_lbp.sh entry point"
        files_in: []
        files_out:
          - tasks/A01_.../runs/run_lbp.sh

  - title: Validate
    detail: "check authored artifacts"
    steps:
      - label: "syntax check"
        type: agent
        required: true
        prompt: "Run syntax check on build_lbp.py"
        files_in:
          - tasks/A01_.../build_lbp.py   # reads Author output
        files_out: []

      - label: "dry-run"
        type: agent
        required: false                  # optional — only if test data exists
        prompt: "Dry-run import check"
        files_in:
          - tasks/A01_.../build_lbp.py
        files_out:
          - tasks/A01_.../results/dry_run.log

  - title: Review
    detail: "QA gate before handoff"
    steps:
      - label: "code review"
        type: agent
        required: true
        prompt: "Review build_lbp.py against spec and template"
        agentType: run-script-reviewer-agent
        files_in:
          - tasks/A01_.../build_lbp.py
          - tasks/A01_.../configs/run_lbp.yaml
          - ref/source_fn_template.py    # compare against template
        files_out:
          - tasks/A01_.../CODE_REVIEW.md
        schema:
          name: VERDICT
          type: object
          required: [verdict]
          properties:
            verdict: { type: string, enum: [pass, warn, fail] }
            issues: { type: array, items: { type: string } }

# ─── O: Output ───────────────────────────────────────────────────
output:
  returns:
    status: ok
    folder: tasks/A01_.../
    files_created:
      - tasks/A01_.../build_lbp.py
      - tasks/A01_.../configs/run_lbp.yaml
      - tasks/A01_.../runs/run_lbp.sh
      - tasks/A01_.../CODE_REVIEW.md
    verdict: pass
  files_out:                             # all files produced (union of step files_out)
    - tasks/A01_.../build_lbp.py
    - tasks/A01_.../configs/run_lbp.yaml
    - tasks/A01_.../runs/run_lbp.sh
    - tasks/A01_.../results/dry_run.log  # only if optional step ran
    - tasks/A01_.../CODE_REVIEW.md
```


Report schema
==============

The Report mirrors the Plan — same phases, same steps — filled with
what actually happened during execution.

```yaml
# ─── Header ──────────────────────────────────────────────────────
name: build-lbp-data-pipeline
plan: ref/plan.yaml                      # which plan this reports on
executed_at: "2026-06-08T14:30:00Z"

# ─── Per-Phase, Per-Step results ─────────────────────────────────
phases:

  - title: Load
    steps:
      - label: "read template"
        status: done                     # done | skipped | failed
        files_in:
          - ref/source_fn_template.py    # ✅ read (42 lines)
          - ref/record_fn_template.py    # ✅ read (38 lines)
        files_out: []

  - title: Author
    steps:
      - label: "write build_lbp.py"
        status: done
        files_in:
          - ref/source_fn_template.py
        files_out:
          - tasks/A01_.../build_lbp.py   # ✅ created (45 lines)
        output: { status: ok, file_path: "tasks/A01_.../build_lbp.py", lines: 45 }

      - label: "fill config"
        status: done
        files_in:
          - ref/config_template.yaml
        files_out:
          - tasks/A01_.../configs/run_lbp.yaml   # ✅ created
        note: "filled 3 fields: source_path, record_path, split_ratio"

      - label: "write run script"
        status: done
        files_in: []
        files_out:
          - tasks/A01_.../runs/run_lbp.sh        # ✅ created

  - title: Validate
    steps:
      - label: "syntax check"
        status: done
        files_in:
          - tasks/A01_.../build_lbp.py
        files_out: []
        output: { clean: true }

      - label: "dry-run"
        status: skipped
        reason: "optional step — no test data available"
        files_in: []
        files_out: []

  - title: Review
    steps:
      - label: "code review"
        status: done
        files_in:
          - tasks/A01_.../build_lbp.py
          - tasks/A01_.../configs/run_lbp.yaml
          - ref/source_fn_template.py
        files_out:
          - tasks/A01_.../CODE_REVIEW.md         # ✅ created
        output: { verdict: pass, issues: [] }

# ─── Overall ─────────────────────────────────────────────────────
summary:
  status: ok
  phases_completed: 4/4
  steps_done: 5
  steps_skipped: 1
  steps_failed: 0
  files_created:
    - tasks/A01_.../build_lbp.py
    - tasks/A01_.../configs/run_lbp.yaml
    - tasks/A01_.../runs/run_lbp.sh
    - tasks/A01_.../CODE_REVIEW.md
  verdict: pass
  issues: []
```


Sub-workflow steps
===================

When a Step calls another skill (type: skill), the plan declares
only sub_I and sub_O. The callee's internal phases are hidden.

```yaml
# In haipipe-probe's plan.yaml
phases:
  - title: Bridge
    steps:
      - label: "scaffold arm-A"
        type: skill                      # calls another skill
        calls: haipipe-task-for-data     # which skill
        required: true
        sub_I:                           # what we give the sub-workflow
          type: data
          name: run_lbp_arm_a
          group: A01_pretraining
          purpose: "LBP arm A — vary learning rate"
        sub_O:                           # what we expect back
          status: { type: string }
          folder: { type: string }
          files_created: { type: array }
        files_in:
          - probes/0608_lr_vs_data/probe.yaml   # arm spec source
        files_out:
          - tasks/A01_.../                       # task folder created by sub-workflow
```

In the Report, the sub-workflow's result surfaces as a summary:

```yaml
      - label: "scaffold arm-A"
        status: done
        sub_report_summary: "task created 3 files (build_lbp_arm_a.py, config, run script), syntax clean"
        files_out:
          - tasks/A01_.../build_lbp_arm_a.py
          - tasks/A01_.../configs/run_lbp_arm_a.yaml
          - tasks/A01_.../runs/run_lbp_arm_a.sh
```


Step fields reference
======================

| Field | Required | Plan | Report | Description |
|-------|----------|------|--------|-------------|
| `label` | yes | yes | yes | Display name for this step |
| `type` | yes | yes | — | `agent` / `skill` / `workflow` |
| `required` | yes | yes | — | `true` = must run, `false` = optional |
| `prompt` | for agent | yes | — | What the agent does |
| `agentType` | no | yes | — | Registered specialist agent |
| `calls` | for skill | yes | — | Which skill to invoke |
| `sub_I` | for skill | yes | — | Input passed to sub-workflow |
| `sub_O` | for skill | yes | — | Expected output schema |
| `schema` | no | yes | — | JSON Schema for agent's structured output |
| `files_in` | yes | yes | yes | Files this step reads |
| `files_out` | yes | yes | yes | Files this step creates/modifies |
| `status` | — | — | yes | `done` / `skipped` / `failed` |
| `reason` | — | — | if skipped | Why this step was skipped |
| `output` | — | — | if done | Structured result from the step |
| `note` | — | — | no | Free-text observation |
| `sub_report_summary` | — | — | if skill | One-line summary from sub-workflow |


Fan modes
==========

| Mode | plan.yaml value | When to use |
|------|-----------------|-------------|
| serial (default) | `fan: serial` | Steps depend on each other |
| parallel | `fan: parallel` | Steps are independent, need all before next phase |
| pipeline | `fan: pipeline` | Multiple items, each flows through steps alone |


Template variables
===================

Inside `prompt` and `label` strings, `{{...}}` refs resolve at
build time (template → specific):

| Ref | Resolves to |
|-----|-------------|
| `{{spec.*}}` | Field from the input args |
| `{{prev.*}}` | Field from the previous step's return value |
| `{{index}}` | Pipeline item index (0-based) |
| `{{phase.title}}` | Current phase title |
