haipipe-discovery-search — Changelog
====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.1.0] — 2026-07-05

Changed (JL, test-2-2222: "为什么 nature human behaviour / pnas 之类的没有被搜?" — arXiv-only sweep misses no-preprint journal literature)
- CHANNEL DIVERSITY mandatory: preprint channel + journal-index channel (semantic-scholar -> OpenAlex/Crossref on rate-limit) every run; knowledge-first confirmations do not count as a sweep.
- TOP-VENUE PASS in full-mode novelty (queries filtered to field flagship venues); light mode records the skipped pass as a coverage caveat.
- sources.md preamble carries the COVERAGE DECLARATION (channels searched AND not searched) per ref/source-format.md.


## [1.0.0] — 2026-07-03

### Added
- Created (JL: each type gets its own specialist, now that buckets = types 1:1; mirrors haipipe-data-source etc.). Owns the Search type's Execute: FIND (arxiv / semantic-scholar / exa-search) + READ (alphaxiv / deepxiv / paper-analyzer) -> `sources.md` + `notes.md`.
- Post-creation patch after a cold-context validation run surfaced gaps: one-off mode spelled out (inline return, no files, local-first when a project is visible), `role:` <-> terminal note, cross-category worker dispatch + answerability stopping rule, VERIFIED defined as independent exact-title lookup, return contract to the caller (terminal paths + source count + NEEDS-VERIFICATION count; discovery.yaml is the orchestrator's to write).
