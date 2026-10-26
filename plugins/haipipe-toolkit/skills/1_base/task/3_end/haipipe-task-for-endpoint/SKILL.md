---
name: haipipe-task-for-endpoint
description: "Endpoint task specialist: scaffolds and executes one nested task that packages a trained ModelInstance_Set into a deployable Stage 6 Endpoint_Set via c_endpoint_nb.py. Called by /haipipe-task when task-type is endpoint; cross-references /haipipe-end for Fn authoring and deploy targets."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
disable-model-invocation: true
metadata:
  version: "0.4.1"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-endpoint
=================================

Scaffolds an **endpoint Job with one nested Task Folder** under canonical BJTR.
The Task (its face is the page a reader opens; a Task is not a Page, JL 261011) takes a trained
ModelInstance_Set (Stage 5, with examples) and packages it into a
self-contained Endpoint_Set (Stage 6) using `Endpoint_Pipeline`.

The task `.py` is an exact copy of `code/scripts/haistepnb/c_endpoint_nb.py`.
CONFIG is overridden at runtime by papermill, NOT by editing the file.

**Invocation modes:** interactive (human steers) OR headless
(`haipipe-task-creator-agent` calls this skill during Phase 2: Build). Legacy
flat endpoint jobs remain readable; every new scaffold uses the nested
`jNN_*/tNN_*/` Task shape owned by `haipipe-task`.

## Type contract

```yaml
task-type: endpoint
skill: haipipe-task-for-endpoint
does: Packages one trained ModelInstance_Set (Stage 5, with examples) into a deployable Endpoint_Set (Stage 6) and tests inference on its example payloads.
worker: scripts/<task_name>.py (Python), an exact copy of code/scripts/haistepnb/c_endpoint_nb.py that papermill runs with the Run's config
config: runs/<run>/config.yaml (seeded from ref/config-seed.yaml), or scripts/config/<run>.yaml in a Block not yet moved
ticket: runs/<run>/<run>.sh, from ../../haipipe-task/ref/run-sh-template.sh (TASK_NAME <task_name>, the worker; it sources .venv and env.sh and runs papermill)
result: $OUTPUT_ROOT/<task>/runs/<run>/result/, with runtime.yaml and metrics.json (REQUIRED_RESULTS, the template default) before the receipt says complete, plus inference_test.json
heavy: _WorkSpace/6-EndpointStore/<endpoint_name>/ (the Endpoint_Set and its .tar.gz, in the stage store)
roles: [make]
companions: [haipipe-end, haipipe-task-for-fit]
plan_sample: ref/workflow-plan-sample.yaml
```


Position in the pipeline
------------------------

```
Data (Stages 1-4) → Model (Stage 5) → Endpoint (Stage 6) → Deploy

haipipe-task-for-data   haipipe-task-for-fit   haipipe-task-for-endpoint
                                                       ↓
                                               /haipipe-end deploy <target>
```


What this scaffolds
-------------------

```
work/bNN_<endpoint-block>/
└── jNN_<endpoint-job>/
    ├── t01_<task_name>/
    │   ├── t01_<task_name>.md       ← Page Face (`folder-kind: task`)
    │   ├── scripts/
    │   │   └── <task_name>.py       ← exact copy of c_endpoint_nb.py (the worker)
    │   ├── runs/
    │   │   └── r01_base/            ← one folder per Run
    │   │       ├── r01_base.sh      ← papermill runner (the ticket)
    │   │       ├── config.yaml      ← endpoint config
    │   │       ├── run.yaml         ← its card (role: make)
    │   │       └── result/          ← created at runtime: runtime.yaml, metrics.json, inference_test.json
    │   ├── workflow/                ← Task Face: plan/report + inbox/
    │   │   └── inbox/application/   ← immutable X2 candidates, when present
    │   └── notebooks/r01_base.ipynb
    └── src/                         ← only if shared by multiple Tasks
```

A Block not yet moved still has the flat `runs/r01_base.sh`, `scripts/config/r01_base.yaml` and
`results/r01_base/`; the ticket template runs both.

The Page Face declares `folder-kind: task`, `task-type: endpoint`, and
`task: .`. An X2 writer may add only a proposed packet under
`workflow/inbox/application/`; Plan/Build/Execute/Report remain owned by the
endpoint Task. Cross-Folder evidence later enters a consumer through its
Supporting/local Run graph, never through a scaffolded binding lane.


Config YAML structure
---------------------

Seeded from `ref/config-seed.yaml`:

```yaml
# Source model (Stage 5)
modelinstance_name: "<name>"
modelinstance_version: "<version>"

# Target endpoint (Stage 6)
endpoint_name: "<endpoint_name>"
endpoint_version: "<version>"

# 5 Inference function names (must exist in code/haifn/fn_endpoint/)
MetaFn:      "<MetaFnName>"
TrigFn:      "<TrigFnName>"
PostFn:      "<PostFnName>"
Src2InputFn: "<Src2InputFnName>"
Input2SrcFn: "<Input2SrcFnName>"

deployment_config:
  environment: "dev"
  platform: "local"     # local | databricks | sagemaker

# Required when SourceFn/Input2SrcFn uses external data
external_contract:
  release: "@<release>"
  source_schema_version: "<version>"
  vector_order_versions: {}
```


