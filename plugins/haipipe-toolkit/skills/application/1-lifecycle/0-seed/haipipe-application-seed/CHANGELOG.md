haipipe-application-seed — Changelog
====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [3.3.1] — 2026-07-14

Fixed (LIVE-INSTRUCTION SWEEP — the body still spoke the retired card vocabulary)
- v3.3.0 migrated the frontmatter and the output map but left the BODY on the pre-v8 contract. An agent obeying the body wrote `status: planned` "PP skeletons" and backfilled `refs` — both DELETED fields — into a probe file whose checker only reads `state:` / `target:`. The skeleton was therefore invisible to `check-probe-cards.sh`, and the DRAFT/PROBE gate it is supposed to enforce could not fire.
- Phases block: DRAFT now raises each feasibility question as a question SECTION (`state: planned`, EMPTY `target:`) in `1-probes/PPNN_<topic>.md`; PROBE's worker is described by the five-step loop (ORGANIZE → MATCH → DISPATCH → POINT → INTERPRET) instead of "PP card creation, index bookkeeping, refs backfill".
- Probe-scope + DRAFT/PROBE-line paragraphs: the invariant is now SECTION STATE (`planned` + empty target vs `read` + a target: resolving to a QA file in the bank), not "card state".
- Done-criteria: "probe cards" → probe sections / probe files; the checker line now says every section's `target:` must resolve. `check-probe-cards.sh` KEEPS its filename (spec PART 7).
- Retired words removed from live prose: `status:` (→ `state:`), "card", "skeleton", "refs", "takeaway", "verdict" (→ `reading:`).

## [3.3.0] — 2026-07-14

Changed (PROBE LAYER REDESIGN — Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14)
- Seed-level FEASIBILITY questions (novelty, prior interventions, external-data obtainability) are raised as SECTIONS in `1-probes/PPNN_<topic>.md` with `serves: 0-seed`. The per-stage `0-lifecycle/0-seed/_PROBE/` folder is RETIRED.
- The `[FORWARD -> CLAIMS]` pointer rule is UNCHANGED: internal-data needs stay `_LOG` pointer lines, not questions.

## [1.0.0] — 2026-06-22

- initial version modeled on paper-seed.

## [2.0.0] — 2026-06-29

- added _LOG_0-seed.md changelog; output folder 0-seed/ (was flat file); borrowed .md + _LOG pattern from paper-seed v2.0.0.

## [3.0.0] — 2026-07-06

- stage folder contract; venue-FREE marker (channel = hunch, not pin); DPRC phases; scaffolding delegated to enter get-or-create (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

## [3.1.0] — 2026-07-06

- 765696f port: visible Probes section in the seed doc + ascii artifact formatting.

## [3.2.0] — 2026-07-07

- Port of paper seed 3.5.0 (paper-alignment round 2, SOP §4 row 7, R3+R4): DRAFT may WebSearch to orient (fuel -> prose + buffered `status: planned` skeletons); PROBE scope narrowed to FEASIBILITY only (novelty + external-data obtainability) and must ALWAYS dispatch the real worker (Skill haipipe-application-probe, from-buffer) -- inline search forbidden in PROBE; internal-data profiling (the intervention's own cohort/engagement data) registers as a `[FORWARD -> CLAIMS] PPNN_<slug>` pointer line in _LOG_0-seed.md (a pointer, not a card; consumed at claims DRAFT); new "Probe scope and FORWARD handoff" section; done-criteria gain the check-probe-cards.sh find-pattern verification.
