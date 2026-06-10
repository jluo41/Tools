C_task — Agent Roster
=====================

Two agents, separated by role. The split is the whole point:

```
haipipe-task-creator-agent   🔨 CREATE  — produces artifacts (plan, code, report)
haipipe-task-reviewer-agent  🔍 REVIEW  — evaluates artifacts (IPO compliance, code bugs, result accuracy)
```

Creator never reviews. Reviewer never creates. They loop until the reviewer says pass.


The 4-stage lifecycle
---------------------

```
Stage 1: PLAN — the contract
  creator → workflow/plan.yaml + plan-script-<name>.yaml
  reviewer → checks IPO schema compliance
  ↺ warn/revise → creator retries with feedback

Stage 2: BUILD — the implementation
  creator → {NN}_{task}.py + configs/<run>.yaml + runs/<run>.sh
  reviewer → Gate 1 code review → CODE_REVIEW.md
  ↺ warn/revise → creator retries with feedback
  after: human can run directly (bash runs/<run>.sh)

Stage 3: EXECUTE — just run
  no agents — human or autoExecute runs bash runs/<run>.sh
  generates: results/<run>/{metrics.json, runtime.yaml, ...}

Stage 4: REPORT — summarize
  creator → workflow/report.yaml + report-script-<name>.yaml
  reviewer → checks accuracy, creates RUN_AUDIT.md
  ↺ warn/revise → creator retries with feedback
```

The lifecycle workflow (`haipipe-task/ref/task-lifecycle.workflow.js`) orchestrates all 4 stages. It can run a single stage (`stages: ["plan"]`) or all 4.


Agent details
--------------

| Agent | Stages | What it does |
|-------|--------|-------------|
| `haipipe-task-creator-agent` | 1, 2, 4 | Plan: drafts IPO plan. Build: writes/fixes code. Report: drafts report. |
| `haipipe-task-reviewer-agent` | 1, 2, 4 | Plan: checks IPO. Build: Gate 1 code review → CODE_REVIEW.md. Report: accuracy check → RUN_AUDIT.md. |


Shared across C_task
---------------------

These agents are used by `haipipe-task` (single task lifecycle via task-lifecycle.workflow.js) and by all type specialists (`haipipe-task-for-*`) that invoke them during their scaffold flow. That's why they live at `C_task/agents/` (shared), not inside any single skill.


