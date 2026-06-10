---
name: haipipe-task-for-inference
description: "inference-performance task-folder build specialist. Scaffolds {NN}_<name>/ task-folders under P-series task-groups that PROFILE a packaged Endpoint_Set's inference — per-step latency breakdown + per-arm scoring decomposition land in results/<run>/latency.json. Operates on Stage-6 artifacts (6-EndpointStore), not the model instance. Called by /haipipe-task orchestrator when task-type=inference. Cross-references /haipipe-end-endpointset (the profile verb)."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-06-01"
  summary: "inference-performance (latency profiling) task-folder build specialist."
  changelog:
    - "1.0.0 (2026-06-01): created — inference latency profiling as a first-class task type (group P)."
---

Skill: haipipe-task-for-inference
=================================

Scaffolds an **inference-performance task-folder**. Consumes a packaged
Endpoint_Set (Stage 6, from `_WorkSpace/6-EndpointStore/`); produces a
per-step LATENCY breakdown + the per-arm scoring decomposition under
`results/<run>/latency.json`.

This is NOT model accuracy (that's `for-eval`). This measures WHERE the
inference wall-clock goes — so a slow endpoint can be diagnosed and fixed.

**Invocation modes (see `../haipipe-task/ref/invocation-modes.md`):**
interactive (a human steers; missing fields get ASKed) OR headless (a full
spec → run silently). `code-creator-for-inference-agent` calls this skill
headless during fan-out, then authors the `<TASK>.py` body. Always end with
the structured return block.


Position in the series
----------------------

```
/haipipe-task-for-data            data-pipeline          (group D)
/haipipe-task-for-algo            algo-dev demo
/haipipe-task-for-training        model training         (group A, Stage 5)
/haipipe-task-for-eval            model evaluation        (group B — accuracy)
/haipipe-task-for-inference  ◀──  inference performance   (group P — LATENCY)  ← here
/haipipe-task-for-display         paper figure / table    (group C)
/haipipe-task-for-individual      individual-centric query
/haipipe-task-for-agent           LLM agent call
```

`for-eval` answers "is the model RIGHT?"  ·  `for-inference` answers
"is the endpoint FAST, and if not, WHERE is the time?"


What this scaffolds
-------------------

```
tasks/P{NN}_<group_name>/                    ← P-series group (inference perf)
└── {NN}_<task_name>/
    ├── {NN}_<task_name>.py
    ├── configs/
    │   └── profile_<endpoint>.yaml          seeded from ref/config-seed.yaml
    ├── runs/
    │   └── profile_<endpoint>.sh
    ├── results/
    │   └── <run>/                           latency.json, breakdown.txt
    └── notebooks/
```

Group letter default: **P** (Performance / Profiling). If P is not yet
registered in the orchestrator's task-type table, fall back to B and note it.
Heavy outputs: none — `results/<run>/` is all light artifacts.


Placement — prefer co-locating with the endpoint group
-------------------------------------------------------

An inference-profile task PROFILES a packaged Endpoint_Set. So when the
project already organizes work by lifecycle stage and has an **endpoint
group** (the one that builds the Endpoint_Set), co-locate the profile task
THERE as a sibling of the endpoint-build task — do NOT spin up a separate
P-series group. The endpoint group then owns the whole endpoint lifecycle:
build → profile.

```
  tasks/C_endpoint/                    ← the endpoint group (project-local letter)
  ├── C1_endpoint/                     builds the Endpoint_Set (Stage 6 package)
  └── C2_inference_profile/            profiles what C1 builds  ← THIS task
      ├── inference_profile.py         cell-marked (mirrors the eval task's *_report.py)
      ├── configs/profile_<cohort>.yaml    cohort = config variant (not a new folder)
      ├── runs/run_<cohort>.sh
      └── results/<run>/  notebooks/
```

Decision rule:
  - Project has an endpoint group (built via /haipipe-end)  → co-locate as
    `<EndpointGroup>/<N>_inference_profile/`, sibling of the build task.
    Cohort-agnostic folder name + per-cohort config (mirror the eval task).
  - Standalone / fresh project, no endpoint group              → use the
    P-series group (`tasks/P{NN}_<group>/`) per the table above.

Worked example (real): `examples/ProjA-Click-01-ClickPred/tasks/C_endpoint/
C2_inference_profile/` — profiles `endpoint_sms_clickpred_v0001smsr4-slenteng`,
records the before/after of the vectorized _compute_scores fix (model_inference
3692 ms → ~19 ms, total 3746 → ~85 ms, scores byte-identical). It sits next to
`C1_endpoint/` (which packaged that endpoint). This co-location overrides the
global P-letter rule by design — the task is endpoint-scoped.


What the `<TASK>.py` measures
-----------------------------

The built-in instrumentation is `endpoint_set.inference(payload, profile=True)`,
which returns a `timing` dict with per-step keys. The task body:

```
1. load the Endpoint_Set:  Endpoint_Set.load_from_disk(<6-EndpointStore path>, SPACE)
2. warm-up once (first call loads + caches the model — cold start)
3. run profiled inference × N warm iterations on a sample payload
4. report per-step medians:
     load_functions · trig_fn · input2src_fn · prefn_pipeline ·
     model_inference · post_fn · total_ms · slowest_step
5. DECOMPOSE model_inference (the arm-dependent step) into:
     - the per-arm dataset-transform cost  (the O(arms^2) HF-Dataset trap)
     - the actual model_tuner.infer cost    (csr build + xgb predict)
   by timing _add_treatment_columns vs model_tuner.infer.
6. (optional) arm-count sweep / concurrency sweep
7. write results/<run>/latency.json + a human breakdown.txt
```

See `ref/inference-perf-notes.md` for the known anti-patterns this task
exists to catch (chiefly: HuggingFace Dataset ops in the per-arm loop).


Cross-reference to endpoint skill
----------------------------------

`/haipipe-end-endpointset profile <endpoint>` runs the SAME breakdown ad-hoc
(no task-folder). Use this `for-inference` skill when you want the profile
recorded as a reproducible, versioned task (e.g. to track latency across
model releases, or to A/B a vectorization fix). The endpointset `profile`
verb is the quick one-off; this is the durable artifact.


Scaffold flow
-------------

See `fn/scaffold.md`. Summary:

  1. Identify project + task-group (letter P).
  2. Collect metadata (NN, name, target endpoint, payload, iterations, _meta).
  3. Create skeleton (.py, configs/, runs/, results/, notebooks/).
  4. Seed config from `ref/config-seed.yaml`.
  5. Copy run-script from `../haipipe-task/ref/run-sh-template.sh`.
  6. Suggest next via cross-skill link.
  7. Emit return contract.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded
artifacts: [paths created]
next:      run the profile, then /haipipe-task-for-display for a latency chart
```


MUST NOT
---------

- Measure accuracy here — that is `for-eval`. This is latency only.
- Report only the cold (first) call — always warm up, report warm medians.
- Skip the model_inference DECOMPOSITION — the per-step total hides whether
  the cost is the arm loop (fixable by vectorizing) or the data transform.
- Mutate any file under `_WorkSpace/6-EndpointStore/` (read-only).
- Create `README.md`.



Workflow plan
--------------

When `/haipipe-task plan` targets an existing task-folder of this type,
the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     ← script-level phases for this type
../haipipe-task/ref/workflow-template.yaml  ← task-level template (Run/Gate1/Gate2)
```

Schema source of truth:
  B_project/haipipe-workflow/ref/plan-schema.md
