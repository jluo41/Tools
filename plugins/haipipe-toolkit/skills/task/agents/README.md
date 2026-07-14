task — Agent Roster
=====================

Three agents forming the orchestrator / creator / reviewer triad.
The orchestrator is the dispatch target for any caller that needs task
work done in CLEAN CONTEXT.
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
or ANSWER A QUESTION.

A question arrives as ONE QUESTION IN GENERAL LANGUAGE and nothing else:
no document, no reference to whoever asked, no reason, no external id. The
orchestrator's clean context IS the boundary. It never learns who asked or
why, and it never writes anyone else's vocabulary into `tasks/`.

Inside, it runs the qa gate (`haipipe-task/fn/qa.md`):

```
   ① QA SCAN   already answered?          → return the QA-file PATH        ~0
   ② DIGEST    results/ answer it, no digest? → write QA/<n>-<slug>.md   cheap
   ③ P-B-E-R   neither → run the lifecycle at the shallowest depth that
               answers it, then write the QA file
   🚫 REFUSE   out of scope for the task layer → the caller re-routes
```

The orchestrator may also be SELF-DIRECTED: with no question pending, it
picks a worthwhile direction and explores it (answerability work). Same
gate, same artifact, no caller at all.


Agent details
--------------

| Agent | Stages | What it does |
|-------|--------|-------------|
| `haipipe-task-orchestrator-agent` | all | Clean-context dispatch target. Routes to creator/reviewer per stage; runs the qa gate on a question. |
| `haipipe-task-creator-agent` | 1, 2, 4 | Plan: drafts IPO plan. Build: writes/fixes code. Report: drafts report — and AUTHORS `QA/<n>-<slug>.md` when a digest is due (this layer holds that pen). |
| `haipipe-task-reviewer-agent` | 1, 2, 4 | Plan: checks IPO. Build: Gate 1 code review. Report: accuracy + Gate 2 result audit + the QA-digest lint. |


Shared across task
---------------------

These agents are used by `haipipe-task` (single task lifecycle) and by
all type specialists (`haipipe-task-for-*`) that invoke them during
their scaffold flow. They live at `task/agents/` (shared), not inside
any single skill.
