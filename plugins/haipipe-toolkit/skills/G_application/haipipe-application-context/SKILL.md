---
name: haipipe-application-context
description: "Per-phase context loader of the haipipe-application family. Given a phase (D/I/K/W) and a task name within the active plan, gathers the relevant inputs (experiment.yaml, prior O/P/K/W entries, plan section) and emits a structured context envelope for the phase skill to consume. Decides: READY (phase skill can execute), BLOCKED (missing prerequisite), or SKIP (already done). NO code. Used internally by /haipipe-application-ask. Trigger: load context, ready-check, /haipipe-application-context."
argument-hint: "[phase: D|I|K|W] [task_name] [--project <path>]"
allowed-tools: Bash, Read, Grep, Glob, Skill
---

Skill: haipipe-application-context
================================

Pre-flight context loader for a phase task. Reads the active plan, the
relevant prior insights, and the relevant experiment artifacts. Decides
whether the phase task can proceed.

```
READY     → phase skill (e.g. /haipipe-insight-data) can run
BLOCKED   → prerequisite missing (e.g. source experiment not confirmed);
            emit reason and STOP
SKIP      → this task already done (entry exists); orchestrator skips
```


Input
-----

```
<phase>                  D | I | K | W (required)
<task_name>              the task identifier from plan.phases.<phase>[*].task
--project <path>         optional; cwd-inferred otherwise

Files read:
  insights/sessions/plans/plan-v{N}-<slug>.yaml        active plan
  insights/INDEX.md                                    insight base summary
  insights/{D,I,K,W}_*/                                prior entries
  experiments/<NN>_<slug>/experiment.yaml              for D-phase tasks
  experiments/<NN>_<slug>/CLAIMS_FROM_RESULTS.md       (optional)
```


Output
------

A context envelope returned to the caller:

```yaml
verdict:    READY | BLOCKED | SKIP
phase:      D | I | K | W
task_name:  <name>

# Filled when verdict=READY
context:
  plan_section:        <yaml block for this phase's task>
  source_experiment:   <yaml block from experiment.yaml>     # D-phase only
  scope_observations:  [D01, D03, D07]                       # I-phase
  scope_patterns:      [I02, I05]                            # K-phase
  scope_knowledge:     [K03]                                 # W-phase
  prior_entries:       <list of existing entries at this layer>

# Filled when verdict=BLOCKED
blocker:
  reason:    "source experiment 04 result.status != confirmed (status=pending)"
  fix:       "wait for experiment to confirm OR adjust plan"

# Filled when verdict=SKIP
skipped:
  reason:    "D entry already exists for experiment 04 (D05)"
```


Workflow
--------

```
Step 1: Parse args (phase, task_name, --project)

Step 2: Resolve project root + locate active plan
  - newest plan-v{N}-<slug>.yaml under insights/sessions/plans/

Step 3: Lookup task in plan.phases.<phase>
  - missing → BLOCKED ("task not in plan")

Step 4: Per-phase readiness check
  D:
    - Source experiment in plan.experiments_needed.confirmed?
    - experiment.yaml result.status == confirmed?
    - D entry for this (experiment, task_name) already exists? → SKIP
  I:
    - All scoped D entries exist?
    - At least 2 D entries scoped?
    - I entry for this task already exists? → SKIP
  K:
    - At least 1 I entry scoped + cited?
    - K entry for this task already exists? → SKIP (unless plan says UPDATE)
  W:
    - At least 1 K entry scoped?
    - W entry already exists? → SKIP

Step 5: Build context envelope and emit
```


Hard rules
----------

- READ-ONLY. Never writes any insights/ entry.
- Never decides to RUN — that's the phase skill's job. Just reports
  readiness.
- Returns a structured envelope; caller (session orchestrator) routes
  based on verdict.


Risk profile
-------------

Pure read-only. No file writes. No external skill calls. Returns an
envelope to the caller.


Specialist tail
---------------

```
status:    ok
verdict:   READY | BLOCKED | SKIP
context:   { phase, task_name, ... }       # see envelope schema
artifacts: []                              # context-only, no files written
next:      caller (session) invokes the phase skill if READY,
           or surfaces blocker reason if BLOCKED
```
