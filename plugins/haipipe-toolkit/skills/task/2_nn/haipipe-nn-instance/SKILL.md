---
name: haipipe-nn-instance
description: "Layer 3 (Instance) specialist of haipipe-nn: materializes a trained ModelInstance by driving its Tuners (registry create -> fit -> save_model). Called by /haipipe-nn; direct invocation works layer-scoped."
argument-hint: "[function] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.1.0"
  last_updated: "2026-07-04"
  summary: "Layer 3 (Instance) specialist of haipipe-nn."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-nn-instance
===========================

Layer 3 specialist.
Owns the ModelInstance materialization in `code/hainn/instance/` and the `5-ModelInstanceStore`.
A ModelInstance is the trained-weights artifact paired with its config — the thing endpoints will consume.
Called by the `/haipipe-nn` orchestrator; can also be invoked directly.

  Function axis:  dashboard | review | generate | test

---

Commands
--------

```
/haipipe-nn-instance                       -> dashboard: 5-ModelInstanceStore status
/haipipe-nn-instance dashboard             -> same
/haipipe-nn-instance review [instance_id]  -> structural review of one ModelInstance
/haipipe-nn-instance generate              -> materialize a ModelInstance from tuner output
/haipipe-nn-instance test [instance_id]    -> smoke-test inference on a ModelInstance
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
              ../haipipe-nn-modelset/
                ref/concepts.md      ../haipipe-nn/fn/fn-generate.md
test          ref/concepts.md        ../haipipe-nn/fn/fn-test.md
(no fn arg)   ref/concepts.md        (ref-only mode)
```

`generate` reads the L4 (modelset) ref because a ModelInstance is the unit that gets registered into a ModelSet pipeline downstream.

---

Step-by-Step Protocol
----------------------

Step 0: Read `../haipipe-nn/ref/overview.md`.
Mandatory.
Step 1: Parse args.
Function vocabulary: dashboard | review | generate | test.
Step 2: Read this skill's `ref/concepts.md` for L3 specifics.
Step 3: Read the umbrella fn doc.
Step 4: For `generate`, also read `../haipipe-nn-modelset/ref/concepts.md`.
Step 5: Execute, scoped to L3 (instance materialization only).
Step 6: Emit the structured tail.

---

Layer Scope
-----------

Owns:
  - ModelInstance classes in `code/hainn/instance/`
  - `_WorkSpace/5-ModelInstanceStore/{modelinstance_name}/{version}/` (no ModelInstance- prefix)
  - Trained weights, paired config, metadata

Upstream dependency (L2):
  Drives the Tuner: creates it via the model_tuner registry, calls
  fit() / save_model(key, model_dir). If materialization fails on
  config-shape mismatch, escalate to `/haipipe-nn-tuner review`.

Hand-off contract (L3 -> L4):
  ModelInstance directory layout is the registration unit ModelSet expects.
  Verify against `../haipipe-nn-modelset/ref/concepts.md`.

Hand-off contract (L3 -> Stage 6):
  ModelInstance is also the input to `/haipipe-end-endpointset package`.
  Layout / metadata must satisfy what the Endpoint_Pipeline consumes.
