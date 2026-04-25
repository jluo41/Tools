---
name: haipipe-data-record
description: "Stage 2 (Record) specialist. Builds, runs, and reviews RecordFn / TriggerFn; inspects 2-RecStore; loads record-layer assets. Called by /haipipe-data orchestrator. Direct invocation works for stage-scoped work, but /haipipe-data is the recommended entry."
argument-hint: [function] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-data-record
==========================

Stage 2 specialist. Owns all RecordFn / TriggerFn work and the 2-RecStore
layer. Called by the `/haipipe-data` orchestrator; can also be invoked
directly.

  Function axis:  dashboard | load | cook | design-chef | design-kitchen | review

---

Commands
--------

```
/haipipe-data-record                        -> dashboard: 2-RecStore status
/haipipe-data-record dashboard              -> same
/haipipe-data-record load                   -> load and inspect existing Record_Set
/haipipe-data-record cook                   -> run Record_Pipeline with config
/haipipe-data-record design-chef            -> create new RecordFn / TriggerFn via builder
/haipipe-data-record design-kitchen         -> modify Record_Pipeline infrastructure
/haipipe-data-record review [file_path]     -> structural review of a Record-layer file
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
design-chef      ref/concepts.md +
                 ../haipipe-data-case/
                   ref/concepts.md           ../haipipe-data/fn/fn-3-design-chef.md
design-kitchen   ref/concepts.md             ../haipipe-data/fn/fn-4-design-kitchen.md
review           ref/concepts.md             ../haipipe-data/fn/fn-review.md
(no fn arg)      ref/concepts.md             (ref-only mode)
```

`design-chef` reads `../haipipe-data-case/ref/concepts.md` because a
RecordFn's output schema must satisfy what CaseFn expects downstream.

---

Step-by-Step Protocol
----------------------

Step 0: Read `../haipipe-data/ref/0-overview.md` for cross-stage context. Mandatory.
Step 1: Parse args after `/haipipe-data-record`. Same vocabulary as the source
        specialist — see its dispatch table.
Step 2: Read this skill's `ref/concepts.md` for stage-2 specifics.
Step 3: Read the umbrella fn doc.
Step 4: For `design-chef`, also read `../haipipe-data-case/ref/concepts.md`.
Step 5: Execute, scoped to Stage 2.
Step 6: Emit the structured tail (`status / summary / artifacts / next`).

---

Stage Scope
------------

Owns:
  - RecordFn / TriggerFn builders under `code-dev/1-PIPELINE/2-Record-WorkSpace/`
  - Generated `code/haifn/fn_record/`
  - `_WorkSpace/2-RecStore/` records
  - `templates/config.yaml` for Record_Pipeline runs

Upstream dependency (Stage 1):
  Reads `_WorkSpace/1-SourceStore/`. If a RecordFn is empty/wrong, root cause
  is often a Source-layer issue — escalate to `/haipipe-data-source review`.

Hand-off contract (Stage 2 -> 3):
  Each Record's columns and time grid must match the keys CaseFn samples on.
  Verify against `../haipipe-data-case/ref/concepts.md` before locking schema.
