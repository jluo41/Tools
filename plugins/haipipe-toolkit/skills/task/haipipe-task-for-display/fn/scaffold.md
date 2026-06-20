fn-scaffold: Scaffold a display task-folder
=============================================

Produce a paper figure or table from upstream eval results.
Group letter default: **C** (display).

Output: `tasks/C{NN}_<group>/{NN}_<task_name>/`.


Step 1 — Identify project + task-group
---------------------------------------

- Auto-detect project from cwd.
- AUTO_MODE: infer from cwd or return `status: blocked`. Interactive: ASK task-group. Group letter must be **C**; scaffold a new `C{NN}_<group_name>/` if needed.


Step 2 — Collect metadata
--------------------------

- 2-digit NN: next free in this group.
- snake_case task_name: descriptive
  (e.g., `main_figure_mae_vs_modelsize`, `table_ablation_horizons`).
- Kind: `figure` | `table`.
- Source runs: list of `<task_path>/results/<run>/` to aggregate from.
- Output format: `.pdf` + `.png` for figures; `.tex` + `.csv` for tables.
- `_meta:` block.


Step 3 — Create skeleton
-------------------------

```
C{NN}_<group>/
└── {NN}_<task_name>/
    ├── {NN}_<task_name>.py
    ├── configs/
    │   └── <kind>_<name>.yaml              from ref/config-seed.yaml
    ├── runs/
    │   └── <kind>_<name>.sh
    ├── results/
    │   └── <run>/                           *.pdf, *.png, *.tex, source_data.csv
    └── notebooks/
```


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to `configs/<kind>_<name>.yaml`. Fill in:
- `_meta:` block.
- `kind:` (figure | table).
- `source_runs:` — list of upstream result paths.
- `plot_params:` (figure) or `table_params:` (table).


Step 5 — Run-script
--------------------

Copy `../haipipe-task/ref/run-sh-template.sh` to `runs/<kind>_<name>.sh`.
Set `TASK_NAME="{NN}_{task_name}"`.


Step 6 — Cross-skill link
--------------------------

After scaffolding, suggest:
- `/haipipe-paper-structure-figure` for figure crafting (axes, palette, legend layout).
- `/haipipe-paper-structure-illustration` for diagram-style figures.


Step 7 — Report
----------------

```
status:    ok
summary:   Scaffolded display task <NN>_<name> (kind=<kind>) under C{NN}_<group>.
artifacts: [paths created]
next:      list source_runs in config, then run.sh
```


MUST NOT
---------

- Hardcode paths in the .py — all sources go in `configs/<kind>_<name>.yaml`.
- Modify upstream `results/<run>/` files (read-only inputs).
- Embed model-training logic — display tasks consume, they don't compute.
- Create `README.md`.


First-run gate
---------------

`runs/<RUN>.sh` blocks execution if `CODE_REVIEW.md` is missing or
stale (gate inherited from `../haipipe-task/ref/run-sh-template.sh`).
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
