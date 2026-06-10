---
name: haipipe-task-for-data
description: "data-pipeline task-folder build specialist. Scaffolds {NN}_<name>/ task-folders under D-series task-groups that run a Stage 1-4 builder (Source / Record / Case / AIData). Called by /haipipe-task orchestrator when task-type=data. Direct invocation works for scoped scaffolding. Cross-references /haipipe-data."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.1.0"
  last_updated: "2026-06-09"
  summary: "data-pipeline task-folder build specialist."
  changelog:
    - "1.1.0 (2026-06-09): unwrap prose; fix agent names; add 4-stage lifecycle paragraph."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-task-for-data
=================================

Scaffolds a **data-pipeline task-folder** — a runnable example that invokes one of the Stage 1-4 builders. Heavy outputs land in `_WorkSpace/{1..4}-*Store/`; the task-folder keeps light pointers and a notebook of the run.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Stage 2: Build, then authors the `<TASK>.py` body). Always end with the structured return block (status / task_folder / run_name / files).



What this scaffolds
-------------------

```
tasks/D{NN}_<group_name>/                   ← group (D-series)
└── {NN}_<task_name>/                       ← task-folder this scaffold creates
    ├── {NN}_<task_name>.py                 source + # %% [parameters] cell
    ├── configs/
    │   └── <task_name>_default.yaml        seeded from ref/config-seed.yaml
    ├── runs/
    │   └── <task_name>_default.sh          from haipipe-task/ref/run-sh-template.sh
    ├── results/                            light pointers + summary
    ├── notebooks/                          papermill output per run
    └── diagram/                            optional, if task diverges from group
```

Group letter default: **D** (data-pipeline).
Heavy outputs land in: `_WorkSpace/{1..4}-*Store/`.


Cross-reference to pipeline skill
----------------------------------

`/haipipe-data` (and its sub-specialists: -source / -record / -case / -aidata) owns the BUILDER code. This skill only scaffolds the example under `examples/`. After scaffolding, suggest `/haipipe-data <stage>` to author the builder logic.


Commands
--------

```
/haipipe-task-for-data                              ASK project / group / name
/haipipe-task-for-data <project> <group> <name>     scaffold direct
```


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
next:      suggested next command (typically /haipipe-data <stage>)
```



Workflow plan
--------------

When `/haipipe-task plan` targets an existing task-folder of this type, the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     ← script-level phases for this type
../haipipe-task/ref/workflow-template.yaml  ← task-level template (Run/Gate1/Gate2)
```

Schema source of truth:
  B_project/haipipe-workflow/ref/plan-schema.md
