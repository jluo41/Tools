haipipe-paper-probe-citation — Changelog
========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 3.1.0 — 2026-07-14 — the HARVEST gate reads the target's state line (R19/R20)

The harvester opened a QA file and transcribed its `## Answer` anchors with NO state check. On the normal path paper-probe's ⑤ INTERPRET gates it, but the DIRECT invocation form (`harvest <stage> <qa_file>`) is published and was unguarded:

- pointed at a `working` file (whose `## Answer` is EMPTY BY CONSTRUCTION) it harvested ZERO anchors and reported a silent no-op — HIDING a live claim;
- pointed at a `superseded-by:` file it transcribed STALE sources into `_CITATION_{stage}.md`, where PLACE then auto-places any key already in `.bib` INTO THE MANUSCRIPT. That is the day-1/day-40 stale-read bug arriving through the HARVEST lane, where the checker's `read-target-superseded` tooth cannot see it.

HARVEST now reads `sed -n 's/^- state:[[:space:]]*//p' <file> | head -1` first: REFUSE on `working` (report "in progress since <started>"), FOLLOW THE CHAIN on `superseded-by:`, REFUSE on a missing state line (`qa-no-state`). Read-only — the harvester still NEVER writes a QA file. Twin: `haipipe-paper-probe-values` 3.1.0.

## 3.0.1 — 2026-07-14

- Harvest mode: input is `harvest <stage> <qa_file>` — the subagent follows the QA file's anchors into the leaf's `sources.md`. The `pick_list` return field is gone (nothing produces it).
- "probe plan" -> question SECTION in ROUTE, the paper-local sweep, and the report template.

## [2.2.2] -- 2026-07-10
## 3.0.0 — 2026-07-14

- PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1b-claims/1b-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
- SUPPLIER DEADLOCK FIXED. This worker is hard-bounded to NEVER search, and its ONLY acquisition door was Agent(haipipe-probe-orchestrator-agent) — which no longer exists, so a citation gap was unfillable: it could not search, and the one door it was told to wait on could not be opened. Acquisition is now: question SECTION -> its `commission:` block, verbatim -> Agent(haipipe-discovery-orchestrator-agent) -> the answering QA file, whose `## Answer` anchors ([→ sources.md#S02]) are the pick_list this worker transcribes. The dead `read|verdicted` sweep predicate becomes `answered | read | answered-local`.

Fixed (fresh-agent audit, C6/M13)
- Phase 4 PLACE made md-first: replace the matching \cite{TOADD} in the .md, then sync (was "place in tex + parenthetical in outline").
- Adoption rule hardened: a sibling's ✅/📌 triggers a .bib re-grep before PLACE (pointer, not proof).

## [2.2.1] -- 2026-07-10

Changed (JL: "for the citation and the value, we prefer to probe previous stages' outcome")
- Paper-local sweep scope widened: prior stages' read|verdicted PP cards are adoptable pointers too — their pick_list/refs name already-reviewed discoveries/*/sources.md (pointer-following, not discovery).

## [2.2.0] -- 2026-07-10

Changed (JL: "you can check previous stage's _CITATION instead of do the heavy one")
- Phase 2 ROUTE: paper-local sweep before any probe plan — grep other stages' _CITATION_*.md maps + the .bib; matches are ADOPTED (`Note: adopted from _CITATION_<stage>.md`, status + provenance carried; ✅/📌 elsewhere -> PLACE directly, 🔍 stays 🔍). Only surviving gaps become probe-plan suggestions.

## [2.1.0] -- 2026-07-10

Changed (JL ruling: real citations from .bib in the draft)
- New Hard Boundary 4: `\cite{TOADD}` is the draft's citation slot (legacy `[CITE:]` treated the same). PROBE greps TOADD, maps each slot to its `_CITATION_` row, finds candidates; TOADD -> real-key replacement happens in the .md FIRST and only after the human's bibtex lands in .bib. Old boundary 4 (USER comments) renumbered to 5.

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
