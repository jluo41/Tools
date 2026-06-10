---
name: haipipe-task-for-algo
description: "algo-dev task-folder build specialist. Scaffolds {NN}_<name>/ task-folders under X-series (paired Track A demo) that smoke-test a newly developed algorithm class end-to-end on a TINY config. NOT for full training — see /haipipe-task-for-fit. Called by /haipipe-task orchestrator when task-type=algo. Cross-references /haipipe-nn-algo."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.1.0"
  last_updated: "2026-06-09"
  summary: "algo-dev task-folder build specialist."
  changelog:
    - "1.1.0 (2026-06-09): unwrap prose; fix agent names; add 4-stage lifecycle paragraph."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-task-for-algo
=================================

Scaffolds an **algo-dev smoke-test task-folder**. Purpose: verify a new algorithm class (forward / loss / metric) runs end-to-end. This is NOT a training run — minimal config, minutes-not-hours, just "did it crash + does the loss go down on one batch".

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Stage 2: Build, then authors the `<TASK>.py` body). Always end with the structured return block (status / task_folder / run_name / files).



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

`/haipipe-nn-algo` owns the algorithm class itself (Layer 1: model, forward, loss, metric). This skill scaffolds the smoke-test demo that exercises it. Typical flow:

  1. `/haipipe-nn-algo` — author the algorithm class.
  2. `/haipipe-task-for-algo` — scaffold the paired demo.
  3. Run the demo. Iterate.
  4. Once stable → `/haipipe-task-for-fit` for the real run.


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



Workflow plan
--------------

When `/haipipe-task plan` targets an existing task-folder of this type, the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     ← script-level phases for this type
../haipipe-task/ref/workflow-template.yaml  ← task-level template (Run/Gate1/Gate2)
```

Schema source of truth:
  B_project/haipipe-workflow/ref/plan-schema.md
