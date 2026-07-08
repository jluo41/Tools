haipipe-discovery-review — Changelog
====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.0.0] — 2026-07-03

### Added
- Created (JL: each type gets its own specialist, now that buckets = types 1:1). Owns the Review type's Execute: judge (prior_art_check / counterevidence -> `verdict.md`) or synthesize (landscape_review / benchmark_landscape -> `landscape.md`); dispatches research-lit / comm-lit-review / academic-researcher.
- Canonical home of the five-rule Review Output Contract (moved from the orchestrator, which keeps a pointer).
- Post-validation patch: return contract to the caller (terminal path + verdict status or cluster/gap counts + NEEDS-VERIFICATION count); one-off mode returns inline, writes no files.
