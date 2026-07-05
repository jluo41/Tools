haipipe-insight — Changelog
===========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [2.0.0] — 2026-06-11

- DIKW producer partition; post-file accumulation check; 3-job design (route + check + dashboard); step-by-step protocol.

## [1.0.0] — 2026-05-31

- baseline metadata added.

## [2.6.0] — 2026-06-20

- renamed user-facing archive flow to review/apply.

## [3.0.0] — 2026-06-22

- DIKW model recut to in-sample-vs-generalization (JL). D/I describe ONE named dataset (require `dataset:`, no p/CI); K is the generalization layer where p/CI/confidence live and has NO probe gate (low-confidence and negative K are recorded); W reads K confidence to set risk posture. Removed the I->K controlled-comparison-probe gate. Updated dikw-boundaries, insight-md-schema, K writer, K/D/I reviewers, review specialist, agents README.
