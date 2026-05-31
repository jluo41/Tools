---
name: haipipe-task-for-agent
description: "agent task-folder build specialist. Scaffolds {NN}_<name>/ task-folders under F-series task-groups that call an LLM agent with prompts + tools — outputs to results/<run>/{transcript.json, summary.md}. Called by /haipipe-task orchestrator when task-type=agent. No corresponding pipeline skill yet."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-task-for-agent
==================================

Scaffolds an **LLM-agent task-folder**. Inputs: prompts + tool spec
+ (optional) data context. Outputs: transcript + structured result
under `results/<run>/`.


Position in the series
----------------------

```
/haipipe-task-for-data            data-pipeline
/haipipe-task-for-algo            algo-dev demo
/haipipe-task-for-training        model training
/haipipe-task-for-eval            model evaluation
/haipipe-task-for-display         paper figure / table
/haipipe-task-for-individual      individual-centric query
/haipipe-task-for-agent       ◀── you are here (LLM agent)
```


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

No corresponding pipeline skill yet. Agent infra (Claude API client,
tool dispatch, transcript logging) is project-owned for now.
Adjacent skills: `/claude-api`.


Scaffold flow
-------------

See `fn/scaffold.md` for the detailed step-by-step. Summary:

  1. Identify project + task-group.
  2. Collect metadata (NN, name, type-specific extras, _meta block).
  3. Create skeleton (.py, configs/, runs/, results/, notebooks/).
  4. Seed config from `ref/config-seed.yaml`.
  5. Copy run-script from `../haipipe-task/ref/run-sh-template.sh`.
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
