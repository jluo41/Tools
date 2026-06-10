fn/workflow-report — generate reports mirroring plans
======================================================

Called by `/haipipe-task report`. Generates reports at two levels:
per-script and task-level. Each report mirrors its corresponding
plan — same phases, same steps — filled with what actually happened.

Schema source of truth:
  ../../B_project/haipipe-workflow/ref/plan-schema.md  (Report schema section)
  ../../B_project/haipipe-workflow/ref/concepts.md     (Report = plan's echo)

The report uses the SAME structure as the plan, adding per-step
result fields: status, output, note, reason.


Two-layer report structure
---------------------------

```
          PLAN (before)              REPORT (after)
task      plan.yaml                  report.yaml
script    plan-script-<name>.yaml    report-script-<name>.yaml
```

Each layer mirrors the one it reports on. Plan = intent. Report = evidence.
Same phases, same steps. You can diff them to find divergences.


When to call
------------

```
/haipipe-task report <task-folder-path>
```


Procedure
---------

### Step 1 — Read plans

Load `workflow/plan.yaml` and all `workflow/plan-script-*.yaml` files.
These are the contracts we report against.

### Step 2 — Scan execution evidence per script

For each `plan-script-<name>.yaml`, gather evidence:

| Source | What it gives |
|--------|--------------|
| `results/<run>/manifest.json` | finished timestamp, paths |
| `results/<run>/log/*.txt` | step-level stdout, errors |
| `notebooks/<run>.ipynb` | cell outputs (row counts, print statements) |
| `results/<run>/*.csv` | actual file sizes, row counts |
| `results/<run>/figures/*.png` | figure file sizes |
| `results/<run>/config_snapshot.yaml` | config used |

### Step 3 — Generate per-script reports

For EACH `plan-script-<name>.yaml`, generate a matching
`report-script-<name>.yaml`.

**The report MUST mirror the plan structure per plan-schema.md
Report schema.** For each step in the plan, fill in:

  label      same as plan (unchanged)
  status     done | skipped | failed
  files_in   files actually read (from plan, with status annotation)
  files_out  files actually created (check existence, add size/rows)
  output     structured result from the step (if any)
  note       free-text observation (optional)
  reason     why skipped (required if status=skipped)

Do NOT use ad-hoc fields like `id`, `name`, `outputs`, `exists`,
`rows`, `size_kb`. Those are not in the schema. File existence and
size go in `note` or `output`.

**Per-script report format (follows plan-schema.md Report schema):**

```yaml
# ─── Header ──────────────────────────────────────────────────────
name: <same as plan>
plan: workflow/plan-script-<name>.yaml
executed_at: "<timestamp>"

# ─── Per-Phase, Per-Step results ─────────────────────────────────
phases:

  - title: <Phase title>
    steps:
      - label: "<phase>:<step-name>"
        status: done
        files_in:
          - _WorkSpace/...
        files_out: []
        note: "train=62,112 test=24,845"

      - label: "<phase>:<step-name>"
        status: done
        files_in: []
        files_out:
          - results/<run>/<file>
        output: { key: value }

      - label: "<phase>:<step-name>"
        status: skipped
        reason: "optional step — no test data available"
        files_in: []
        files_out: []

  - title: <Next phase>
    steps:
      - label: "..."
        # ...

# ─── Overall ─────────────────────────────────────────────────────
summary:
  status: ok | incomplete | failed
  phases_completed: "N/N"
  steps_done: X
  steps_skipped: Y
  steps_failed: 0
  files_created:
    - results/<run>/<file1>
    - results/<run>/<file2>
  verdict: <pass | warn | fail | inconclusive>
  issues: []
```

### Step 4 — Generate task-level report.yaml

The task report mirrors `workflow/plan.yaml` — same phases (Run,
Gate1, Gate2), same steps, filled with results.

**Task report format (follows plan-schema.md Report schema):**

```yaml
# ─── Header ──────────────────────────────────────────────────────
name: <same as plan>
plan: workflow/plan.yaml
executed_at: "<timestamp>"

# ─── Per-Phase, Per-Step results ─────────────────────────────────
phases:

  - title: Run
    steps:
      - label: "run:<script-name>"
        status: done
        files_in:
          - <script>.py
          - configs/<run_name>.yaml
          - _WorkSpace/...
        files_out:
          - results/<run>/<file1>
          - results/<run>/<file2>
        note: "238s, N test rows"

  - title: Gate1
    steps:
      - label: "gate1:code-review"
        status: done
        files_in:
          - <script>.py
          - configs/<run_name>.yaml
        files_out:
          - CODE_REVIEW.md
        output: { verdict: warn, issues: ["..."] }
        note: "fixes applied: ..."

  - title: Gate2
    steps:
      - label: "gate2:result-audit"
        status: done
        files_in:
          - results/<run>/*
          - workflow/plan-script-<name>.yaml
        files_out:
          - RUN_AUDIT.md
        output: { verdict: warn, findings: ["..."] }

# ─── Overall ─────────────────────────────────────────────────────
summary:
  status: ok
  phases_completed: "N/N"
  steps_done: X
  steps_skipped: Y
  steps_failed: 0
  files_created:
    - results/<run>/<file1>
    - CODE_REVIEW.md
    - RUN_AUDIT.md
  verdict: <pass | warn | fail>
  issues: []
```

### Step 5 — Progress output

After writing all reports, output the task-level summary:

```
📋 Report: <task-name>
   script reports:
     report-script-<name>.yaml (X/Y steps done)
   task report: report.yaml (N/N phases, M steps)
```


Return contract
---------------

```yaml
status: ok | incomplete | failed
report_path: workflow/report.yaml
script_reports: [workflow/report-script-*.yaml]
phases_completed: "P/P"
steps_done: X
steps_total: Y
verdict: ok
```
