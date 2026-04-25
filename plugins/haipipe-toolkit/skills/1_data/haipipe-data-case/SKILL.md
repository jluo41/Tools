---
name: haipipe-data-case
description: "Stage 3 (Case) specialist. Builds, runs, and reviews CaseFn; inspects 3-CaseStore; loads case-layer assets. Called by /haipipe-data orchestrator. Direct invocation works for stage-scoped work, but /haipipe-data is the recommended entry."
argument-hint: [function] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-data-case
========================

Stage 3 specialist. Owns CaseFn work and the 3-CaseStore layer. Called by
the `/haipipe-data` orchestrator; can also be invoked directly.

  Function axis:  dashboard | load | cook | design-chef | design-kitchen | review

---

Commands
--------

```
/haipipe-data-case                          -> dashboard: 3-CaseStore status
/haipipe-data-case dashboard                -> same
/haipipe-data-case load                     -> load and inspect existing Case_Set
/haipipe-data-case cook                     -> run Case_Pipeline with config
/haipipe-data-case design-chef              -> create new CaseFn via builder
/haipipe-data-case design-kitchen           -> modify Case_Pipeline infrastructure
/haipipe-data-case review [file_path]       -> structural review of a Case-layer file
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
                 ../haipipe-data-aidata/
                   ref/concepts.md           ../haipipe-data/fn/fn-3-design-chef.md
design-kitchen   ref/concepts.md             ../haipipe-data/fn/fn-4-design-kitchen.md
review           ref/concepts.md             ../haipipe-data/fn/fn-review.md
(no fn arg)      ref/concepts.md             (ref-only mode)
```

`design-chef` reads `../haipipe-data-aidata/ref/concepts.md` because a
CaseFn must produce keys/shapes that TfmFn / SplitFn can consume.

---

Step-by-Step Protocol
----------------------

Step 0: Read `../haipipe-data/ref/0-overview.md`. Mandatory.
Step 1: Parse args after `/haipipe-data-case`.
Step 2: Read this skill's `ref/concepts.md` for stage-3 specifics.
Step 3: Read the umbrella fn doc.
Step 4: For `design-chef`, also read `../haipipe-data-aidata/ref/concepts.md`.
Step 5: Execute, scoped to Stage 3.
Step 6: Emit the structured tail.

---

Stage Scope
------------

Owns:
  - CaseFn builders under `code-dev/1-PIPELINE/3-Case-WorkSpace/`
  - Generated `code/haifn/fn_case/`
  - `_WorkSpace/3-CaseStore/` cases (cohort sampling)
  - `templates/config.yaml` for Case_Pipeline runs

Upstream dependency (Stage 2):
  Reads `_WorkSpace/2-RecStore/`. Empty cases usually mean upstream record
  rows didn't satisfy the trigger condition.

Hand-off contract (Stage 3 -> 4):
  Each Case must expose the fields TfmFn will tensorize. Verify against
  `../haipipe-data-aidata/ref/concepts.md`.
