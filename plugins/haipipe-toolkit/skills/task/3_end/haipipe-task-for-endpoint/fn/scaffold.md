fn-scaffold: Scaffold an endpoint-packaging task-folder
========================================================

Package a trained ModelInstance_Set (Stage 5) into a deployable Endpoint_Set
(Stage 6) via `Endpoint_Pipeline`. Group letter is PROJECT-SPECIFIC
(orchestrator rule; follow the project's existing scheme); the default ABC
convention uses **C** for endpoint groups.

Output: `tasks/C{NN}_<group>/{NN}_<task_name>/` (or the project's letter).


Step 1 — Identify project + task-group
---------------------------------------

- Auto-detect project from cwd.
- AUTO_MODE: infer group from cwd or return `status: blocked`.
  Interactive: ASK task-group. Scaffold `C{NN}_<group_name>/` if needed
  (or the project's endpoint letter).


Step 2 — Collect metadata
--------------------------

- 2-digit NN: next free in this group.
- snake_case task_name (e.g., `package_mortality_xgb`).
- Source model: `modelinstance_name` + `modelinstance_version` (Stage 5,
  must have examples from ExampleConfig).
- Target: `endpoint_name` + `endpoint_version`.
- The 5 Fn names (MetaFn / TrigFn / PostFn / Src2InputFn / Input2SrcFn) —
  must exist in `code/haifn/fn_endpoint/`; author missing ones via
  `/haipipe-end design <fn-type>` first. Src2InputFn + Input2SrcFn are
  per-platform: pick the pair matching `deployment_config.platform`.
- `_meta:` block.


Step 3 — Create skeleton
-------------------------

```
C{NN}_<group>/
└── {NN}_<task_name>/
    ├── 1_<task_name>.py                exact copy of code/scripts/haistepnb/c_endpoint_nb.py
    ├── configs/
    │   └── run_<task_name>.yaml        from ref/config-seed.yaml
    ├── runs/
    │   └── run_<task_name>.sh          papermill runner
    ├── results/                        (created at runtime)
    └── notebooks/                      (created at runtime)
```

The task `.py` is an EXACT copy of the template — CONFIG is overridden at
runtime by papermill, never by editing the file (see SKILL.md).


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to `configs/run_<task_name>.yaml`. Fill:
- `_meta:` block.
- Source model block (`modelinstance_name`, `modelinstance_version` — no @ prefix).
- Target endpoint block (`endpoint_name`, `endpoint_version`).
- The 5 Fn names.
- `deployment_config` (platform: local | databricks | sagemaker).


Step 5 — Run-script
--------------------

Copy `../../../haipipe-task/ref/run-sh-template.sh` to `runs/run_<task_name>.sh`.
Set `TASK_NAME="{NN}_{task_name}"`. The body sources `.venv` + `env.sh`
(Endpoint_Pipeline needs the haipipe import path + store env vars).


Step 6 — Execute + verify (per SKILL.md pipeline flow)
-------------------------------------------------------

`bash runs/run_<task_name>.sh` drives c_endpoint_nb.py:
load ModelInstance_Set → Endpoint_Pipeline.run() → save to 6-EndpointStore/
→ verify every example has payload.json → test inference on sample payloads
→ package .tar.gz. See SKILL.md "Pipeline flow" for the step list and
`../../haipipe-end/ref/0-overview.md` for the Endpoint_Set layout contract.


Step 7 — Cross-skill link + report
-----------------------------------

After a successful package, suggest:
- `/haipipe-end deploy <target> <endpoint>` for deployment.
- `/haipipe-end profile <endpoint>` for an ad-hoc latency breakdown.

```
status:    ok
summary:   Scaffolded endpoint-packaging task <NN>_<name> under <G>{NN}_<group>.
artifacts: [paths created]
next:      bash runs/run_<task_name>.sh, then /haipipe-end deploy <target>
```


MUST NOT
---------

- Edit the copied c_endpoint_nb.py body (config-driven only).
- Package a ModelInstance_Set that has no examples (payload generation needs them).
- Mutate an existing `_WorkSpace/6-EndpointStore/` entry — new version, new folder.
- Create `README.md`.
