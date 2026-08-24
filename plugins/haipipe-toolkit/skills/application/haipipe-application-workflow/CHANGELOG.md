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

0.4.0 · 260824 · JL (restyled after haipipe-paper-workflow 0.5.0)
- Phases are NAMED BY THEIR AUTHORITY PAGE, old verb kept as a parenthesized alias: Meta (scope), Chain (climb), Wisdom (hand off), Brief (frame), Design (compose). One vocabulary, not two.
- ACCEPT retired AS A PHASE. Its acceptance row lives on P4's own division, so it had no authority page of its own; a phase that cannot name one is a gate wearing a phase's clothes. It is now G5.
- Gates numbered G0-G5, each a grep-able assertion over pages that already exist, replacing three prose bullets.
- The FOURTH human gate named: card release inside P4. haipipe-design added it on 260824 and this file still said "three gates" while four were live.
- Receipts move onto the pages that grant them (the paper family's rule). The _runs/application/log.md line is demoted to a trace, and a trace that disagrees with the pages loses; the old text admitted the location had NO auditor.
- Added: the terminology law, why-this-is-not-the-retired-lifecycle-lane with its deletion test, the group mapping, a gazette of retired names, the never-scheduled rule, and how to resolve "what phase are we in" (highest gate whose assertion holds, per lane and per question).
- The climb loop and the compose loop each stated as a lap with three pens that never cross, mirroring the paper family's establish loop.

