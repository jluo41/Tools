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


0.5.0 · 260827 · JL
- The climb loop's interior law delegated to the new insight door /haipipe-insight (0.1.0), exactly as 0.3.0 delegated the compose loop to /haipipe-design. The section heading gains "(delegated)" and its first line names the owner.
- This file keeps what was always its own: the lap, the partition-major climb ORDER, and gates G0-G3. The three-pens text stays in the section as an echo, mirroring the compose loop's treatment, with the door as its law home.
- Intro and description updated: the workflow never states EITHER board's interior law.

0.6.0 · 260827 · JL
- The insight lane gains its own phase machine, haipipe-insight-workflow 0.1.0: six phases named by the lane's six page types (I0 Meta, I1 Question, I2 Data, I3 Information, I4 Knowledge, I5 Wisdom), gates GI0-GI6, the register CELL (question × partition) as the frontier unit.
- Refinement, not contradiction, and the mapping is declared in both files: 🔎P0 = I0+I1, P1 = I2-I4, P2 = I5; G0-G3 read the same cells GI0-GI6 assert over.
- The partition-major climb order moved to that machine, which owns it; the section here becomes the refinement table and a pointer. This file stays the authority for the two-lane view, the PageX crossing, gates G0-G5, and where a run stops.
- Cold-read audit fixes (260827, fresh-context tester): the climb-loop join restated as a ROUND TRIP (the cell cites the closing page by id; that page's handoff SERVES row names the question id back) — the old "one string in three places" matched no conformant board; G1's subject corrected (a question faces ONE rung; the chain below the frontier page is walked by citations); "two sit inside one" → one each inside P1 and P4; the lap entry accepts any unsettled register state, deferring the cell vocabulary to haipipe-page-for-question 0.3.0.

0.7.0 · 260827 · JL
- The design lane gains its symmetric interior machine, haipipe-design-workflow 0.1.0: D0 Brief, D1 Direction, D2 Unit, D3 Verdict, D4 Division, gates GD0-GD5, the DIVISION as frontier unit, the ROUND, the two-faced verdict (reflect ex-post · prospect ex-ante) and the EMIT edge into the insight lane's registers.
- Refinement, not contradiction, declared in both files: 🎨P3 = D0, P4 = D1-D4; G4 = GD0; G5 = GD5's all-accepted close. This file stays the authority for the two-lane view, the crossing, G0-G5, and where a run stops.

0.8.0 · 260827 · JL (cold-read repair, in step with haipipe-design-workflow 0.2.0)
- The naming law gains its stated tier: a lane machine finer-grained than the page names phases by authority ARTIFACT class, same cannot-name-one-is-a-gate test.
- G5 defers to haipipe-page-for-design's acceptance-row grammar (the old field list failed every live accepted row on B00) and admits the emitted: terminal.
- The compose loop's release line admits the recorded blanket over NAMED cards (haipipe-plugin-direction 0.3.0), which B00's live run had already used without a law behind it.

- 0.8.1 (260828, same-day sync riders): the compose-loop sketch reads card.md-in-thread-folder (one-thread-one-folder merge) and cites haipipe-plugin-design §card law 1 (haipipe-plugin-direction deleted); the design-lane phase list gained D1 Card and D5 PageDown.