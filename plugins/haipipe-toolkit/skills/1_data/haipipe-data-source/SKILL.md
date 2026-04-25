---
name: haipipe-data-source
description: "Stage 1 (Source) specialist. Builds, runs, and reviews SourceFn / HumanFn; inspects 1-SourceStore; loads source-layer typed frames. Called by /haipipe-data orchestrator. Direct invocation works for stage-scoped work, but /haipipe-data is the recommended entry."
argument-hint: [function] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-data-source
==========================

Stage 1 specialist. Owns all SourceFn / HumanFn work and the 1-SourceStore
layer of the pipeline. Called by the `/haipipe-data` orchestrator; can also
be invoked directly.

  Function axis:  dashboard | load | cook | design-chef | design-kitchen | review

---

Commands
--------

```
/haipipe-data-source                        -> dashboard: 1-SourceStore status
/haipipe-data-source dashboard              -> same
/haipipe-data-source dashboard rawdata      -> 0-RawDataStore inventory (no manifest check)
/haipipe-data-source load                   -> load and inspect existing Source_Set
/haipipe-data-source cook                   -> run Source_Pipeline with config
/haipipe-data-source design-chef            -> create new SourceFn / HumanFn via builder
/haipipe-data-source design-kitchen         -> modify Source_Pipeline infrastructure
/haipipe-data-source review [file_path]     -> structural review of a Source-layer file
```

---

Dispatch Table
--------------

After parsing, read these files:

```
Invocation             This skill's ref            Umbrella's fn doc
---------------------- --------------------------- ---------------------------------------------------
dashboard              ref/concepts.md             ../haipipe-data/fn/fn-0-dashboard.md
dashboard rawdata      ref/concepts.md             ../haipipe-data/fn/fn-0-dashboard.md
load                   ref/concepts.md             ../haipipe-data/fn/fn-1-load.md
cook                   ref/concepts.md             ../haipipe-data/fn/fn-2-cook.md
design-chef            ref/concepts.md +
                       ../haipipe-data-record/
                         ref/concepts.md           ../haipipe-data/fn/fn-3-design-chef.md
design-kitchen         ref/concepts.md             ../haipipe-data/fn/fn-4-design-kitchen.md
review                 ref/concepts.md             ../haipipe-data/fn/fn-review.md
(no fn arg)            ref/concepts.md             (ref-only mode)
```

Why `design-chef` reads the next stage's ref: a SourceFn contract is satisfied
by what RecordFn downstream expects. You need both ref docs to design correctly.

---

Step-by-Step Protocol
----------------------

Step 0: Read the cross-stage overview FIRST (it has the 6-layer map and
        cooking metaphor): `../haipipe-data/ref/0-overview.md`. Mandatory.

Step 1: Parse args after `/haipipe-data-source`. Extract:
          function  in { dashboard, load, cook, design-chef, design-kitchen, review, (none) }
          extras    e.g. `rawdata` for dashboard, file_path for review
        If no args -> dashboard.
        If only ref-style probe -> read `ref/concepts.md`, summarize, stop.

Step 2: Read THIS skill's `ref/concepts.md` for stage-1 specifics.

Step 3: Read the umbrella fn doc per the dispatch table above.

Step 4: For `design-chef`, also read `../haipipe-data-record/ref/concepts.md`
        so you know the downstream contract.

Step 5: Execute the procedure described by the fn doc, scoped to Stage 1.

Step 6: Emit the structured tail (orchestrator parses this):

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was done at Stage 1
artifacts: [paths created, read, or modified]
next:      suggested next command (often a /haipipe-data-record action)
```

---

Stage Scope
------------

Owns:
  - SourceFn / HumanFn builders under `code-dev/1-PIPELINE/1-Source-WorkSpace/`
  - Generated `code/haifn/fn_source/`
  - `_WorkSpace/1-SourceStore/` typed frames
  - `templates/config.yaml` for Source_Pipeline runs

Does not own:
  - 0-RawDataStore content (that's source data, owned by the dataset)
  - 2-RecStore (`/haipipe-data-record`) and beyond

Hand-off contract (Stage 1 -> 2):
  Each Source frame must carry the keys RecordFn needs to bucket rows into
  records. Confirm by reading `../haipipe-data-record/ref/concepts.md` before
  finalizing any SourceFn.
