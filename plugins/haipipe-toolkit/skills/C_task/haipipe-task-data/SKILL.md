---
name: haipipe-task-data
description: "data-pipeline task-folder build specialist. Scaffolds {NN}_<name>/ task-folders under D-series task-groups that run a Stage 1-4 builder (Source / Record / Case / AIData). Called by /haipipe-task orchestrator when task-type=data. Direct invocation works for scoped scaffolding. Cross-references /haipipe-data."
argument-hint: [project_id] [group] [task-name]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-task-data
=================================

Scaffolds a **data-pipeline task-folder** — a runnable example that
invokes one of the Stage 1-4 builders. Heavy outputs land in
`_WorkSpace/{1..4}-*Store/`; the task-folder keeps light pointers
and a notebook of the run.


Position in the series
----------------------

```
/haipipe-task-data        ◀── you are here (data-pipeline)
/haipipe-task-algo            algo-dev demo
/haipipe-task-training        model training
/haipipe-task-eval            model evaluation
/haipipe-task-display         paper figure / table
/haipipe-task-individual      subject-centric query
/haipipe-task-agent           LLM agent call
```


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

`/haipipe-data` (and its sub-specialists: -source / -record / -case /
-aidata) owns the BUILDER code. This skill only scaffolds the example
under `examples/`. After scaffolding, suggest `/haipipe-data <stage>`
to author the builder logic.


Commands
--------

```
/haipipe-task-data                              ASK project / group / name
/haipipe-task-data <project> <group> <name>     scaffold direct
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
