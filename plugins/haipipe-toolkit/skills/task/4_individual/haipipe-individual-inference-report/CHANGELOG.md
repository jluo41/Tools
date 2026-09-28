haipipe-individual-inference-report — Changelog
===============================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [0.1.2] - 2026-09-28 - No content hashes (JL 260928)

- AGENTS.md rule 9: `meta.json` `evidence_binding` names `forecast.json` and `report.json` plus the selection, with no hashes (`scripts/make_report_cli.py`, `SKILL.md`, `src/report_schema.py`).

## [0.1.1] — 2026-09-20

- Defined a deterministic four-way forecast trend rule and require the report model to follow it.
- Added `confidence=unavailable` abstention when calibrated uncertainty evidence is absent.
- Replaced forced causal attribution with evidence-only explanation or an explicit unknown cause.
- Described trend by exact adjacent-step direction, with no magnitude cutoff or clinical-significance claim.

## [0.1.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.0; older entries below keep their original numbers).

## [1.0.0] — 2026-05-31

- baseline metadata added.
