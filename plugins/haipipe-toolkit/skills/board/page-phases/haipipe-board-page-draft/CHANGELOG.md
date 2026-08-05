haipipe-board-page-draft · Changelog
=====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.3.1 - 2026-08-05

- Opening now states DRAFT's own risk (a hidden hole reaches print) instead of the three-line ownership couplet shared verbatim with REVISE and CHECK, the 260802 form-letter failure repeating one level down.
- Q-consumer and stake get a defining line at first use; this file is loadable standalone.

## 0.3.0 - 2026-08-04

- Adds the shared RUN receipt boundary: DRAFT names the promise authority it
  exercised, its changed artifacts and visible evidence, and one legal route.
- Keeps round ownership in the controller so a DRAFT entered after reopening
  does not increment the round twice or approve its own result.

## 0.2.0 - 2026-08-04

- Renamed from `haipipe-board-page-for-stage-draft` and moved under `page-phases/`.
- DRAFT now applies to any Page Type and is defined by authority over purpose, Aims, and promised shape rather than first creation or a specific editing operation.
- Returning from REVISE or CHECK to DRAFT explicitly starts a new round on the same Page.
- DRAFT raises the stake-bearing Q-consumer and leaves Q-executor, routing, evidence collection, and interpretation to PROBE.

## 0.1.0 - 2026-08-04

**Created** (JL: "ok, I agree, please go ahead and make them.").

Split out of the family workers so the four-phase loop has ONE rulebook instead of
one per family. Measured 260804: the paper and application families each shipped
their own draft/probe/revise/check hubs (1,263 lines against 531), and NONE of the
eight loaded `haipipe-board-page` at all, so each had copied the page grammar from
memory. `haipipe-paper-draft` still named `## Items to Finish` five times, a
section renamed that morning.

- Host-agnostic on purpose: names no venue, no markup, no checker. A family worker
  adds its artifact knowledge and obeys this file.
- Settles `QC6 A4.1`: paper and application share a CONTRACT, not folder names.
