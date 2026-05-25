fn-scaffold: Scaffold an evaluation task-folder
================================================

Score a trained ModelInstance on an AIData split; produce metrics under
`results/<run>/`. Group letter default: **B** (evaluation).

Output: `tasks/B{NN}_<group>/{NN}_<task_name>/`.


Step 1 — Identify project + task-group
---------------------------------------

- Auto-detect project from cwd.
- ASK task-group if not given. Group letter must be **B**;
  scaffold a new `B{NN}_<group_name>/` if needed.


Step 2 — Collect metadata
--------------------------

- 2-digit NN: next free in this group.
- snake_case task_name: descriptive
  (e.g., `eval_clm_h24`, `eval_event_horizon2h`).
- Target ModelInstance: `modelinstance_name` + `modelinstance_version`
  (from a sibling A-task or external).
- AIData split: `val | test_id | test_od`.
- Metrics + horizon: what to compute.
- `_meta:` block.


Step 3 — Create skeleton
-------------------------

```
B{NN}_<group>/
└── {NN}_<task_name>/
    ├── {NN}_<task_name>.py
    ├── configs/
    │   └── eval_<target>.yaml              from ref/config-seed.yaml
    ├── runs/
    │   └── eval_<target>.sh
    ├── results/
    │   └── <run>/                           metrics.json, eval_log.txt
    └── notebooks/
```


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to `configs/eval_<target>.yaml`. Fill in:
- `_meta:` block.
- `modelinstance_name` + `version` (pin to a specific trained model).
- `aidata_name` + `version`, `split`.
- `EvaluationArgs:` (metrics, horizon, batch_size).


Step 5 — Run-script
--------------------

Copy `../haipipe-task/ref/run-sh-template.sh` to `runs/eval_<target>.sh`.
Set `TASK_NAME="{NN}_{task_name}"`.


Step 6 — Cross-skill link
--------------------------

After scaffolding, suggest:
- `/haipipe-end` for Stage-6 inference + scoring helpers, if needed.
- `/haipipe-task-display` to build a figure/table from these eval results.


Step 7 — Report
----------------

```
status:    ok
summary:   Scaffolded evaluation task <NN>_<name> under B{NN}_<group>.
artifacts: [paths created]
next:      run the eval, then /haipipe-task-display
```


MUST NOT
---------

- Evaluate on the training split — always `val | test_id | test_od`.
- Skip pinning `modelinstance_version` — eval must be reproducible.
- Mutate any file under `_WorkSpace/5-ModelInstanceStore/` (read-only).
- Create `README.md`.


First-run gate
---------------

`runs/<RUN>.sh` blocks execution if `CODE_REVIEW.md` is missing or
stale (gate inherited from `../haipipe-task/ref/run-sh-template.sh`).
For the first run after this scaffold, do ONE of:

  1. **Recommended** — run the Run Script Reviewer agent on this
     task-folder to produce a fresh `CODE_REVIEW.md`:
     `Tools/plugins/haipipe-toolkit/agents/run-script-reviewer.md`

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
