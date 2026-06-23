fn-scaffold: Scaffold a model-training task-folder
====================================================

Train a real model with full hyperparameters; checkpoint to `_WorkSpace/5-ModelInstanceStore/`. Group letter default: **A** (model-run). For smoke-testing an algorithm, use `/haipipe-task-for-algo` instead.

Output: `tasks/A{NN}_<group>/{NN}_<task_name>/`.


Step 1 — Identify project + task-group
---------------------------------------

- Auto-detect project from cwd.
- AUTO_MODE: infer from cwd or return `status: blocked`. Interactive: ASK task-group. Group letter must be **A**; scaffold a new `A{NN}_<group_name>/` if needed.


Step 2 — Collect metadata
--------------------------

- 2-digit NN: next free in this group (no gaps).
- snake_case task_name: descriptive
  (e.g., `train_clm_num_modelsize`, `finetuning_event_reg_horizon24`).
- `ModelInstanceClass`: model class under `code/hainn/`.
- `modelinstance_name` + `modelinstance_version`: output name (`<name>/@v<NNNN>`).
- Tuner: which hyperparam grid (see `/haipipe-nn-tuner`).
- AIData name + version.
- `_meta:` block.


Step 3 — Create skeleton
-------------------------

```
A{NN}_<group>/
└── {NN}_<task_name>/
    ├── {NN}_<task_name>.py
    ├── configs/
    │   └── 5_model_<name>.yaml             from ref/config-seed.yaml
    ├── runs/
    │   └── 5_model_<name>_<variant>.sh     one per variant
    ├── results/                             metrics.json + model_path.txt (light)
    ├── notebooks/
    └── sbatch/                              optional, for GPU-partitioned sweeps
```


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to `configs/5_model_<name>.yaml`. Fill in:
- `_meta:` block.
- `ModelInstanceClass:`, `modelinstance_name`, `modelinstance_version`.
- `model_tuner_name:` (from /haipipe-nn-tuner).
- `aidata_name` + `aidata_version`.
- `ModelArgs / TrainingArgs / InferenceArgs / EvaluationArgs`.


Step 5 — Run-script
--------------------

Copy `../../haipipe-task/ref/run-sh-template.sh` for each variant.
Set `TASK_NAME="{NN}_{task_name}"`. Variant differences go via
papermill `-p key value` overrides in the run script.


Step 6 — Cross-skill link
--------------------------

After scaffolding, suggest:
- `/haipipe-nn-tuner` to define the hyperparam grid if not present.
- `/haipipe-nn-instance` to materialize a ModelInstance from a sweep result.


Step 7 — Report
----------------

```
status:    ok
summary:   Scaffolded training task <NN>_<name> under A{NN}_<group>.
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

`runs/<RUN>.sh` blocks execution if `CODE_REVIEW.md` is missing or
stale (gate inherited from `../../haipipe-task/ref/run-sh-template.sh`).
For the first run after this scaffold, do ONE of:

  1. **Recommended** — run the Run Script Reviewer agent on this
     task-folder to produce a fresh `CODE_REVIEW.md`:
     `Tools/plugins/haipipe-toolkit/skills/task/agents/haipipe-task-reviewer-agent.md`

  2. **Temporary bypass** — set env var at launch:
     `HAIPIPE_SKIP_REVIEW=1 bash runs/<RUN>.sh`
     (skips the gate for one run; logs a warning to stderr.)

  3. **Permanent skip for this config** — add to `configs/<RUN>.yaml`:
     ```yaml
     _meta:
       skip_review: true
     ```
     (Only appropriate for throwaway / disposable runs.)

Surface this to the user in the orchestrator's `next:` line so they
know **before** trying to launch.
