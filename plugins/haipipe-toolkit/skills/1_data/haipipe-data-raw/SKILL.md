---
name: haipipe-data-raw
description: "Stage 0' (raw cohort) specialist. Helps researchers and presenters build a clear, business-readable understanding of how a single data point in a raw cohort extract is generated — BEFORE the data enters Stage 1 (Source). Domain-agnostic: works for CGM streams, EHR encounter tables, claims lines, sensor logs, messaging extracts, etc. Owns _WorkSpace/0-RawStore/<cohort>/. Output is a datapoint-timeline.txt describing one row's lifecycle: pre-data background, in-data events, fog of war, late-visible signals, cross-cutting events. Distinct from haipipe-data-external (sideways dimension/lookup pantry) and haipipe-data-source (Stage 1 wrapping). Trigger: raw, rawstore, 0-rawstore, raw cohort, data point generation, datapoint timeline, lifecycle, fog of war, /haipipe-data-raw."
argument-hint: "[function] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-data-raw
=======================

Stage 0' (raw cohort) specialist. Owns the raw-extract folders under
`_WorkSpace/0-RawStore/<cohort>/` and the practice of writing a
single-data-point lifecycle diagram BEFORE the cohort is wrapped into
SourceFn (Stage 1).

Domain-agnostic: a "raw cohort" can be a CGM stream, an EHR encounter
table, a claims/billing line, a sensor session log, a messaging /
engagement extract, or any vendor delivery. The 5-zone timeline shape
applies equally to all.

  Function axis:  dashboard | load | understand | review | hand-off

Distinct from `haipipe-data-external` (sideways pantry of dimension
lookups, e.g. NPI / NDC / zip3 in US-healthcare contexts, station /
device-model lookups in IoT contexts) — raw is the cohort-specific
event extract that becomes the spine of Stages 1+.

---

Commands
--------

```
/haipipe-data-raw                              -> dashboard: list cohorts under 0-RawStore/
/haipipe-data-raw dashboard                    -> same
/haipipe-data-raw load <cohort>                -> read parquet schema + every descriptive
                                                  .txt in the cohort folder; emit a 1-page
                                                  orientation summary
/haipipe-data-raw understand <cohort>          -> ITERATIVE discussion to draft
                                                  datapoint-timeline.txt for one data point
                                                  (see ref/concepts.md for procedure)
/haipipe-data-raw review <cohort>              -> audit cohort/datapoint-timeline.txt:
                                                  required sections, parquet-claim alignment,
                                                  eligibility / fog / drift caveats
/haipipe-data-raw hand-off <cohort>            -> derive a SourceFn-ready checklist from
                                                  the timeline (columns to wrap, derived
                                                  fields to compute, eligibility flags
                                                  to keep separate, upstream asks)
```

---

Dispatch Table
--------------

```
Invocation     This skill's ref / templates              Umbrella's fn doc
-------------- ----------------------------------------- ------------------------------------
dashboard      ref/concepts.md                           ../haipipe-data/fn/fn-0-dashboard.md
load           ref/concepts.md                           ../haipipe-data/fn/fn-1-load.md
understand     ref/concepts.md +
               templates/datapoint-timeline.txt          (handled inline — see Protocol)
review         ref/concepts.md                           ../haipipe-data/fn/fn-review.md
hand-off       ref/concepts.md +
               ../haipipe-data-source/ref/concepts.md    (handled inline — see Protocol)
(no fn arg)    ref/concepts.md                           (ref-only mode)
```

`hand-off` reads Stage-1 Source's ref because the timeline directly
drives the SourceFn schema downstream.

---

Step-by-Step Protocol
----------------------

```
Step 0: Read ../haipipe-data/ref/0-overview.md for cross-stage context. Mandatory.
Step 1: Parse args after /haipipe-data-raw. First positional = function,
        remaining = cohort name + optional flags.
Step 2: Read this skill's ref/concepts.md for the 5-zone timeline shape +
        understand/review/hand-off procedures.
Step 3: Read additional refs / templates per the dispatch table.
Step 4: Execute, scoped to _WorkSpace/0-RawStore/<cohort>/.
Step 5: Emit the structured tail (status / summary / artifacts / next).
```

For `understand` specifically: do NOT write the datapoint-timeline.txt
up front. The procedure is *iterative dialogue* — see ref/concepts.md
"The understand Procedure" for the conversation pattern (restate user's
framing → confirm/challenge → draft → validate against parquet →
write only after alignment).

For `hand-off`: the output is a checklist, not a code change. Stage 1
(SourceFn) work is owned by `haipipe-data-source` — this skill stops
at "here's what SourceFn must do for this cohort."

---

Stage Scope
------------

Owns:
  - `_WorkSpace/0-RawStore/<cohort>/` folders
  - The discipline of writing a single-data-point lifecycle diagram
  - The hand-off contract from Stage 0' → Stage 1

Does NOT own:
  - Stage 1 SourceFn implementation        — see haipipe-data-source
  - Reference / dimension lookups           — see haipipe-data-external
  - Push / pull of raw extracts to remote   — see haipipe-data-remote

Hand-off contract (Stage 0' → Stage 1):
  Every concept in datapoint-timeline.txt that is marked "derive" or
  "ask upstream" MUST be addressed by SourceFn — either by computing
  the column or by carrying a TODO referencing the upstream ask.
  Eligibility flags (system / cohort gating) MUST stay separate from
  operational outcome flags (individual behaviour, device dropout,
  engagement drop-off, etc.).

Reference cohorts (worked examples):
  Any raw extract works — CGM streams, EHR encounter tables, claims
  lines, sensor session logs, messaging / engagement extracts, vendor
  drops. The 5 zones (pre-T₀ background, in-data events, fog of war,
  late-visible signals, cross-cutting events) apply uniformly.

  Cohorts under `_WorkSpace/0-RawStore/` that already have a
  `datapoint-timeline.txt` can serve as starting templates regardless
  of their domain.
