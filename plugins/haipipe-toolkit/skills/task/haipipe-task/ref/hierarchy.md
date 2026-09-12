# Task hierarchy — Block / Job / Task / Run

This file is the conceptual authority for the Task family. Load
`../../../run/haipipe-run/SKILL.md` when Run identity, Ticket/Result pairing,
receipts, or audit semantics are in scope.

**Task Folder = Page Folder = `tNN_<task>/`.** It is one physical Folder with
an executable Task Face and a reader-facing Page Face. Its parent
`jNN_<job>/` is only the Job container.

```text
level    canonical path                                      meaning
Block    tasks/bNN_<noun>_<qualifier>/                       one Task Board
Job      tasks/bNN_<block>/jNN_<noun>_<qualifier>/           one submittable unit
Task     .../jNN_<job>/tNN_<noun>_<qualifier>/               one pipeline and Page
Run      .../tNN_<task>/scripts/config/rNN_<run>.yaml        one execution identity
```

The four prefixes form the execution address: `b02j01t03r04`. Each prefix is
read from the path; none is mapped or computed.

## Project

```text
examples/<project>/
├── tasks/       all Task Blocks
├── diagram/     project-level narrative
└── papers/      optional paper work
```

Executable work under `tasks/` always passes through Block, Job, and Task.

## Block = Task Board

```text
tasks/bNN_<block>/
├── board.md                    board-kind: task-block
├── jNN_<job>/
├── jNN_<job>/
└── diagram/                    optional shared narrative
```

A Block contains Jobs and documentation only. It has no code, config, Ticket,
Result, notebook, or batch lane. The tree owns Board membership and default
order:

```text
Block = Board  →  Job = Group  →  Task Folder = Page Folder = Page
                                      └── Run = execution record
```

Prefer a few coherent Blocks. Split when the Jobs no longer share one topic,
dependency boundary, or Board narrative.

## Job = submittable unit

```text
jNN_<job>/
├── src/                         shared by two or more Tasks
│   └── config-defaults.yaml     optional Job defaults and store declaration
├── tNN_<task>/
├── tNN_<task>/
├── sbatch/                      optional; spans at least two Tasks
├── tNN_<task>/results/<run>/    generated in self-serving mode, inside the Task Folder that owns the Run
├── <task>/notebooks/<run>.ipynb
└── diagram/                     optional operational narrative
```

A Job is the largest thing one scheduler submission owns and the smallest unit
that runs without importing code from a sibling Job. Cross-Job dependency is a
data dependency: downstream config names an exact upstream Run receipt.

`src/` contains only code or defaults shared by multiple Tasks in this Job.
Task-owned code always lives in that Task's `scripts/` lane.

## Task Folder = Page Folder

```text
tNN_<task>/
├── tNN_<task>.md                Page opened by a reader
├── outline/                     Page context, evidence, reading, open threads
├── workflow/                    P-B-E-R intent and evidence
├── scripts/
│   ├── <worker>.py              one pipeline
│   ├── config/
│   │   ├── _defaults.yaml       optional shared settings for this Task
│   │   ├── r01_<run>.yaml       one Run config
│   │   └── prompts/             config-owned prompts
│   └── <helpers>                Task-owned helpers
├── runs/
│   ├── r01_<run>.sh             one Ticket for the matching config
│   └── r02_<run>.sh
└── sbatch/                      optional; serves only this Task
```

A Task is one function: one computation, one output contract, one code path.
It earns a separate Task only when all three tests pass:

1. Reuse: the code can run unchanged on another cohort.
2. Output: it owns Result files no other Task writes.
3. Rerun: it is the smallest meaningful unit to rerun after an input change.

A cohort, segment, fold, source, or parameter change creates a new config and
Run. A different output contract creates a new Task. A unit that no longer
shares the Job's source or submission boundary creates a new Job.

## Run = execution identity

One Run has four paired projections with the same `rNN_<run>` stem:

```text
tNN_<task>/scripts/config/rNN_<run>.yaml       frozen authored inputs
tNN_<task>/runs/rNN_<run>.sh                   authored Ticket
$OUTPUT_ROOT/tNN_<task>/results/rNN_<run>/     generated Result and receipt
$OUTPUT_ROOT/tNN_<task>/notebooks/rNN_<run>.ipynb
```

The generated notebook template is
`$OUTPUT_ROOT/tNN_<task>/notebooks/_source.ipynb`. Both notebooks are generated;
edit the `.py` source, never an `.ipynb` projection.

