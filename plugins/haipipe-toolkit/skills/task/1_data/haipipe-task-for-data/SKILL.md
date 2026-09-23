---
name: haipipe-task-for-data
description: "Data-pipeline Job specialist: scaffolds and executes canonical BJTR Jobs whose Task Folders build or run Stage 1-4 Source/Record/Case/AIData work, including Source raw-name coverage and external-data contracts. Called by /haipipe-task when task-type=data."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.5.2"
  last_updated: "2026-09-22"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-data
=================================

Scaffolds AND executes **data-pipeline jobs** — runnable examples that invoke Stage 1-4 builders.
Heavy outputs land in `_WorkSpace/{1..4}-*Store/`; the job keeps light pointers and a notebook of the run.

**Two modes:**
- **Scaffold** (new task): creates skeleton from notebook template
- **Execute** (existing task): runs the pipeline, stage-aware with partition support


What this scaffolds
-------------------

```
tasks/bNN_<block>/
└── jNN_<job>/
    ├── src/                               shared by two or more Tasks
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── outline/
        ├── workflow/
        ├── scripts/
        │   ├── <worker>.py
        │   └── config/rNN_<run>.yaml
        ├── runs/rNN_<run>.sh
        ├── results/rNN_<run>/runtime.yaml
        └── notebooks/rNN_<run>.ipynb
```

Heavy outputs land in: `_WorkSpace/{1..4}-*Store/`.


Notebook template pattern
--------------------------

The task `.py` is an **instantiation** of a generic template from `code/scripts/haistepnb/`.
Only the CONFIG default and docstring change.
The `.ipynb` is auto-generated at runtime — it is NOT source.

```
Template (generic)                         Task .py (exact copy)
──────────────────                         ──────────────────────────────────────
code/scripts/haistepnb/a1_source_nb.py →   {task}/1_source_<project>.py
code/scripts/haistepnb/a2_record_nb.py →   {task}/2_record_<project>.py
code/scripts/haistepnb/a3_case_nb.py   →   {task}/3_case_<project>.py
code/scripts/haistepnb/a4_aidata_nb.py →   {task}/4_aidata_<project>.py
```

Scaffold step: exact copy of template → rename file.
CONFIG overridden at runtime by papermill.
See `ref/notebook-templates.md` for the full mapping and conventions.


Execution flow
---------------

Two execution paths:

**(a) Notebook (papermill)** — standard path via `bash runs/<RUN>.sh`:
  1. `convert_to_notebooks.py` converts `.py` → `.ipynb` (template)
  2. `papermill` injects CONFIG + executes → `notebooks/<RUN>.ipynb`
  3. `run.sh` writes `results/<RUN>/runtime.yaml`

**(b) CLI (direct)** — for parallel workers or scripted pipelines:
  ```
  python -m scripts.haistepcli.source --config <config>
  python -m scripts.haistepcli.record --config <config> --num-partitions 20 --use-cache
  python -m scripts.haistepcli.case   --config <config> --num-partitions 0 --num-workers 4
  python -m scripts.haistepcli.aidata --config <config>
  ```

See `fn/execute.md` for the detailed stage-aware execution protocol.


Partition support
------------------

```
Stage    Partitions     CLI flags                                    Notebook params
──────   ────────────   ──────────────────────────────────────────   ────────────────────
1 Source none           (none)                                       (none)
2 Record creates @i1nN  --num-partitions N --use-cache               NUM_PARTITIONS, PARTITION_INDEX
3 Case   follows @i*n*  --num-partitions 0 --num-workers N --use-cache NUM_PARTITIONS, PARTITION_INDEX
4 AIData merges all     --use-cache (auto-discovers partitions)      NUM_PARTITIONS
```

- **Record** splits patients into N partitions. Each loads only its slice via
  Ptt.parquet + predicate pushdown (memory: ~30GB vs 120GB+ full).
