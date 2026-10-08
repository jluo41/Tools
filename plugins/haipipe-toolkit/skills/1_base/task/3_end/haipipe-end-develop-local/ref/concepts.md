haipipe-end-develop-local — Concepts
======================================

Local develop conventions.
This skill is a thin sequencer over `/haipipe-nn modelset` + `/haipipe-end-endpointset package`, so most of the "how it works" is in those skills.
This file covers the small amount of state this wrapper owns directly.

---

Local develop registry
----------------------

Records produced by this skill (one line per develop run):

```
_WorkSpace/.haipipe-end/develop-local-registry.tsv

run_id    timestamp_iso8601    modelset    endpoint_set_path    pid    log_path    status
```

Used by `dashboard`, `monitor`, `teardown`.
Treat the file as append-only during a run; rotate or clean up via `teardown <run_id>`.

---

Pid + log layout
----------------

For background runs (`develop ...
--bg`):

```
_WorkSpace/.haipipe-end/develop-local/<run_id>/
├── run.pid                   process id of the foreground driver
├── run.log                   combined stdout + stderr
└── manifest.yaml             run config snapshot (modelset, endpoint_set, args)
```

`monitor <run_id>`        →  `tail -f run.log` `teardown <run_id>`       →  `kill $(cat run.pid)` then optional cleanup of
                              the run directory

---

Sequencing semantics
--------------------

The two delegated calls are sequential, not parallel:

```
Step 1: nn modelset run     ──► must complete with status: ok
Step 2: endpointset package  ──► consumes Step 1's output
```

If Step 1 fails, do NOT attempt Step 2.
The combined `status` returned by this skill is `failed` in that case, with `summary` pointing at the failed step and `next` suggesting `/haipipe-nn modelset review`.

---

When to use this vs `-develop-sagemaker`
-----------------------------------------

```
                 local                       sagemaker
                 ─────                       ─────────
hardware         laptop / dev box            ml.m5.xlarge+ on AWS
data scale       small / sampled             full datasets
reproducibility  best effort                 pinned image + Pipeline params
output           synced 6-EndpointStore/      synced 6-EndpointStore/ + UC/Registry
duration         minutes                      minutes-to-hours
deploy targets   local / docker / sagemaker  any (sagemaker/databricks/local/mlflow)
```

Use local for:
  - Fast iteration on Tuner / Algorithm changes
  - Smoke-testing a new ModelSet config end-to-end before pipeline submit
  - Producing an Endpoint_Set for `-deploy-local` testing

Use sagemaker for:
  - Production / release artifacts (those need RegisterModel governance)
  - Anything involving full-scale data
  - Anything that has to be re-runnable by CI without a developer's laptop

---

Cross-skill boundaries
----------------------

This is a SEQUENCER skill.
The boundary is sharp:

```
                 ┌────────────────────┐         ┌─────────────────────────┐
─── develop ─►   │ /haipipe-nn        │ ──►    │ /haipipe-end-endpointset │
                 │  modelset run       │         │  package                 │
                 └────────────────────┘         └─────────────────────────┘
                         ▲                                ▲
                         │                                │
                         └──── owned by 2_nn              └──── owned by 3_end-endpointset

This skill (-develop-local) ONLY sequences the two calls.
                 If logic beyond sequencing is needed, push it into one of
                 the delegate skills, not into this wrapper.
```
