---
date: 2026-06-23
status: open
source: process audit of P.0623a + diagram analysis
scope: haipipe-probe-orchestrator-agent dispatch architecture
---

# Orchestrator expected 16 dispatches, actual 0

The designed architecture for P.0623a (4 evidence items: 1 link, 1 run,
2 build+run) expected 16 sub-agent dispatches across 5 agent types:

```
Expected dispatch tree:
  probe-orchestrator (1 root)
  ├── probe-creator   ×5  (link E1, link E2, link E3, link E4, write evidence.md)
  ├── probe-reviewer  ×2  (gather review, read review)
  ├── task-orchestrator ×3 (E2 run, E3 build+run, E4 build+run)
  │   ├── task-creator  ×2 (E3 write script, E4 write script)
  │   └── task-reviewer ×5 (E2 Gate 2, E3 Gate 1+2, E4 Gate 1+2)
  Total: 16 dispatches, 7 review artifacts expected
```

Actual: 0 dispatches, 0 review artifacts. Single monolithic session.

Missing artifacts:
- 2 × CODE_REVIEW.md (E3 theory_alignment.py, E4 permutation_test.py)
- 3 × RUN_AUDIT.md (E2 theory_fit run, E3 alignment run, E4 permutation run)
- 1 × gather completeness review
- 1 × read review (no-verdict-leaked check)

Root causes:
1. Orchestrator has Write/Edit/Bash tools → CAN do everything itself
2. 16 agent dispatches is slow; writing code directly is fast (path of
   least resistance)
3. Caller prompt was prescriptive (gave script logic) → orchestrator
   treated it as direct instructions, not as specs for task-creator

Fix options (ranked by enforcement strength):
1. STRUCTURAL: remove Write/Edit from orchestrator tool list — it literally
   cannot write code, must dispatch. Orchestrator keeps Read/Grep/Bash(read-only)/Agent.
2. PROCEDURAL: add hard rule to agent definition: "You MUST NOT write Python
   code. If you find yourself writing code, STOP and dispatch task-orchestrator.
   Your job is to coordinate, not to produce."
3. PROMPT-SIDE: caller prompts should say "dispatch task-orchestrator to build
   a script that does X" not "create a script that does X" — the verb matters.
4. POST-HOC: add a process audit step that checks: did any sub-agents get
   dispatched? If not, flag as process violation before accepting results.

Recommendation: apply fix #1 (structural) + #3 (prompt discipline). The
structural fix makes it impossible to bypass; the prompt fix makes the intent
clear. Fix #2 alone is too weak (agents ignore procedural rules under pressure).
Fix #4 catches violations but doesn't prevent them.
