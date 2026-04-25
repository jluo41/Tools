---
name: haipipe-nn-algo
description: "Layer 1 (Algorithm) specialist of haipipe-nn. Defines the algorithm contract — model class, forward pass, loss, metric. Covers mlpredictor, tsforecast, tefm, tediffusion, bandit. Called by /haipipe-nn orchestrator. Direct invocation works for layer-scoped work."
argument-hint: [function] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-nn-algo
=======================

Layer 1 specialist. Owns the algorithm definitions in `code/hainn/algo/`.
Algorithms are the model classes — forward pass, loss, metric — without
any hyperparameter sweep or training loop logic. Called by the
`/haipipe-nn` orchestrator; can also be invoked directly.

  Function axis:  dashboard | review | generate | test

---

Commands
--------

```
/haipipe-nn-algo                       -> dashboard: registered algorithms
/haipipe-nn-algo dashboard             -> same
/haipipe-nn-algo review [class_name]   -> structural review of an algorithm class
/haipipe-nn-algo generate              -> scaffold a new algorithm class
/haipipe-nn-algo test [class_name]     -> run unit / smoke tests for the algorithm
```

---

Dispatch Table
--------------

```
Invocation     This skill's ref      Umbrella's fn doc
-------------- --------------------- ------------------------------
dashboard      ref/concepts.md       ../haipipe-nn/fn/fn-dashboard.md
review         ref/concepts.md       ../haipipe-nn/fn/fn-review.md
generate       ref/concepts.md +
               ../haipipe-nn-tuner/
                 ref/concepts.md     ../haipipe-nn/fn/fn-generate.md
test           ref/concepts.md       ../haipipe-nn/fn/fn-test.md
(no fn arg)    ref/concepts.md       (ref-only mode)
```

`generate` reads the L2 (tuner) ref because a new algorithm must satisfy
the tuner's expected `__init__` signature for hyperparameter binding.

---

Step-by-Step Protocol
----------------------

Step 0: Read `../haipipe-nn/ref/overview.md` for the 4-layer map. Mandatory.
Step 1: Parse args. Function vocabulary: dashboard | review | generate | test.
Step 2: Read this skill's `ref/concepts.md` for L1 specifics.
Step 3: Read the umbrella fn doc.
Step 4: For `generate`, also read `../haipipe-nn-tuner/ref/concepts.md`.
Step 5: Execute, scoped to L1 (algorithm class only — no tuner / instance work).
Step 6: Emit the structured tail (`status / summary / artifacts / next`).

---

Layer Scope
-----------

Owns:
  - Algorithm class definitions in `code/hainn/algo/`
  - Per-family conventions: mlpredictor, tsforecast, tefm, tediffusion, bandit
  - Forward pass, loss, metric

Does NOT own:
  - Hyperparameter sweep logic (`/haipipe-nn-tuner`)
  - Trained instance weights (`/haipipe-nn-instance`)
  - Multi-instance pipelines (`/haipipe-nn-modelset`)

Hand-off contract (L1 -> L2):
  Algorithm `__init__` parameters become the tuner's search-space schema.
  Verify against `../haipipe-nn-tuner/ref/concepts.md` before locking
  parameter names.
