---
name: haipipe-task-training
description: "model-run task-folder build specialist. Scaffolds {NN}_<name>/ task-folders under A-series task-groups that train a model — full hyperparam config, real GPU sweep, checkpoint to _WorkSpace/5-ModelInstanceStore/. NOT for algorithm development — see /haipipe-task-algo. Called by /haipipe-task orchestrator when task-type=training. Cross-references /haipipe-nn-tuner and /haipipe-nn-instance."
argument-hint: [project_id] [group] [task-name]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-task-training
=====================================

Scaffolds a **model-training task-folder**. Full training config,
heavy outputs to `_WorkSpace/5-ModelInstanceStore/`, designed for
cross-run comparison and paper-grade results.


Position in the series
----------------------

```
/haipipe-task-data            data-pipeline
/haipipe-task-algo            algo-dev demo
/haipipe-task-training    ◀── you are here (training)
/haipipe-task-eval            model evaluation
/haipipe-task-display         paper figure / table
/haipipe-task-individual      subject-centric query
/haipipe-task-agent           LLM agent call
```


Not the same as task-algo
--------------------------

See `haipipe-task-algo/SKILL.md` for the full comparison.
Short version: algo-dev = smoke test, training = real run.


What this scaffolds
-------------------

```
tasks/A{NN}_<group_name>/                    ← A-series group (model-run)
└── {NN}_<task_name>/
    ├── {NN}_<task_name>.py
    ├── configs/
    │   └── 5_model_<name>.yaml              seeded from ref/config-seed.yaml
    ├── runs/
    │   └── 5_model_<name>_<variant>.sh
    ├── results/
    │   └── <run>/                           model_path.txt + metrics.json (light)
    ├── notebooks/
    └── sbatch/                              optional, for GPU-partitioned sweep
```

Group letter default: **A** (model-run).
Heavy outputs land in: `_WorkSpace/5-ModelInstanceStore/`.


Cross-reference to pipeline skill
----------------------------------

`/haipipe-nn-tuner` defines the hyperparameter search space; 
`/haipipe-nn-instance` materializes a ModelInstance from a tuner
sweep. This skill scaffolds the example task that drives both.

  1. `/haipipe-nn-algo`   — algorithm class exists.
  2. `/haipipe-nn-tuner`  — author the sweep.
  3. `/haipipe-task-training` — scaffold the example task.
  4. Run sweep → ModelInstance → `/haipipe-task-eval`.


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
next:      suggested next command (/haipipe-nn-tuner or run.sh)
```
