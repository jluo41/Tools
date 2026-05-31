---
name: haipipe-probe-bridge
description: "Bridge specialist of haipipe-probe. Takes a designed probe.yaml (claim + planned arms) and MATERIALIZES it into runnable tasks in C_task. Invokes the Run Script Reviewer agent on each scaffolded task before deploy (centralized intent ↔ implementation review), runs a sanity arm first, then launches the full arm set. The 'design → execution' connector between D_probe and C_task. Called by /haipipe-probe orchestrator. Direct invocation works for bridge-scoped work."
argument-hint: "[bridge|sanity|deploy|status] [probe_ref] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Task
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
---

Skill: haipipe-probe-bridge
=================================

The **design → execution connector**. Where `-design` defines what to
test (claim + arms in `probe.yaml`) and `-result` interprets what
came back, this specialist **makes the probe actually run**: it
scaffolds the arms as tasks in C_task, optionally Codex-reviews the
implementation, runs a sanity arm first, then launches the rest.

This is the migrated `probe-bridge` from research-toolkit
(Workflow 1.5), adapted to read from D_probe's `probe.yaml`
instead of `EXPERIMENT_PLAN.md`, and to call C_task specialists
instead of `/run-probe` directly.


Commands
--------

```
/haipipe-probe bridge <probe>
  Full bridge: read probe.yaml → review code → sanity → deploy all arms.

/haipipe-probe bridge sanity <probe>
  Only run the smallest arm to validate setup. Don't deploy the rest.

/haipipe-probe bridge deploy <probe>
  Skip sanity, deploy all arms (only safe after a passing sanity run).

/haipipe-probe bridge status <probe>
  Show: which arms have been materialized as tasks, which are running,
  which have results linked.
```


Constants
---------

```
CODE_REVIEW    = true   Invoke Run Script Reviewer agent on each scaffolded
                        task before deploy. Centralized intent ↔ impl review
                        used by both C_task pre-flight and this bridge —
                        running it here means launches won't be blocked at
                        run.sh time.
SANITY_FIRST   = true   Run smallest arm first to catch setup bugs.
MAX_PARALLEL   = 4      Parallel arms during deploy.
AUTO_DEPLOY    = false  When true, skip user approval after sanity passes.
```

Override inline:
`/haipipe-probe bridge <probe> — code review: false, max parallel: 2`


Bridge flow (one probe)
----------------------------

```
Step 1: PARSE
  Read probes/<GROUP>_<group_slug>/<NN>_<slug>/probe.yaml
  Extract: claim, arms.<arm>.task_type, arms.<arm>.run_specs,
  priority, compute_budget.
  Identify sanity arm (smallest N / shortest training / lowest cost).

Step 2: SCAFFOLD into C_task
  For each arm run_spec:
    Skill("haipipe-task", args="task-folder <task_type> <arm-task-id>")
    Materialize the task folder under examples/Proj-X/tasks/
    Wire the task's configs/<run>.yaml from the run_spec params.

Step 3: PRE-FLIGHT CODE REVIEW (CODE_REVIEW=true)
  For each scaffolded task-folder from Step 2, invoke the
  **Run Script Reviewer** agent (out-of-family intent ↔ impl audit).
  The agent is a role-doc (not a registered subagent_type) — dispatch
  it by reading its file and handing the body to a Task subagent:

    Read  skills/C_task/agents/reviewers/run-script-reviewer-agent.md
    Task tool (general-purpose subagent), Prompt = that file's body +
            "Pre-flight review for bridge deploy.
             task-folder:   <absolute path>
             probe:        P.A01 / A01 / probes/A_baseline_controls/01_lhm_vs_baseline
             hypothesis:    <quoted from probe.yaml>
             arm:           <arm name>"

  The agent reads <TASK>.py + configs/<RUN>.yaml + imported model
  module(s) + this probe.yaml hypothesis, runs a two-stage review
  (sonnet draft + Codex out-of-family), and writes CODE_REVIEW.md
  sidecar in the task-folder.

  Wait for the agent's verdict:
    pass | skipped → proceed
    warn           → proceed; copy warnings into bridge-log.md
    fail           → STOP. Surface action items. Choose:
                       a) re-scaffold with fixes (back to Step 2), or
                       b) hand back to user.
                     Cap at 2 fix rounds before escalating.
    failed (agent error) → log and fall back to manual review

  This is the SAME agent the C_task `run.sh` pre-flight gate checks for.
  Running it here means launches at deploy time won't be blocked by a
  missing CODE_REVIEW.md.

Step 4: SANITY (SANITY_FIRST=true)
  Deploy ONLY the sanity arm via 2_nn (which calls C_task tasks).
  Wait for completion. Verify:
    - training loop runs without error
    - metrics computed and saved
    - GPU memory within bounds
    - output format matches expectations
  On failure → AUTO-DEBUG (max 3 attempts):
    1. Read error / traceback / log
    2. Classify: OOM / ImportError / FileNotFoundError / CUDA / NaN / etc.
    3. Apply targeted fix, retry
    4. Still failing after 3 → STOP, report all attempted fixes
  Never give up on first failure.

Step 5: HUMAN GATE (AUTO_DEPLOY=false, default)
  Present sanity result + planned deploy.
  Wait for user approval before launching remaining arms.

Step 6: DEPLOY rest of arms
  Up to MAX_PARALLEL in parallel.
  Each arm: 2_nn training → metrics.json → linked back to probe arm.

Step 7: LINK runs to arms
  For each completed arm:
    Skill("haipipe-probe-design", args="link <probe> <run-path>")
  probe.yaml arms.<arm>.runs now points to materialized runs.

Step 8: HANDOFF
  All arms linked → ready for /haipipe-probe result <probe> (aggregate)
  followed by /haipipe-probe review claim <probe> (Codex verdict).
```


