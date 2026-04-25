haipipe Plugin
===============

Skills for the haipipe pipeline — from raw data to trained models to deployed
endpoints. Covers all 6 stages plus a per-subject data contract and project
scaffolding.

**v2.0 layout** — five user-facing **umbrella** skills parse intent and
dispatch to per-stage / per-target / per-risk-profile **specialists**. You
only need to remember the umbrellas; specialists exist as real skills (each
with its own `SKILL.md`) but are normally called by the umbrella via `Skill()`.


User-facing surface (memorize only these)
------------------------------------------

```
/haipipe-data        Stages 1-4 orchestrator
/haipipe-nn          Stage 5 orchestrator
/haipipe-end         Stage 6 orchestrator (artifact + deploy targets)
/haipipe-project     project lifecycle orchestrator
/haipipe-subject     per-subject contract (standalone, not decomposed)
```

Each umbrella accepts:
  - Positional args (`/haipipe-data source cook`)
  - Flexible arg order (`/haipipe-data cook source`)
  - Aliases (`/haipipe-data 1 cook`, `/haipipe-data 1-source cook`)
  - Free-form natural language (`/haipipe-data "build a SourceFn for Dexcom"`)


Tier 1 — user-facing umbrellas
-------------------------------

| Umbrella | Stages | What it covers |
|---|---|---|
| `/haipipe-data` | 1-4 (project-wide) | SourceFn, RecordFn, CaseFn, TfmFn, SplitFn — pipeline runs, dashboards, reviews. Routes by stage. |
| `/haipipe-nn` | 5 | mlpredictor / tsforecast / tefm / tediffusion / bandit; algorithm / tuner / instance / modelset layers. Routes by layer. |
| `/haipipe-end` | 6 | Endpoint_Set artifact + deploy targets (SageMaker, Databricks, Flask, MLflow). Routes by artifact-vs-target. |
| `/haipipe-project` | — | Project scaffold / review / reorganize. Routes by risk profile (build / read / modify). |
| `/haipipe-subject` | 0-2 (per subject) | Per-subject `0-RawDataStore`, `1-SourceStore`, `2-RecStore`. Standalone — not decomposed. |


Tier 2 — specialists (called by umbrellas)
-------------------------------------------

Specialists each have their own `SKILL.md` and can be invoked directly for
power-user work, but the recommended entry is always the umbrella.


Folder layout
--------------

Skills are grouped into family folders under `skills/`. Folder names are
pure organization — only the `name:` field in each SKILL.md frontmatter
identifies the skill. Numeric prefixes follow the data flow order
(data → nn → end), then cross-cutting (project), then inference-time (subject).

```
skills/
├── 1_data/
│   ├── haipipe-data/                (umbrella — orchestrator)
│   ├── haipipe-data-source/         Stage 1 (SourceFn, HumanFn)
│   ├── haipipe-data-record/         Stage 2 (RecordFn, TriggerFn)
│   ├── haipipe-data-case/           Stage 3 (CaseFn)
│   └── haipipe-data-aidata/         Stage 4 (TfmFn, SplitFn)
│
├── 2_nn/
│   ├── haipipe-nn/                  (umbrella)
│   ├── haipipe-nn-algo/             L1 (Algorithm)
│   ├── haipipe-nn-tuner/            L2 (Tuner / hyperparameter sweep)
│   ├── haipipe-nn-instance/         L3 (ModelInstance materialization)
│   └── haipipe-nn-modelset/         L4 (ModelSet / pipeline composition)
│
├── 3_end/
│   ├── haipipe-end/                 (umbrella)
│   ├── haipipe-end-endpointset/     artifact lifecycle (package/design/test/review)
│   ├── haipipe-end-sagemaker/       target: AWS SageMaker
│   ├── haipipe-end-databricks/      target: Databricks Model Serving
│   ├── haipipe-end-flask/           target: local Flask / FastAPI HTTP
│   └── haipipe-end-mlflow/          target: MLflow registry + serve
│
├── 4_project/
│   ├── haipipe-project/             (umbrella)
│   ├── haipipe-project-new/         BUILD: scaffold new project
│   ├── haipipe-project-inspect/     READ: review, summarize, inventory, overview
│   └── haipipe-project-organize/    MODIFY: reorganize files
│
└── 5_subject/
    └── haipipe-subject/             standalone (per-subject inference contract)
```


Stage map
----------

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


Architecture
------------

**Umbrella -> Specialist contract.** Each umbrella SKILL.md owns:
  - Keyword tables (stage / layer / target / verb)
  - Intent parsing logic
  - `Skill("haipipe-<group>-<scope>", args=...)` dispatch
  - Cross-scope inline behaviors (cross-stage dashboards, overview/explain modes)

Each specialist SKILL.md owns:
  - Its scope-specific `ref/concepts.md` (or equivalent)
  - Stage/layer/target-specific procedures
  - A structured **return tail** the umbrella can parse:

```
status:    ok | blocked | failed
summary:   2-3 sentences
artifacts: [paths created, read, or modified]
next:      suggested next command
```

**Discipline.** Specialists never modify state owned by another specialist.
For example, target deployers (`-sagemaker`, `-databricks`, etc.) read the
Endpoint_Set produced by `-endpointset` but never modify it. If a deploy
fails because of an artifact issue, the fix lives in `-endpointset`, not in
the target skill.


Decomposition axes
-------------------

| Umbrella | Axis | Why |
|---|---|---|
| `/haipipe-data` | pipeline stage | 4 stages with distinct concepts and ref content |
| `/haipipe-nn` | model layer | 4 layers with distinct contracts |
| `/haipipe-end` | artifact vs. target | one artifact (Endpoint_Set) consumed by N target deployers |
| `/haipipe-project` | risk profile | build / read / modify need different `allowed-tools` |
| `/haipipe-subject` | — | content too small; per-subject semantic is the whole point |


Principle
---------

**Data contract split.** Project-wide stages 1-4 are for building models. Per-subject
stages 0-2 are for serving one subject's data to a deployed endpoint. The split mirrors
train-time vs. inference-time: the endpoint doesn't need 4-AIDataStore, it needs a
record.

**Skill-first development.** Make a skill work locally first, then wire it
into an umbrella's keyword table. The skill prompt is the source of truth.
