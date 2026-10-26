---
name: haipipe-task-for-agent
description: "agent Task specialist: scaffolds a tNN_<task>/ Task whose Runs call an LLM agent with prompts + tools -> $OUTPUT_ROOT/<task>/runs/rNN_<run>/result/{transcript.json, summary.md}. Called by /haipipe-task when task-type=agent. Engine: its llm-engine part (_parts/llm-engine/PART.md: Claude/Codex/DeepSeek SDK calls, model routing, CallStore recovery). Trigger: agent task, llm engine, agent sdk, callstore."
argument-hint: "[project_id] [bNN_<block>/jNN_<job>] [tNN_<task>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.3.0"
  last_updated: "2026-10-25"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-agent
==================================

Scaffolds an **LLM-agent job**.
The scaffolded script makes its LLM calls through the domain's engine, this skill's part `_parts/llm-engine/PART.md` (owns `code/haiutils/llm_engine/`).
Inputs: prompts + tool spec + (optional) data context.
Outputs: transcript + structured result under `$OUTPUT_ROOT/<task>/runs/rNN_<run>/result/`.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Phase 2: Build, then authors the `<TASK>.py` body).
Always end with the structured return block (status / summary / artifacts / next — the same tail every task skill emits).


## Type contract

```yaml
task-type: agent
skill: haipipe-task-for-agent
does: Calls an LLM agent with prompts, optional tools and a data context, and records its transcript and a structured result.
worker: scripts/<worker>.py (Python), prompts in scripts/config/prompts/, LLM calls through _parts/llm-engine (code/haiutils/llm_engine/)
config: runs/<run>/config.yaml (seeded from ref/config-seed.yaml), or scripts/config/<run>.yaml in a Block not yet moved
ticket: runs/<run>/<run>.sh, from ../../haipipe-task/ref/run-sh-template.sh
result: $OUTPUT_ROOT/<task>/runs/<run>/result/, with runtime.yaml, transcript.json, summary.md and result.json before the receipt says complete
heavy: none
roles: [trial, make]
companions: [claude-api]
plan_sample: ref/workflow-plan-sample.yaml
```


What this scaffolds
-------------------

```text
work/bNN_<block>/
├── board.md
└── jNN_<job>/
    ├── src/                         shared code + config-defaults.yaml
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── draft/
        ├── workflow/                plan.yaml + report.yaml
        ├── scripts/<worker>.py
        ├── scripts/config/prompts/      system.md + user.md, shared by every Run
        └── runs/rNN_<run>/              one folder per Run
            ├── rNN_<run>.sh             the ticket
            ├── config.yaml              this Run's settings
            ├── run.yaml                 its card (role: trial | make)
            └── result/                  runtime.yaml (the receipt) + the agent's outputs

Generated: $OUTPUT_ROOT/tNN_<task>/runs/rNN_<run>/result/
           $OUTPUT_ROOT/tNN_<task>/notebooks/rNN_<run>.ipynb
A Block not yet moved still has the flat runs/rNN_<run>.sh, scripts/config/rNN_<run>.yaml
and results/rNN_<run>/; the ticket template runs both.
```

Hierarchy prefixes are bNN / jNN / tNN / rNN; domain belongs in the descriptive suffix.
Heavy outputs: none.


Cross-reference to pipeline skill
----------------------------------

Engine: `_parts/llm-engine/PART.md` (LLM call runtime).
Agent infra (Claude API client, tool dispatch, transcript logging) is project-owned for now.
Adjacent skills: `/claude-api`.


Scaffold flow
-------------

See `fn/scaffold.md` for the detailed step-by-step.
Summary:

  1. Identify project + block.
  2. Collect metadata (NN, name, type-specific extras, _meta block).
  3. Create the canonical Task Page, workflow/, scripts/config/prompts/, worker and the Run folder `runs/rNN_<run>/` with its card `run.yaml`; resolve generated output through OUTPUT_ROOT.
  4. Seed `runs/rNN_<run>/config.yaml` from `ref/config-seed.yaml`.
  5. Copy run-script from `../../haipipe-task/ref/run-sh-template.sh` to `runs/rNN_<run>/rNN_<run>.sh`.
  6. Suggest next via cross-skill link.
  7. Emit return contract.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded
artifacts: [paths created]
next:      suggested next command (runs/<run>/<run>.sh / edit scripts/config/prompts/)
```



Workflow plan
--------------

When `/haipipe-task plan` targets an existing job of this type, the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     ← Run Spec example with internal domain steps
../../haipipe-task/ref/workflow-template.yaml  ← authoritative Run Spec template with entry/exit gates
```

Schema source of truth:
  ../../../project/haipipe-run/ref/plan-schema.md

Resolve `RESULT_STORE`, then the Job store declaration, then the Job root as OUTPUT_ROOT.
Use the same output-root contract as `haipipe-task`; no physical output is moved by scaffolding.
