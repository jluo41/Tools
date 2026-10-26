---
name: haipipe-task-for-fit
description: "model-fitting Task specialist: scaffolds jNN_<job>/tNN_<task>/ Task folders that fit/train a model (full hyperparam config, real GPU sweep, checkpoint to _WorkSpace/5-ModelInstanceStore/). NOT algorithm dev -- see /haipipe-task-for-algo. Called by /haipipe-task when task-type=fit. Cross-references /haipipe-nn tuner and /haipipe-nn instance. Its parts _parts/gpu and _parts/gpu-training own GPU queues (exclusive cards, preflight, OOM backoff, sequential handoff) and checkpoint resume. Trigger: fit task, train model, GPU sweep, GPU queue, checkpoint resume."
argument-hint: "[project_id] [bNN_<block>/jNN_<job>] [tNN_<task>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.3.0"
  last_updated: "2026-10-25"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-fit
=====================================

Scaffolds a **model-training job**.
Full training config, heavy outputs to `_WorkSpace/5-ModelInstanceStore/`, designed for cross-run comparison and paper-grade results.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during the internal Build step of the owning Task authoring Run, then authors the `<TASK>.py` body).
Always end with the structured return block (status / task_folder / run_name / files).

## Type contract

```yaml
task-type: fit
skill: haipipe-task-for-fit
does: Trains one model with its full hyperparameters (a real GPU sweep when declared) into a ModelInstance and scores it on the validation split.
worker: scripts/<worker>.py (Python), calling the ModelInstance and tuner classes under code/hainn/
config: runs/<run>/config.yaml (seeded from ref/config-seed.yaml), or scripts/config/<run>.yaml in a Block not yet moved
ticket: runs/<run>/<run>.sh, from ../../haipipe-task/ref/run-sh-template.sh (REQUIRED_RESULTS metrics.json and model_path.txt); a GPU queue runs it through `_parts/gpu/PART.md`
result: $OUTPUT_ROOT/<task>/runs/<run>/result/, with runtime.yaml, model_path.txt and metrics.json before the receipt says complete
heavy: _WorkSpace/5-ModelInstanceStore/<modelinstance_name>/@v<NNNN>/ (the checkpoints; the Result keeps the pointer model_path.txt)
roles: [trial, make, fix]
companions: [haipipe-nn, haipipe-task-for-eval]
plan_sample: ref/workflow-plan-sample.yaml
```

## GPU queue handoff

When the fit job uses a real GPU, a multi-run sweep, or an OOM fallback, also
read this skill's parts `_parts/gpu/PART.md` and
`_parts/gpu-training/PART.md`. Keep training semantics, checkpoints,
and metrics here; let the generic GPU companion own exclusive-card preflight,
sequential Ticket handoff, teardown, and queue receipts, while the training
companion owns checkpoint integrity, safe resume, preemption, effective-batch
accounting, and training-specific fallbacks.



Not the same as task-algo
--------------------------

See `../../2_nn/haipipe-task-for-algo/SKILL.md` for the full comparison.
Short version: algo-dev = smoke test, training = real run.


What this scaffolds
-------------------

```text
work/bNN_<block>/
├── board.md
└── jNN_<job>/
    ├── src/                         shared code + config-defaults.yaml
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── draft/
        ├── workflow/                plan.yaml + report.yaml
        ├── scripts/<worker>.py
        └── runs/rNN_<run>/              one folder per Run
            ├── rNN_<run>.sh             the ticket
            ├── config.yaml              this Run's settings
            ├── run.yaml                 its card (role: trial | make | fix)
            └── result/                  runtime.yaml (the receipt) + metrics.json, model_path.txt

Generated: $OUTPUT_ROOT/tNN_<task>/runs/rNN_<run>/result/
           $OUTPUT_ROOT/tNN_<task>/notebooks/rNN_<run>.ipynb
A Block not yet moved still has the flat runs/rNN_<run>.sh, scripts/config/rNN_<run>.yaml
and results/rNN_<run>/; the ticket template runs both.
```

Hierarchy prefixes are bNN / jNN / tNN / rNN; domain belongs in the descriptive suffix.
Heavy outputs land in: `_WorkSpace/5-ModelInstanceStore/`.


Cross-reference to pipeline skill
----------------------------------

`/haipipe-nn tuner` defines the hyperparameter search space; `/haipipe-nn instance` materializes a ModelInstance from a tuner sweep.
This skill scaffolds the example task that drives both.

  1. `/haipipe-nn algo`   — algorithm class exists.
  2. `/haipipe-nn tuner`  — author the sweep.
  3. `/haipipe-task-for-fit` — scaffold the example task.
  4. Run sweep → ModelInstance → `/haipipe-task-for-eval`.


Scaffold flow
-------------

See `fn/scaffold.md` for the detailed step-by-step.
Summary:

  1. Identify project + block.
  2. Collect metadata (NN, name, type-specific extras, _meta block).
  3. Create the canonical Task Page, workflow/, worker and one Run folder runs/rNN_<run>/ (Ticket, config.yaml, run.yaml); resolve generated output through OUTPUT_ROOT.
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
next:      suggested next command (/haipipe-nn tuner or run.sh)
```



Lessons learned
----------------

Canonical lessons live in `LESSON.md` (same folder): L1 temporal-leak filter, L2 PID/PatientID format, L4 empty prediction_results.json = silent bug, L5 `-p SKIP_TRAINING "true"` fast iteration, L6 what the Step-8 reproducibility check actually tests.
Read it before building a fit task; do not restate its content here.

Quick pointers:
- ExampleFn builder lives in the same-numbered task as training (same number = same stage); builder templates at `code/scripts/haibuilder/5-instance/` (workspace-dependent path).
- `prediction_results.json` must be non-empty after training (LESSON.md L4).


Workflow plan
--------------

When `/haipipe-task plan` targets an existing job of this type, the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     ← Run Spec example with internal domain steps
../../haipipe-task/ref/workflow-template.yaml  ← authoritative Run Spec template with entry/exit gates
```

Schema source of truth:
  project/haipipe-run/ref/plan-schema.md

Resolve `RESULT_STORE`, then the Job store declaration, then the Job root as OUTPUT_ROOT.
Use the same output-root contract as `haipipe-task`; no physical output is moved by scaffolding.
