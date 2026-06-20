fn-scaffold: Scaffold a data-pipeline task-folder
==================================================

Invokes one of the Stage 1-4 builders (Source / Record / Case / AIData)
to produce data artifacts under `_WorkSpace/{1..4}-*Store/`.
Group letter default: **D**. Output: `tasks/D{NN}_<group>/{NN}_<task_name>/`.


Step 1 — Identify project + task-group
---------------------------------------

- Auto-detect project from cwd (look for `examples/Proj*/`).
- AUTO_MODE: infer from cwd or return `status: blocked`. Interactive: ASK task-group. Group letter must be **D**; scaffold a new `D{NN}_<group_name>/` if needed (see `../haipipe-task/fn/task-group.md`).


Step 2 — Collect metadata
--------------------------

- 2-digit NN: next free in this group (no gaps).
- snake_case task_name: descriptive
  (e.g., `build_source_wellreadi`, `build_record_cgm5min`, `build_aidata_eventglucose`).
- Stage (1..4): which builder stage.
- FnClass: `SourceFn` | `RecordFn` | `CaseFn` | `TfmFn` | `SplitFn`.
- Dataset name + version (the `Args.dataset_name` to be built).
- `_meta:` block (purpose / note / input / output).


Step 3 — Create skeleton (from notebook template)
---------------------------------------------------

The `.py` is an instantiation of a generic template. Copy the right
template from `code/scripts/haistepnb/`, then change only the CONFIG
default and docstring:

```
Stage A1 → cp code/scripts/haistepnb/a1_source_nb.py → {task}/{NN}_{task_name}.py
Stage A2 → cp code/scripts/haistepnb/a2_record_nb.py → {task}/{NN}_{task_name}.py
Stage A3 → cp code/scripts/haistepnb/a3_case_nb.py   → {task}/{NN}_{task_name}.py
Stage A4 → cp code/scripts/haistepnb/a4_aidata_nb.py → {task}/{NN}_{task_name}.py
```

After copy:
- Set CONFIG default to `examples/<project>/tasks/<group>/<task>/configs/run_<name>.yaml`
- Update the docstring (first line + Input/Output) with project-specific info

Result:
```
{G}{NN}_<group>/
└── {NN}_<task_name>/
    ├── {NN}_<task_name>.py                  instantiation of haistepnb template
    ├── configs/
    │   └── run_<task_name>.yaml             from ref/config-seed.yaml
    ├── runs/
    │   └── run_<task_name>.sh               from haipipe-task/ref/run-sh-template.sh
    ├── results/                              empty (heavy data → _WorkSpace/)
    └── notebooks/
```

The `.ipynb` is NOT created at scaffold time — `run.sh` auto-generates it
via `convert_to_notebooks.py` at execution time. It is an intermediate
output, not source.


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to `configs/{stage}_{layer}_{dataset}.yaml`.
Fill in:
- `_meta:` (purpose / input / output).
- `stage:` (1..4).
- `FnClass:` and `Args.dataset_name:`.
- Stage-specific args (cohort, partitions, lookups, ...).


Step 5 — Run-script
--------------------

Copy `../haipipe-task/ref/run-sh-template.sh` to
`runs/{stage}_{layer}_{dataset}.sh`. Set `TASK_NAME="{NN}_{task_name}"`.


Step 6 — Cross-skill link
--------------------------

After scaffolding, suggest one of:
- `/haipipe-data-source`   (stage 1)
- `/haipipe-data-record`   (stage 2)
- `/haipipe-data-case`     (stage 3)
- `/haipipe-data-aidata`   (stage 4)

These specialists author the actual builder logic in
`code-dev/1-PIPELINE/{stage}-*-WorkSpace/`.


Step 7 — Report
----------------

```
status:    ok
summary:   Scaffolded data-pipeline task <NN>_<name> under D{NN}_<group>; stage <S>.
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
