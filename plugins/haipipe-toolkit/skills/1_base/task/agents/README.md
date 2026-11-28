task — Agent Roster
=====================

Three agents forming the orchestrator / creator / reviewer triad.
The orchestrator is the dispatch target for any caller that needs task
work done in CLEAN CONTEXT.
Creator produces artifacts. Reviewer evaluates artifacts.

```
hai-task-orchestrator-agent   🎯 ORCHESTRATE — dispatch target, coordinates lifecycle
hai-task-creator-agent        🤖 CREATE      — produces plan, code, report
hai-task-reviewer-agent       🔍 REVIEW      — evaluates plan, code (Gate 1), results (Gate 2)
```

Orchestrator dispatches creator + reviewer in loops. Creator never
reviews. Reviewer never creates. They loop until reviewer says pass.


The four lifecycle commands
---------------------

```
Command 1: PLAN      creator drafts plan.yaml        → reviewer checks plan     → loop if revise
Command 2: BUILD     creator writes/fixes code+config → reviewer checks code     → loop if revise
Command 3: EXECUTE   (run, not creator)               → reviewer checks results  → loop if fail
Command 4: REPORT    creator drafts report.yaml       → reviewer checks report   → loop if revise
```


Dispatch — and the clean-context rule
--------------------------------------

```
   any caller ──▶ 🧱 ──▶ task-orchestrator   (clean context)
   a task spec,     the        │
   OR one QUESTION  wall       ├── task-creator
   in general                  └── task-reviewer
   language
```

The orchestrator is dispatched whenever a session needs task work done
without polluting its own context — to run a script, build a new analysis,
or resolve a bounded question. A question is answered by reusing an existing
Run/Result or by opening the shallowest new Run and completing the normal
Plan → Build → Execute → Report lifecycle. The orchestrator's clean context
keeps downstream stake out of Task files.

The orchestrator may also be SELF-DIRECTED: with no question pending, it
picks a worthwhile direction and explores it. The artifact is always the
paired Run/Result receipt.


Agent details
--------------

| Agent | Stages | What it does |
|-------|--------|-------------|
| `hai-task-orchestrator-agent` | all | Clean-context dispatch target. Routes to creator/reviewer per stage and returns the Run/Result receipt. |
| `hai-task-creator-agent` | 1, 2, 4 | Plan: drafts Run Specs. Build: writes/fixes code. Report: drafts the report. |
| `hai-task-reviewer-agent` | 1, 2, 3, 4 | Plan: checks Run Specs. Build: Gate 1 code review. Execute: Gate 2 Result audit. Report: accuracy. |


Shared across task
---------------------

These agents are used by `hai-task` (single task lifecycle) and by
all type specialists (`hai-task-for-*`) that invoke them during
their scaffold flow. They live at `1_base/task/agents/` (shared), not inside
any single skill.
