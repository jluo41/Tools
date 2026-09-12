# Task Folder structure

This is the concrete filesystem contract. `ref/hierarchy.md` owns the
conceptual model; `ref/authoring-conventions.md` owns code and runtime rules.

## Canonical tree

```text
tasks/
└── bNN_<block>/
    ├── board.md
    ├── diagram/
    └── jNN_<job>/
        ├── src/
        │   └── config-defaults.yaml
        ├── sbatch/
        ├── tNN_<task>/
        │   ├── tNN_<task>.md
        │   ├── outline/
        │   ├── workflow/
        │   ├── scripts/
        │   │   ├── <worker>.py
        │   │   └── config/
        │   │       ├── _defaults.yaml
        │   │       ├── prompts/
        │   │       └── rNN_<run>.yaml
        │   ├── runs/rNN_<run>.sh
        │   └── sbatch/
        ├── tNN_<task>/results/rNN_<run>/
        │   ├── runtime.yaml
        │   └── metrics.json
        └── notebooks/tNN_<task>/rNN_<run>.ipynb
```

`Task Folder = Page Folder`. Do not create a second Page container for it.

## Block rules

- Name: `bNN_<noun>_<qualifier>`.
- Must contain `board.md` with `board-kind: task-block`.
- Direct executable children are Jobs named `jNN_*`.
- May contain `diagram/` for the shared narrative.
- Must not contain code, config, Tickets, Results, notebooks, or batchers.
- Board rows, when explicit, use full relative Page paths:
  `jNN_<job>/tNN_<task>/tNN_<task>.md`.

## Job rules

- Name: `jNN_<noun>_<qualifier>`.
- Must contain `src/`, even when empty, to make shared-code ownership visible.
- Must contain at least one direct `tNN_*` Task Folder.
- `src/` holds only code/defaults shared by multiple Tasks.
- `src/config-defaults.yaml` may declare a Job-level `store:`.
- Job `sbatch/` coordinates at least two Tasks.
- Generated output uses `<task>/results/<run>/` and
  `<task>/notebooks/<run>.ipynb` under resolved `$OUTPUT_ROOT`.
- Must not contain Task-owned `scripts/` or root worker programs.

## Task Folder rules

- Name: `tNN_<noun>_<qualifier>`.
- Must contain a same-stem Markdown Page.
- Must contain `scripts/`, `scripts/config/`, `runs/`, `workflow/`, and
  `outline/`.
- `scripts/` holds Task-owned workers and helpers.
- `scripts/config/` holds shared Task settings plus one config per Run.
- `runs/` holds one Ticket per Run.
- Task `sbatch/` may coordinate only this Task's Tickets.
- Must not contain `src/`, generated `results/`, or root `config/`.

## Run spine

For each Run stem, these projections pair exactly:

```text
tNN_<task>/scripts/config/rNN_<run>.yaml
tNN_<task>/runs/rNN_<run>.sh
$OUTPUT_ROOT/tNN_<task>/results/rNN_<run>/runtime.yaml
$OUTPUT_ROOT/tNN_<task>/notebooks/rNN_<run>.ipynb
```

Shared files under `scripts/config/` omit the `rNN_` prefix and do not require
a Ticket. Every Ticket derives identity from its path and names one matching
config. A Ticket does not loop over sibling Tickets; orchestration belongs in
`sbatch/`.

## Results and notebooks

Light Results include metrics, logs, reports, small data extracts, and display
files. Heavy artifacts go to `_WorkSpace/` and are represented by pointers and
hashes in the Result.

The worker receives `RESULT_DIR` and must write there. It must not construct a
Task-local output path. The Ticket creates and updates `runtime.yaml`
atomically and marks the Run complete only after the declared Result gate.

Python Tasks use a diff-friendly `.py` source with `# %%` cells. The Ticket
generates `$OUTPUT_ROOT/<task>/notebooks/_source.ipynb` and executes it with
papermill into `$OUTPUT_ROOT/<task>/notebooks/<run>.ipynb`. Notebook retention
is selected by `_meta.notebook: full | thin | off` in the Run config.

## Batch rules

- Job batcher: `<job>/sbatch/run_*.sh`; references at least two `tNN_*` paths.
- Task batcher: `<task>/sbatch/run_*.sh`; references Tickets from that Task.
- Batchers call Tickets, not worker programs.
- Batchers declare mode, capacity, collision keys, and reason.
- Alternative entry points are descriptively named, not sequence-numbered.

## Documentation

- Block overview: `board.md` and optional `diagram/`.
- Task explanation: same-stem Task Page plus `outline/`.
- Job-specific operational detail: optional `diagram/`.
- Generated status pages are rebuilt from the tree; do not hand-copy an
  inventory that can drift.

## Ticket templates

Use `ref/run-sh-template.sh` for Python/papermill execution. Copy it into the
Task's `runs/` lane, then set `TASK_NAME`, `RUN_FAMILY`, `RUN_OPERATION`,
`RUN_TARGET`, `REQUIRED_RESULTS`, and any additional `RUN_INPUTS`.

The Stata engine is wholly owned by `haipipe-task-for-stata`; its Task Folder
still obeys the Block/Job/Task/Run hierarchy and uses `scripts/config/` for
Run configuration.

## Required validation

```bash
python3 ref/check_task_tree.py <block-or-tasks-dir>
```

Before trusting a changed checker, run it on a scratch copy with one planted
violation and `--expect-fail`. Then run the same checker on the target tree and
require zero findings.
