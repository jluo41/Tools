---
name: haipipe-task-for-data
description: "data-pipeline task-folder specialist. Scaffolds AND executes {NN}_<name>/ task-folders that run Stage 1-4 builders (Source / Record / Case / AIData) with multi-partition support. Called by /haipipe-task orchestrator when task-type=data. Cross-references /haipipe-data for Fn authoring."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-06-11"
  summary: "data-pipeline task-folder specialist (scaffold + execute + partition)."
  changelog:
    - "2.0.0 (2026-06-11): add execute path, notebook template pattern, multi-partition support."
    - "1.1.0 (2026-06-09): unwrap prose; fix agent names; add 4-stage lifecycle paragraph."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-task-for-data
=================================

Scaffolds AND executes **data-pipeline task-folders** — runnable examples
that invoke Stage 1-4 builders. Heavy outputs land in `_WorkSpace/{1..4}-*Store/`;
the task-folder keeps light pointers and a notebook of the run.

**Two modes:**
- **Scaffold** (new task): creates skeleton from notebook template
- **Execute** (existing task): runs the pipeline, stage-aware with partition support


What this scaffolds
-------------------

```
tasks/{G}{NN}_<group_name>/                 ← group (letter is project-specific)
└── {NN}_<task_name>/                       ← task-folder
    ├── {NN}_<task_name>.py                 source (instantiation of haistepnb template)
    ├── configs/
    │   └── run_<task_name>.yaml            seeded from ref/config-seed.yaml
    ├── runs/
    │   └── run_<task_name>.sh              from haipipe-task/ref/run-sh-template.sh
    ├── results/                            runtime.yaml per run
    ├── notebooks/                          papermill output per run
    └── workflow/                           plan.yaml + report.yaml
```

Heavy outputs land in: `_WorkSpace/{1..4}-*Store/`.


Notebook template pattern
--------------------------

The task `.py` is an **instantiation** of a generic template from
`code/scripts/haistepnb/`. Only the CONFIG default and docstring change.
The `.ipynb` is auto-generated at runtime — it is NOT source.

```
Template (generic)                         Task .py (exact copy)
──────────────────                         ──────────────────────────────────────
code/scripts/haistepnb/a1_source_nb.py →   {task}/1_source_<project>.py
code/scripts/haistepnb/a2_record_nb.py →   {task}/2_record_<project>.py
code/scripts/haistepnb/a3_case_nb.py   →   {task}/3_case_<project>.py
code/scripts/haistepnb/a4_aidata_nb.py →   {task}/4_aidata_<project>.py
```

Scaffold step: exact copy of template → rename file. CONFIG overridden at runtime by papermill.
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
  python -m scripts.haistep.source --config <config>
  python -m scripts.haistep.record --config <config> --num-partitions 20 --use-cache
  python -m scripts.haistep.case   --config <config> --num-partitions 0 --num-workers 4
  python -m scripts.haistep.aidata --config <config>
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


The 00_develop pattern
-----------------------

Each pipeline stage has a paired develop task: `NN_<stage>_fn_develop_mimic/`
builds the Fns, `NN_<stage>_mimiciv/` runs the pipeline. Same number = same stage.

```
A01_data_pipeline_mimic/
  01_source_fn_develop_mimic/  + 01_source_mimiciv/
  02_record_fn_develop_mimic/  + 02_record_mimiciv/
  03_case_fn_develop_mimic/    + 03_case_mimiciv_mortality/
  04_aidata_fn_develop_mimic/  + 04_aidata_mimiciv_mortality/
```

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

See `fn/scaffold.md` for the detailed step-by-step. Summary:

  1. Identify project + task-group.
  2. Collect metadata (NN, name, stage, _meta block).
  3. Copy notebook template from `haistepnb/{N}_{stage}_nb.py`, set CONFIG default.
  4. Seed config from `ref/config-seed.yaml` (with partition fields for Stage 2+).
  5. Copy run-script from `../haipipe-task/ref/run-sh-template.sh`.
  6. Suggest next via cross-skill link.
  7. Emit return contract.


Execute flow
-------------

See `fn/execute.md` for the detailed step-by-step. Summary:

  1. Detect stage from script imports (SourceSet/RecordSet/CaseSet/AIData).
  2. Read config for partition_number and stage-specific args.
  3. Execute via notebook (run.sh) or CLI (python -m scripts.haistep.{stage}).
  4. Write results/<RUN>/runtime.yaml.
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

When `/haipipe-task plan` targets an existing task-folder of this type, the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     ← script-level phases for this type
../haipipe-task/ref/workflow-template.yaml  ← task-level template (Run/Gate1/Gate2)
```

Schema source of truth:
  project/haipipe-workflow/ref/plan-schema.md
