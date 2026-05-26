---
name: haipipe-task-algo
description: "algo-dev task-folder build specialist. Scaffolds {NN}_<name>/ task-folders under X-series (paired Track A demo) that smoke-test a newly developed algorithm class end-to-end on a TINY config. NOT for full training — see /haipipe-task-training. Called by /haipipe-task orchestrator when task-type=algo. Cross-references /haipipe-nn-algo."
argument-hint: [project_id] [group] [task-name]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-task-algo
=================================

Scaffolds an **algo-dev smoke-test task-folder**. Purpose: verify a
new algorithm class (forward / loss / metric) runs end-to-end. This
is NOT a training run — minimal config, minutes-not-hours, just
"did it crash + does the loss go down on one batch".


Position in the series
----------------------

```
/haipipe-task-data            data-pipeline
/haipipe-task-algo        ◀── you are here (algo-dev demo)
/haipipe-task-training        model training
/haipipe-task-eval            model evaluation
/haipipe-task-display         paper figure / table
/haipipe-task-individual      individual-centric query
/haipipe-task-agent           LLM agent call
```


task-algo vs task-training (don't confuse them)
------------------------------------------------

```
                    task-algo (this)        task-training
Purpose             smoke-test algorithm    train + sweep a model
Group letter        X (paired demo)         A (model-run)
Config              minimal / 1-batch       full hyperparam grid
Runtime             minutes                 hours-to-days
Outputs             "didn't crash" + loss   checkpoint → _WorkSpace/5
Audience            algo developer self     cross-run comparison
Pipeline skill      /haipipe-nn-algo        /haipipe-nn-tuner+instance
```


What this scaffolds
-------------------

```
tasks/X_algo/                                ← X-series group (paired Track A)
└── {NN}_test_<algo_name>/
    ├── {NN}_test_<algo_name>.py
    ├── configs/
    │   └── algo_<name>_tiny.yaml            seeded from ref/config-seed.yaml
    ├── runs/
    │   └── algo_<name>_tiny.sh
    ├── results/                             loss.json, "ran" marker
    └── notebooks/
```

Group letter default: **X** (algo-dev demo).
Heavy outputs: none (tiny / disposable).


Cross-reference to pipeline skill
----------------------------------

`/haipipe-nn-algo` owns the algorithm class itself (Layer 1: model,
forward, loss, metric). This skill scaffolds the smoke-test demo
that exercises it. Typical flow:

  1. `/haipipe-nn-algo` — author the algorithm class.
  2. `/haipipe-task-algo` — scaffold the paired demo.
  3. Run the demo. Iterate.
  4. Once stable → `/haipipe-task-training` for the real run.


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
next:      suggested next command (run the demo / /haipipe-nn-algo refine)
```
