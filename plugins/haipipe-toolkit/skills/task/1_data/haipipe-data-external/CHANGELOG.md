haipipe-data-external — Changelog
=================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.2.0] — 2026-07-08

- skill-diagnose fixes: `code-dev/0-EXTERNAL/` now explicitly a WellDoc-SPACE snapshot everywhere (caveats added to fn-2-cook, fn-3-design-chef, asset-catalog; SKILL caveat trigger corrected to "without code-dev/0-EXTERNAL/" — REACH has a gitignored code-dev/ leftover); `@{YYMMDD}R{N}` tag claim softened (discover via $EXTERNAL_VERSION, e.g. @v1215); patient_id join key stated consistently (cohort joins on patient_id_encoded; external column becomes patient_id_original) in asset-catalog + join-contract; WellDoc SourceSet example names -> placeholders/REACH names; dispatch-table column header fixed ("fn doc to read" — most rows are this skill's own fn/ docs).

## [1.1.0] — 2026-07-04

- wired into the /haipipe-data dispatcher (was orphaned while claiming dispatcher parentage).

## [1.0.0] — 2026-05-31

- baseline metadata added.
