haipipe-individual-inference — Changelog
========================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [0.1.2] - 2026-09-28 - No content hashes (JL 260928)

- AGENTS.md rule 9: `src/forecast_evidence.py` drops `file_sha256`. The report evidence binding is checked by content: report.json equals the report, and the forecast recomputed from forecast.json matches the bound selection and the report's summary. A leftover `*_sha256` field is ignored.

## [0.1.1] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.1.0; older entries below keep their original numbers).

## [1.1.0] — 2026-07-04

- sibling description corrected: haipipe-individual builds Subject-* folders (not 'loads data only').

## [1.0.0] — 2026-05-31

- baseline metadata added.
