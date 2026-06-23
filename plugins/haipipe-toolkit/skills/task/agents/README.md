task — Agent Roster
=====================

Three agents forming the orchestrator / creator / reviewer triad.
The orchestrator is the dispatch target for cross-layer calls
(probe-orchestrator, or any skill needing task work in clean context).
Creator produces artifacts. Reviewer evaluates artifacts.

```
haipipe-task-orchestrator-agent   🎯 ORCHESTRATE — dispatch target, coordinates lifecycle
haipipe-task-creator-agent        🤖 CREATE      — produces plan, code, report
haipipe-task-reviewer-agent       🔍 REVIEW      — evaluates plan, code (Gate 1), results (Gate 2)
```

Orchestrator dispatches creator + reviewer in loops. Creator never
reviews. Reviewer never creates. They loop until reviewer says pass.


The 4-stage lifecycle
---------------------

```
Stage 1: PLAN      creator drafts plan.yaml        → reviewer checks plan     → loop if revise
Stage 2: BUILD     creator writes/fixes code+config → reviewer checks code     → loop if revise
Stage 3: EXECUTE   (run, not creator)               → reviewer checks results  → loop if fail
Stage 4: REPORT    creator drafts report.yaml       → reviewer checks report   → loop if revise
```


Cross-layer dispatch
--------------------

```
probe-orchestrator ──▶ task-orchestrator
                         │
                         ├── task-creator
                         └── task-reviewer
```

The task-orchestrator is dispatched during probe Gather when a probe
needs task work (run a script, create a new analysis). It coordinates
the full Plan → Build → Execute → Report cycle, or just Execute if
the task already exists.


Agent details
--------------

| Agent | Stages | What it does |
|-------|--------|-------------|
| `haipipe-task-orchestrator-agent` | all | Dispatch target. Routes to creator/reviewer per stage. |
| `haipipe-task-creator-agent` | 1, 2, 4 | Plan: drafts IPO plan. Build: writes/fixes code. Report: drafts report. |
| `haipipe-task-reviewer-agent` | 1, 2, 4 | Plan: checks IPO. Build: Gate 1 code review. Report: accuracy + Gate 2 result audit. |


Shared across task
---------------------

These agents are used by `haipipe-task` (single task lifecycle) and by
all type specialists (`haipipe-task-for-*`) that invoke them during
their scaffold flow. They live at `task/agents/` (shared), not inside
any single skill.
