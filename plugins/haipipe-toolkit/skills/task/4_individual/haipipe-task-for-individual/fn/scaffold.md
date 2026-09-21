fn-scaffold: Scaffold an individual-query job
======================================================

Query / visualize ONE individual's data (CGM trace, meal timeline, treatment events).
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
  (e.g., `view_cgm_timeline`, `view_meal_glucose_overlay`).
- `subject_id`: REQUIRED — the patient to query.
- View: `timeline | meal_overlay | treatment_event | ...`.
- Time window: e.g. `7d`, `2026-01-01..2026-01-08`.
- Source layer: `1-SourceStore | 2-RecStore | 3-CaseStore`.
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
- `subject_id:`, `subject_group:`.
- `view:` (one of the supported view names).
- `time_window:` (absolute or relative).
- `source_layer:` (which Store to read from).


Step 5 — Run-script
--------------------

Copy `../../../haipipe-task/ref/run-sh-template.sh` to `runs/rNN_<run>.sh`.
Set `TASK_NAME="<worker>"` (the worker filename without .py); config and Ticket share the exact `rNN_<run>` stem.


Step 6 — Cross-skill link
--------------------------

After scaffolding, suggest:
- `/haipipe-individual` for per-individual data access (`Subject-*` folder layout
  under `_WorkSpace/A-User-Store/`).
- `/haipipe-individual-inference` if the view includes model predictions.


Step 7 — Report
----------------

```
status:    ok
summary:   Scaffolded individual-query task <NN>_<name> (view=<view>) under the selected bNN Block / jNN Job.
artifacts: [paths created]
next:      verify subject_id exists, then run.sh
```


MUST NOT
---------

- Hardcode `subject_id` in the `.py` — it lives in `scripts/config/rNN_<run>.yaml`
  so different subjects can be queried by config change alone.
- Include PHI / PII beyond the project's data policy.
- Place full data dumps in `results/` — only summary plots + tables.
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
