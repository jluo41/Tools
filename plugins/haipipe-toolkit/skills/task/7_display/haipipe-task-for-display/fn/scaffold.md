fn-scaffold: Scaffold a display job
=============================================

Produce the verified display-ready summary input for a paper figure or table from upstream results.
Group letter default: **C** (display).

Output: `tasks/C{NN}_<group>/{NN}_<job_name>/`.


Step 1 — Identify project + block
---------------------------------------

- Auto-detect project from cwd.
- AUTO_MODE: infer from cwd or return `status: blocked`. Interactive: ASK block. Group letter is PROJECT-SPECIFIC (orchestrator rule; follow the project's existing scheme). Default **C**; scaffold a new `C{NN}_<block_name>/` if needed.


Step 2 — Collect metadata
--------------------------

- 2-digit NN: next free in this group.
- snake_case task_name: descriptive
  (e.g., `main_figure_mae_vs_modelsize`, `table_ablation_horizons`).
- Intended display kind: `figure` | `table` | `diagram` | `illustration`.
- Source runs: list of `<task_path>/results/<run>/` to aggregate from.
- Output format: `source_data.csv` + `provenance.json`; optional diagnostic images stay under `diagnostics/`.
- `_meta:` block.


Step 3 — Create skeleton
-------------------------

```
C{NN}_<group>/
└── {NN}_<job_name>/
    ├── {NN}_<job_name>.py
    ├── configs/
    │   └── <kind>_<name>.yaml              from ref/config-seed.yaml
    ├── runs/
    │   └── <kind>_<name>.sh
    ├── results/
    │   └── <run>/                           source_data.csv, provenance.json, diagnostics/ (optional)
    └── notebooks/
```


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to `configs/<kind>_<name>.yaml`.
Fill in:
- `_meta:` block.
- `display_kind:` (figure | table | diagram | illustration).
- `source_runs:` — list of upstream result paths.
- `summary_params:` — selected columns, grouping, filters, and unit of analysis.

The run must also write `results/<run>/provenance.json` using
`ref/provenance-template.json`.
It records the producing task holder, run, output hash, upstream artifacts, selected columns,
filters, and the assertion that the CSV is display-safe and contains no raw or PHI data.


Step 5 — Run-script
--------------------

Copy `../../../haipipe-task/ref/run-sh-template.sh` to `runs/<kind>_<name>.sh`.
Set `TASK_NAME="{NN}_{job_name}"`.


Step 6 — Next step
-------------------

After scaffolding, suggest running the task (`bash runs/<run>.sh`), then materializing its
`source_data.csv` into the display unit's `intake/` with a manifest that names this task holder,
run, canonical artifact, hashes, and permitted use.
Figure crafting standards (axes, palette, legend layout) live with Display; this skill only
guarantees the summary-data and provenance contract.


Step 7 — Report
----------------

```
status:    ok
summary:   Scaffolded display job <NN>_<name> (kind=<kind>) under C{NN}_<group>.
artifacts: [paths created]
next:      list source_runs in config, then run.sh
```


MUST NOT
---------

- Hardcode paths in the .py — all sources go in `configs/<kind>_<name>.yaml`.
- Modify upstream `results/<run>/` files (read-only inputs).
- Embed model-training logic — display tasks consume, they don't compute.
- Create `README.md`.
- Treat a PDF, PNG, or TeX emitted here as a canonical paper asset. Diagnostics are allowed only
  under `results/<run>/diagnostics/`; the Display unit owns the promoted asset and its wrapper.


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

  3. **Permanent skip for this config** — add to `configs/<RUN>.yaml`:
     ```yaml
     _meta:
       skip_review: true
     ```
     (Only appropriate for throwaway / disposable runs.)

Surface this to the user in the orchestrator's `next:` line so they know **before** trying to launch.
