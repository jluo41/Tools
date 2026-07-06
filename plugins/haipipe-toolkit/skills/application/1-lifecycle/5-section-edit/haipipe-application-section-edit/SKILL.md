---
name: haipipe-application-section-editing
description: "Stage 5 of the intervention lifecycle. Per-section comment -> reply -> apply cycle on 0-sections/*.tex, adapted from paper's write-edit cycle. Always required. Trigger: section-editing, edit sections, refine, /haipipe-application section-editing."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.0.0"
  last_updated: "2026-07-02"
  summary: "Stage 5 -- per-section comment -> reply -> apply editing cycle."
  changelog:
    - "3.0.0 (2026-07-02): replaced minimap with section-editing; per-section comment->reply->apply cycle adapted from paper's write-edit."
    - "2.0.0 (2026-06-23): renamed from delivery to minimap; match paper vocabulary; venue-gated."
    - "1.0.0 (2026-06-22): initial version as haipipe-application-delivery."
---

Skill: haipipe-application-section-editing
============================================

Stage 5 of the intervention lifecycle. Runs a per-section
comment -> reply -> apply editing cycle on `0-sections/*.tex`,
adapted from the paper lifecycle's write-edit cycle.

Always required (all venues).


Question answered
==================

"Are the report sections polished and accurate?"


Input
======

- `0-sections/*.tex` -- the 6 report sections:
  - `01-subgroup-profile.tex`
  - `02-exploration.tex`
  - `03-findings.tex`
  - `04-messages.tex`
  - `05-performance.tex`
  - `06-gate-check.tex`


Output
=======

- Edited `0-sections/*.tex` files (in place)
- Edit log in `0-lifecycle/5-section-editing/`


The 5-stage edit cycle
=======================

Same structure as the paper write-edit cycle:

```
1. Format check   [sequential]
   Verify each section compiles, labels resolve, structure matches
   the venue template.

2. Annotate       [fan out per section]
   Insert `%% {CC-<topic>-v<DATE>}: <finding>` comments into each
   section file. One comment per finding, placed inline next to
   the relevant text.

3. Human reply    [human + AI]
   User (or AI copilot) replies to each comment:
     ========> {JL v<DATE>}: accept | reject | revise <instructions>

4. Apply          [sequential]
   Apply all accepted comments. Remove resolved comment blocks.

5. Clean + diff   [sequential]
   Strip any remaining comment scaffolding. Produce a diff summary
   for the edit log.
```


Edit topics
============

Six topics, adapted from the paper's editing dimensions:

**tone** -- Does the voice match the intended audience (clinical
staff, pharmacist, patient)? Flag register mismatches.

**char-count** -- For message text in section 04-messages, enforce
character limits from the venue profile (e.g. SMS 160 chars).

**citations** -- Do claims trace back to K/W insight cards? Flag
unsupported assertions.

**reading-level** -- Is the text at the appropriate grade level?
Patient-facing content targets 6th grade.

**distinctiveness** -- Do the messages in section 04-messages
actually differ from each other? Flag near-duplicates.

**consistency** -- Are terms, labels, metric names, and cohort
definitions used consistently across all 6 sections?


Comment protocol
=================

Same as the paper convention:

```
%% {CC-tone-v0702}: This sentence uses clinical jargon that may
%% not be appropriate for the patient audience.
========> {JL v0702}: accept
```

Topics are namespaced in the comment tag: `CC-tone`, `CC-charcount`,
`CC-citations`, `CC-readlevel`, `CC-distinct`, `CC-consistency`.


Definition of done
===================

```
[ ] All 6 sections have no open (unreplied) comments
[ ] Format check passes (compiles, labels resolve)
[ ] Edit log written to 0-lifecycle/5-section-editing/
```


Risk profile
=============

WRITES edits to `0-sections/*.tex`. Does not modify
`0-lifecycle/` planning files (narrative, claims, display, etc.).
