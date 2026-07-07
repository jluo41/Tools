haipipe-paper-probe-citation — Changelog
========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [2.0.0] — 2026-07-07

Changed (Part-0 harvester ruling, JL: "they are the harveste agents... just one step within the whole probe" + "I think search should be done with haipipe-discovery-orchestrated agent")
- BREAKING: Phase 2 SEARCH retired → Phase 2 ROUTE. This worker NEVER searches (no WebSearch, no Semantic Scholar, no side-channel agents); Phase-1 gaps become probe-plan suggestions handed to the PROBE hub, which dispatches the gateway (SWEEP: reuse | ENRICH — the cheap path for one-off lookups | fresh). Every citation now enters _CITATION_ through exactly one door: gateway → discovery → pick_list → HARVEST → mechanical acceptance. Resolves B8 (the inline-search contradiction with the probe hard boundary) and the "light probe = WebSearch" vocabulary collision (light/full now mean only the gateway modes).
- allowed-tools: WebSearch/Agent dropped; WebFetch retained for pointer-following only (verify a KNOWN DOI/publisher URL in Phase 5 REVIEW).
- Provenance legend: `agent-found via WebSearch` retired → `harvested` (gateway provenance); historical agent-found entries downgraded to 📋-grade until REVIEW verifies.
- B7: the _CITATION_ file-organization template's "Density by paragraph" markdown table → bullet lines (the template was teaching a format its own acceptance grep rejects).
- Sibling shape description updated to the harvester model (all three workers = harvest step; citation/values now share AUDIT→ROUTE→CANDIDATE→PLACE→REVIEW; display = AUDIT→PLAN→LINK→REVIEW).

## [1.6.0] — 2026-07-07

Fixed
- Phase 1b tool repointed from the never-shipped `check_refs.py` to the sibling `checks.sh` (bash, stdlib only) at `../../3-check/haipipe-paper-check/`; audits `\label`/`\ref`/`\cite` resolution and bibtex-in-markdown, with `--md`/`--depth` options.
- `predecessors:` frontmatter corrected — was self-referencing this skill; now names the two archived skills it absorbed (`haipipe-paper-edit-check-reference` Phase 1, `haipipe-paper-edit-manual-review-citations` Phase 5).
- Sibling-shape claim corrected: citation/values/display do NOT share one lifecycle (values uses TRACE, display uses PLAN→ROUTE→LINK); each owns one working-doc type.

Changed
- No-bibtex rule de-duplicated (was restated ~10×): kept in the frontmatter `description`, one Hard Boundaries rule, and one anti-pattern; removed the pure-repeat restatements (summary parenthetical, Hard Boundaries Rule 5, CHECK-tips parenthetical, redundant anti-pattern).

## [1.5.2] — 2026-07-05

Changed (test-123333333: harvest read the spec but rendered the status as `retrieved ✅ (discovery, arXiv API 2026-07-05) · JL bibtex ⬜` — same meaning, different string)
- Canonical status strings declared VERBATIM: they are grep anchors, not templates to reword. Semantically-equivalent renderings are defective cards; the probe worker's acceptance grep is literal (worker 2.4.1).

## [1.5.1] — 2026-07-05

Changed (test-2-2222: all 5 harvest cards said "🔍 candidate (unverified)" while sources.md held 15/15 VERIFIED-with-method; JL: "每一个都是unverified的，为什么")
- Status rule hardened: two levels, never flattened. Discovery-verified sources carry `VERIFIED-by-discovery (<method>, <date>) · 🔍 awaiting JL Scholar+bibtex`; bare "unverified" on a discovery-verified source = defective card (discards earned provenance). 🔍 half never auto-clears (Scholar+bibtex are human-only).

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
