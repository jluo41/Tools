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

### Block number ranges (JL, 260922)

The Block number says which lifecycle stage the Block belongs to, so the same
number means the same stage in every Project and every SPACE:

```text
b00          raw          understand each extracted dataset, read-only; never extracts
b01          source       SourceFn + SourceStore          (Stage 1)
b02          record       HumanFn/RecordFn + RecordStore  (Stage 2)
b03          case         TriggerFn/CaseFn + CaseStore    (Stage 3)
b04          aidata       TfmFn/SplitFn + AIDataStore     (Stage 4)
b11 to b19   model        one Block per prediction question; one Job per model
b21 to b29   evaluation   fairness, calibration, external validation of a model
b31 to b39   endpoint     inference Fns, Endpoint_Set packaging, deployment
b51 to b59   auxiliary    external stores, benchmarks, shared vocabularies
```

- One stage is one Block. Source, Record, Case, and AIData are never Jobs of a
  single "data pipeline" Block: each stage has two axes of its own (datasets or
  Fn families as Jobs, tables or Fns as Tasks), and a Job has room for only one.
- Extraction from an operational database is never a stage Block. It lives in
  its own extraction Project and writes `0-RawDataStore/<dataset>/`
  (`haipipe-task-for-raw` § Extraction Job). Every Project that uses the data
  understands it in its own `b00` (§ Raw understanding Block), which never
  writes RawStore.
- Jobs split into two ranges in every data Block (JL 260923). `j01`-`j49`
  are TOPIC Jobs: project-wide, built once, named by Fn kind first
  (`j01_procdf_cohort`, `j03_recordfn_diab_signal`, `j01_triggerfn_visit`,
  `j02_casefn_diab_event`, `j01_tfmfn_label`). `j51`-`j99` are DATASET Jobs, one per raw dataset
  version, with the same number in `b00` to `b03` and numbered inside the
  Project, never copied from the extraction Project:
  `b00/j51_reachpd2d_v260922_raw` hands off to
  `b01/j51_reachpd2d_v260922_source`. The next extraction is `j52_…` in
  `b00` to `b03`. `j00` and `j50` stay unused, as `b10` and `b50` do. So the
  Job number alone says whether a Job is built once or once per dataset.
  Datasets take numbers in extraction-date order (the `v<yymmdd>`). A Project
  that grouped datasets by family under the old numbering keeps its family
  digits by adding 50 (WellDoc Proj01: WellDoc `j51`-`j57`, AI-READI `j72`,
  external `j91`-`j96`).
- A raw dataset is named `<cohort>-v<yymmdd>`, the day its extraction was
  launched (`haipipe-data-raw` § Dataset naming); the Job drops the hyphens.
- A range above the data stages starts at `x1`: `b11` is the first model
  Block, `b12` the next question, `b31` the first endpoint Block, as `b51`
  already is in WellDoc and DrFirst. `b10`, `b20`, `b30`, `b50` stay unused. A
  range with no work has no Block.
- A topic Job groups the Fns that change together: the ProcName contracts of
  one topic in `b01`, the RecordFns of the same topic in `b02` with the SAME
  number (`b01/j03_procdf_diab_signal` and `b02/j03_recordfn_diab_signal`),
  one Fn family per Job in `b03`. Built once, it serves every dataset that
  stores its ProcNames; datasets need not share ProcNames (a CGM dataset and
  an EHR dataset in one Project each use only their own topics, and a dataset
  Job cards only the ProcNames it stores). Topics are by what changes
  together, never by dataset.
  - `j01` is always the cohort topic in `b01` and `b02`: the patient roster
    ProcName (`Ptt`, `PatientUniverse`) and its contract in `b01`, the HumanFn
    as `t01_humanfn_<HumanFn>` in `b02`. There is one per Project.
  - `b03` families: `j01_triggerfn_<name>` (who and when a case is), then
    `casefn_label` for outcome CaseFns and `casefn_feature` for input
    CaseFns, split further by topic only when one Job holds too many
    (`casefn_feature_cgm`).
  Code the topic Jobs of a Block share lives in the Block's
  `src/`, and rules they share in the Block's `src/config-defaults.yaml`,
  under each Job's own (task_entry reads both).
