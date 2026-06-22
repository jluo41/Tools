haipipe Plugin
===============

Skills for the haipipe pipeline — from raw data to trained models to deployed endpoints. Covers all 6 stages plus a per-individual data contract and project scaffolding.

**v2.0 layout** — five user-facing **umbrella** skills parse intent and dispatch to per-stage / per-target / per-risk-profile **specialists**. You only need to remember the umbrellas; specialists exist as real skills (each with its own `SKILL.md`) but are normally called by the umbrella via `Skill()`.


Two organizing axes
-------------------

The toolkit is laid out along **two orthogonal axes**. They are not siblings — they meet at one point (a `task` run), and you usually use both.

```
Task      0–6   ENGINEERING substrate — "how data becomes a model and ships"
                1_data → 2_nn → 3_end → 4_individual
                produces the Stores (RawData → … → Endpoint).
                Driven by /haipipe-data, /haipipe-nn, /haipipe-end,
                /haipipe-individual, /haipipe-project.
                ► THIS README documents the task-domain axis.

Research        RESEARCH lifecycle — "how to turn runs into trustworthy,
                publishable science"
                discover → project → task → probe → insight
                → paper → application
                Driven by /haipipe-discover, /haipipe-task, /haipipe-probe,
                /haipipe-insight, /haipipe-application, and the paper commands.
                ► See MENTAL_MODEL.md (the model) and USAGE.md (the recipes).
                ► See blueprints/ for expected end-to-end project run shapes.
```

The seam between the axes is `task`: a task's `run.sh` *executes* a stage of
the task-domain pipeline and emits `metrics.json`; the research layer wraps
those runs with scientific bookkeeping (DIKW cards, probe arms, claims).

Glossary (one concept, three names you will see):

```
probe   = the concept (a claim-directed probe)
probe = the folder name (skills/probe/, probes/)
/haipipe-probe = the command
```


User-facing surface (memorize only these)
------------------------------------------

