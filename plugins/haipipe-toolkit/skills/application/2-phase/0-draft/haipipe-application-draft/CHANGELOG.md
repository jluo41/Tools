haipipe-application-draft — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [1.2.1] — 2026-07-14 — one name per thing

Changed
- Convention pointer repointed: `../../../haipipe-application/fn/probe-plans.md` → `fn/probes.md`. The document is unchanged; only its name is. The paper twin was already `fn/probes.md`, and `skills/STRUCTURE.md:63` lists `1-probe-plans/` among the layer's dead words — so the application bucket was the last place preserving the retired noun as a live filename. One name per thing.

## [1.2.0] — 2026-07-14

Changed (PROBE LAYER REDESIGN — Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14)
- DRAFT IS THE BIRTHPLACE OF THE QUESTIONS. What it cannot answer, it RAISES as a question SECTION (`state: planned`, empty `target:`) in the right topic's probe file under `1-probes/PPNN_<topic>.md` — not as a PPNN card skeleton in a per-stage `_PROBE/` folder (RETIRED), and not as an index row in `1-probe-plans/README.md` (RETIRED).
- DRAFT may write the `commission` (the question in general language) when the question is already clear. It may NEVER write the `## Why` into a commission: the stake stays in the probe file. Always.
- The line is now SECTION STATE, not card state: DRAFT leaves `planned`; only PROBE reaches `read`, with a `target:` that RESOLVES to a QA file in the bank. `check-probe-cards.sh` enforces it mechanically at VERIFY and again at the CHECK gate.
- The WebSearch-as-orientation-fuel rule (v1.1) is UNCHANGED: "DRAFT may search; PROBE must dispatch."

## [1.1.0] — 2026-07-07

- Port of paper draft 3.4.0/3.5.0 (paper-alignment round 2, SOP §4 row 6, R3): allowed-tools gains WebSearch, WebFetch; new "DRAFT may search; PROBE must dispatch" section -- inline search is DRAFT-only orientation fuel with two legal destinations (stage-doc prose; buffered `status: planned` PPNN skeletons), never refs/findings into cards; real evidence lands only via haipipe-application-probe; the line is card state, mechanically enforced by check-probe-cards.sh at VERIFY/CHECK.

## [1.0.0] — 2026-07-06

- NEW phase worker (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0; full-DPRC ruling R4).
