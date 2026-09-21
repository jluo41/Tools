---
name: haipipe-task-for-agent
description: "agent job specialist: scaffolds {NN}_<name>/ jobs in the agent block (default F-series) that call an LLM agent with prompts + tools -> $OUTPUT_ROOT/<task>/results/rNN_<run>/{transcript.json, summary.md}. Called by /haipipe-task when task-type=agent. Engine: /haipipe-task-llm-engine."
argument-hint: "[project_id] [group] [job-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.3"
  last_updated: "2026-07-04"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-agent
==================================

Scaffolds an **LLM-agent job**.
The scaffolded script makes its LLM calls through the domain's engine, `/haipipe-task-llm-engine` (owns `code/haiutils/llm_engine/`).
Inputs: prompts + tool spec + (optional) data context.
Outputs: transcript + structured result under `$OUTPUT_ROOT/<task>/results/rNN_<run>/`.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Phase 2: Build, then authors the `<TASK>.py` body).
Always end with the structured return block (status / summary / artifacts / next — the same tail every task skill emits).



What this scaffolds
-------------------

```text
tasks/bNN_<block>/
├── board.md
└── jNN_<job>/
    ├── src/                         shared code + config-defaults.yaml
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── outline/
        ├── workflow/                plan.yaml + report.yaml
        ├── scripts/<worker>.py
        ├── scripts/config/rNN_<run>.yaml
        └── runs/rNN_<run>.sh

Generated: $OUTPUT_ROOT/tNN_<task>/results/rNN_<run>/
           $OUTPUT_ROOT/tNN_<task>/notebooks/rNN_<run>.ipynb
Task-local prompts/system.md + prompts/user.md hold agent prompts.
```

Hierarchy prefixes are bNN / jNN / tNN / rNN; domain belongs in the descriptive suffix.
Heavy outputs: none.


Cross-reference to pipeline skill
----------------------------------

Engine: /haipipe-task-llm-engine (LLM call runtime).
Agent infra (Claude API client, tool dispatch, transcript logging) is project-owned for now.
Adjacent skills: `/claude-api`.


Scaffold flow
-------------

See `fn/scaffold.md` for the detailed step-by-step.
Summary:

  1. Identify project + block.
  2. Collect metadata (NN, name, type-specific extras, _meta block).
  3. Create the canonical Task Page, workflow/, scripts/config/, worker and matching rNN Ticket; resolve generated output through OUTPUT_ROOT.
  4. Seed config from `ref/config-seed.yaml`.
  5. Copy run-script from `../../haipipe-task/ref/run-sh-template.sh`.
  6. Suggest next via cross-skill link.
  7. Emit return contract.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded
artifacts: [paths created]
next:      suggested next command (run.sh / edit prompts/)
```



Workflow plan
--------------

When `/haipipe-task plan` targets an existing job of this type, the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     ← Run Spec example with internal domain steps
../../haipipe-task/ref/workflow-template.yaml  ← authoritative Run Spec template with entry/exit gates
```

Schema source of truth:
  ../../haipipe-workflow/ref/plan-schema.md

Resolve `RESULT_STORE`, then the Job store declaration, then the Job root as OUTPUT_ROOT.
Use the same output-root contract as `haipipe-task`; no physical output is moved by scaffolding.
