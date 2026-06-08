fn/workflow-report — generate report.yaml after execution
==========================================================

Called by `/haipipe-task` after execution completes (or manually to
capture an already-completed run). Reads the plan.yaml + actual
results and generates report.yaml mirroring the plan.


When to call
------------

Automatically after execution. Also callable standalone:

```
/haipipe-task report <task-folder-path>
```


Procedure
---------

### Step 1 — Read the plan

Load `workflow/plan.yaml`. This is the contract we report against.

### Step 2 — Scan execution evidence

For each Step in the plan, check what actually happened:

**From results/<NAME>/:**
- `runtime.yaml` → status, timing, exit_code, git_sha
- `manifest.json` → file listing, checksums
- `summary.txt` → audit notes
- `metrics.json` → measured numbers (if applicable)

**From notebooks/<NAME>.ipynb:**
- Exists? → execution record available
- Cell outputs? → full vs thin notebook

**From _WorkSpace/ files_out:**
- Each expected output file: exists? size? modified date?

### Step 3 — Collect _WorkSpace I/O

Scan all steps and separate _WorkSpace paths into two lists:

**_WorkSpace used (input):** files read from _WorkSpace by any step
  - Include a `role:` one-line description of what each file is
  - Mark `optional: true` for files that may not exist

**_WorkSpace generated (output):** files created in _WorkSpace by any step
  - Include `role:` description
  - Include `rows:` or `count:` when known from metrics/summary

### Step 4 — Record agents & skills used

Track what was invoked during the workflow:

**execution.mode:** `manual` | `subagent` | `workflow-engine`
**execution.agents_used:** list of agent names invoked (e.g. `code-creator-for-data-agent`)
**execution.skills_used:** list of skills invoked (e.g. `haipipe-task`, `haipipe-data-external`)
**execution.lifecycle_agent:** which agent ran the audit → fix → plan → report lifecycle
  - type: subagent | workflow-engine | human
  - skill_invoked: which skill it called
  - fn_procedures: which fn/ docs it followed

Per step, also record `agent:` if an agent was used for that step.

### Step 5 — Write report.yaml

The report.yaml has THREE sections:

**Section 1: Preview (comment block at top)**

A compact tree-style summary readable at a glance. This is what gets
shown to the user in the Claude Code session. Format:

```
# ─── Preview ─────────────────────────────────────────────────────
#
# <task_name> — task execution report
#
# I: <key input files, one per line>
#    _WorkSpace/... (role)
#
# ├── P1: <Phase title>
# │   ├── S1: <step label>                    ✅/❌/⏭️ status
# │   │       run: <run_trigger>
# │   │       → <key files_out, _WorkSpace paths>
# │   │       note: <if any>
# │   ├── S2: ...
# │   └── S3: ...
# │
# └── P2: <Phase title>
#     ├── S1: ...
#     └── S2: ...
#
# O: { status, verdict, phases, steps summary }
#    _WorkSpace used (input):
#      _WorkSpace/... (role)
#    _WorkSpace generated (output):
#      _WorkSpace/... (role)
#    agents: [list or "none"]
#    skills: [list]
```

**Section 2: Structured YAML data**

```yaml
name: <workflow name>
plan: workflow/plan.yaml
executed_at: <timestamp>
reported_at: <date>

execution:
  mode: manual | subagent | workflow-engine
  agents_used: [...]
  skills_used: [...]
  lifecycle_agent:
    type: subagent
    skill_invoked: haipipe-task
    fn_procedures: [fn/workflow-audit.md, fn/workflow-plan.md, fn/workflow-report.md]

workspace:
  used:
    - path: _WorkSpace/...
      role: "description"
      optional: false
  generated:
    - path: _WorkSpace/...
      role: "description"
      rows: 1141176          # when known

phases:
  - title: Phase Name
    steps:
      - label: "S1: step name"
        status: done | skipped | failed
        run_trigger: runs/<NAME>.sh
        agent: <agent-name> | null
        files_in: [...]
        files_out: [...]
        output: { ... }       # from runtime.yaml + metrics.json
        note: "..."           # if any

summary:
  status: ok | incomplete | failed
  phases_completed: "2/2"
  steps_done: 4
  steps_skipped: 1
  steps_failed: 0
  verdict: ok
  issues: []
```

**Section 3: nothing else** — the preview + YAML are the full report.

### Step 6 — Completeness check

Before writing, verify:
- Were all required steps executed?
- Were all expected files_out created?
- Were any steps skipped? Why?
- Are all _WorkSpace generated files accounted for?

### Step 7 — Progress output to user

After writing report.yaml, output the Preview section (the compact tree)
directly to the user in the Claude Code session. This is the IPO summary
they see without opening the file.


Return contract
---------------

```yaml
status: ok | incomplete | failed
report_path: workflow/report.yaml
phases_completed: "2/2"
steps_done: 4
steps_skipped: 1
steps_failed: 0
files_expected: 12
files_created: 12
files_missing: 0
issues: []
```
