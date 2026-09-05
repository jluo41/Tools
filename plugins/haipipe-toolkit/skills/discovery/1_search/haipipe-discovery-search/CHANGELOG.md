haipipe-discovery-search — Changelog
====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## 0.5.0 · 2026-09-04

- Keep acquisition under D1 `ACQUIRE`, route source-map/source-reading craft
  through Page `03 CONTENT / WRITE`, and make the cross-workflow handoff
  explicit.

## [0.4.1] — 2026-09-03

- Route citation aggregation through the Outline Evidence Workspace at
  `outline/evidence/bibex/`; the retired Evidence plugin is compatibility-only.

## [0.4.0] — 2026-09-02

- Own ACQUIRE craft across Discovery and contribute source-map/source-reading
  article work during SYNTHESIZE; Evidence owns citation aggregation.

## [0.3.0] — 2026-09-01

- Serve the canonical `source-map` and `source-reading` Discovery Page Types;
  Search is now a specialist route rather than the durable type field.
- Write the root Page in its promised article form and declare Discovery
  runtime family plus paper/source analysis operation for every admitted Run.

## [0.2.0] — 2026-09-01

- Search now finds candidates, resolves canonical Subjects, and materializes
  one numbered paired Paper Run/Result per admitted source.
- Topic Page source maps are derived from Results; new monolithic
  `sources.md`/`notes.md` ledgers are forbidden.
- Secondary links are Triggers; the resolved evidence Subject owns RUNNAME and
  the one-entry Result Bib.


## [0.1.3] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.3.0; older entries below keep their original numbers).

## [1.3.0] — 2026-07-08

Changed (JL: API keys now live in env.sh / env.ps1 — make the channels key-aware)
- Workers block documents the env contract: `SEMANTIC_SCHOLAR_API_KEY` (non-empty = keyed S2, sweep confidently; empty = ~1 req/s, fall through to OpenAlex/Crossref on 429), `EXA_API_KEY` (empty = exa channel UNAVAILABLE — skip and record in the coverage declaration instead of burning turns), `OPENALEX_MAILTO` (append `&mailto=` for the polite pool).


## [1.2.0] — 2026-07-08

Changed (JL: pin the mechanical sweep half to Haiku so wide fan-out runs cheap)
- FIND step: wide sweeps (2+ channels or 3+ queries/channel) MAY fan out `haipipe-discovery-search-worker-agent` (new, `model: haiku`, no Write/Edit) one per channel in parallel, when the running context has the Agent tool. Workers harvest + transcribe + verify only; the dispatcher keeps relevance curation, cross-channel dedup, and all writes to sources.md/notes.md.


## [1.1.0] — 2026-07-05

Changed (JL, test-2-2222: "为什么 nature human behaviour / pnas 之类的没有被搜?" — arXiv-only sweep misses no-preprint journal literature)
- CHANNEL DIVERSITY mandatory: preprint channel + journal-index channel (semantic-scholar -> OpenAlex/Crossref on rate-limit) every run; knowledge-first confirmations do not count as a sweep.
- TOP-VENUE PASS in full-mode novelty (queries filtered to field flagship venues); light mode records the skipped pass as a coverage caveat.
- sources.md preamble carries the COVERAGE DECLARATION (channels searched AND not searched) per ref/source-format.md.


## [1.0.0] — 2026-07-03

### Added
- Created (JL: each type gets its own specialist, now that buckets = types 1:1; mirrors haipipe-data-source etc.). Owns the Search type's Execute: FIND (arxiv / semantic-scholar / exa-search) + READ (alphaxiv / deepxiv / paper-analyzer) -> `sources.md` + `notes.md`.
- Post-creation patch after a cold-context validation run surfaced gaps: one-off mode spelled out (inline return, no files, local-first when a project is visible), `role:` <-> terminal note, cross-category worker dispatch + answerability stopping rule, VERIFIED defined as independent exact-title lookup, return contract to the caller (terminal paths + source count + NEEDS-VERIFICATION count; discovery.yaml is the orchestrator's to write).
