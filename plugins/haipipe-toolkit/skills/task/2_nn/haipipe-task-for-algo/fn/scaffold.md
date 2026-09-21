fn-scaffold: Scaffold an algo-dev demo job
====================================================

Purpose: verify a newly developed algorithm class (forward / loss / metric) runs end-to-end on a TINY config.
NOT for full training — see `/haipipe-task-for-fit` for that.
Hierarchy prefixes are bNN / jNN / tNN / rNN; domain belongs in the descriptive suffix.

Output: `tasks/bNN_<block>/jNN_<job>/tNN_<task>/`.


Step 1 — Identify project + block
---------------------------------------

- Auto-detect project from cwd.
- AUTO_MODE: infer from cwd or return `status: blocked`. Interactive: resolve the Block and Job; create missing canonical containers through the shared Task owner.


Step 2 — Collect metadata
--------------------------

- Allocate the next unused Task index inside the selected Job and Run index inside that Task; preserve existing indices.
- snake_case task_name: typically `test_<algo_name>`
  (e.g., `test_te_clm_lhm`, `test_te_diffusion`).
- algo_class: the algorithm class under `code/hainn/algo/<family>/`.
- Tiny config knobs: `batch_size=1`, `max_steps≤5`, `aidata.split=tiny`.
- `_meta:` (purpose explicitly says "smoke-test").


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
- `_meta:` (purpose: "smoke-test <algo>").
- `algo_class:` (e.g., `te_clm_lhm`).
- `tiny:` knobs (`batch_size=1`, `max_steps=5`, `aidata.split=tiny`).


Step 5 — Run-script
--------------------

Copy `../../../haipipe-task/ref/run-sh-template.sh` to `runs/rNN_<run>.sh`.
Set `TASK_NAME="<worker>"` (the worker filename without .py); config and Ticket share the exact `rNN_<run>` stem.


Step 6 — Cross-skill link
--------------------------

After scaffolding, suggest:
- `/haipipe-nn-algo` to author or refine the algorithm class itself
  (Layer 1: model, forward, loss, metric).
- Once the demo passes → `/haipipe-task-for-fit` for the real run.


Step 7 — Report
----------------

```
status:    ok
summary:   Scaffolded algo-dev demo for <algo_name> under the selected bNN Block / jNN Job.
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
