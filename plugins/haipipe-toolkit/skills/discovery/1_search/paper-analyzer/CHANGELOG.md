paper-analyzer — Changelog
==========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [0.2.1] — 2026-09-20

- Add a shared assessment receipt to generated notes: evaluator, rubric
  version, assessment timestamp, and the owning Run or exact source snapshot.

## [0.2.0] — 2026-09-20

- Replace the unanchored 0–10 paper-quality score with criterion-level evidence
  states and explicit source locators; distinguish author claims from reader
  inferences and keep unresolved relevance out of the admitted evidence set.
- Generate notes as `draft` / `not-assessed`, and keep the graph helper to
  bibliographic indexing without a default score or analyzed flag. Re-indexing
  keeps legacy fields in an explicitly unvalidated record for inspection and
  leaves assessment status with the note.


## [0.1.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.0; older entries below keep their original numbers).

## [1.0.0] — 2026-05-31

- baseline metadata added.
