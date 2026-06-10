fn-scaffold: Scaffold an algo-dev demo task-folder
====================================================

Purpose: verify a newly developed algorithm class (forward / loss / metric) runs end-to-end on a TINY config. NOT for full training — see `/haipipe-task-for-training` for that. Group letter default: **X** (X_algo).

Output: `tasks/X_algo/{NN}_test_<algo_name>/`.


Step 1 — Identify project + task-group
---------------------------------------

- Auto-detect project from cwd.
- AUTO_MODE: infer from cwd or return `status: blocked`. Interactive: ASK task-group. Group is always `X_algo` for algo-dev. Scaffold the group if absent (see `../haipipe-task/fn/task-group.md`).


Step 2 — Collect metadata
--------------------------

- 2-digit NN: next free in `X_algo/`.
- snake_case task_name: typically `test_<algo_name>`
  (e.g., `test_te_clm_lhm`, `test_te_diffusion`).
- algo_class: the algorithm class under `code/hainn/<algo>/models/<class>/`.
- Tiny config knobs: `batch_size=1`, `max_steps≤5`, `aidata.split=tiny`.
- `_meta:` (purpose explicitly says "smoke-test").


Step 3 — Create skeleton
-------------------------

```
X_algo/
└── {NN}_test_<algo_name>/
    ├── {NN}_test_<algo_name>.py
    ├── configs/
    │   └── algo_<algo_name>_tiny.yaml       from ref/config-seed.yaml
    ├── runs/
    │   └── algo_<algo_name>_tiny.sh
    ├── results/                              loss.json, "ran" marker
    └── notebooks/
```


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to `configs/algo_<algo_name>_tiny.yaml`.
Fill in:
- `_meta:` (purpose: "smoke-test <algo>").
- `algo_class:` (e.g., `te_clm_lhm`).
- `tiny:` knobs (`batch_size=1`, `max_steps=5`, `aidata.split=tiny`).


Step 5 — Run-script
--------------------

Copy `../haipipe-task/ref/run-sh-template.sh` to
`runs/algo_<algo_name>_tiny.sh`. Set `TASK_NAME="{NN}_test_<algo_name>"`.


Step 6 — Cross-skill link
--------------------------

After scaffolding, suggest:
- `/haipipe-nn-algo` to author or refine the algorithm class itself
  (Layer 1: model, forward, loss, metric).
- Once the demo passes → `/haipipe-task-for-training` for the real run.


Step 7 — Report
----------------

```
status:    ok
summary:   Scaffolded algo-dev demo for <algo_name> under X_algo.
artifacts: [paths created]
next:      /haipipe-nn-algo (refine algo)  OR  run the demo
```


MUST NOT
---------

- Use full-size config — defeats the smoke-test purpose.
- Treat the loss/metric as publishable — tiny aidata is meaningless.
- Place a real checkpoint anywhere — the demo shouldn't produce one.
- Create `README.md`.


First-run gate
---------------

`runs/<RUN>.sh` blocks execution if `CODE_REVIEW.md` is missing or
stale (gate inherited from `../haipipe-task/ref/run-sh-template.sh`).
For the first run after this scaffold, do ONE of:

  1. **Recommended** — run the Run Script Reviewer agent on this
     task-folder to produce a fresh `CODE_REVIEW.md`:
     `Tools/plugins/haipipe-toolkit/skills/C_task/agents/haipipe-task-reviewer-agent.md`

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
