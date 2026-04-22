haipipe Plugin
===============

Skills for the haipipe pipeline — from raw data to trained models to deployed endpoints.
Covers all 6 stages plus a per-patient data contract and project scaffolding.


Skills
------

| Skill | Stages | What it covers |
|---|---|---|
| /haipipe-subject | 0-2 (per subject) | Per-subject `0-RawDataStore`, `1-SourceStore`, `2-RecStore` under `_WorkSpace/A-User-Store/UserGroup/Subject-*`. Read-only contract for inference/serving. |
| /haipipe-data | 1-4 (project-wide) | SourceFn, HumanFn, RecordFn, TriggerFn, CaseFn, TfmFn, SplitFn. Running pipelines, inspecting `_WorkSpace` assets. |
| /haipipe-nn | 5 | tefm, tsforecast, mlpredictor, tediffusion, bandit — all 4 layers (algorithm, tuner, instance, modelset/pipeline). |
| /haipipe-end | 6 | Endpoint packaging, inference functions (MetaFn/TrigFn/PostFn/Src2InputFn/Input2SrcFn), Databricks or local deploy. |
| /haipipe-project | — | New-project scaffolding, project review, `examples/` structure, script-result alignment. |

(Skill order: `-subject` for inference-time data, `-data/-nn/-end` for training-time pipeline, `-project` for scaffolding.)


Stage Map
---------

```
0-RawDataStore   →  1-SourceStore  →  2-RecStore  →  3-CaseStore  →  4-AIDataStore  →  5-ModelInstanceStore  →  6-EndpointStore
(dataset dumps)     (typed frames)    (records)      (cases)         (train tensors)    (trained weights)         (deployable)

                    └──────── project-wide stores in _WorkSpace/ ────────────┘

Per-subject slice (/haipipe-subject):
_WorkSpace/A-User-Store/UserGroup/Subject-{dataset}-{id}/
├── 0-RawDataStore/   ← subject's raw rows/files
├── 1-SourceStore/    ← subject's source frames
└── 2-RecStore/       ← subject's record(s)
   (3-6 NOT per-subject — those are for model dev; at inference the subject calls the endpoint)
```


Principle
---------

**Data contract split.** Project-wide stages 1-4 are for building models. Per-subject
stages 0-2 are for serving one subject's data to a deployed endpoint. The split mirrors
train-time vs. inference-time: the endpoint doesn't need 4-AIDataStore, it needs a
record.
