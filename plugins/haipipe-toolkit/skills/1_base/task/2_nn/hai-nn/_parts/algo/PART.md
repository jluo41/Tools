---
name: algo
part-of: hai-nn
description: "Layer 1 (Algorithm) specialist of hai-nn: defines the algorithm contract (model class, forward pass, loss, metric). Covers mlpredictor, tsforecast, tefm, tediffusion, bandit. Called by /hai-nn."
argument-hint: "[function] [args...]"
metadata:
  version: "0.1.2"
  last_updated: "2026-10-25"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: hai-nn algo
=======================

Layer 1 specialist.
Owns the algorithm definitions in `code/hainn/algo/`.
Algorithms are the model classes — forward pass, loss, metric — without any hyperparameter sweep or training loop logic.
Called by the `/hai-nn` orchestrator, which reads this file as a part (not a separate skill).

  Function axis:  dashboard | review | generate | test

---

Commands
--------

```
/hai-nn algo                       -> dashboard: registered algorithms
/hai-nn algo dashboard             -> same
/hai-nn algo review [class_name]   -> structural review of an algorithm class
/hai-nn algo generate              -> scaffold a new algorithm class
/hai-nn algo test [class_name]     -> run unit / smoke tests for the algorithm
```

---

Dispatch Table
--------------

```
Invocation     This skill's ref      Umbrella's fn doc
-------------- --------------------- ------------------------------
dashboard      ref/concepts.md       ../../fn/fn-dashboard.md
review         ref/concepts.md       ../../fn/fn-review.md
generate       ref/concepts.md +
               ../tuner/
                 ref/concepts.md     ../../fn/fn-generate.md
test           ref/concepts.md       ../../fn/fn-test.md
(no fn arg)    ref/concepts.md       (ref-only mode)
```

`generate` reads the L2 (tuner) ref because a new algorithm must satisfy the tuner's expected `__init__` signature for hyperparameter binding.

---

Step-by-Step Protocol
----------------------

Step 0: Read `../../ref/overview.md` for the 4-layer map.
Mandatory.
Step 1: Parse args.
Function vocabulary: dashboard | review | generate | test.
Step 2: Read this skill's `ref/concepts.md` for L1 specifics.
Step 3: Read the umbrella fn doc.
Step 4: For `generate`, also read `../tuner/ref/concepts.md`.
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
  - Hyperparameter sweep logic (`/hai-nn tuner`)
  - Trained instance weights (`/hai-nn instance`)
  - Multi-instance pipelines (`/hai-nn modelset`)

Hand-off contract (L1 -> L2):
  Algorithm `__init__` parameters become the tuner's search-space schema.
  Verify against `../tuner/ref/concepts.md` before locking
  parameter names.
