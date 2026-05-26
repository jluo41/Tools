---
name: haipipe-task-eval
description: "evaluation task-folder build specialist. Scaffolds {NN}_<name>/ task-folders under B-series task-groups that score a trained model against an AIData split — metrics land in results/<run>/metrics.json. Called by /haipipe-task orchestrator when task-type=eval. Cross-references /haipipe-end or future eval skill."
argument-hint: [project_id] [group] [task-name]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-task-eval
=================================

Scaffolds an **evaluation task-folder**. Consumes a trained
ModelInstance + an AIData split; produces metrics + diagnostic
plots under `results/<run>/`.


Position in the series
----------------------

```
/haipipe-task-data            data-pipeline
/haipipe-task-algo            algo-dev demo
/haipipe-task-training        model training
/haipipe-task-eval        ◀── you are here (evaluation)
/haipipe-task-display         paper figure / table
/haipipe-task-individual      individual-centric query
/haipipe-task-agent           LLM agent call
```


What this scaffolds
-------------------

```
tasks/B{NN}_<group_name>/                    ← B-series group (evaluation)
└── {NN}_<task_name>/
    ├── {NN}_<task_name>.py
    ├── configs/
    │   └── eval_<target>.yaml               seeded from ref/config-seed.yaml
    ├── runs/
    │   └── eval_<target>.sh
    ├── results/
    │   └── <run>/                           metrics.json, plots/, source_data.csv
    └── notebooks/
```

Group letter default: **B** (evaluation).
Heavy outputs: none — `results/<run>/` is all light artifacts.


Cross-reference to pipeline skill
----------------------------------

Currently no dedicated `/haipipe-eval` skill. Evaluation logic
typically calls into `/haipipe-end` (Stage 6 inference + scoring)
or a project-local eval script. This may grow into its own skill;
for now, the eval code is project-owned.


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
next:      suggested next command (run.sh / next eval target)
```
