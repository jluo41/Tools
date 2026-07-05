haipipe-discovery-idea — Changelog
==================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.0.0] — 2026-07-03

### Added
- Created (JL: each type gets its own specialist, now that buckets = types 1:1). Owns the Idea type's Execute — the full ideation loop: idea_generation (idea-creator -> `ideas.md`, ranked candidates with novelty tags + testability) and novelty_check (novelty-check -> `verdict.md`, closest prior work as one-paper-one-subsection).
- Post-validation patch: return contract to the caller (terminal path + candidate count or novelty outcome + NEEDS-VERIFICATION count); one-off mode returns inline, writes no files.
