---
name: haipipe-nn-modelset
description: "Layer 4 (ModelSet / Pipeline) specialist of haipipe-nn. Composes multiple ModelInstances into a registry-backed pipeline. Called by /haipipe-nn orchestrator. Direct invocation works for layer-scoped work."
argument-hint: [function] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-nn-modelset
===========================

Layer 4 specialist. Owns ModelSet (pipeline) composition — combining
multiple ModelInstances into a registry-backed serving pipeline (e.g. an
ensemble, a router, a multi-stage forecast). Called by the `/haipipe-nn`
orchestrator; can also be invoked directly.

  Function axis:  dashboard | review | generate | test

---

Commands
--------

```
/haipipe-nn-modelset                      -> dashboard: registered ModelSets
/haipipe-nn-modelset dashboard            -> same
/haipipe-nn-modelset review [set_name]    -> structural review of a ModelSet
/haipipe-nn-modelset generate             -> compose a new ModelSet from instances
/haipipe-nn-modelset test [set_name]      -> smoke-test the ModelSet end-to-end
```

---

Dispatch Table
--------------

```
Invocation    This skill's ref       Umbrella's fn doc
------------- ---------------------- ------------------------------
dashboard     ref/concepts.md        ../haipipe-nn/fn/fn-dashboard.md
review        ref/concepts.md        ../haipipe-nn/fn/fn-review.md
generate      ref/concepts.md        ../haipipe-nn/fn/fn-generate.md
test          ref/concepts.md        ../haipipe-nn/fn/fn-test.md
(no fn arg)   ref/concepts.md        (ref-only mode)
```

L4 is the terminal layer of haipipe-nn — `generate` does NOT need a
downstream layer ref. The next consumer is `/haipipe-end` (Stage 6).

---

Step-by-Step Protocol
----------------------

Step 0: Read `../haipipe-nn/ref/overview.md`. Mandatory.
Step 1: Parse args. Function vocabulary: dashboard | review | generate | test.
Step 2: Read this skill's `ref/concepts.md` for L4 specifics.
Step 3: Read the umbrella fn doc.
Step 4: Execute, scoped to L4 (composition only — no instance retraining).
Step 5: Emit the structured tail.

---

Layer Scope
-----------

Owns:
  - ModelSet definitions in `code/hainn/nn/` (pipeline composition)
  - Registry of which instances participate in which set
  - Cross-instance routing / ensemble logic

Upstream dependency (L3):
  Reads `_WorkSpace/5-ModelInstanceStore/ModelInstance-*/` directories.
  A ModelSet is a referenced registry; if an instance is missing, escalate
  to `/haipipe-nn-instance review`.

Hand-off contract (L4 -> Stage 6):
  ModelSet name + member ModelInstance list is what `/haipipe-end-endpointset
  package` consumes. Layout must satisfy the Endpoint_Pipeline's expectations.
