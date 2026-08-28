---
name: haipipe-insight-workflow
description: >-
  The InsightBoard-level phase machine: six phases named after the six page types the lane owns — I0 Meta (scope) → I1 Question (ask) → I2 Data (observe) → I3 Information (derive) → I4 Knowledge (claim) → I5 Wisdom (hand off) — with gates GI0-GI6, each a checkable assertion over existing pages. The frontier's atomic unit is the register CELL (one question × one partition): phases climb the rows, partitions widen the columns, only the X group lets columns meet, and a partition is born at I0 and nowhere else. It refines the application machine's insight lane (P0 = I0+I1, P1 = I2-I4, P2 = I5) and owns the partition-major climb order; interior law stays with the door /haipipe-insight, page lifecycle with haipipe-page-workflow, every verdict with an independent CHECK plus a human tick. Use when asking which rung a question sits on, whether a cell may advance, what the next runnable page is, where a new subgroup enters, or where a run must stop. Trigger: insight workflow, run the insight board, climb the ladder, next rung, frontier cell, insight phase, add a partition, partition column, /haipipe-insight-workflow.
metadata:
  version: "0.4.0"
  last_updated: "2026-08-27"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-insight-workflow · know the cell, test the gate, mint the next rung

Load `haipipe-insight` first; it says what an InsightBoard IS and this file is its phase authority. It refines `haipipe-application-workflow`'s insight lane and never contradicts it: that machine keeps the two-lane view and gates G0-G5, this one names the rungs inside. It never edits a page, never runs a page's lifecycle (that is `haipipe-page-workflow`), never states board law (that is the door), and never judges content (that is CHECK plus the human ticks).

## 🔤 Terminology law

An **insight phase** is one digit, `I0`-`I5`. A rung PAGE id always carries two digits and usually a partition letter (`I03`, `BI03`), so a one-digit `I<n>` in any Application document is a phase, never a page — the same digit-count rule that already separates phase `P0` from principle page `P01`. Against the application machine: `🔎P0 = I0+I1`, `🔎P1 = I2-I4`, `🔎P2 = I5`; the aliases scope, ask, observe, derive, claim, hand off are legal in prose, never in a folder or page id.

## 🗺 The six phases · the phases are the rungs

