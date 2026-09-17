---
name: haipipe-task-for-data
description: "Data-pipeline Job specialist: scaffolds and executes canonical BJTR Jobs whose Task Folders build or run Stage 1-4 Source/Record/Case/AIData work, including Source raw-name coverage and external-data contracts. Called by /haipipe-task when task-type=data."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.3.0"
  last_updated: "2026-09-13"
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


SourceFn Job pattern
--------------------

One Job represents one version/family of shared SourceFn logic. Every raw name
that owns a distinct ProcessDF output contract gets one plainly named Task.
Reserve the final Tasks for integration:

```
j01_source_contract_<family>/
├── t01_<raw_name_one>_processdf/
├── t02_<raw_name_two>_processdf/
├── t03_<raw_name_three>_processdf/
├── ...
├── t51_sourcefn_<family>/          build the generated SourceFn
└── t52_source_pipeline_<family>/   run and validate the HAI pipeline
```

If later Raw Data has a different structure or needs a different shared
transformation, create `j02_*`; do not hide a new SourceFn version inside a Run.
Within each Task, cohorts/parameters become `rNN_*` Runs.

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
- `/haipipe-data-source` — Stage 1 SourceFn/HumanFn
- `/haipipe-data-record` — Stage 2 RecordFn/TriggerFn
- `/haipipe-data-case` — Stage 3 CaseFn
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
../../haipipe-task/ref/workflow-template.yaml  ← task-level template (Run/Gate1/Gate2)
```

Schema source of truth:
  task/haipipe-workflow/ref/plan-schema.md
