---
name: haipipe-task-batch
description: "Batch orchestrator for C_task. Fan out MANY task-groups in ONE session: parse N typed specs, dispatch one code-creator-for-<type>-agent per spec (in parallel), flow each through GATE 1 -> run -> GATE 2 independently, collect for human review. Two engines: native parallel Agent calls (a few, in-loop) or the Workflow pipeline (deterministic, resumable batch). Use when the user wants to build/run several tasks at once, fan out arms, or automate multi-task creation. Trigger: build several tasks, run multiple task-groups, fan out, batch scaffold, /haipipe-task-batch."
argument-hint: "[specs-or-path] [--auto-run]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Task, Workflow
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
  summary: "Batch orchestrator for C_task."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-task-batch
=========================

The **fan-out entry** for C_task. Where `haipipe-task-for-<type>` builds ONE
task (interactively or headless), this orchestrates MANY at once and runs each
through the full gate chain. It is a THIN router — it holds no authoring or
review logic; it dispatches to the agents and collects.

The shape it drives (matches "spell out specs -> produce -> I review"):

```
you: spell out N typed specs (front-loaded)
        │  parse -> N specs, each with a `type`
        ▼  FAN-OUT (parallel, one creator per spec)
   code-creator-for-<type>-agent  ×N      (calls its haipipe-task-for-<type> headless, then authors)
        │  each result flows INDEPENDENTLY (pipeline, no barrier):
        ▼
   run-script-reviewer-agent (GATE 1) -> [run] -> run-result-auditor-agent (GATE 2)
        │
        ▼  collect N results -> you review (back-loaded)
```

Reviewers are shared across all specs; creators are chosen per type. Adding a
task type costs nothing here — the chain is type-agnostic except the creator.


The spec
--------

Each task-group is one spec object:

```yaml
- type:    training | data | eval | display | individual | algo | agent
  name:    run_seed42_lhm          # run NAME (run_-prefixed, snake_case)
  group:   A01_pretraining          # task-group target
  purpose: "LHM arm, seed 42"       # REQUIRED (the headless _meta gate)
  params:  { ... }                  # type hyperparams / pipeline config
  note|input|output: ...            # optional
```

A complete spec lets the type skill run SILENT (no ASK). A spec missing
`purpose` comes back `blocked` — fill it and re-dispatch.


Two engines
-----------

```
                       a few, you want to watch        many, deterministic + resumable
                       ──────────────────────────       ───────────────────────────────
ENGINE                 native parallel Agent calls       Workflow pipeline
HOW                    one message, multiple Task uses    Workflow({scriptPath}, args)
INDEPENDENCE           you coordinate                     pipeline() — each spec flows alone
FAILURE                you handle                         failed spec drops to null
RESUME                 no                                 resumeFromRunId
```

### Engine A — native parallel (default for a handful)

For each spec, in ONE assistant message issue parallel Task calls:

```
Task(subagent_type="code-creator-for-<type>-agent", prompt=<spec>)   # ×N concurrent
```

Then per result: `code-creator → run-script-reviewer-agent (GATE 1) → [run] → run-result-auditor-agent (GATE 2)`.
Collect and present.

### Engine B — Workflow pipeline (for real batch)

The deterministic pipeline lives at:

```
ref/batch-pipeline.workflow.js
```

Run it:

```
Workflow({ scriptPath: ".../skills/C_task/haipipe-task-batch/ref/batch-pipeline.workflow.js" },
         args = [ <spec>, <spec>, ... ])          # or { specs: [...], autoRun: true }
```

It fans out one `code-creator-for-<type>-agent` per spec, then flows each
through GATE 1 → run → GATE 2 as an independent pipeline (a fast spec is not
blocked by a slow one). Returns `{ summary: [{name,type,folder,authored,gate1,run,gate2}] }`.

Note: Workflow needs explicit user opt-in — only run it when the user asked
to. If `agentType` does not resolve in a given environment, the script's
prompts are self-contained (each says "act as code-creator-for-<type>-agent"),
so dropping the `agentType` option still works.


The GPU gate (default-safe)
---------------------------

The workflow's `autoRun` defaults to **false**: it stops after GATE 1 and
returns for your approval — it does NOT burn GPU on N runs unattended. Pass
`autoRun: true` (or `--auto-run`) only for well-tested arm templates. A
`gate1: fail` spec is never run regardless.


Relation to the bridge
-----------------------

`D_probe bridge` is the probe-driven sibling: it scaffolds arms FROM a
`probe.yaml` and runs the same GATE 1. This skill is the general,
probe-agnostic batch entry — use it when the N specs come from you directly,
not from a probe. Both ultimately fan out the same creator + reviewer agents.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "batch: 3 specs -> 3 authored, 2 gate1-pass, paused for run approval"
artifacts: [task-folders, CODE_REVIEW.md ×N, (RUN_AUDIT.md ×N if autoRun)]
next:      review GATE 1 results -> re-run with autoRun:true to deploy
```