Pipeline flow (c_endpoint_nb.py steps)
---------------------------------------

```
[1] Load ModelInstance_Set (with examples from ExampleConfig)
[2] Endpoint_Pipeline.run()
    → loads examples from ModelInstance_Set.examples_data
    → Src2InputFn(ProcName_to_ProcDf) → payload.json per example
    → packages Endpoint_Set
[3] Save to 6-EndpointStore/
[4] Verify examples have payload.json
[5] Test inference with sample payloads
[6] Package for deployment (.tar.gz)
```

Packaging also verifies the training SourceFn versus serving Input2SrcFn
ProcessDF parity and records the external release plus Source vector
schema/order versions in `manifest.json`.

Output structure:

```
6-EndpointStore/{endpoint_name}/   (canonical layout: ../../haipipe-end/ref/0-overview.md)
├── model/                    ← copied from ModelInstance_Set
├── code/                     ← codebase snapshot (haipipe, hainn, haifn)
├── external/                 ← pinned release used by SourceFn/Input2SrcFn
├── examples/                 ← from ModelInstance_Set + payload.json
│   ├── example_000/
│   │   ├── ProcName_to_ProcDf/   real source data (parquet)
│   │   ├── payload.json          generated by Src2InputFn
│   │   ├── example_info.json     case identifiers
│   │   ├── prediction_results.json
│   │   └── df_case_example.json
│   └── ...
├── meta.json                 ← MetaFn output (name mappings + metadata)
└── manifest.json             ← config + full lineage chain
```


Prerequisites
--------------

1. **Stage 5 complete** with examples:
   - `ModelInstance_Set` must have `examples_data` (from `ExampleConfig` in training config)
   - Each example has `ProcName_to_ProcDf/` (real patient source data as parquet)

2. **5 Fns authored** in `code/haifn/fn_endpoint/`:
   - Build via the endpoint fn_develop task folder’s `{a1,b1,c1,d1,e1}_build_*.py` (legacy: `code-dev/1-PIPELINE/6-Endpoint-WorkSpace/`)
   - OR use `/haipipe-end <fn-type> design` interactively

3. **ExampleConfig in the fit Task's training config**:
   ```yaml
   ExampleConfig:
     enabled: true
     ExampleFnName: <name>
     num_examples: 3
   ```


Execution
----------

CLI (A layer):
```bash
python code/scripts/haistepcli/endpoint.py \
    --config <project>/work/bNN_<block>/jNN_<job>/t01_<task_name>/runs/r01_base/config.yaml
```

Notebook (B layer — papermill):
```bash
papermill 1_endpoint_*.ipynb output.ipynb \
    -p CONFIG <project>/work/bNN_<block>/jNN_<job>/t01_<task_name>/runs/r01_base/config.yaml
```


After packaging → deploy
--------------------------

```
/haipipe-end deploy local <endpoint>       ← FastAPI on localhost
/haipipe-end deploy databricks <endpoint>  ← Databricks Model Serving
/haipipe-end deploy sagemaker <endpoint>   ← AWS SageMaker
```

Latency profiling (formerly this skill's scope) is now a verb:
```
/haipipe-end profile <endpoint>
```


Cross-references
-----------------

- `/haipipe-end` — Fn authoring, endpointset verbs, deploy targets
- `/haipipe-task fit` — training (produces the ModelInstance_Set)
- `/haipipe-task data` — data pipeline (produces the AIDataSet)
- `code/scripts/haistepnb/c_endpoint_nb.py` — the template
- `code/scripts/haistepcli/endpoint.py` — the CLI entry point
- `ref/notebook-templates.md` (in haipipe-task-for-data) — full ABC template guide


Scaffold flow
-------------

  1. Identify project + canonical `bNN_*` Block and `jNN_*` Job.
  2. Collect metadata (NN, name, model ref, 5 Fn names, _meta).
  3. Create `t01_<task_name>/t01_<task_name>.md` and `workflow/`.
  4. Copy `c_endpoint_nb.py` to `t01_<task_name>/scripts/<task_name>.py`
     (exact copy).
  5. Seed `runs/r01_base/config.yaml` from `ref/config-seed.yaml`.
  6. Create `runs/r01_base/r01_base.sh` from the shared template (`TASK_NAME="<task_name>"`,
     the worker) and its `run.yaml` card.
  7. Emit return contract.


MUST NOT
---------

- Edit the template `.py` — it is an exact copy of `c_endpoint_nb.py`.
- Put project configs in `code/scripts/haistepconfig/` — those are reference templates only.
- Skip `ExampleConfig` in training — without examples, no `payload.json`.
- Create `README.md`.
- Put Task-owned code/config/runs at the job root; new work uses the nested
  Task Folder.
- Follow an unpinned host-level ExternalStore release or call a live API from
  Input2SrcFn.


Return contract
---------------

```
status:     ok | blocked | failed
task_folder: <path to scaffolded task folder>
run_name:   r01_base
artifacts:  [t01_<task_name>.md, scripts/<task_name>.py, runs/r01_base/r01_base.sh,
             runs/r01_base/config.yaml, runs/r01_base/run.yaml]
next:       run the task, then /haipipe-end deploy <target>
```
