haipipe-application-draft — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.1.0] — 2026-07-07

- Port of paper draft 3.4.0/3.5.0 (paper-alignment round 2, SOP §4 row 6, R3): allowed-tools gains WebSearch, WebFetch; new "DRAFT may search; PROBE must dispatch" section -- inline search is DRAFT-only orientation fuel with two legal destinations (stage-doc prose; buffered `status: planned` PPNN skeletons), never refs/findings into cards; real evidence lands only via haipipe-application-probe; the line is card state, mechanically enforced by check-probe-cards.sh at VERIFY/CHECK.

## [1.0.0] — 2026-07-06

- NEW phase worker (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0; full-DPRC ruling R4).

## [1.2.0] — 2026-07-09

- Template registry added (ladder restage follow-up, JL: stage skills had "no ref/ no template"): WRITE now reads the calling stage's canonical `ref/<stage>-template.md` alongside its SKILL.md artifact spec — 10-row registry table covering seed, the 1a-1d rungs, venue, pitch, narrative, display, section-edit. This worker carries no templates of its own (paper draft parity). The 9 template files live with their stage skills.

## [1.3.0] — 2026-07-09

- RELEASE MENU (JL bench ruling: "at the end of each draft, it should let me know what probes to release as well"): DRAFT gains step 5 PRESENT — the phase reply ends by listing every buffered planned card (PP id — question — mode — route — fills/settles) and stops for the user's release picks. Return contract gains the `probes:` line. Pairs with the probe worker's STEP 1.5 RELEASE GATE (2.1.0), which remains the backstop for DRAFT-skipping paths.
