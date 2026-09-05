haipipe-discovery-idea — Changelog
==================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## 0.5.0 · 2026-09-04

- Route ideation synthesis through Page `03 CONTENT / WRITE`, novelty evidence
  gaps back to D1 ACQUIRE, and consume the one aggregate built by SYNTHESIZE.

## [0.4.1] — 2026-09-03

- Route the Idea citation aggregate through Outline's Evidence Workspace at
  `outline/evidence/bibex/`.

## [0.4.0] — 2026-09-02

- Own SYNTHESIZE for ideation/novelty Pages, route prior-work gaps back to
  ACQUIRE, and use the Outline Evidence Workspace for citation aggregation.

## [0.3.0] — 2026-09-01

- Serve canonical `ideation` and `novelty-verdict` Page Types; Idea is a
  specialist route rather than a durable type field.
- Keep idea synthesis on the root Page, with optional ideas/verdict records;
  only analyzed prior-work Subjects receive Runs.

## [0.2.0] — 2026-09-01

- Idea generation remains Topic-level Page work and no longer masquerades as a
  Run. Every prior-work paper used for novelty evidence receives its own
  numbered Paper Run/Result.


## [0.1.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.0; older entries below keep their original numbers).

## [1.0.0] — 2026-07-03

### Added
- Created (JL: each type gets its own specialist, now that buckets = types 1:1). Owns the Idea type's Execute — the full ideation loop: idea_generation (idea-creator -> `ideas.md`, ranked candidates with novelty tags + testability) and novelty_check (novelty-check -> `verdict.md`, closest prior work as one-paper-one-subsection).
- Post-validation patch: return contract to the caller (terminal path + candidate count or novelty outcome + NEEDS-VERIFICATION count); one-off mode returns inline, writes no files.