- **Case** is embarrassingly parallel — each partition is independent. Use
  `--num-workers 4` for 4x speedup.
- **AIData** auto-discovers all CaseSet partitions and merges via streaming
  HF Dataset (memory-efficient).
- Partition naming: `@i{i}n{n}` (1-based). Discovery: glob `@i*n*`.


SourceFn Block pattern
----------------------

Source is Block `b01` (see `haipipe-task/ref/hierarchy.md` § Block number
ranges). Its output is `ProcName_to_ProcDf`: one table (ProcDf) per ProcName.
Reference implementation: WellDoc-SPACE
`examples-1-data/Proj01-CGM-RawData/tasks/b02_sourcestore/` (numbered before
the ranges were fixed).

```
b01_sourcestore/
├── j00_procname_to_procdf_contract/      the written contract, one Task per ProcName
│   ├── t01_procdf_<procname>/            config rNN_<procname>_card.yaml IS the contract
│   ├── ...
│   ├── tNN_coverage_matrix/              only when two or more datasets
│   └── tNN_conformance_check/            every SourceSet vs every contract
└── jNN_<cohort>_v<yymmdd>_source/       one Job per dataset version; same jNN as its b00 Job
    ├── t00_sourcefn_develop_and_use/
    │   ├── runs/r01_build_<sourcefn>.sh         regenerates code/haifn/fn_source/<SourceFn>.py
    │   ├── runs/r02_materialize_<dataset>.sh    fills 1-SourceStore/<dataset>/@<SourceFn>/
    │   └── runs/r03_inventory_<dataset>.sh      declared ProcNames vs tables actually stored
    ├── t01_procdf_<procname>/            card of a STORED table, numbered like j00; none for an unstored one
    └── ...
```

- `j00` Task order follows `b00`'s `audit_file_routing`; a contract column
  follows the SourceFn's existing name where there is one, else CamelCase
  (`cohort_id` → `PatientID`). Every raw column is in the contract, so
  nothing is dropped silently.
- One ProcName per raw table. Source renames and types; it never merges tables,
  drops rows, or applies a clinical threshold. Those belong to the Fn that uses
  the decision (a CaseFn label, a TriggerFn cohort).
- A contract config states `row`, `grain`, `read_by` (the RecordFn), and per
  column `meaning`, `type`, `origin` (raw, derived, external) and `required`.
  Required = the RecordFn lists the column in `raw_columns`; everything else is
  carried. A missing required column fails the table; a missing carried column
  makes it partial.
- A new SourceFn version is a new `r0N_build_<sourcefn>` Run in `t00` of the
  first dataset Job it serves, never a new Task or Job. Name it
  `<Family>V<yymmdd>`, e.g. `WellDocDataV251226`. Older versions stay as Runs.
- Ticket suffix says where a Run executes: `.sh` on the local machine, `.cmd`
  on a remote server. In a PHI SPACE (REACH) EVERY Run is a `.cmd` Databricks
  ticket, as in Project-0 J21: the ticket deploys, runs the Task's ONE entry
  `scripts/run_<task>.py` (first line `# Databricks notebook source`, a `RUNS`
  map, then `code/haiutils/haistep/task_entry.py` `pick_run` + `run_task`)
  inline on the cluster, and fetches `results/<run>/`. Workers are
  `main(ctx)`; they write only counts and cards into `ctx.out`. Each Job has
  `sbatch/run_all.cmd`, and every Task has a bundle job generated by
  `safer/scripts/gen_project_run_jobs.py`; `safer/scripts/check_run_tickets.py`
  must report 0 problems.
- Generate the SourceFn and each RecordFn FROM the `j00` contracts. A deploy
  replaces the cluster's copy of the repo, so the committed Fn is the one that
  runs: the build Run regenerates it, returns the text in its Result, and
  FAILS when the committed file differs. A column the RecordFn needs but the
  extraction leaves out on purpose is `origin: not_extracted`: Source writes it
  as null and the card grades the table `partial`, not failed.