- A Task folder names its Fn or ProcName exactly, CamelCase kept
  (`t02_recordfn_REACHPatientUniverse`, `t05_procdf_Social`), and its Runs
  name only the action (`r01_build`, `r01_card`, `r02_materialize`): the
  Task already says what they act on.
- In a dataset Job, `t01`-`t09` cover the whole dataset (build, materialize,
  conformance) and `t11` onward are its tables in ONE fixed topic order;
  `t91`+ close the dataset (routing, hand-off). When raw tables map one to
  one onto ProcNames (REACH), b00 and b01 share the numbers: b00 `t14`
  profile and b01 `j51/t14` card are the same table. When several raw tables
  feed one ProcName (WellDoc: 50 raw tables, 16 ProcNames), b00 numbers raw
  tables and b01 numbers ProcNames, and the numbers do not line up.
- A dataset version is a Job in `b00`, `b01`, `b02` and `b03`, with the same
  `jNN` in all (`b02/j51_reachpd2d_v260922_record`). Its per-item Tasks exist
  only where items differ by dataset: `b01`'s per-table cards, yes; `b02`'s
  per-record cards, no. A `b02` dataset Job is one Task with one Run that
  builds and counts the RecordSet. (DrFirst still makes each dataset a
  Run of one materialize Task; both shapes are one ticket per dataset.)
- Case Block: one topic Job per Fn family with one Task per Fn
  (`j01_triggerfn_visit`, `j02_casefn_diab_event`, `j03_casefn_feature`),
  then one dataset Job
  per raw dataset (`j51_<cohort>_v<yymmdd>_case/t01_casestore_materialize`).
  A CaseSet is still per dataset (`3-CaseStore/<RecordSet>/...`).
- AIData Block is where datasets MERGE (JL 260923): one AIDataSet reads the
  CaseSets of several raw datasets. Topic Jobs `j01`-`j49` hold the TfmFns
  and SplitFns (`j01_tfmfn_<name>`, `j02_splitfn_<name>`); each `j51`-`j99`
  is one AIDataSet (`j51_welldocglucose_aidata/t01_aidatastore_materialize`),
  with its own number, matching no raw dataset Job. Its
  `src/config-defaults.yaml` lists every dataset it merges
  (`record_set_names:`).
- The one piece that spans datasets before `b04` is the Source coverage
  matrix (which dataset stores which ProcName): `b01/j49_procdf_coverage/
  t01_coverage_matrix`, only with 2+ datasets. `b02` and `b03` need none,
  because each dataset Job's materialize Run counts its own records or cases.
- Source Blocks follow `haipipe-task-for-data` § SourceFn Block pattern.

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
├── sbatch/                      optional; serves only this Task
└── studio/                      optional; the Page's kept chat and draw
    └── chat/<YYMMDD-HHMM>/      one kept session (haipipe-workbench-studio)
        ├── digest.md            what it decided · the reading path
        └── transcript.md        the raw exchange · reference only
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
- The scaffolder writes `runtime.yaml` atomically at `planned`; the Ticket
  owns its `running` and truthful terminal updates.
- `complete` requires process success plus the declared Result gate.
- Light Result artifacts live below `$OUTPUT_ROOT/<task>/results/<run>/`.
  In self-serving mode this is beside the authored Task's `runs/` and
  `scripts/`; consumer-serving mode resolves the same suffix in its declared
  mirrored store. Historical Job-level `results/<task>/<run>/` remains
  readable through its recorded resolver.
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
- Current generated Results use `$OUTPUT_ROOT/<task>/results/`, never
  `scripts/`; this lies inside the authored Task Folder only in self-serving
  mode. A Page-authorized display unit may use the destination specified by
  the Page evidence/display contract, with its path and hashes in the Task
  Result envelope; `result.yaml` and `runtime.yaml` stay in the Task store.
- A Task never contains `src/`; a Job never contains `scripts/`.
- The documentation surface is `board.md`, the Task Page, and `diagram/`, not a
  root README.