Where things live
------------------

```
examples/Proj-X/
├── probes/<GROUP>_<group_slug>/<NN>_<slug>/
│   ├── probe.yaml              ← READ: source of truth (arms + claim)
│   ├── bridge-log.md                ← APPEND: per-arm scaffold/sanity/deploy log
│   └── (no code here — only meta)
│
└── tasks/<arm-task-id>/             ← WRITE: scaffolded by Step 2
    ├── configs/<run>.yaml           ← run_spec params + _meta
    ├── runs/<run>.sh                ← run wrapper
    └── results/<run>/               ← runtime.yaml + metrics.json
```


Disambiguation
---------------

  - No verb (just <probe>) → `bridge` (full flow with defaults).
  - "deploy" + no sanity passed yet → WARN before proceeding.
  - "status" with no in-progress bridge → show "ready to bridge".
  - <probe> doesn't exist → bail; suggest `/haipipe-probe design new <slug> --group A` first.


Risk profile
-------------

WRITES heavily:
- New task folders under `examples/Proj-X/tasks/` (via C_task scaffold)
- `bridge-log.md` per-probe
- Updates `probe.yaml` with linked-run pointers (via `-design link`)
- Triggers GPU training jobs (via 2_nn / C_task execution)
- Invokes the **Run Script Reviewer** agent once per arm during Step 3
  (the agent internally calls Codex MCP — bridge no longer calls Codex
  directly)

GPU cost is the dominant cost. Use sanity-first + human gate for first-time
deploys; switch to `AUTO_DEPLOY=true` only for well-tested arm templates.


Relation to other layers
------------------------

```
D_probe-design       defines arms (in probe.yaml)
        │
        ▼
D_probe-bridge       ← YOU ARE HERE
  ├──► C_task          scaffolds tasks per arm
  └──► 2_nn               runs training
        │
        ▼
D_probe-design link  binds completed runs back to arms
        │
        ▼
D_probe-result       aggregates linked runs into stats + claim
```


Specialist tail
---------------

```
status:    ok | blocked | failed | sanity_passed | deploy_complete
summary:   "P.A01 bridge: 3/3 arms scaffolded, sanity passed, 2/3 arms deployed"
artifacts: [bridge-log.md, scaffolded task IDs, linked run paths]
next:      /haipipe-probe result <probe>     (after all arms complete)
          /haipipe-probe review claim <probe> (Codex verdict on aggregated results)
```