A journey phase is NAMED BY ITS AUTHORITY PAGE (the application machine's naming law), and this lane owns exactly six page types, so the ladder itself is the phase spine:

```text
phase                     authority page              what the phase produces
──────────────────────────────────────────────────────────────────────────────
I0 Meta (scope)           MT00-meta                   the inventory: sources, grain,
                                                      window, freshness, limits ·
                                                      the PARTITION REGISTER
I1 Question (ask)         MT01-MT04 registers         the question matrix: one row
                          ← the scoreboard hub        per question, one column per
                                                      partition, a state per CELL
I2 Data (observe)         the D page                  run-bound observations, every
                                                      value bound to a QA file
I3 Information (derive)   the I page                  rates and contrasts from
                                                      named D rows
I4 Knowledge (claim)      the K page                  propositions with strength,
                                                      rivals, boundary
I5 Wisdom (hand off)      the W page                  counsel + the SIGNED Design
                                                      Handoff
   ↺ I1→I2→I3→I4→I5→I1 is the CLIMB LOOP · exits through the register at GI6
```

Two positions deliberately did not become phases, by the test that retired ACCEPT: the pooling VERDICT rides on an ordinary K page in X and is GI4's partition-major assertion, and SETTLE is a register act and is GI6. A position that cannot name a page type of its own is a gate.

Each phase performs one EPISTEMIC OPERATION and each gate is an AUTHORITY TRANSFER: passing GI<n> is the moment the rung below becomes citable and nothing else does — the Climb Law read as a process instead of a structure. That is why the aliases are verbs of knowing (scope, ask, observe, derive, claim, hand off), not verbs of doing.

## ✚ The second axis · partitions are columns, and the frontier is a CELL

Phase is read per question AND per partition: the atomic unit is the register cell, so `QI5` may be ✅ on F, 🟡 on B and ⬜ on D at once, and "what phase is this board in" has no one-number answer — the register matrix IS the frontier map.

A subgroup passes through three moments, each owned by one phase:

```text
noticed   I3/I4   an I page's partition column diverges, or a K boundary names a cut
asked     I1      a register row: does this cut deserve its own ladder?
born      I0      one MT00 partition-register row (letter · filter · config) +
                  one group folder beside X · the door's `partition` verb
```

The ladder notices, the register asks, Meta births — a partition is born at I0 and nowhere else, and it is a CONFIG, never a code change (`ref/partition.md`).

**The partition test, at I0.** A partition is an AUDIENCE stratum: a grouping of the unit the counsel is FOR — in an SMS application, the humans receiving it. Not every cut of the data qualifies; birth requires three yeses, each mechanically checkable:

```text
① disjoint + stable    no counsel unit sits in TWO groups, and none drifts across a
                       boundary mid-window · partitions need NOT be exhaustive: a unit
                       in no group is read by the template alone, and a coverage gap
                       is legal where an overlap never is
② exogenous            not a knob the design chooses (send time, variant, channel
                       are the ARM axis: the design bets on them, nobody serves them)
③ addressable          the DesignBoard could give this group its own DS page
                       (audience × job × venue) — a group no design could target
                       separately can never SPLIT, so it never needed its own ladder
```

The test applies to SUBGROUP partitions only: the template F deliberately contains them all, fails ① by construction, and is seated on MT00's partition register as the TEMPLATE row, not as a partition that passed.

The failures route, they are not discarded — and TIME is the canonical case, wearing three guises with three existing homes:

```text
time as send-knob      weekday/hour of send        fails ② → arm axis, an I column
                                                   (A00's QI4/QI9), a design bet
time as pattern        engagement over the window  an I column, never a group
time as epoch          a new window / next round   a NEW EXTRACT → a NEW InsightBoard
                                                   (the one-dataset law), with MT00's
                                                   freshness rule owning the seam
```

The deep reason: the partition axis exists so the pooling verdict can ask "one counsel or several," and counsel is PER-AUDIENCE — the insight lane's partition columns mirror the design lane's DS-page audience axis. A dimension that could never become an audience can never split the counsel, so making it a partition buys mirrors nobody will consume.

**The routing test, at I1.** The two axes never mix inside one question because registration classifies it once, by one mechanically checkable property — how many partition groups its `what-would-answer` field needs rows from:

```text
rows from ONE group      → a COLUMN question: asked identically of every partition,
                           one cell per column, answered on each partition's own ladder
rows from TWO OR MORE    → an X question: registered once, dot cells on every partition
                           column, answered only in the X group — "how far apart", "do
                           they genuinely differ", "pool or split"
rows from the EXTRACT    → an F-ONLY question: a property identical in every partition
itself, no cut of it       (the variant catalog, the extract's shape, what a next round
                           should learn) · answered ONCE on the template ladder and
                           refused `🚫 F-only` on every partition column, because
                           re-deriving an invariant per partition invites drift
```

A question id is partition-free either way (`QI5` spans all columns; there is no `QI5-B`), so "subgroup" is never a kind of question: it is either the COLUMN a question is asked in, or the SUBJECT of an X question about the columns' relationship.

**The instrument shadow.** Both tests above have a mechanical shadow in the task layer, because every ladder topic is backed by ONE task folder and the reuse pattern must agree with the classification:

```text
a COLUMN question   the SAME folder runs once per partition config — one call may
                    even produce every column's numbers at once (A00's ⬜calc cells)
a PARTITION         configs/<partition>.yaml over the same code · needing DIFFERENT
                    CODE for a subgroup disproves the partition or the topic
an X question       its OWN folder, reading the siblings' outputs — a contrast is
                    a new derivation, never a re-filter
a NEW EXTRACT       the next board re-runs the SAME folders under a new source
                    config — the topic library is an instrument bank that travels
```

The split underneath: the task folder holds the CONVERGENT reasoning (code, one logic for every group and every extract), the page holds the DIVERGENT reasoning (this group's numbers, read in this group's context). Computation is reused; interpretation never is — a mirror page restates no sibling's prose, it re-reads its own numbers.

**How the ladders cross.** Only in X, and X is a mini-ladder with no D of its own — its raw material is the siblings' MIRRORED I rows, which is why its two contract exceptions exist:

```text
XI  contrast        I-from-mirrored-I: the one legal same-rung citation
XK  heterogeneity   claims the difference, with strength and boundary
XK  pooling verdict K-from-K: a claim about claims — POOL or SPLIT
                    └─▶ conditions EVERY W page: under POOL the non-template W
                        defers by id and exports no handoff; under SPLIT the
                        partition W may counsel its own action
```

**The escalation ladder.** A subgroup earns first-class standing in three steps, each with its own trigger, and skipping one is the defect:

```text
L0  a segment column inside an I page      rung-major default · costs one column
      │ trigger: readers keep asking K questions about the segment
L1  a PARTITION with its own ladder        partition-major · born at I0 · mirrors F
      │ trigger: a SPLIT verdict + the subgroup has its OWN consumer
L2  a child InsightBoard                   the verdict page is its birth certificate
```

**Late arrival** (a partition added after siblings have climbed) has four consequences, all mechanical:

```text
① its cells are born ⬜ and NEVER inherit a sibling's refusal — a 🚫 reason is
  re-earned per partition (A00, 260827: three `thin` marks did not survive the
  D partition's arrival; the defect class's sixth instance)
② the X group REOPENS: contrast, heterogeneity and the pooling verdict must be
  recomputed with the new column
③ a reopened verdict stales every W page's verdict citation, template included —
  the W pages are re-conditioned, and re-signed if their counsel moves
④ every OTHER partition's D/I/K pages are untouched
```

A partition may become its own board only by citing a SPLIT verdict; `ref/partition.md` stays the grammar's single source.

## 🔁 The climb, and its one cross-chain order

The door's lap (`haipipe-insight` §The lap, step by step) is HOW a cell moves; this file owns WHERE a cell may move to. Within one chain the order is fixed by the Climb Law: D before I before K before W, no rung skipped. Across chains, a rung-major board has no constraint; a partition-major board has exactly one, because X consumes the mirrored ladders and every W cites the verdict:

```text
F's D/I/K first ─▶ each partition's D/I/K mirror, in parallel ─▶ X group
                                                                  │ XI → XK → verdict
                                                                  ▼
                                                 every W page last, template
                                                 included, all citing the verdict
```

This order moved here from `haipipe-application-workflow` (0.6.0), which keeps a pointer.

## 🚪 The gates

Each gate is an assertion over pages that already exist; a gate that cannot be tested by reading named files is misdesigned. Gates are per-CELL except GI0, which is per-board, and GI4's verdict clause, which is per-column-set.

```text
GI0  Meta → Question      MT00 is past 🔴 and its source resolves to a run · the four
                          registers exist · on partition-major the partition register
                          and the shared-threshold pointer exist
GI1  Question → Data      the cell's row carries target, raiser, what-would-answer,
                          and a state cell · its partition group exists on disk
GI2  Data → Information   the D page is CHECK-closed, every value bound to a QA file
                          by path
GI3  Information → Knowledge   the I page is CHECK-closed and derives only from named
                          D rows (X contrast: mirrored I rows, the one exception)
GI4  Knowledge → Wisdom   the K page is CHECK-closed · on partition-major the X
                          group's pooling verdict exists and is current against the
                          partition register — a late partition voids this gate
GI5  Wisdom → signed      ✋ the handoff's `signed:` row reads `✅ <initials> <YYMMDD>`
                          (haipipe-page-for-wisdom) · `⬜` blocks · no machine
                          writes it · under POOL a non-template W closes as a DEFERRAL
                          by id, exports no handoff, and owes no signature
GI6  settle               the register cell flips ✅, or 🚫 with a reason, or 🟡 <page>
                          final when the page states why the remainder cannot close
                          (for-question) — always citing the closing page ·
                          gaps remain → the next lap
```

A value produced by EXTENDING an already-digested task run binds to the run's new artifact paths; whether the task QA digest reopens is the task layer's law, not this file's — an extension annotates the digest's anchors and never rewrites its answer.

The DERIVED-HEADER rule (for-question) covers every on-register restatement of the Queue — headers, Diagrams, Openings — and status WORDS as well as counts, by the fixed mapping: any lap-eligible cell → 🟡 PARTIAL, all cells terminal → ✅ SETTLED. Reconciling any of them is register-pen work citing the Queue, and authorizing a header fix authorizes the PAGE's derived surfaces, not one division of them.

**The two human gates never have an auto mode**: probe release sits INSIDE any rung page's RUN at its PROBE phase, per page; handoff signing is GI5. Every dispatch pins `mode: copilot`. A blocked gate is a clean stop: report the cell, the waiting artifact, and the person's owed decision.

## 🗃 Group mapping

```text
I0        0-MT-meta/MT00-meta/
I1        0-MT-meta/MT01-MT04/
I2-I4     rung-major:       1-D-data/ · 2-I-information/ · 3-K-knowledge/
          partition-major:  <N>-<L>-<partition>/ with the partition letter prefixed
                            to every page id · X-cross/ for the contrast and verdict
                            (index-free, letters sort last · legacy: 9-X-cross/)
I5        rung-major 4-W-wisdom/, or each partition group's W page
```

## 🚚 Dispatch: one page at a time

```text
select   the frontier cell whose gate is open and whose inputs exist; prefer cells
         the register marks `⬜ calc` (computed, unauthored — for-question)
         before cells needing new runs, because authoring is cheaper than running
load     haipipe-page + the matching haipipe-page-for-<type> contract
run      haipipe-page-workflow over that ONE page · mode: copilot always
fold     move the register cell ONLY on CLOSE; every other terminal is a named
         non-settlement and the cell does not move
repeat   until every cell is settled or a gate blocks
```

A cell whose inputs do not exist is not runnable, and naming WHY is this skill's answer, never scaffolding the missing input silently.

## 🧾 Phase receipts

A transition leaves one receipt on the page that GRANTED it — except a 🟡-final settle, which leaves TWO (§Marks: the register's and the answering page's) — a dated Log row — MT00 for GI0 and every partition birth, the register for GI1 and GI6, the closing rung page for GI2-GI4, the W page for GI5. No separate receipt store is authoritative; the pages are the record.

## ⏱ Advancement is never scheduled

A gate test may be run any time; a gate may only be DECLARED passed by the human tick or CHECK verdict it names. Nothing here may be wired to a timer or a loop that advances cells on wall-clock time.

## 🔀 Resolving "what phase are we in"

Per cell: the highest gate whose assertion currently holds. Per board: the register matrix read whole — and a board-level scalar is a lie this file refuses to mint. The application machine's `🔎P<n>` reading is derived from the same cells (P0 = any register gap, P1 = any cell between GI1 and GI4, P2 = any W owed its tick).

## 🌐 The machine is content-free

Nothing in this file names SMS, messages, or any domain. Domain content enters at exactly three declared points, and substituting all three re-instantiates the whole machine unchanged:

```text
① the EXTRACT       MT00: source, unit, grain, window — a CGM stream, a wearable
                    feed, a claims table are all one `source:` line away
② the QUESTIONS     MT01-MT04: what is asked is the board's, never the machine's
③ the VENUE PACKS   the design side's 8 packs (sms · email · dashboard · report ·
                    push · reminder · checklist · ui-card) — the counsel's outlet
```

The counsel UNIT is whatever MT00's unit-and-grain declares — a patient for SMS, a patient or a patient-event for a wearable board, a provider for a provider-facing one — and the partition test reads "audience" against THAT unit. An observational extract with no arms changes only which questions the registers hold; the Climb Law, the gates, and the verdict machinery do not notice.

## 📜 Contract bumps have a blast radius

A version bump edits no page, yet it can move the frontier: a new closing check un-closes every page that fails it, and the register then contradicts its own pages with nobody having touched either. Two rules make that safe:

```text
① every bump SHIPS ITS MIGRATION NOTE, the way ref/partition.md grandfathers
  9-X-cross/ by name: what happens to artifacts settled under the older version.
  The default is OWE-ON-NEXT-TOUCH — settled cells stay settled, the page owes the
  new check when next opened. The exception is a bump that ADDS A HUMAN GATE
  (a signature, a release): that blocks immediately, because the risk it guards
  is live from the moment it is law.
② the bumping desk COMPUTES THE BLAST RADIUS before shipping: grep the live
  boards for every artifact the new check fails, AND the sibling law for every
  version pin the bump stales, and list both in the migration note by id. A bump
  that names FW01 and silently un-closes FW02 shipped half a migration — and
  sibling citations are best written UNPINNED, so there is nothing to stale.
  A patch that lands a rule must grep the family for every sentence stating the
  OLD rule: two rounds running, a rule split across files was updated in some
  and contradicted by the rest.
```

The register never flips backward on a bump: an affected cell KEEPS its mark and gains the blocked reading at the gate the new check guards, so "settled under 0.2.0, owing under 0.3.0" is visible without rewriting history.

## 🧾 Marks, spelling and receipts

```text
token spelling     a mark's spelling INCLUDES its spacing: `🚫 F-only` is the token,
                   `🚫Fonly` is not it. Canonical forward; a live board is re-spelled
                   only in an authorized sweep, and its tables re-pad in the same
                   sweep — two spellings in one column defeats the mark
a mark is not an edit   🧊 and its kin annotate ADJACENT to a sentence; the sentence
                   itself stays byte-identical. Marking a fenced line is therefore
                   legal where editing it is not
🧊 lifecycle       the mark names its staling event AND its clearing condition; it
                   clears when that condition lands, and a 🧊 whose clearing
                   condition has already occurred is a finding, not a mark
🟡-final receipts  the flip leaves TWO receipts, whoever flips — a person, a lap, or
                   a charter: the register's Log row QUOTING the licensing sentence,
                   and one dated row in the ANSWERING page's ## Log naming the
                   QUESTION id and the word final (the shape the checker scans) —
                   staleness travels by citation, and a citation invisible from the
                   cited end cannot travel
```

## 🛑 Stop rules

- STOP at GI5 per question: a signed handoff is the lane's export; composing from it is the DesignBoard's.
- STOP at any gate: report and end, never wait in a loop.
- STOP on contradiction: a cell that derives to two phases at once (the register says answered, the page says 🔴) is reported as a defect, never repaired silently.
- **Known-stale is marked, not repaired.** A line known stale but deliberately left (a frozen handoff, a fenced page) is marked `🧊 <staling event>` where it stands, so frozen debt is distinguishable from unnoticed drift; an unmarked stale line remains a finding.
- **Refusal is convergence.** A 🚫 with a reason is a terminal state equal in rank to ✅: the lane terminates because refusing is answering, and a board rich in refusal reasons (thin, F-only, defer, no-measure) is converging, not failing. The defect is the cell that can neither answer nor refuse.

## ↩ Return

The frontier cells by phase, the pages dispatched this run with their CHECK outcomes, the gate now blocking with the person's owed decision, and the next runnable cell once that gate clears.
