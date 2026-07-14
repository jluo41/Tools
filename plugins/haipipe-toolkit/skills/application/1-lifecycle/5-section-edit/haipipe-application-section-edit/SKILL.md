---
name: haipipe-application-section-edit
description: "Stage 5 of the intervention lifecycle (venue-gated: sectioned venues only — report, dashboard spec; skipped for sms/push/reminder/checklist/email unless the venue profile says otherwise). Per-section DRAFT-PROBE-REVISE-CHECK on the sections the VENUE PROFILE declares, syncing prose to 0-sections/. Renamed from haipipe-application-section-editing; the hardcoded 6-section report list moved to _venue/venue-report (venue knowledge, not skill logic). Trigger: section-edit, section, §N, edit sections, refine sections, /haipipe-application section-edit."
argument-hint: "[section-name-or-§N] [intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "4.1.0"
  last_updated: "2026-07-14"
  summary: "Generalized: section list comes from the pinned venue profile (was: hardcoded 01-subgroup-profile..06-gate-check report sections, now in _venue/venue-report). Runs per-section DPRC via the 2-phase/ workers; keeps the comment->reply->apply convention and the six edit topics as REVISE/CHECK lenses. v4.1.0 (probe redesign, Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3 approved JL 2026-07-14): a section's evidence gap raises a question SECTION in 1-probes/ (serves: 5-section-edit), not a card in a per-stage _PROBE/ folder (retired); citations trace to a settled claim in 1-claims.md -- whose evidence is a probe section's target: QA file -- since 'verdicted' is a deleted state."
  changelog:
    - "4.0.0 (2026-07-06): paper-alignment — renamed section-edit; venue-profile-driven section list; DPRC via shared 2-phase workers; stage folder 0-lifecycle/5-section-edit/."
    - "3.0.0 (2026-07-02): replaced minimap with section-editing; per-section comment->reply->apply cycle adapted from paper's write-edit."
    - "2.0.0 (2026-06-23): renamed from delivery to minimap; match paper vocabulary; venue-gated."
    - "1.0.0 (2026-06-22): initial version as haipipe-application-delivery."
---

Skill: haipipe-application-section-edit
========================================

Stage 5 of the intervention lifecycle, for **sectioned venues only** (the pinned venue's profile declares whether this stage fires and which sections exist). Runs per-section DRAFT-PROBE-REVISE-CHECK on the venue's section list, syncing prose to `0-sections/`.

Question answered
==================

"Does each section's prose do its assigned job?"

Where the section list comes from
==================================

The VENUE PROFILE, never this skill. `_venue/venue-<name>/README.md` declares the section structure (e.g. `venue-report` carries the report section list; a venue without a `sections:` block skips this stage entirely — check `STATUS.md | stages_skipped |`). The display stage's per-unit jobs say what each section must carry; this stage makes the prose deliver it.

Input
======

- `STATUS.md` → venue, stages_skipped (BLOCK if this stage is skipped)
- `_venue/venue-<name>/README.md` → section list + per-section jobs
- `0-lifecycle/4-display/4-display.md` → element-to-section mapping
- `0-lifecycle/1-claims/1-claims.md` → the ledger (claims language must not outrun it)
- `0-sections/*` → the prose under edit

Output
=======

- Edited `0-sections/*` files (in place)
- Per-section scaffolds + logs in `0-lifecycle/5-section-edit/{section}/` (outline `.md`, `_LOG`); a section that spawns an evidence need raises a question SECTION in `1-probes/` (serves: 5-section-edit)

Per-section DPRC
=================

Each section runs the shared phase cycle via the `2-phase/` workers (users invoke this stage; it dispatches):

```
DRAFT   settle the section's outline + draft sentences against its job
        (haipipe-application-draft)
PROBE   trace numbers to task results, claims to ledger/K-W anchors; buffer
        question SECTIONS in 1-probes/ for real evidence gaps (haipipe-application-probe)
REVISE  the comment -> reply -> apply cycle (below) + venue style-profile +
        audience conformance (haipipe-application-revise rules)
CHECK   per-section exit: prose does its job, no open comments, flags resolved
        or parked (haipipe-application-check; section rows in the stage _LOG,
        stage-level Gate Ledger row when ALL sections pass)
```

The comment -> reply -> apply cycle (REVISE convention)
========================================================

Same convention as the paper family:

```
1. Annotate     insert `%% {CC-<topic>-v<DATE>}: <finding>` comments inline,
                one per finding
2. Human reply  `========> {JL v<DATE>}: accept | reject | revise <instructions>`
3. Apply        apply accepted comments, remove resolved comment blocks
4. Clean+diff   strip leftover scaffolding, write a diff summary to the _LOG
```

Edit topics (lenses for REVISE/CHECK)
======================================

**tone** -- voice matches the audience profile (clinician / pharmacist / patient register).
**length** -- element/message text respects the venue profile's limits.
**citations** -- claims trace to a settled claim in 1-claims.md (whose evidence is a probe section's `target:` QA file) or to a ledger anchor; flag unsupported assertions.
**reading-level** -- patient-facing content at the audience profile's target grade level.
**distinctiveness** -- parallel elements (message variants, panels) actually differ; flag near-duplicates.
**consistency** -- terms, labels, metric names, cohort definitions consistent across sections.

Definition of done
===================

```
[ ] Every venue-declared section has prose that does its job (per display's mapping)
[ ] No open (unreplied) comments in any section
[ ] Format check passes (renders/compiles where applicable, labels resolve)
[ ] Section rows logged; stage Gate Ledger row written on CHECK approve
```

Risk profile
=============

WRITES edits to `0-sections/*` and scaffolds under `0-lifecycle/5-section-edit/`. Does not modify upstream lifecycle docs (claims, narrative, display) -- upstream problems are loopback suggestions.
