haipipe-application-revise — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [0.1.1] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.1.0; older entries below keep their original numbers).

## [1.1.0] — 2026-07-19

- WEAVE step disambiguated: it folds in the STAGE DOC's a-consumer (the Q-consumer `Answer:` line,
  station 2), not a probe-file field. Vocabulary: `a-consumer:` as a PROBE-FILE FIELD is gone — the probe entry's answer subsection is
  `### a-executor` (the copy of the answering QA file's answer, the consumer-side single source of truth).
  The a-consumer CONCEPT is untouched: it remains the per-consumer interpretation written in the STAGE DOC
  (station 2, anchored `[source: PP<NN>]`).

## [1.0.0] — 2026-07-06

- NEW phase worker (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0; full-DPRC ruling R4).
