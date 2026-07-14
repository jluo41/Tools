haipipe-application-revise — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.0.1] — 2026-07-14

Fixed (LIVE-INSTRUCTION SWEEP — probe redesign, Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3)
- WEAVE told the worker to replace a flagged NEED with "the anchored takeaway or verdict-backed statement". Both carriers are RETIRED: `## Takeaways` and `## Verdict` are DELETED blocks (R7), and `check-probe-cards.sh` FLAGS either word as dead vocabulary — so the instruction pointed the worker at text that no longer exists on disk.
- WEAVE now names the live carriers: a probe section's `reading:`, anchored to the QA file its `target:` points at, or a claim already settled in `1-claims.md` (the only home of a claim's status).

## [1.0.0] — 2026-07-06

- NEW phase worker (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0; full-DPRC ruling R4).
