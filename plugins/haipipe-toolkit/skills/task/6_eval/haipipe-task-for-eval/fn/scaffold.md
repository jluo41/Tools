fn-scaffold: Scaffold an evaluation job
================================================

Score a trained ModelInstance on an AIData split; produce metrics under `$OUTPUT_ROOT/<task>/results/rNN_<run>/`.
Hierarchy prefixes are bNN / jNN / tNN / rNN; domain belongs in the descriptive suffix.

Output: `tasks/bNN_<block>/jNN_<job>/tNN_<task>/`.


Step 1 — Identify project + block
---------------------------------------

- Auto-detect project from cwd.
- AUTO_MODE: infer from cwd or return `status: blocked`. Interactive: resolve the Block and Job; create missing canonical containers through the shared Task owner.


Step 2 — Collect metadata
--------------------------

- Allocate the next unused Task index inside the selected Job and Run index inside that Task; preserve existing indices.
- snake_case task_name: descriptive
  (e.g., `eval_clm_h24`, `eval_event_horizon2h`).
- Target ModelInstance: `modelinstance_name` + `modelinstance_version`
  (from a sibling training Task or external).
- AIData split: `val | test_id | test_od`.
- Metrics + horizon: what to compute.
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
- `modelinstance_name` + `version` (pin to a specific trained model).
- `aidata_name` + `version`, `split`.
- `EvaluationArgs:` (metrics, horizon, batch_size).


Step 5 — Run-script
--------------------

Copy `../../../haipipe-task/ref/run-sh-template.sh` to `runs/rNN_<run>.sh`.
Set `TASK_NAME="<worker>"` (the worker filename without .py); config and Ticket share the exact `rNN_<run>` stem.


Step 6 — Cross-skill link
--------------------------

After scaffolding, suggest:
- `/haipipe-end` for Stage-6 inference + scoring helpers, if needed.
- `/haipipe-task-for-display` to build a figure/table from these eval results.


Step 7 — Report
----------------

```
status:    ok
summary:   Scaffolded evaluation job <NN>_<name> under the selected bNN Block / jNN Job.
artifacts: [paths created]
next:      run the eval, then /haipipe-task-for-display
```


MUST NOT
---------

- Evaluate on the training split — always `val | test_id | test_od`.
- Skip pinning `modelinstance_version` — eval must be reproducible.
- Mutate any file under `_WorkSpace/5-ModelInstanceStore/` (read-only).
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
