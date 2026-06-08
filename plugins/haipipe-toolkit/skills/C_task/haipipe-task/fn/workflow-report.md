fn/workflow-report — generate reports mirroring plans
======================================================

Called by `/haipipe-task report`. Generates reports at two levels:
per-script (detailed step-by-step results) and task-level (roll-up).
Each report mirrors its corresponding plan — same structure, filled
with what actually happened.


Three-layer report structure
-----------------------------

```
          PLAN (before)              REPORT (after)
task      plan.yaml                  report.yaml
script    plan-script-<name>.yaml    report-script-<name>.yaml
run       configs/<run>.yaml         results/<run>/{manifest,log,outputs}
```

Each layer aggregates the one below. Plan = intent. Report = evidence.
Same tree shape, so you can diff them to find divergences.


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

**How to fill each step's result:**
1. Read the plan step (id, name, outputs)
2. Check if each planned output exists under `results/<run>/`
3. For CSV outputs: count rows (`wc -l` or read first line)
4. For PNG outputs: get file size
5. For display-only steps (no files): mark as done if notebook cell ran
6. Read notebook cell outputs for row counts, print statements

**Per-script report format:**

```yaml
# --- Preview -----------------------------------------------------------
# <script_name>.py — execution report
#
# I: <input file>                   ok (<row count> rows)
#    <input file>                   ok (<detail>)
#
# +-- S1: <step name>                              done
# +-- S2: <step name>                              done
# |       -> <output.csv>                          <N> rows
# +-- S3: <step name>                              done
# |       -> <figure.png>                          <size> KB
# +-- S4: <step name>                              skipped
#
# O: <N> CSVs + <M> PNGs under results/<run>/
#    status: ok   steps: X/Y done   duration: Zs
# -------------------------------------------------------------------

script: <script_name>.py
run_name: <run_name>
plan: workflow/plan-script-<name>.yaml
finished: "<timestamp from manifest.json>"
status: ok | incomplete | failed

inputs:
  - path: _WorkSpace/...
    status: ok
    detail: "<row count> rows"     # if readable
  - path: _WorkSpace/...
    status: ok

steps:
  - id: S1
    name: "<step name>"
    status: done | skipped | failed
  - id: S2
    name: "<step name>"
    status: done
    outputs:
      - path: trait_dictionary.csv
        exists: true
        rows: 10                   # for CSVs
  - id: S3
    name: "<step name>"
    status: done
    outputs:
      - path: figures/01_*.png
        exists: true
        size_kb: 48                # for images

outputs:
  - path: results/<run>/<file>
    exists: true
    rows: 10                       # or size_kb for non-CSV
    from_step: S2
```

### Step 4 — Collect agents & skills used

Track what was invoked during execution:
- `execution.mode`: manual | subagent | workflow-engine
- `execution.agents_used`: list of agents called
- `execution.skills_used`: list of skills called

### Step 5 — Generate task-level report.yaml

Roll up the script reports:

```yaml
# --- Preview -----------------------------------------------------------
# <task_name> — task execution report
#
# I: <key _WorkSpace inputs with status>
#
# +-- P1: <Phase> (<script1>.py)           done  N/N steps
# +-- P2: <Phase> (<script2>.py)           done  M/M steps
# +-- G1: run-script-reviewer              pass | warn | fail
# +-- G2: run-result-auditor               pass | warn | fail
#
# O: status=ok  phases=P/P  steps=X/Y done
#    _WorkSpace used (input): [list with status]
#    _WorkSpace generated (output): [list or "none"]
#    agents: [list or "none"]
#    skills: [list]
# -------------------------------------------------------------------

name: <task-name>
plan: workflow/plan.yaml
reported_at: "<date>"

execution:
  mode: manual | subagent | workflow-engine
  agents_used: [...]
  skills_used: [...]

scripts:
  - report: workflow/report-script-<name1>.yaml
    status: ok
    steps_done: N
    steps_total: N
  - report: workflow/report-script-<name2>.yaml
    status: ok
    steps_done: M
    steps_total: M

workspace:
  used:
    - path: _WorkSpace/...
      role: "..."
      status: ok
  generated:
    - path: _WorkSpace/...
      role: "..."
      # or empty if read-only task

summary:
  status: ok
  phases_completed: "P/P"
  steps_done: X
  steps_skipped: Y
  steps_failed: 0
  verdict: ok
```

### Step 6 — Progress output

After writing all reports, output the task-level preview tree to the
user. This is the IPO summary they see in the session.

```
📋 Report: B01_explore_physician
   script reports:
     report-script-explore_physician.yaml (10/10 steps done)
     report-script-show_final_physician.yaml (2/2 steps done)
   task report: report.yaml (2/2 phases, 12/12 steps)
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
