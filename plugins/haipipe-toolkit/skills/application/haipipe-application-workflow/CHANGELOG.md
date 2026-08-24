# haipipe-application-workflow · version history

0.1.0 · 260823 · JL
- New skill, split out as the Application family's RUN head, mirroring the page family's "one folder, one head skill" pattern (haipipe-page-workflow).
- Six phases in two lanes: InsightBoard SCOPE/CLIMB/HANDOFF, DesignBoard FRAME/COMPOSE/ACCEPT, joined only at the PageX crossing.
- Three human gates, always blocking: probe release (per page, inside CLIMB), handoff signing, acceptance.
- Phase state derived from disk, shared with haipipe-application's Status verb; no status file.
- Partition-major climb order: F template first, partition groups in parallel, X group, then W pages citing the verdict.
- One-line run receipt at <application-root>/_runs/application/log.md; page receipts stay the detailed record.

0.2.0 · 260823 · JL (reviewer audit)
- Every page dispatch pins mode: copilot, because page-auto defers approved:/accepted: onto the --owed ledger and would mechanically pass gates 1 and 3.
- Explicit phase-to-frontier mapping table; maturity stays solely the Status verb's output.
- "Signed" defined: the person's tick on the W page's Design Handoff division; the workflow reads it, never writes it.
- The PageX dataset-first alternative to a local handoff acknowledged at the crossing.
- Climb order owned by this skill explicitly (F's D/I/K first, mirrors in parallel, X, every W last); fold only on CLOSE; the receipt location marked unaudited; lane-emoji prefix to disambiguate phase digits.