A Ticket names exactly one config and executes one Task. It may select an
execution slice, but may not repeat values already owned by the config. It
records every effective value in `runtime.yaml` before expensive work begins.

## Two output modes

```text
self-serving
  OUTPUT_ROOT = <job>/

consumer-serving
  OUTPUT_ROOT = <store>/<path-of-job-below-tasks>/
```

Resolution order:

1. `RESULT_STORE` supplied by a dispatching consumer.
2. `store:` in `<job>/src/config-defaults.yaml`.
3. The Job directory.

The `<task>/<run>` suffix is identical in both modes. All generated,
data-dependent artifacts follow `$OUTPUT_ROOT`, including `results/`,
`notebooks/`, and Run audits. Authored Task code/config/Tickets remain in the
Task Folder. A Job can serve multiple cohorts only when each call has a
distinct Run identity and frozen input receipt.

## Naming

Every Block, Job, Task, and Run uses:

```text
<level-letter><two-digit-index>_<concrete-noun>_<qualifier>
```

Examples:

```text
b01_physician_candidates
j01_candidates_from_review_sites
t01_physician_urls_normalized
r01_healthgrades_full
```

The stranger test is binding: someone who has never opened the Folder must be
able to answer “what thing?” and “which one?” from the name alone. Shape words
such as `data`, `table`, `pipeline`, `pool`, `rank`, and `analysis` may qualify
a concrete noun but cannot stand alone.

Indices start at `01`, use exactly two digits, and are unique within their
parent. Scaffolding uses the next free index and never renumbers existing
siblings after deletion.

## Config, Ticket, and Result rules

- Per-Run config and Ticket stems match exactly.
- Shared config in `scripts/config/` does not use an `rNN_` prefix.
- Prompts are config and resolve relative to the config that names them.
- A Ticket derives Block, Job, Task, and Run identity from its own real path.
- A Ticket writes `runtime.yaml` atomically at `planned`, `running`, and a
  truthful terminal state.
- `complete` requires process success plus the declared Result gate.
- Light Result artifacts live below `<task>/results/<run>/`, beside the Task's `runs/` and `scripts/` (JL ruling 260909; before it they sat at the Job level under `<task>/results/<run>/`).
- Model weights, large arrays, raw tables, and other heavy artifacts live in
  `_WorkSpace/`; the Result stores pointers and checksums.

## Batch placement

```text
<job>/sbatch/                 coordinates two or more Tasks in this Job
<task>/sbatch/                coordinates Runs of exactly one Task
```

Batchers call Tickets, never worker code directly. They declare sequential or
parallel mode, capacity ceiling, collision keys, and a one-line reason. A Job
batcher must reference at least two Task Folders.

## Page closure

The Task Folder's `workflow/` lane is its machine-facing lifecycle record.
Its `outline/` lane and same-stem Markdown file are the human-facing record.
Report completion does not settle the Folder by itself. Closure requires:

- terminal P-B-E-R receipts;
- current load-bearing Run Results;
- a current person-read `#### READING · current` table;
- a CHECK receipt naming that reading.

A new or superseding Run reopens the affected reading and therefore reopens
the Task Page on its Block Board.

## Mechanical checks

From a Job root, config/Ticket pairing must print nothing:

```bash
comm -3 \
  <(find t[0-9][0-9]_*/scripts/config -type f -name 'r[0-9][0-9]_*' | sed 's|/scripts/config/|/|; s|\.[^./]*$||' | sort) \
  <(find t[0-9][0-9]_*/runs -type f -name 'r[0-9][0-9]_*' | sed 's|/runs/|/|; s|\.[^./]*$||' | sort)
```

The full structural gate is `ref/check_task_tree.py`. Prove it can fail on a
deliberately broken scratch copy before trusting a zero-finding run.

## Mandatory rules

- Jobs always live inside Blocks; Tasks always live inside Jobs.
- Every Block is a Task Board and every Task Folder is a Page Folder.
- A Job contains at least one Task Folder and a Task Folder contains at least
  one `rNN_` Ticket.
- Block/Job/Task/Run names must pass the grammar and stranger test.
- Generated Results live in the Task Folder's `results/`, never at the Job level and never under `scripts/`.
- A Task never contains `src/`; a Job never contains `scripts/`.
- The documentation surface is `board.md`, the Task Page, and `diagram/`, not a
  root README.
