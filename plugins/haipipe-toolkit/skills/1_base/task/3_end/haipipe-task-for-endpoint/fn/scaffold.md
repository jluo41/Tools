fn-scaffold: Scaffold an endpoint-packaging job
========================================================

Package a trained ModelInstance_Set (Stage 5) into a deployable Endpoint_Set (Stage 6) via `Endpoint_Pipeline`.
Output: `work/bNN_<endpoint_block>/jNN_<endpoint_job>/tNN_<task>/`.


Step 1 — Identify project + block
---------------------------------------

- Auto-detect project from cwd.
- AUTO_MODE: infer the Block and Job from cwd or return `status: blocked`.
  Interactive: ASK block. Scaffold canonical `bNN_<block_name>/` if needed.


Step 2 — Collect metadata
--------------------------

- 2-digit NN: the next free Task index tNN in this Job.
- snake_case task_name (e.g., `package_mortality_xgb`).
- Source model: `modelinstance_name` + `modelinstance_version` (Stage 5,
  must have examples from ExampleConfig).
- Target: `endpoint_name` + `endpoint_version`.
- The 5 Fn names (MetaFn / TrigFn / PostFn / Src2InputFn / Input2SrcFn) —
  must exist in `code/haifn/fn_endpoint/`; author missing ones via
  `/haipipe-end design <fn-type>` first. Src2InputFn + Input2SrcFn are
  per-platform: pick the pair matching `deployment_config.platform`.
- `_meta:` block.


Step 3 — Create canonical nested Task Folder
---------------------------------------------

```
work/bNN_<block>/
└── jNN_<job_name>/
    ├── t01_<task_name>/
    │   ├── t01_<task_name>.md          Page Face · folder-kind/task-type
    │   ├── scripts/
    │   │   └── <task_name>.py          exact copy of c_endpoint_nb.py (the worker)
    │   ├── runs/r01_base/              one folder per Run
    │   │   ├── r01_base.sh             papermill runner (the ticket)
    │   │   ├── config.yaml             from ref/config-seed.yaml
    │   │   ├── run.yaml                its card (role: make)
    │   │   └── result/                 created at runtime
    │   ├── workflow/                   plan/report + inbox/application/
    │   └── notebooks/r01_base.ipynb
    └── src/
```

The Task Page declares `folder-kind: task`, `task-type: endpoint`, and `task: .`.
The task `.py` is an EXACT copy of the template — CONFIG is overridden at
runtime by papermill, never by editing the file (see SKILL.md). Legacy flat
endpoint jobs remain readable but are never scaffolded.


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to
`t01_<task_name>/runs/r01_base/config.yaml` (`scripts/config/r01_base.yaml` in a Block not yet moved).
Fill:
- `_meta:` block.
- Source model block (`modelinstance_name`, `modelinstance_version` — no @ prefix).
- Target endpoint block (`endpoint_name`, `endpoint_version`).
- The 5 Fn names.
- `deployment_config` (platform: local | databricks | sagemaker).
- `external_contract` when enrichment is used: release, Source schema
  version, and vector order versions.


Step 5 — Run-script
--------------------

Copy `../../../haipipe-task/ref/run-sh-template.sh` to
`t01_<task_name>/runs/r01_base/r01_base.sh`, and write its `run.yaml` card.
Set `TASK_NAME="<task_name>"`: the worker's file name without `.py` (the ticket runs
`scripts/$TASK_NAME.py`), never the Task folder name `t01_<task_name>`.
The body sources `.venv` + `env.sh` (Endpoint_Pipeline needs the haipipe import path + store env vars).


Step 6 — Execute + verify (per SKILL.md pipeline flow)
-------------------------------------------------------

`bash t01_<task_name>/runs/r01_base/r01_base.sh` drives c_endpoint_nb.py: load
ModelInstance_Set → Endpoint_Pipeline.run() → save to 6-EndpointStore/ → verify
every example has payload.json → test inference on sample payloads → package
.tar.gz.
The verification compares training SourceFn and serving Input2SrcFn ProcessDF
schemas/values, including vector fields and external release metadata.
See SKILL.md "Pipeline flow" for the step list and `../../haipipe-end/ref/0-overview.md` for the Endpoint_Set layout contract.


Step 7 — Cross-skill link + report
-----------------------------------

After a successful package, suggest:
- `/haipipe-end deploy <target> <endpoint>` for deployment.
- `/haipipe-end profile <endpoint>` for an ad-hoc latency breakdown.

```
status:    ok
summary:   Scaffolded endpoint Task tNN_<task> under bNN_<block>/jNN_<job>.
artifacts: [paths created]
next:      bash t01_<task_name>/runs/r01_base/r01_base.sh, then /haipipe-end deploy <target>
```


MUST NOT
---------

- Edit the copied c_endpoint_nb.py body (config-driven only).
- Package a ModelInstance_Set that has no examples (payload generation needs them).
- Mutate an existing `_WorkSpace/6-EndpointStore/` entry — new version, new folder.
- Create `README.md`.
- Put Task code, config, runs, or workflow material at the job root.
