haipipe-insight-data — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [2.1.0] — 2026-07-05

- Mandatory-read paths fixed: `../../ref/` → `../ref/` (5 sites; the old prefix resolved to a nonexistent skills/ref/).
- Probe source paths flattened to the real shape `probes/<MMDD>_<slug>/` (was a two-level GROUP/NN form that exists nowhere on disk).
- Step 1 now parses `--dataset` and `--id` (both were in the argument-hint but missing from the parse list).
- Grammar: "a approved by review ... source" → "a review-approved ... source" (bulk-sed artifact), in description and body.

## [2.0.0] — 2026-06-22

- recut to the in-sample model (JL). D = ONE named dataset's profile (require `dataset:`, no p/CI). A null/ns finding is no longer an 'inconclusive D' — it is a K (does not generalize).

## [1.1.0] — 2026-06-20

- repositioned as review-called writer API; source_ref may be task/probe/discover/lit.

## [1.0.0] — 2026-05-31

- baseline metadata added.
