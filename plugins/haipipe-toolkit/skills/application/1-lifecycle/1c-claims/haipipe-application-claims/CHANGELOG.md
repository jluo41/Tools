haipipe-application-claims — Changelog
======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [7.2.0] — 2026-07-17

- Q-consumer migration (full, option A): the rich in-doc `Probes` PP evidence-plans move OUT to 1-probes/ (where they already live); the stage doc keeps a lean `Q-consumer` (`## Q` question blocks) + the Evidence Campaign. mode/route/Refutes-if organize into the probe file at APPROVE. Template + SKILL (description, DRAFT line, artifact block) updated.

## [7.1.0] — 2026-07-17

- Template D1 (silent-defect fix): the Probes section's PP02 used `Status: <status>` with no Refutes-if while PP01 used `State: <full enum>` + Refutes-if — PP02 now mirrors PP01. This lives in 1c-claims.md, which the probe-file checker does not scan, so the drift was silent and would have propagated the retired `Status` field to every intervention copying PP02.

## [1.0.0] — 2026-06-22

- initial version modeled on paper-claims.

## [2.0.0] — 2026-06-23

- added claims_depth (light/medium/full) driven by venue profile.

## [3.0.0] — 2026-06-29

- added _LOG, _EVIDENCE_ tracking file, _PROBE/ subfolder for claim-gap probe plans (was flat 1-probe-plans/). Output folder 2-claims/ (was flat file). Borrowed per-stage tracking pattern from paper.

## [4.0.0] — 2026-07-06

- venue-FREE ledger moved BEFORE venue; stage folder + _LOG + _EVIDENCE_ + _PROBE/ cards + index; settlement-depth-at-gate replaces content-depth modes; supported|refuted|inconclusive enum; plan-from-need retired (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

## [5.0.0] — 2026-07-06

- Port of paper claims 4.0.0 (765696f): evidence-campaign brain — three sections (Claims short / Probes full / Evidence Campaign with dispatch order + deps); no Hypotheses section (app delta, mechanism lives in seed/pitch); _EVIDENCE_ → _VALUES_; _CITATION_ sectioned venues only; settlement gate reads the campaign table; ascii heading + one-sentence-per-line artifact formatting.

## [5.1.0] — 2026-07-07

- Port of paper claims 4.1.0 (paper-alignment round 2, SOP §4 row 8, R4): FORWARD reader clause — claims DRAFT opens by grepping seed's `_LOG_0-seed.md` for `[FORWARD -> CLAIMS]` pointers; each becomes a PP entry in Probes + an Evidence Campaign row or is explicitly declined in `_LOG`; new done-criterion fails CHECK on any unconsumed pointer. Closes the writer-without-reader gap at the seed→claims handoff.

## [6.0.0] — 2026-07-09

- Ladder restage (SOP-ladder-restage.md, JL 2026-07-09): stage 1 split into the venue-FREE evidence ladder 1a-descriptions -> 1b-themes -> 1c-claims -> 1d-principles (echoing D->I->K->W); this skill is now rung 1c, the K rung. Folder git-mv'd `1-lifecycle/1-claims/` -> `1-lifecycle/1c-claims/`; intervention paths `0-lifecycle/1c-claims/1c-claims.md` (+ `_LOG`/`_VALUES_`/`_CITATION_`/`_PROBE/`).
- Slimmed to pure claim work: claims carry theme tags (`C1 (T1, primary)`) resolving to 1b; a claim with no theme parent loops back to 1b instead of orphan-tagging.
- FORWARD reader clause MOVED to 1a (R5): 1a consumes seed's `[FORWARD -> CLAIMS]` pointers and materializes verdict-shaped needs as planned PP skeletons in this doc's Probes section; this rung inherits them at DRAFT.
- Insight KB downgraded to optional anchor (R7): `supported` requires a full-mode probe verdict or equivalently reviewed result; K/W cards valid when present, never required. New done-criteria: theme tags resolve; no unresolved `[STALE ...]` tags (1a refresh stamps, R3).
- Handoff changed: promote -> principles (1d derives the directives); venue/pitch move after the ladder gate.
- ref/claims-template.md added (canonical artifact template adapted from paper's: theme tags, no Hypotheses, mode/route probe fields; JL follow-up 2026-07-09) + SKILL.md pointer line.

## [6.1.0] — 2026-07-09

- BREADTH ROUND (JL flywheel discussion): full hook consumption — every 1b hook becomes a C entry or a line in the new Declined-hooks section (the rung's reservoir, re-mined at every DRAFT open). Every primary claim carries a Rival line (the strongest alternative explanation); its probe plan must be refute-capable (Refutes-if: states the result that would FLIP the claim, not only confirm it).
- Multi-round DPRC (self-assess -> [ROUND n] -> CHECK when dry; medium+ venues loop-until-dry on THIS rung) + mid-phase back-routing ([ROUTE -> themes], [ROUTE -> descriptions]) per wiki/08 Rounds.