```
/haipipe-data        Stages 1-4 orchestrator
/haipipe-nn          Stage 5 orchestrator
/haipipe-end         Stage 6 orchestrator (artifact + deploy targets)
/haipipe-project     project lifecycle orchestrator
/haipipe-individual     per-individual contract (standalone, not decomposed)
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
| `/haipipe-end` | 6 | 3-axis router: per-Fn-type (meta/trig/post/src2input/input2src), artifact-as-whole (endpointset), and deploy target (sagemaker/databricks/local/mlflow). |
| `/haipipe-project` | — | Project scaffold / review / reorganize. Routes by risk profile (build / read / modify). |
| `/haipipe-individual` | 0-2 (per individual) | Per-individual `0-RawDataStore`, `1-SourceStore`, `2-RecStore`. Standalone — not decomposed. |


Tier 2 — specialists (called by umbrellas)
-------------------------------------------

Specialists each have their own `SKILL.md` and can be invoked directly for power-user work, but the recommended entry is always the umbrella.


Folder layout
--------------

Skills are grouped into family folders under `skills/`. Folder names are pure
organization — only the `name:` field in each SKILL.md frontmatter identifies
the skill. Data, NN, endpoint, and individual inference now live inside
`task/` as task-domain families.

```
skills/
├── task/
│   ├── haipipe-task/                lifecycle hub: Plan / Build / Execute / Report
│   ├── haipipe-task-for-*/          task-type bridge specialists
│   │
│   ├── 1_data/
│   │   ├── haipipe-data/            (umbrella — orchestrator)
│   │   ├── haipipe-data-source/     Stage 1 (SourceFn, HumanFn)
│   │   ├── haipipe-data-record/     Stage 2 (RecordFn, TriggerFn)
│   │   ├── haipipe-data-case/       Stage 3 (CaseFn)
│   │   └── haipipe-data-aidata/     Stage 4 (TfmFn, SplitFn)
│   │
│   ├── 2_nn/
│   │   ├── haipipe-nn/              (umbrella)
│   │   ├── haipipe-nn-algo/         L1 (Algorithm)
│   │   ├── haipipe-nn-tuner/        L2 (Tuner / hyperparameter sweep)
│   │   ├── haipipe-nn-instance/     L3 (ModelInstance materialization)
│   │   └── haipipe-nn-modelset/     L4 (ModelSet / pipeline composition)
│   │
│   ├── 3_end/
│   │   ├── haipipe-end/             (umbrella — 4-axis router)
│   │   ├── haipipe-end-endpointset/ artifact-as-whole
│   │   ├── haipipe-end-meta/        per-Fn-type: MetaFn
│   │   ├── haipipe-end-trig/        per-Fn-type: TrigFn
│   │   ├── haipipe-end-post/        per-Fn-type: PostFn
│   │   ├── haipipe-end-src2input/   per-Fn-type: Src2InputFn
│   │   ├── haipipe-end-input2src/   per-Fn-type: Input2SrcFn
│   │   └── haipipe-end-deploy-*/    deploy targets
│   │
│   └── 4_individual/
│       ├── haipipe-individual/                  per-individual data contract
│       ├── haipipe-individual-inference/        per-individual inference run
│       ├── haipipe-individual-inference-report/ report persona
│       └── haipipe-individual-inference-judge/  judge persona
│
├── project/                       (cross-cutting — research axis)
│   ├── haipipe-project/             (umbrella)
│   ├── haipipe-project-inspect/     READ: review, summarize, inventory, overview
│   └── haipipe-project-organize/    MODIFY: reorganize files
```

Note: research families (`discover/`, `project/`, `task/`, `probe/`,
`insight/`, `paper/`, `application/`, `narrative/`) live under `skills/`.
The numbered execution families are now nested under `task/`. Folder name is
organization only — a skill is identified solely by its `name:` frontmatter.


Stage map
----------

```
0-RawDataStore   →  1-SourceStore  →  2-RecStore  →  3-CaseStore  →  4-AIDataStore  →  5-ModelInstanceStore  →  6-EndpointStore
(dataset dumps)     (typed frames)    (records)      (cases)         (train tensors)    (trained weights)         (deployable)

                    └──────── project-wide stores in _WorkSpace/ ────────────┘

Per-individual slice (/haipipe-individual):
_WorkSpace/A-User-Store/UserGroup/Subject-{dataset}-{id}/
├── 0-RawDataStore/   ← individual's raw rows/files
├── 1-SourceStore/    ← individual's source frames
└── 2-RecStore/       ← individual's record(s)
   (3-6 NOT per-individual — those are for model dev; at inference the individual calls the endpoint)
```


Architecture
------------

**Umbrella → Specialist contract.** Each umbrella SKILL.md owns:
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

**Discipline.** Specialists never modify state owned by another specialist. For example, target deployers (`-sagemaker`, `-databricks`, etc.) read the Endpoint_Set produced by `-endpointset` but never modify it. If a deploy fails because of an artifact issue, the fix lives in `-endpointset`, not in the target skill.


Decomposition axes
-------------------

| Umbrella | Axis | Why |
|---|---|---|
| `/haipipe-data` | pipeline stage | 4 stages with distinct concepts and ref content |
| `/haipipe-nn` | model layer | 4 layers with distinct contracts |
| `/haipipe-end` | Fn-type / artifact / deploy-target | 5 inference Fn-types (meta/trig/post/src2input/input2src), 1 artifact-as-whole (endpointset), 4 deploy targets (sagemaker/databricks/local/mlflow); umbrella picks axis from intent |
| `/haipipe-project` | risk profile | build / read / modify need different `allowed-tools` |
| `/haipipe-individual` | — | content too small; per-individual semantic is the whole point |


Principle
---------

**Data contract split.** Project-wide stages 1-4 are for building models. Per-individual stages 0-2 are for serving one individual's data to a deployed endpoint. The split mirrors train-time vs. inference-time: the endpoint doesn't need 4-AIDataStore, it needs a record.

**Skill-first development.** Make a skill work locally first, then wire it into an umbrella's keyword table. The skill prompt is the source of truth.
