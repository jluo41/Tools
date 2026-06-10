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


Step 3 — Create skeleton
-------------------------

```
D{NN}_<group>/
└── {NN}_<task_name>/
    ├── {NN}_<task_name>.py                  papermill source; calls Fn.build()
    ├── configs/
    │   └── {stage}_{layer}_{dataset}.yaml   from ref/config-seed.yaml
    ├── runs/
    │   └── {stage}_{layer}_{dataset}.sh     from haipipe-task/ref/run-sh-template.sh
    ├── results/                              empty (heavy data → _WorkSpace/)
    └── notebooks/
```


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
