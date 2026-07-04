haipipe-paper-probe-citation — Changelog
========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [1.5.0] — 2026-07-04

Changed (JL: agent produces, worker reviews)
- Harvest is ALWAYS a dispatched subagent: input = probe agent's pick_list; the subagent opens only the picked sources.md entries in its own clean context, expands them into _CITATION_ cards, writes the file, returns counts. The calling worker does mechanical acceptance only (card count, summary/finding/anchor present, no bibtex) — producer and reviewer are never the same context. Transcribe-inline form retired.

## [1.4.1] — 2026-07-04

Changed
- Harvest card format fixed: one paper per ### with summary + finding + relevance bullets (transcribed from the manifest); identity-only entries are a DEFECTIVE harvest. Numbered one-line entries demoted to bare reference lists in demand-pull phases only.

## [1.4.0] — 2026-07-04

Changed
- Harvest gains two forms: TRANSCRIBE (default, inline — input is the probe agent's structured sources manifest; no project files read in the paper session) and SUBAGENT (fallback for >~20 entries or multi-discovery merges — walks the refs in its own clean context and writes _CITATION_ directly).

## [1.3.1] — 2026-07-04

Changed
- Harvest format relaxed: within a `##` literature group, numbered one-line entries are as valid as per-`###` subsections (house rule allows numbered one-line reference lists); tables remain forbidden.

## [1.3.0] — 2026-07-04

Added
- HARVEST mode (supply-push, any stage): distill sources a probe brought back into `_CITATION_{stage}.md` — walk probe_ref -> evidence_refs -> discovery sources.md, one paper per ### subsection with source_ref provenance, 🔍 candidates only, NO fresh searching in harvest mode. Called by haipipe-paper-probe after a gateway probe returns (seed landscape case).

## [1.2.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE).

## [1.1.0] — 2026-07-02

- no bibtex in _CITATION_ (plain-text descriptions only); provenance tracking (🧑/🤖/📋 source); .bib↔_CITATION_ sync protocol in Phase 1; key-discovery step in Phase 4; user tips section.

## [1.0.0] — 2026-07-02

- merged check-reference (mechanical audit) + manual-review-citations (pre-submission 3-axis walk) + 4 feedback items into one skill with 6 phases. Defined hard boundaries. Defined _CITATION_ candidate format.

## [0.0.1] — 2026-06-29

- stub with scope only.
