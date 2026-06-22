fn-scaffold: Scaffold an individual-query task-folder
======================================================

Query / visualize ONE individual's data (CGM trace, meal timeline, treatment events). Group letter default: **E** (individual).

Output: `tasks/E{NN}_<group>/{NN}_<task_name>/`.


Step 1 — Identify project + task-group
---------------------------------------

- Auto-detect project from cwd.
- AUTO_MODE: infer from cwd or return `status: blocked`. Interactive: ASK task-group. Group letter must be **E**; scaffold a new `E{NN}_<group_name>/` if needed.


Step 2 — Collect metadata
--------------------------

- 2-digit NN: next free in this group.
- snake_case task_name: descriptive
  (e.g., `view_cgm_timeline`, `view_meal_glucose_overlay`).
- `subject_id`: REQUIRED — the patient to query.
- View: `timeline | meal_overlay | treatment_event | ...`.
- Time window: e.g. `7d`, `2026-01-01..2026-01-08`.
- Source layer: `1-SourceStore | 2-RecStore | 3-CaseStore`.
- `_meta:` block.


Step 3 — Create skeleton
-------------------------

```
E{NN}_<group>/
└── {NN}_<task_name>/
    ├── {NN}_<task_name>.py
    ├── configs/
    │   └── individual_<view>.yaml             from ref/config-seed.yaml
    ├── runs/
    │   └── individual_<view>.sh
    ├── results/
    │   └── <run>/                           plot.pdf, table.csv
    └── notebooks/
```


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to `configs/individual_<view>.yaml`. Fill in:
- `_meta:` block.
- `subject_id:`, `subject_group:`.
- `view:` (one of the supported view names).
- `time_window:` (absolute or relative).
- `source_layer:` (which Store to read from).


Step 5 — Run-script
--------------------

Copy `../../haipipe-task/ref/run-sh-template.sh` to `runs/individual_<view>.sh`.
Set `TASK_NAME="{NN}_{task_name}"`.


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
summary:   Scaffolded individual-query task <NN>_<name> (view=<view>) under E{NN}_<group>.
artifacts: [paths created]
next:      verify subject_id exists, then run.sh
```


MUST NOT
---------

- Hardcode `subject_id` in the `.py` — it lives in `configs/individual_<view>.yaml`
  so different subjects can be queried by config change alone.
- Include PHI / PII beyond the project's data policy.
- Place full data dumps in `results/` — only summary plots + tables.
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
