haipipe-page-check · Changelog
==============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.3.1 - 2026-08-05

- Opening now states CHECK's own risk (becoming a hidden revision) instead of the shared ownership couplet.

## 0.3.0 - 2026-08-04

- Adds the shared RUN receipt and immutable version gate: CHECK records the
  source/render identity, verdict, findings, evidence, route, and human gate.
- Enforces producer != judge, re-CHECK after every content change, CLOSE only
  after pass, and HOLD for missing human evidence or concurrent mutation.

## 0.2.0 - 2026-08-04

- Renamed from `haipipe-board-page-for-stage-check` and moved under `page-phases/`.
- CHECK now applies to any Page Type, judges one concrete version, and routes to close, REVISE, PROBE, DRAFT new round, or an explicit hold.
- Removes the assumptions that CHECK is always last, always human, or always feeds the next DRAFT.
- Corrects `new round`: it reopens the promise on the same persistent Page and does not automatically create another unit.

## 0.1.0 - 2026-08-04

**Created** (JL: "ok, I agree, please go ahead and make them.").

Split out of the family workers so the four-phase loop has ONE rulebook instead of
one per family. Measured 260804: the paper and application families each shipped
their own draft/probe/revise/check hubs (1,263 lines against 531), and NONE of the
eight loaded `haipipe-page` at all, so each had copied the page grammar from
memory. `haipipe-paper-draft` still named `## Items to Finish` five times, a
section renamed that morning.

- Host-agnostic on purpose: names no venue, no markup, no checker. A family worker
  adds its artifact knowledge and obeys this file.
- Settles `QC6 A4.1`: paper and application share a CONTRACT, not folder names.
