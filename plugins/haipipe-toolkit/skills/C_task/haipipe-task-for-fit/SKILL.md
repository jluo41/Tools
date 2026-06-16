---
name: haipipe-task-for-fit
description: "model-fitting task-folder build specialist. Scaffolds {NN}_<name>/ task-folders that fit/train a model — full hyperparam config, real GPU sweep, checkpoint to _WorkSpace/5-ModelInstanceStore/. NOT for algorithm development — see /haipipe-task-for-algo. Called by /haipipe-task orchestrator when task-type=fit. Cross-references /haipipe-nn-tuner and /haipipe-nn-instance."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.1.0"
  last_updated: "2026-06-09"
  summary: "model-run task-folder build specialist."
  changelog:
    - "1.1.0 (2026-06-09): unwrap prose; fix agent names; add 4-stage lifecycle paragraph."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-task-for-fit
=====================================

Scaffolds a **model-training task-folder**. Full training config, heavy outputs to `_WorkSpace/5-ModelInstanceStore/`, designed for cross-run comparison and paper-grade results.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Stage 2: Build, then authors the `<TASK>.py` body). Always end with the structured return block (status / task_folder / run_name / files).



Not the same as task-algo
--------------------------

See `haipipe-task-for-algo/SKILL.md` for the full comparison.
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

`/haipipe-nn-tuner` defines the hyperparameter search space; `/haipipe-nn-instance` materializes a ModelInstance from a tuner sweep. This skill scaffolds the example task that drives both.

  1. `/haipipe-nn-algo`   — algorithm class exists.
  2. `/haipipe-nn-tuner`  — author the sweep.
  3. `/haipipe-task-for-fit` — scaffold the example task.
  4. Run sweep → ModelInstance → `/haipipe-task-for-eval`.


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



Lessons learned (MIMIC-IV endpoint session)
---------------------------------------------

### ExampleFn and ExampleConfig

- Trained models generate examples via `ExampleConfig` in the training YAML.
- The ExampleFn builder lives in `01_model_fn_develop_mimic/` (same number as
  the training task — same number = same stage).
- Builder reference templates at `code/scripts/haibuilder/5-instance/`.

### SKIP_TRAINING parameter

- `b_model_nb.py` supports `-p SKIP_TRAINING "true"` to skip steps 2-3
  (train + save) and reuse the existing model on disk.
- Steps 4-9 (verify examples, reload, PreFn, reproducibility, inference)
  run normally.
- Use for debugging validation steps without re-training (~20 min to ~20 sec).

### Step 8 reproducibility check

- Compares `model.infer()` on each saved example's PreFn output against
  `prediction_results.json`.
- If `prediction_results.json` is empty, that is a bug (see L1/L4 in
  `3_end/LESSON.md`).

### prediction_results.json

- Must be non-empty after training.
- If empty, the `_infer_examples` step in `ModelInstance_Pipeline` failed
  silently — investigate before proceeding to endpoint packaging.


Workflow plan
--------------

When `/haipipe-task plan` targets an existing task-folder of this type,
the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     ← script-level phases for this type
../haipipe-task/ref/workflow-template.yaml  ← task-level template (Run/Gate1/Gate2)
```

Schema source of truth:
  B_project/haipipe-workflow/ref/plan-schema.md
