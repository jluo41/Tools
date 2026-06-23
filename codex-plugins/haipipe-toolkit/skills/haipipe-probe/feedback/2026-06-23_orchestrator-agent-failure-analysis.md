---
date: 2026-06-23
status: open
source: P.0623a/b/c monolithic + P.0623f hang
scope: haipipe-probe-orchestrator-agent design
---

# Orchestrator agent failed in TWO different ways on TWO different prompts

The probe-orchestrator-agent was tested twice with different prompt styles.
Both failed, but for DIFFERENT reasons. This reveals the core design tension.

## Failure Mode 1: Monolithic (P.0623a/b/c)

Prompt style: PRESCRIPTIVE ("here is the script logic, create and run it")
Result: orchestrator did everything itself, 0 sub-agent dispatches
Root cause: the prompt gave it enough information to act directly,
  and acting directly is faster than dispatching sub-agents.
  Write/Edit/Bash tools let it bypass the architecture.

## Failure Mode 2: Hang (P.0623f)

Prompt style: DISPATCH-ORIENTED ("you MUST dispatch sub-agents, do NOT
  write code yourself")
Result: orchestrator spent entire runtime deliberating on folder naming
  and task numbering, never dispatched anything.
Root cause: the dispatch instruction was followed (it tried to dispatch
  task-orchestrator-agent), but the 3-level nesting (probe-orch →
  task-orch → task-creator) is too deep. The orchestrator got stuck on
  pre-dispatch planning (where to put the task folder, what number to use)
  — questions that the task-creator would have handled if dispatched.

## The Core Design Tension

```
  prescriptive prompt → agent has enough info to do it itself → monolithic
  dispatch prompt     → agent lacks task-level details → hangs on planning
```

The orchestrator needs to be smart enough to PLAN the dispatch but dumb
enough to not DO the work. This is a narrow target that current LLM agents
hit inconsistently.

## Three Structural Problems

### Problem 1: Tool set is too powerful
The orchestrator has Write/Edit/Bash — same tools as the creator.
Nothing PREVENTS it from doing creator work. It's like giving a manager
the same desk and keyboard as the engineer — they'll just do it themselves.

Fix: remove Write/Edit from orchestrator. It keeps Read/Grep/Bash(read-only)/Agent.
It literally CANNOT write code, must dispatch.

### Problem 2: Nesting depth > 2 doesn't work
probe-orch → task-orch → task-creator is 3 levels of agent dispatch.
At each level, the agent must understand the downstream agent's
interface, compose the right prompt, and wait. By level 3, context
is lost and the chain hangs.

Fix: max 2 levels. Orchestrator dispatches workers directly, never
dispatches another orchestrator. The probe-orchestrator should call
task-creator-agent directly (not task-orchestrator-agent) for simple
single-script jobs.

```
  ❌ probe-orch → task-orch → task-creator   (3 levels, hangs)
  ✅ probe-orch → task-creator               (2 levels, works)
  ✅ main-loop  → probe-orch → task-creator  (2 levels from orch, works)
```

### Problem 3: Pre-dispatch planning is unbounded
The orchestrator tried to figure out the task folder name, task number,
file paths, etc. BEFORE dispatching. These are IMPLEMENTATION details
that the creator agent should decide. The orchestrator should specify
WHAT to build, not WHERE to put it.

Fix: orchestrator prompts should say "build a script that does X" not
"build a script at path Y with number Z." Let the creator handle
file-system decisions.

## Recommended Architecture Change

```
BEFORE (designed but failed):
  probe-orchestrator → task-orchestrator → task-creator
                                         → task-reviewer
                     → probe-creator
                     → probe-reviewer

AFTER (proposed):
  probe-orchestrator → task-creator    (direct, skip task-orch)
                     → task-reviewer   (direct, skip task-orch)
                     → probe-creator   (direct)
                     → probe-reviewer  (direct)

  task-orchestrator is only used when called from MAIN CONTEXT
  (user or skill), not from inside another orchestrator.
```

This means:
- task-orchestrator = dispatch target for skills/users (interactive)
- probe-orchestrator = dispatch target for paper/skills (has Agent tool,
  dispatches workers directly)
- No orchestrator dispatches another orchestrator. Ever.

## Impact on Agent Definitions

1. probe-orchestrator-agent.md: change "dispatch task-orchestrator" to
   "dispatch task-creator + task-reviewer directly"
2. Remove task-orchestrator from probe-orchestrator's dispatch chain
3. Document the 2-level max nesting rule in all orchestrator definitions
4. Remove Write/Edit from orchestrator tool lists (structural enforcement)
