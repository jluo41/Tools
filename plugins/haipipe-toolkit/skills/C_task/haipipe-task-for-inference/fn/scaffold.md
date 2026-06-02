fn-scaffold: Scaffold an inference-performance task-folder
===========================================================

Profile a packaged Endpoint_Set's inference latency; produce a per-step
breakdown under `results/<run>/`. Group letter default: **P** (Performance).

Output: `tasks/P{NN}_<group>/{NN}_<task_name>/`.


Step 1 — Identify project + task-group  (placement decision)
------------------------------------------------------------

- Auto-detect project from cwd.
- DECIDE placement (see SKILL.md "Placement"):
  • If the project HAS an endpoint group (the one that built the Endpoint_Set,
    e.g. `C_endpoint/` with a `*_endpoint` build task) → CO-LOCATE there as a
    sibling: `<EndpointGroup>/<N>_inference_profile/`. Do NOT make a P group.
    Use the project's local task-numbering (e.g. `C2_inference_profile`) and a
    cohort-agnostic folder name + per-cohort config.
  • Else (no endpoint group / standalone) → ASK task-group; group letter **P**,
    scaffold `P{NN}_<group_name>/` if needed.


Step 2 — Collect metadata
--------------------------

- 2-digit NN: next free in this group.
- snake_case task_name (e.g., `profile_smsr4_slearner`, `latency_clickpred`).
- Target Endpoint_Set: path under `_WorkSpace/6-EndpointStore/`
  (e.g. `endpoint_sms_clickpred_v0001smsr4-slenteng`).
- Sample payload: a path to a `payload.json` (usually the endpoint's own
  `examples/example_001/payload.json`).
- warm_iterations: how many warm calls to median over (default 5).
- decompose_model_inference: true → time the per-arm loop sub-components.
- `_meta:` block.


Step 3 — Create skeleton
-------------------------

```
P{NN}_<group>/
└── {NN}_<task_name>/
    ├── {NN}_<task_name>.py
    ├── configs/
    │   └── profile_<endpoint>.yaml         from ref/config-seed.yaml
    ├── runs/
    │   └── profile_<endpoint>.sh
    ├── results/
    │   └── <run>/                          latency.json, breakdown.txt
    └── notebooks/
```


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to `configs/profile_<endpoint>.yaml`. Fill:
- `_meta:` block.
- `endpoint_set_path` (under 6-EndpointStore).
- `payload_path`.
- `ProfileArgs:` (warm_iterations, decompose_model_inference, arm_sweep).


Step 5 — Run-script
--------------------

Copy `../haipipe-task/ref/run-sh-template.sh` to `runs/profile_<endpoint>.sh`.
Set `TASK_NAME="{NN}_{task_name}"`. The body sources `.venv` + `env.sh`
(the profiler loads the real Endpoint_Set, needs the haipipe import path).


Step 6 — Author the `<TASK>.py` body  (code-creator-for-inference does this)
----------------------------------------------------------------------------

The body MUST:
- `Endpoint_Set.load_from_disk(endpoint_set_path, SPACE)`.
- run ONE warm-up call (silences the cold model-load).
- run `inference(payload, profile=True)` × `warm_iterations`; median each key.
- if `decompose_model_inference`: monkeypatch `mi._add_treatment_columns` and
  `mi.model_tuner.infer` with timers to split model_inference into
  (per-arm dataset-transform) vs (csr build + xgb predict).
- write `results/<run>/latency.json` + a readable `breakdown.txt`.

See `ref/inference-perf-notes.md` for the harness shape + the anti-patterns.


Step 7 — Cross-skill link + report
-----------------------------------

After scaffolding, suggest:
- `/haipipe-end-endpointset profile <endpoint>` for the same breakdown ad-hoc.
- `/haipipe-task-for-display` to chart latency across model releases.

```
status:    ok
summary:   Scaffolded inference-perf task <NN>_<name> under P{NN}_<group>.
artifacts: [paths created]
next:      run the profile, then /haipipe-task-for-display
```


MUST NOT
---------

- Report cold-call latency as "the" number — warm up, report warm medians.
- Skip the model_inference decomposition — that is the whole point.
- Use HuggingFace Dataset for any custom timing fixture (it is the thing
  being diagnosed; use numpy/scipy if you build a synthetic input).
- Mutate `_WorkSpace/6-EndpointStore/` (read-only).
- Create `README.md`.
