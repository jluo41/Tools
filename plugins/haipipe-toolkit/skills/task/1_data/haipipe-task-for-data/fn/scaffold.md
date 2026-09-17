fn-scaffold: Scaffold a data-pipeline job
==================================================

Invokes one of the Stage 1-4 builders (Source / Record / Case / AIData) to produce data artifacts under `_WorkSpace/{1..4}-*Store/`.
Output: `tasks/bNN_<block>/jNN_<job>/tNN_<task>/`.


Step 1 — Identify project + block
---------------------------------------

- Auto-detect project from cwd (look for `examples/Proj*/`).
- AUTO_MODE: infer from cwd or return `status: blocked`. Interactive: ASK Block. Scaffold a canonical `bNN_<block_name>/` if needed (see `../../../haipipe-task/fn/block.md`).


Step 2 — Collect metadata
--------------------------

- `jNN_*`: one shared logic/version family; `tNN_*`: next free Task index.
- snake_case task_name: descriptive
  (e.g., `build_source_wellreadi`, `build_record_cgm5min`, `build_aidata_eventglucose`).
- Stage (1..4): which builder stage.
- FnClass: `SourceFn` | `RecordFn` | `CaseFn` | `TfmFn` | `SplitFn`.
- Dataset name + version (the `Args.dataset_name` to be built).
- `_meta:` block (purpose / note / input / output).


Step 3 — Create skeleton (from notebook template)
---------------------------------------------------

The `.py` is an instantiation of a generic template.
Copy the right template from `code/scripts/haistepnb/`, then change only the CONFIG default and docstring:

```
Stage A1 → copy code/scripts/haistepnb/a1_source_nb.py into tNN_<task>/scripts/<worker>.py
Stage A2 → copy code/scripts/haistepnb/a2_record_nb.py into tNN_<task>/scripts/<worker>.py
Stage A3 → copy code/scripts/haistepnb/a3_case_nb.py into tNN_<task>/scripts/<worker>.py
Stage A4 → copy code/scripts/haistepnb/a4_aidata_nb.py into tNN_<task>/scripts/<worker>.py
```

After copy:
- Set CONFIG default to `examples/<project>/tasks/bNN_<block>/jNN_<job>/tNN_<task>/scripts/config/rNN_<run>.yaml`
- Update the docstring (first line + Input/Output) with project-specific info

Result:
```
bNN_<block>/
└── jNN_<job>/
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── scripts/<worker>.py
        ├── scripts/config/r01_base.yaml
        ├── runs/r01_base.sh
        ├── results/
        ├── notebooks/
        ├── outline/
        └── workflow/
```

The `.ipynb` is NOT created at scaffold time — `run.sh` auto-generates it via `convert_to_notebooks.py` at execution time.
It is an intermediate output, not source.


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to `scripts/config/r01_base.yaml`.
Fill in:
- `_meta:` (purpose / input / output).
- `stage:` (1..4).
- `FnClass:` and `Args.dataset_name:`.
- Stage-specific args (cohort, partitions, lookups, ...).


Step 5 — Run-script
--------------------

Copy `../../../haipipe-task/ref/run-sh-template.sh` to `runs/r01_base.sh`.
Set `TASK_NAME="tNN_<task>"`.


Step 6 — Cross-skill link
--------------------------

After scaffolding, suggest one of:
- `/haipipe-data-source`   (stage 1)
- `/haipipe-data-record`   (stage 2)
- `/haipipe-data-case`     (stage 3)
- `/haipipe-data-aidata`   (stage 4)

These specialists author the actual builder logic in the group's paired `NN_<stage>_fn_develop_<cohort>/` task folder.


Step 7 — Report
----------------

```
status:    ok
summary:   Scaffolded data-pipeline Task tNN_<task> under bNN_<block>/jNN_<job>; stage <S>.
artifacts: [paths created]
next:      /haipipe-data-{source|record|case|aidata}  OR run the builder
```


MUST NOT
---------

- Place heavy artifacts (`.npy`, `.h5`, `.parquet`, `.pkl > 1 MB`) in `results/`.
  Heavy outputs land in `_WorkSpace/{1..4}-*Store/` per the builder contract.
- Skip the `_meta:` block.
- Symlink `configs/` from another task — each task owns its own.
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