- A RecordFn reads ONE ProcName. The record framework keeps only the patients
  present in EVERY RawName a RecordFn lists, so a RecordFn over two tables
  silently drops patients. Signal tables kept apart in Source become one
  RecordFn each; the TriggerFn or CaseFn combines them.
- Prove the wiring on the laptop with a selftest, not a Run: drive every entry
  through `safer/cluster/run_inline.py` with stand-in dbutils and Spark against
  a scratch Volume holding a synthetic twin of the dataset (real stems and
  columns from `b00`, invented values). REACH:
  `safer/selftest/pd2d_inline_contract.py`.

Source Tasks may attach pinned ExternalStore data and emit list/vector-valued
data. Their contract records dtype, ordering, missing mask, external release,
and snapshot metadata. Record/Case tasks consume that contract rather than
rebuilding the external representation.

- Builder reference templates at `code/scripts/haibuilder/{1-source,2-record,3-case,4-aidata}/`.
- D-prefix dictionary tables (`DRGCode`, `DIcdDiagnoses`, `DLabItems`,
  `DIcdProcedures`, `DHcpcs`, `DItems`) are SourceFn-only — no CaseFn reads
  them, and they must NOT enter examples or payloads.


Cross-references
-----------------

Pipeline code (Fn authoring, review, inspection):
- `/haipipe-data` — orchestrator for all stages
- `/haipipe-data-source` — Stage 1 SourceFn
- `/haipipe-data-record` — Stage 2 HumanFn/RecordFn
- `/haipipe-data-case` — Stage 3 TriggerFn/CaseFn
- `/haipipe-data-aidata` — Stage 4 TfmFn/SplitFn

CLI scripts (direct execution):
- `code/scripts/haistepcli/source.py` — Stage 1
- `code/scripts/haistepcli/record.py` — Stage 2 (multi-partition)
- `code/scripts/haistepcli/case.py` — Stage 3 (multi-partition + parallel)
- `code/scripts/haistepcli/aidata.py` — Stage 4 (multi-CaseSet merge)

Notebook templates:
- `code/scripts/haistepnb/a1_source_nb.py` through `a4_aidata_nb.py`


Commands
--------

```
/haipipe-task-for-data                              ASK project / group / name
/haipipe-task-for-data <project> <group> <name>     scaffold direct
```


Scaffold flow
-------------

See `fn/scaffold.md` for the detailed step-by-step.
Summary:

  1. Identify project + canonical `bNN_*` Block and `jNN_*` Job.
  2. Collect Task metadata (`tNN_*`, stage, Page Face, `_meta` block).
  3. Copy notebook template from `haistepnb/{N}_{stage}_nb.py`, set CONFIG default.
  4. Seed `scripts/config/rNN_<run>.yaml` from `ref/config-seed.yaml`.
  5. Copy run-script from `../../haipipe-task/ref/run-sh-template.sh`.
  6. Suggest next via cross-skill link.
  7. Emit return contract.


Execute flow
-------------

See `fn/execute.md` for the detailed step-by-step.
Summary:

  1. Detect stage from script imports (SourceSet/RecordSet/CaseSet/AIData).
  2. Read config for partition_number and stage-specific args.
  3. Execute via notebook (run.sh) or CLI (python -m scripts.haistepcli.{stage}).
  4. Write `results/rNN_<run>/runtime.yaml` inside the Task Folder.
  5. Emit return contract.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was done
artifacts: [paths created]
next:      suggested next command
```


Workflow plan
--------------

When `/haipipe-task plan` targets an existing job of this type, the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     ← script-level phases for this type
../../haipipe-task/ref/workflow-template.yaml  ← authoritative Run Spec template with entry/exit gates
```

Schema source of truth:
  task/haipipe-workflow/ref/plan-schema.md
