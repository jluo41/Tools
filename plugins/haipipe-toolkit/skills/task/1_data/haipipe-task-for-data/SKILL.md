---
name: haipipe-task-for-data
description: "Data-pipeline Job specialist: scaffolds and executes canonical BJTR Jobs whose Task Folders build or run Stage 1-4 Source/Record/Case/AIData work, including Source raw-name coverage and external-data contracts. Called by /haipipe-task when task-type=data."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.8.4"
  last_updated: "2026-09-24"
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

Config binding (DrFirst 260923). A Ticket exports `RUN_CONFIG` (its own
config). The worker MUST read it: `CONFIG = os.environ.get("RUN_CONFIG",
CONFIG)` right after the `# %% [parameters]` cell, so the hard-coded default
only serves plain `python` runs. A worker that ignores `RUN_CONFIG` silently
reruns its default config for every new Run (a new dataset's Run rebuilt the
old one). The cook Ticket (`t01_*_materialize`) checks the output it wrote
names the config's `cohort:` / target and fails otherwise. Review a shared
cook worker for this before adding a Run to it.

Adding a dataset by copying a Job. Copy code, configs, Tickets, and Task
pages; never `results/`, `notebooks/`, outline logs, or another Job's
review. Then, before the first Run:
  1. Retarget the one dataset-defaults file (`src/config-defaults.yaml`) and
     rename Job/Task strings; grep the old dataset name to zero hits.
  2. Every Task Folder has its same-stem page (`tNN_<task>/tNN_<task>.md`);
     Tickets refuse to run without it.
  3. Write a fresh `CODE_REVIEW.md` at the current `git_sha`, stating what was
     diffed against the source Job; a copied review is stale and blocks.
  4. Check config binding (above) for every worker the new Runs use.
  5. Pick the dataset's Fn version. Reuse the old one while the SourceFn's
     `ProcName_to_ProcDf` shape is unchanged; otherwise name a new one
     (`v<Label><yymmdd>`) and add a build Run with `fn_version:` to every
     SourceFn, HumanFn, RecordFn, TriggerFn and CaseFn builder the dataset
     uses. Every b01-b03 Run of the `j5N` Job, builder and cook, carries that
     same `fn_version:` (`haipipe-data/ref/0-overview.md` § Fn Versions).


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
Reference implementation: REACH-SPACE
`examples/Project-REACH-PD2D/tasks/b01_sourcestore/` (one dataset) and WellDoc-SPACE
`examples-1-data/Proj01-CGM-RawData/tasks/b01_sourcestore/` (11 datasets, five
topic Jobs, a fixed card number per ProcName `t11`-`t26`, cross-dataset checks
in `j49_procdf_coverage`; migrated 260923).

```
b01_sourcestore/
├── src/contract_card.py                   shared by every topic Job
├── j01_procdf_<topic>/                    topic Job: the written contract of one topic's ProcNames
│   ├── t01_procdf_<ProcName>/             config r01_card.yaml IS the contract
│   └── ...
├── j02_procdf_<topic>/ ...                j01-j49: built once, every dataset
├── j49_procdf_coverage/t01_coverage_matrix/   only with 2+ datasets: dataset × ProcName stored?
└── j51_<cohort>_v<yymmdd>_source/        dataset Job: j51-j99, same number in b00-b03
    ├── t01_sourcefn_develop_and_use/
    │   ├── runs/r01_build.cmd              regenerates code/haifn/fn_source/<SourceFn>.py
    │   └── runs/r02_materialize.cmd        fills 1-SourceStore/<dataset>/@<SourceFn>/
    ├── t02_conformance_check/              this SourceSet vs every contract
    ├── t11_procdf_<ProcName>/              card of a STORED table, in the dataset's table order
    └── ...
```

- Contracts are grouped by topic (cohort, one signal family, EHR context),
  one Job each; the dataset Job lists its tables in that same topic order,
  numbered `t11` onward. The numbers match `b00`'s only when raw tables map
  one to one onto ProcNames (see `haipipe-task/ref/hierarchy.md`). A contract column
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
- A new SourceFn version is a new `r0N_build` Run in `t01` of the
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
- Generate the SourceFn and each RecordFn FROM the topic-Job contracts (a
  config glob over `b01_sourcestore/j[0-4][0-9]_procdf_*`). A deploy
  replaces the cluster's copy of the repo, so the committed Fn is the one that
  runs: the build Run regenerates it, returns the text in its Result, and
  FAILS when the committed file differs. A column the RecordFn needs but the
  extraction leaves out on purpose is `origin: not_extracted`: Source writes it
  as null and the card grades the table `partial`, not failed.
