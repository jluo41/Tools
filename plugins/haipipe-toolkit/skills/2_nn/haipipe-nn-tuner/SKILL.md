---
name: haipipe-nn-tuner
description: "Layer 2 (Tuner) specialist of haipipe-nn. Defines the hyperparameter search space and the tuner that drives sweeps. Called by /haipipe-nn orchestrator. Direct invocation works for layer-scoped work."
argument-hint: [function] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-nn-tuner
========================

Layer 2 specialist. Owns the tuner classes in `code/hainn/tuner/` — search
space declarations, hyperparameter sampling, and the loop that wraps L1
algorithms. Called by the `/haipipe-nn` orchestrator; can also be invoked
directly.

  Function axis:  dashboard | review | generate | test

---

Commands
--------

```
/haipipe-nn-tuner                      -> dashboard: registered tuners
/haipipe-nn-tuner dashboard            -> same
/haipipe-nn-tuner review [class_name]  -> structural review of a tuner class
/haipipe-nn-tuner generate             -> scaffold a new tuner / search space
/haipipe-nn-tuner test [class_name]    -> run a short tuner smoke sweep
```

---

Dispatch Table
--------------

```
Invocation    This skill's ref       Umbrella's fn doc
------------- ---------------------- ------------------------------
dashboard     ref/concepts.md        ../haipipe-nn/fn/fn-dashboard.md
review        ref/concepts.md        ../haipipe-nn/fn/fn-review.md
generate      ref/concepts.md +
              ../haipipe-nn-instance/
                ref/concepts.md      ../haipipe-nn/fn/fn-generate.md
test          ref/concepts.md        ../haipipe-nn/fn/fn-test.md
(no fn arg)   ref/concepts.md        (ref-only mode)
```

`generate` reads the L3 (instance) ref because the tuner's output
(best-config + ckpt) becomes the input contract for ModelInstance.

---

Step-by-Step Protocol
----------------------

Step 0: Read `../haipipe-nn/ref/overview.md`. Mandatory.
Step 1: Parse args. Function vocabulary: dashboard | review | generate | test.
Step 2: Read this skill's `ref/concepts.md` for L2 specifics.
Step 3: Read the umbrella fn doc.
Step 4: For `generate`, also read `../haipipe-nn-instance/ref/concepts.md`.
Step 5: Execute, scoped to L2 (tuner only — no algorithm class edits).
Step 6: Emit the structured tail.

---

Layer Scope
-----------

Owns:
  - Tuner classes in `code/hainn/tuner/`
  - Search-space declarations (param names, ranges, samplers)
  - The sweep loop that orchestrates L1 algorithm trials

Upstream dependency (L1):
  Tuner search space must match the algorithm's `__init__` signature. If a
  param is missing or extra, escalate to `/haipipe-nn-algo review`.

Hand-off contract (L2 -> L3):
  Tuner emits a `best_config` and a checkpoint path; ModelInstance consumes
  these to materialize trained weights. Verify against
  `../haipipe-nn-instance/ref/concepts.md`.
