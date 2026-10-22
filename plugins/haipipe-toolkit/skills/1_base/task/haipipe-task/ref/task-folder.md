# The Task folder · what a Task holds and how its Runs sit in it

The Task level of Block → Job → Task → Run: one `tNN_<task>/` folder. This file is the folder's
contract. The levels around it have their own owners, so this file names them and does not repeat them:

```text
level   folder            its face        who owns it
Block   work/bNN_<topic>/ board.md        haipipe-block (face, scaffold) · haipipe-project ref/ladder.md (shape)
Job     jNN_<job>/        jNN_<job>.md    haipipe-job (face, Tasks in order, ## Deliverables)
Task    tNN_<task>/       tNN_<task>.md   haipipe-task (this file, ref/task-page.md, ref/lifecycle.md)
Run     runs/<run>/       run.yaml        haipipe-run (identity, card, receipt, role, prune, Workflow)
```

The address is read from the path, never computed: `b02j01t03r04` (compact), `b02.j01.t03.r04`
(readable), `<project-slug>:b02j01t03r04` (global). A partial address keeps its letters (`j01t03`,
`t03r04`); a bare number tuple is invalid. A staged pipeline Project numbers its Blocks by stage
(`ref/pipeline-blocks.md`); any other Project numbers them by topic.

## The folder

```text
tNN_<task>/
├── tNN_<task>.md              the face: state, goal, close, task-type, Opening (ref/task-page.md)
├── scripts/                   this Task's own code: <worker>.py (or .do, .R), its helpers
│   └── config/                settings several Runs share: _defaults.yaml, prompts/; a Block that
│                              has not moved keeps each Run's rNN_<run>.yaml here too
├── runs/
│   └── rNN_<noun>_<qualifier>/   one folder per Run (haipipe-run, since 261006)
│       ├── rNN_<…>.sh         the ticket (.ps1 for Stata on Windows, .cmd where only cmd.exe runs)
│       ├── config.yaml        this Run's own settings (config.do for Stata)
│       ├── run.yaml           its card: run, kind, role, type, status, … (haipipe-run)
│       ├── result/            what it wrote: runtime.yaml (the receipt), metrics.json, headline.txt,
│       │                      small tables, figures, heavy.yaml (a pointer to its big files)
│       └── passes/pNN-<MMDD>/ each execution's logs, when one Run executes more than once
├── notebooks/                 generated papermill copies, when the ticket makes them
├── draft/                     only when the Task writes: a draft Task's plan and sentences, or a
│                              Task Page's plan (haipipe-draft)
├── sbatch/                    a supervisor that runs this Task's tickets in order
├── workflow/                  optional: plan.yaml (haipipe-run ref/workflow.md) and report.yaml
└── studio/                    optional: haipipe-studio's kept chat sessions; topics live in the Block's studio/
```

1. **The face** is the one page a reader opens. Its header lines and its reading are `ref/task-page.md`.
   `draft/`'s layout and its check (`page.py check-page-folder`) are haipipe-draft's; a kept chat
   session in `studio/chat/<YYMMDD-HHMM>/` holds both `digest.md` and `transcript.md` (haipipe-studio).
2. **`scripts/`** holds only this Task's code. Code two Tasks share goes in the Job's `src/`, never in a
   Task; a Job holds no `scripts/`.
3. **`runs/`** holds one folder per Run. A Task made before 261006 keeps the flat layout,
   `runs/<run>.sh` beside `results/<run>/`, until `haipipe-project` `ladder.py update` moves its Block.
4. **No root README**, no `src/`, no root `config/`, no `results/` (old layout only), no copy or link
   to a big file. The reader's surfaces are the Block's `board.md`, the Job's face and this face.
5. **No Task lives outside a Job**, and every Job sits in a Block.

## What earns a Task

A Task is one computation, one output contract and one code path. It is its own Task only when all
three hold:

1. **Reuse**: its code runs unchanged on another cohort, fold or source.
2. **Output**: it owns Result files no other Task writes.
3. **Rerun**: it is the smallest unit worth rerunning after an input changes.

A new cohort, segment, fold, source or parameter set is a new Run with its own config, never a new
Task. A different output contract is a new Task. A unit that no longer shares the Job's code or
submission boundary is a new Job (haipipe-job). A cross-Job dependency is a data dependency: the
downstream config names the exact upstream Run's Result.

## A Run inside the Task

haipipe-run owns what a Run is (hard or soft, its card, its receipt, its role, when it is pruned).
This Task owns the ticket's body, the shared parts every type uses:

1. **The ticket** finds the Block, Job, Task and Run from its own real path and names its one config.
   Copy `ref/run-sh-template.sh` to `runs/<run>/<run>.sh` (a type skill may give its own, Stata's
   `.ps1`) and set `TASK_NAME` (the worker's name), `RUN_FAMILY`, `RUN_OPERATION`, `RUN_TARGET`,
   `REQUIRED_RESULTS` (the files its Result gate needs; the default is `metrics.json`) and any extra
   `RUN_INPUTS`; optionally `WORKER_PATH` (a worker the Job shares, `src/<worker>.py`) and
   `NOTEBOOK_NAME` (a notebook named for what it shows). It runs the SPACE's `.venv` Python and hands
   the worker `REPO_ROOT`, `JOB_DIR`, `TASK_DIR`, `RUN_NAME`, `RUN_CONFIG`, `RESULT_DIR` and `HEAVY_DIR`.
   A ticket never loops over sibling tickets; a supervisor in `sbatch/` does.
2. **The receipt**: the ticket writes `result/runtime.yaml` as `running` before expensive work and
   marks it `complete` only after its declared Result gate passes, else `failed` or `partial`
   (`ref/runtime-yaml-schema.md`). A zero exit with no evidence check is a smoke test, role `trial`.
3. **The worker** writes only where the ticket points it (`RESULT_DIR`); it never builds its own output
   path. A configured name that does not resolve raises and names what is missing.
4. **A Result is light**: metrics, logs, small tables, figures. Big files go to the Run's `HEAVY_DIR`,
   `_WorkSpace/ProjectResult/<Project>/<block>/<job>/<task>/<run>/`, and the Result keeps the pointer
   `heavy.yaml` (`ref/authoring-conventions.md` § Artifact placement). A pipeline asset (a SourceSet,
   a RecordSet) goes to its stage store instead.
5. **The card**: a new Run's `run.yaml` is written with its folder (`fn/run.md`, a type skill's scaffold),
   and `haipipe-project` `ladder.py update` writes any that is missing; the ticket sets its `status:`
   (`running`, then `done` or `failed`).
6. **Charts and Table Cards are Runs**: a `role: figures` Run draws a Task's charts into its own
   `result/`, and a `role: describe` Run writes a stored table's Table Card. Neither is hand-made.
7. **Keep only the meaningful Runs**: a Run that was replaced or never ran is pruned once nothing in use
   reads it (haipipe-run `prune_runs.py`). A rerun of an unchanged contract is a new pass of the same
   Run; a changed target, input or close rule is a new Run with `supersedes:`.

## Two output modes

```text
self-serving      OUTPUT_ROOT = <job>/                             Results inside the Task's runs/<run>/result/
consumer-serving  OUTPUT_ROOT = <store>/<path-of-job-below-work>/  the same suffix, in a consumer's store
```

Resolution order: `RESULT_STORE` from a dispatching consumer, then `store:` in the Job's
`src/config-defaults.yaml`, then the Job itself. The suffix `<task>/runs/<run>/result/` is the same in
both modes. Authored code, config and tickets always stay in the Task folder; one Job serves several
cohorts only when each call has its own Run and frozen inputs.

## Supervisors

```text
<job>/sbatch/    runs the tickets of two or more of the Job's Tasks
<task>/sbatch/   runs the tickets of this Task only
```

A supervisor calls tickets, never worker code. It says whether it runs them one by one or in parallel,
its ceiling, its collision keys and a one-line reason. A Job supervisor names at least two Tasks. A
long one runs in `tmux` on the machine that holds the data.

## Names

Every Block, Job, Task and Run is `<level letter><two digits>_<concrete noun>_<qualifier>`
(`b01_physician_candidates`, `j01_candidates_from_review_sites`, `t01_physician_urls_normalized`,
`r01_healthgrades_full`).

1. **The stranger test**: someone who never opened the folder answers "what thing?" and "which one?"
   from the name alone. Shape words (`data`, `table`, `pipeline`, `analysis`, `pool`, `rank`, `set`,
   `baseline`) may qualify a noun, never stand alone (`j01_candidate_pool` is weak,
   `j01_physician_candidates_by_region` is clear).
2. **Level and order**: the letter says the level and the index the order inside the parent; neither
   encodes a stage or a type. Indices are two digits, start at `01`, are unique in their parent, take
   the next free number, and never renumber after a deletion.
3. **The Project's words**: use terms the Project already defines; never coin a synonym a reader must
   translate.
4. **Unique siblings**: a Job name is unique in its Block, a Task name in its Job, a Run name in its
   Task. Cross-Job references use full paths or full addresses.
5. **Look names up**: a script resolves a declared name and raises when it is absent; it never slices
   a folder name or falls back to a default.
6. **The tree is the inventory**: no hand-kept list of Tasks or tickets; a view reads the disk. Store
   only an explicit ordering decision (a Job's `## Tasks`).
7. **A Run's name says what differs between Runs**: its fold, source, model or action. In a staged
   pipeline Task that names its Fn exactly, a Run names only its action (`t05_procdf_Social/r01_card`,
   `ref/pipeline-blocks.md`); a type skill may fix its own Run names (`r01_describe_<table>`). Renaming
   the words after an index keeps the address; changing an index changes it, so every exact reference
   is updated.

## Checks

```bash
python Tools/plugins/haipipe-toolkit/skills/1_base/task/haipipe-task/scripts/check_task_tree.py <block or work/>
python Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-project/scripts/ladder.py audit <block> --today
```

The first checks this folder contract (names, tickets, configs, receipts; `ref/task-tree-checklist.md`
lists its rows); the second checks the ladder's shape and today's rules. Before trusting a changed
checker, plant a break in a scratch copy and require `--expect-fail` to see it.
