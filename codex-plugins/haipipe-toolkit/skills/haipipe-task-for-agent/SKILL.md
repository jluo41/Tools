---
name: haipipe-task-for-agent
description: "agent task-folder build specialist. Scaffolds {NN}_<name>/ task-folders under F-series task-groups that call an LLM agent with prompts + tools — outputs to results/<run>/{transcript.json, summary.md}. Called by /haipipe-task orchestrator when task-type=agent. No corresponding pipeline skill yet."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.1.0"
  last_updated: "2026-06-09"
  summary: "agent task-folder build specialist."
  changelog:
    - "1.1.0 (2026-06-09): unwrap prose; fix agent names; add 4-stage lifecycle paragraph."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-task-for-agent
==================================

Scaffolds an **LLM-agent task-folder**. Inputs: prompts + tool spec + (optional) data context. Outputs: transcript + structured result under `results/<run>/`.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Stage 2: Build, then authors the `<TASK>.py` body). Always end with the structured return block (status / task_folder / run_name / files).



What this scaffolds
-------------------

```
tasks/F{NN}_<group_name>/                    ← F-series group (agent)
└── {NN}_<task_name>/
    ├── {NN}_<task_name>.py
    ├── prompts/                             system + user prompt files
    │   ├── system.md
    │   └── user.md
    ├── configs/
    │   └── agent_<name>.yaml                seeded from ref/config-seed.yaml
    ├── runs/
    │   └── agent_<name>.sh
    ├── results/
    │   └── <run>/                           transcript.json, summary.md
    └── notebooks/
```

Group letter default: **F** (agent).
Heavy outputs: none.


Cross-reference to pipeline skill
----------------------------------

No corresponding pipeline skill yet. Agent infra (Claude API client, tool dispatch, transcript logging) is project-owned for now. Adjacent skills: `/claude-api`.


Scaffold flow
-------------

See `fn/scaffold.md` for the detailed step-by-step. Summary:

  1. Identify project + task-group.
  2. Collect metadata (NN, name, type-specific extras, _meta block).
  3. Create skeleton (.py, configs/, runs/, results/, notebooks/).
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

When `/haipipe-task plan` targets an existing task-folder of this type, the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     ← script-level phases for this type
../../haipipe-task/ref/workflow-template.yaml  ← task-level template (Run/Gate1/Gate2)
```

Schema source of truth:
  project/haipipe-workflow/ref/plan-schema.md
