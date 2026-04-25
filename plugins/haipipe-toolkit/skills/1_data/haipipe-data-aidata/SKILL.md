---
name: haipipe-data-aidata
description: "Stage 4 (AIData) specialist. Builds, runs, and reviews TfmFn / SplitFn; inspects 4-AIDataStore; loads AIData-layer assets and tensors. Called by /haipipe-data orchestrator. Direct invocation works for stage-scoped work, but /haipipe-data is the recommended entry."
argument-hint: [function] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-data-aidata
==========================

Stage 4 specialist. Owns TfmFn / SplitFn work and the 4-AIDataStore layer
(model-ready tensors and splits). Called by the `/haipipe-data` orchestrator;
can also be invoked directly.

  Function axis:  dashboard | load | cook | design-chef | design-kitchen | review

---

Commands
--------

```
/haipipe-data-aidata                        -> dashboard: 4-AIDataStore status
/haipipe-data-aidata dashboard              -> same
/haipipe-data-aidata load                   -> load and inspect existing AIData_Set
/haipipe-data-aidata cook                   -> run AIData_Pipeline with config
/haipipe-data-aidata design-chef            -> create new TfmFn / SplitFn via builder
/haipipe-data-aidata design-kitchen         -> modify AIData_Pipeline infrastructure
/haipipe-data-aidata review [file_path]     -> structural review of an AIData-layer file
```

---

Dispatch Table
--------------

```
Invocation       This skill's ref            Umbrella's fn doc
---------------- --------------------------- ---------------------------------------------------
dashboard        ref/concepts.md             ../haipipe-data/fn/fn-0-dashboard.md
load             ref/concepts.md             ../haipipe-data/fn/fn-1-load.md
cook             ref/concepts.md             ../haipipe-data/fn/fn-2-cook.md
design-chef      ref/concepts.md             ../haipipe-data/fn/fn-3-design-chef.md
design-kitchen   ref/concepts.md             ../haipipe-data/fn/fn-4-design-kitchen.md
review           ref/concepts.md             ../haipipe-data/fn/fn-review.md
(no fn arg)      ref/concepts.md             (ref-only mode)
```

Stage 4 is the terminal data stage — `design-chef` does NOT need a downstream
ref because the next stage (`/haipipe-nn`) consumes whatever AIData produces.

---

Step-by-Step Protocol
----------------------

Step 0: Read `../haipipe-data/ref/0-overview.md`. Mandatory.
Step 1: Parse args after `/haipipe-data-aidata`.
Step 2: Read this skill's `ref/concepts.md` for stage-4 specifics.
Step 3: Read the umbrella fn doc.
Step 4: Execute, scoped to Stage 4.
Step 5: Emit the structured tail.

---

Stage Scope
------------

Owns:
  - TfmFn / SplitFn builders under `code-dev/1-PIPELINE/4-AIData-WorkSpace/`
  - Generated `code/haifn/fn_aidata/`
  - `_WorkSpace/4-AIDataStore/` tensors and split definitions
  - `templates/config.yaml` for AIData_Pipeline runs

Upstream dependency (Stage 3):
  Reads `_WorkSpace/3-CaseStore/`. Tensorization issues usually trace back to
  inconsistent CaseFn output schemas — escalate to `/haipipe-data-case review`.

Hand-off contract (Stage 4 -> 5):
  AIData_Set is the input contract for `/haipipe-nn`. Splits, tensor shapes,
  and target column conventions must match what algorithms in
  `code/hainn/algo/` expect.