- Record Block, same shape one stage later:
  `b02/j01_recordfn_<topic>/` ... hold the RecordFns of each `b01` topic,
  same Job number; the cohort Job starts with `t01_humanfn_<HumanFn>` (roster
  = one ProcName; its `Excluded_RawNameList` is generated from the `b01`
  contracts), then one `tNN_recordfn_<RecordFn>` per RecordFn, built once for
  every dataset. `b02/j51_<cohort>_v<yymmdd>_record/t01_recordstore_materialize` has one Run
  per dataset that builds the RecordSet and counts every record
  (`records.json`: partitions, rows, patients, rows not kept). An event
  RecordFn keeps a date window (`date_min` in `b02_recordstore/src/config-defaults.yaml`, up to now).
- Case Block, same shape again: topic Jobs by Fn family, then one dataset Job
  per raw dataset (the CaseSet is still per dataset):

  ```
  b03_casestore/
  ├── j01_triggerfn_<name>/t01_triggerfn_<TriggerFn>/     r01_build
  ├── j02_casefn_<family>/t01_casefn_<CaseFn>/ ...        r01_build, one Task per CaseFn
  └── j51_<cohort>_v<yymmdd>_case/t01_casestore_materialize/   r01_<trigger>, one per CaseSet
  ```

- AIData Block is where raw datasets MERGE, so its dataset Jobs are AIDataSets,
  not raw datasets. Each `j5N` has its own number and lists the datasets it
  reads in `src/config-defaults.yaml` (`record_set_names:`):

  ```
  b04_aidatastore/
  ├── j01_tfmfn_<name>/t01_tfmfn_<TfmFn>/                 r01_build
  ├── j02_splitfn_<name>/t01_splitfn_<SplitFn>/           r01_build
  └── j51_<aidataset>_aidata/t01_aidatastore_materialize/ r01_<version>, e.g. j51_welldocglucose_aidata
  ```

- A RecordFn reads ONE ProcName. The record framework keeps only the patients
  present in EVERY RawName a RecordFn lists, so a RecordFn over two tables
  silently drops patients. Signal tables kept apart in Source become one
  RecordFn each; the TriggerFn or CaseFn combines them.
- A cluster the stages never ran on gets a probe Run FIRST (PD2D
  `b00/j01_probe_cluster/t01_probe_cluster_env`, about two minutes): runtime and
  package versions in `probe.json`, a `datasets` save/load round-trip on the
  Volume, and whether the raw dataset is `_FROZEN`. Every receipt also records
  `env` (runtime, pandas, pyarrow, datasets) from `task_entry.env_versions()`.
- A stage that needs packages beyond the runtime lists them as `pip:` in its
  Job's `src/config-defaults.yaml`; the worker calls
  `task_entry.ensure_packages` BEFORE anything imports pandas or pyarrow. What
  is missing installs into a driver-local folder, never into the cluster's own
  Python, which the Spark extraction Runs share.
- A generated Fn never embeds a count from the data (rows, patients): only
  contracts and schema. A size decision (chunking) is made when the Fn runs,
  from the parquet footer, so a new extraction does not make the committed Fn stale.
- Prove the wiring on the laptop with a selftest, not a Run: drive every entry
  through `safer/cluster/run_inline.py` with stand-in dbutils and Spark against
  a scratch Volume holding a synthetic twin of the dataset (real stems and
  columns from `b00`, invented values). REACH:
  `safer/selftest/pd2d_inline_contract.py`.

Source Tasks attach external data through the asset model
(`haipipe-data-external/ref/asset-model.md`): an explicit `lookup` per asset
with `obs_dt`, versions pinned by a lock, and a shared `enrich_<table>()`.
Their contract records dtype, ordering, missing behavior, and the lock and
asset versions (`external-dependency.json`). Record/Case tasks consume those
fields and never reopen ExternalStore. External assets themselves are built,
frozen, validated, and locked in the auxiliary `b51` Block (§ Build Block of
the asset model), not in a data stage Block.

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
