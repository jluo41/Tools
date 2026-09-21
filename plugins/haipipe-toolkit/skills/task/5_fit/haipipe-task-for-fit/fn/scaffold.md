fn-scaffold: Scaffold a model-training job
====================================================

Train a real model with full hyperparameters; checkpoint to `_WorkSpace/5-ModelInstanceStore/`.
Hierarchy prefixes are bNN / jNN / tNN / rNN; domain belongs in the descriptive suffix.
For smoke-testing an algorithm, use `/haipipe-task-for-algo` instead.

Output: `tasks/bNN_<block>/jNN_<job>/tNN_<task>/`.


Step 1 — Identify project + block
---------------------------------------

- Auto-detect project from cwd.
- AUTO_MODE: infer from cwd or return `status: blocked`. Interactive: resolve the Block and Job; create missing canonical containers through the shared Task owner.


Step 2 — Collect metadata
--------------------------

- Allocate the next unused Task index inside the selected Job and Run index inside that Task; preserve existing indices.
- snake_case task_name: descriptive
  (e.g., `train_clm_num_modelsize`, `finetuning_event_reg_horizon24`).
- `ModelInstanceClass`: model class under `code/hainn/`.
- `modelinstance_name` + `modelinstance_version`: output name (`<name>/@v<NNNN>`).
- Tuner: which hyperparam grid (see `/haipipe-nn-tuner`).
- AIData name + version.
- `_meta:` block.


Step 3 — Create skeleton
-------------------------

```text
tasks/bNN_<block>/
├── board.md
└── jNN_<job>/
    ├── src/                         shared code + config-defaults.yaml
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── outline/
        ├── workflow/                plan.yaml + report.yaml
        ├── scripts/<worker>.py
        ├── scripts/config/rNN_<run>.yaml
        └── runs/rNN_<run>.sh

Generated: $OUTPUT_ROOT/tNN_<task>/results/rNN_<run>/
           $OUTPUT_ROOT/tNN_<task>/notebooks/rNN_<run>.ipynb
```


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to `scripts/config/rNN_<run>.yaml`.
Fill in:
- `_meta:` block.
- `ModelInstanceClass:`, `modelinstance_name`, `modelinstance_version`.
- `model_tuner_name:` (from /haipipe-nn-tuner).
- `aidata_name` + `aidata_version`.
- `ModelArgs / TrainingArgs / InferenceArgs / EvaluationArgs`.


Step 5 — Run-script
--------------------

Copy `../../../haipipe-task/ref/run-sh-template.sh` for each variant.
Set `TASK_NAME="<worker>"` (the worker filename without .py); config and Ticket share the exact `rNN_<run>` stem.
Each variant gets its own `scripts/config/rNN_<run>.yaml` and matching Ticket; freeze overrides in that config and receipt.


Step 6 — Cross-skill link
--------------------------

After scaffolding, suggest:
- `/haipipe-nn-tuner` to define the hyperparam grid if not present.
- `/haipipe-nn-instance` to materialize a ModelInstance from a sweep result.


Step 7 — Report
----------------

```
status:    ok
summary:   Scaffolded training job <NN>_<name> under the selected bNN Block / jNN Job.
artifacts: [paths created]
next:      /haipipe-nn-tuner (define sweep) OR run a variant
```


MUST NOT
---------

- Place heavy artifacts (`.pt`, `.ckpt`, `.safetensors`, `.bin`) in `results/`.
  Checkpoints belong in `_WorkSpace/5-ModelInstanceStore/<name>/@v<NNNN>/`.
- Run with `_meta:` empty — at least `purpose:` is mandatory.
- Reuse a `modelinstance_version` across runs (immutable once a run starts).
- Create `README.md`.


First-run gate
---------------

`runs/<RUN>.sh` blocks execution if `CODE_REVIEW.md` is missing or stale (gate inherited from `../../../haipipe-task/ref/run-sh-template.sh`).
For the first run after this scaffold, do ONE of:

  1. **Recommended** — run the haipipe-task-reviewer-agent (Gate 1) on this
     job to produce a fresh `CODE_REVIEW.md`:
     `Tools/plugins/haipipe-toolkit/skills/task/agents/haipipe-task-reviewer-agent.md`

  2. **Temporary bypass** — set env var at launch:
     `HAIPIPE_SKIP_REVIEW=1 bash runs/<RUN>.sh`
     (skips the gate for one run; logs a warning to stderr.)

  3. **Permanent skip for this config** — add to `scripts/config/<RUN>.yaml`:
     ```yaml
     _meta:
       skip_review: true
     ```
     (Only appropriate for throwaway / disposable runs.)

Surface this to the user in the orchestrator's `next:` line so they know **before** trying to launch.
