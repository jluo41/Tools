haipipe-application-claims — Changelog
======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [5.2.1] — 2026-07-14 — one name per thing

Changed
- Convention pointer repointed: `../../../haipipe-application/fn/probe-plans.md` → `fn/probes.md`. The document is unchanged; only its name is. The paper twin was already `fn/probes.md`, and `skills/STRUCTURE.md:63` lists `1-probe-plans/` among the layer's dead words — so the application bucket was the last place preserving the retired noun as a live filename. One name per thing.

## [5.2.0] — 2026-07-14

Changed (PROBE LAYER REDESIGN — Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14, ruling R7)
- **THE CLAIM LEDGER IS NOW THE ONLY HOME OF A CLAIM'S STATUS.** R7 killed the probe `## Verdict` block and the `verdicted` state, so `supported | refuted | inconclusive` — plus `confidence`, `claim_type`, and the G1/G2/G3 gates — land HERE, per-claim, private to this intervention. A probe section's `reading` FEEDS this ledger; it no longer carries a judgment of its own. (Judgment CONTENT is still governed by the probe-review skill — only its LANDING SITE moved.)
- Why this is not bookkeeping: two consumers reading the SAME bank fact may legitimately reach DIFFERENT judgments about their own claims. The fact is shared; the judgment is not. Putting the verdict in the probe froze consumer-1's frame into evidence that was supposed to be reusable.
- Probe files live at `1-probes/PPNN_<topic>.md` (one file per topic, one SECTION per question); the per-stage `_PROBE/` folder and the `1-probe-plans/` index are RETIRED. Section states: `planned | commissioned | answered | read | answered-local | failed`.
- DRAFT now RAISES the questions and dispatches nothing; the PROBE phase MATCHes the bank's QA corpus first (most questions stop there — a commission is the exception) and commissions only what is missing, straight to the task/discovery orchestrators (the probe gateway is retired).
- `--backfill <PPNN>` reads the section's `reading`, not a verdict block.
- NEW done-criteria, both mechanical: every settled claim traces to a section whose `target:` RESOLVES to a QA file on disk (a status with no resolving target is the exact shortcut this ledger exists to prevent); and no section is `planned` or OVERDUE-`commissioned` (`check-probe-cards.sh --stage 1-claims`).
- NEW principle: this stage NEVER executes bank work inline (LAW 1). It raises questions; the probe worker binds them. A claims session that opens `tasks/.../results/` and starts writing has already broken the wall.

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
