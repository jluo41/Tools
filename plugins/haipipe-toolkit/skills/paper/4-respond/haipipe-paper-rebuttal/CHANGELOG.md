haipipe-paper-rebuttal — Changelog
==================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 1.1.1 — 2026-07-19 — vocabulary: a probe question is an ENTRY, not a SECTION

### Changed
The probe file's unit of one question was renamed `## Q-<Stage>-<n>` SECTION (flat `serves:` /
`target:` / `a-consumer:` fields) -> `## QX<n>` ENTRY (four `###` subsections) when the probe model
changed. This file still said SECTION, so an agent reading it wrote the OLD flat structure, which
`check-probe-cards.sh` FAILs as `stale-old-format` -- that stage's PROBE phase could then never go
green. Mechanical rename, no design change. (JL ruling 2026-07-19, board 260719-04-SEED-2PHASE D5:
"如果这样的话，那还是叫entry 吧". Swept 31 lines across 15 files; phrase-level, because "section"
also legitimately means a MANUSCRIPT section in these docs.)

## 1.1.0 — 2026-07-14

- AUTO_EXPERIMENT + the evidence-gap flow: raise one question SECTION per experiment; ② MATCH runs first (a rebuttal experiment is often already answered by an existing task's QA file) and only what MATCH cannot close is commissioned. The "evidence gateway" reference is removed.

## [1.0.0] — 2026-05-31

- baseline metadata added.
