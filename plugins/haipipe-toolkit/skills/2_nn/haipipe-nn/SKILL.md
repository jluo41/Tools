---
name: haipipe-nn
description: "Run any Stage 5 NN pipeline work. Parses intent (layer + function) and dispatches to the right specialist (haipipe-nn-algo/-tuner/-instance/-modelset). Use for algorithms (mlpredictor/tsforecast/tefm/tediffusion/bandit), tuner sweeps, ModelInstance materialization, ModelSet pipelines, dashboards, reviews, generation, testing. Trigger: nn pipeline, model, algorithm, tuner, instance, modelset, /haipipe-nn."
argument-hint: [layer] [function] [args...]
allowed-tools: Bash, Read, Grep, Glob, Skill
---

Skill: haipipe-nn (orchestrator)
=================================

User-facing entry for Stage 5. Parses intent, dispatches to the right
layer specialist via `Skill()`.

```
/haipipe-nn                       -> cross-layer dashboard
/haipipe-nn <layer>               -> ref-only view of one layer
/haipipe-nn <layer> <fn> [args]   -> dispatch to specialist
/haipipe-nn <fn> <layer> [args]   -> same (flexible order)
/haipipe-nn <fn>                  -> ASK which layer (don't guess across L1-L4)
/haipipe-nn L0                    -> architecture overview (umbrella inline)
/haipipe-nn "<natural language>"  -> infer layer + fn from keywords, dispatch
```

---

Specialists
-----------

```
haipipe-nn-algo       L1: Algorithm (model class, forward, loss, metric)
haipipe-nn-tuner      L2: Tuner (hyperparameter sweep, search space)
haipipe-nn-instance   L3: ModelInstance (materialized weights + config)
haipipe-nn-modelset   L4: ModelSet / Pipeline (composition of instances)
```

---

Layer Keyword Map
------------------

```
algorithm, algo, mlpredictor, tsforecast, tefm,
tediffusion, bandit, model class, forward, loss   -> algo
tuner, hyperparameter, hp, sweep, search space    -> tuner
instance, ModelInstance, weights, trained model,
ckpt, checkpoint                                  -> instance
ModelSet, modelset, pipeline, registry,
ensemble, multi-instance                          -> modelset
```

Layer aliases (positional):
```
1, L1, layer-1, algorithm  -> algo
2, L2, layer-2, tuner      -> tuner
3, L3, layer-3, instance   -> instance
4, L4, layer-4, modelset   -> modelset
0, L0, overview            -> umbrella inline
```

---

Function Verb Map
------------------

```
status, dashboard, what's there       -> dashboard
review, audit, check, validate        -> review
generate, build, create, scaffold     -> generate
test, smoke, run                      -> test
```

---

Routing Logic
-------------

```
Step 1: Parse $ARGUMENTS.

Step 2: Resolve (layer, function):
  - First positional matches layer alias?  -> layer = that
  - Else first positional matches verb?    -> function = that
  - Scan keyword maps for any unmatched terms.
  - layer = L0 / overview                  -> handle inline (overview mode)

Step 3: Decide handling:
  - No args                                -> CROSS-LAYER DASHBOARD (inline)
  - layer = L0                             -> read ref/overview.md, summarize
  - layer resolved, no function            -> dispatch to <layer> with arg "(none)"
                                              -> specialist returns ref-only summary
  - both resolved                          -> dispatch to specialist
  - function resolved, no layer            -> ASK which layer

Step 4: Dispatch:
    Skill("haipipe-nn-<layer>", args="<function> <remaining_args>")

Step 5: Capture the specialist's structured tail (status / summary /
        artifacts / next), present it.
```

---

Cross-Layer Dashboard (no-arg case)
------------------------------------

When invoked with no arguments, fan out to every specialist's dashboard
in a single message (parallel) and concatenate:

```
Skill("haipipe-nn-algo",      args="dashboard")
Skill("haipipe-nn-tuner",     args="dashboard")
Skill("haipipe-nn-instance",  args="dashboard")
Skill("haipipe-nn-modelset",  args="dashboard")
```

Emit a 4-line summary (one per layer) plus an overall header.

---

L0 / Overview Mode (inline)
----------------------------

`/haipipe-nn L0` and `/haipipe-nn overview` are handled inline:

  1. Read `ref/overview.md`.
  2. Summarize the 4-layer architecture, registry, YAML templates.
  3. Suggest the next layer-scoped command.

---

Disambiguation Rules
---------------------

  - Layer unclear -> list 4 layer options, wait.
  - Verb unclear, layer clear -> default to `dashboard`.
  - Multi-layer request ("review L1 to L3") -> dispatch sequentially,
    reporting after each.

---

Specialist Return Contract
---------------------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was done at the layer
artifacts: [paths created, read, or modified]
next:      suggested next command
```

---

Files Owned by This Umbrella
-----------------------------

```
ref/overview.md          cross-layer architecture + registry + YAML templates
fn/fn-dashboard.md       dashboard procedure (used by every specialist)
fn/fn-review.md          review procedure (used by every specialist)
fn/fn-generate.md        generate procedure (used by every specialist)
fn/fn-test.md            test procedure (used by every specialist)
```

These fn docs are SHARED across specialists. Each specialist reads its own
`ref/concepts.md` plus the relevant umbrella fn doc.
