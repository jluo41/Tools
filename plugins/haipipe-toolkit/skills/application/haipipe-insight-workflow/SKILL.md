---
name: haipipe-insight-workflow
description: >-
  The InsightBoard Workflow Runtime over six RunType-owned Folder kinds: I0 Meta →
  I1 Question → I2 Data → I3 Information → I4 Knowledge → I5 Wisdom. Owns
  GI0-GI6 runtime control keys, derived partition-by-DIKW Question Groups, the
  CELL frontier, climb order, dispatch, receipts, and stops; each RunType skill owns both Folder faces and
  its plugins. Use to run or inspect an InsightBoard. Trigger: insight
  workflow, climb ladder, next rung, frontier cell, /haipipe-insight-workflow.
metadata:
  version: "1.2.2"
  last_updated: "2026-09-15"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-insight-workflow · run the cell, record control, mint the next RunType

Load `haipipe-insight` and `haipipe-folder` first. This is the only authority
for I0-I5 RunType ordering and GI0-GI6 control keys. `haipipe-application-workflow` may delegate
here and record a crossing, but it owns no alias RunTypes or duplicate controls.
This workflow never edits a Page Face itself; the selected RunType delegates Page
work to `haipipe-page-workflow`.

Read `../haipipe-insight/ref/question-groups.md` before registration, status,
or dispatch, and `../haipipe-insight/ref/page-v2-adapter.md` before running or
checking a rung Page. These references own the two-dimensional group projection
and the boundary between Page CLOSE and GI advancement.
Read `../../task/haipipe-workflow/ref/workflow-runtime.md` when creating,
resuming, or auditing the board's `workflow_runtime_id` and its control records.

This is the Application InsightBoard workflow. Task-side topic instances use
the item/checkpoint workflow table owned by `haipipe-page-insight/ref/`.
Independent questions there are item Runs inside one Page, not this ladder's
separate rung Folders.

## 🔤 Terminology law

An **Insight RunType** is one domain rung, `I0`-`I5`: Meta, Question, Data,
Information, Knowledge, or Wisdom. The numeric label identifies reusable
RunType vocabulary, not a runtime instance. `GI0`-`GI6` are stable runtime
control keys; they are assertions/evaluations, not a second Gate identity.
`workflow_runtime_id` identifies one board execution, while concrete work
keeps its owner-native Run identity. Scope, ask, observe, derive, claim, and
hand off are prose aliases only.

## 🧭 Workflow Runtime

The Application Insight workflow has one aggregate Runtime per execution:

```text
Workflow Definition = I0..I5 RunTypes + Run Specs + GI policies + Routes
Workflow Runtime    = workflow_runtime_id
                      + concrete owner-native Runs
                      + GI evaluations + route decisions + CELL frontier
Question Group      = partition × DIKW target (derived view, never a Run)
```

The Runtime opens or resumes one `workflow_runtime_id`, selects one runnable
Question Group/CELL, materializes the owner-native Run when work is needed,
records the GI evaluation and route, then advances or holds the frontier. A
Page workflow pass may be nested inside a Run; it is not silently promoted to
an Insight Run or counted as a new Gate.

## 🗺 The six Insight RunTypes · legacy phase labels

Each RunType is represented by the Folder kind it owns. Its RunType skill
carries both faces, plugin profile, control policy, and handoff; the ladder is
the domain spine. Existing `phase` fields remain compatibility/display labels.

```text
RunType                   authority page              what the RunType produces
──────────────────────────────────────────────────────────────────────────────
I0 Meta (scope)           MT00-meta                   the inventory: sources, grain,
                                                      window, freshness, limits ·
                                                      the PARTITION REGISTER
I1 Question (ask)         MT01-MT04 registers         the question matrix: one row
                          ← the scoreboard hub        per question, one column per
                                                      partition, a state per CELL
I2 Data (observe)         the D page                  run-bound observations, every
                                                      value bound to a named Run Result
I3 Information (derive)   the I page                  rates and contrasts from
                                                      named D rows
I4 Knowledge (claim)      the K page                  propositions with strength,
                                                      rivals, boundary
I5 Wisdom (hand off)      the W page                  counsel + the SIGNED Design
                                                      Handoff
   ↺ I1→I2→I3→I4→I5→I1 is the CLIMB LOOP · exits through the register at GI6
```

Two positions deliberately did not become RunTypes: the pooling verdict is I4
Knowledge work in X and part of GI4; SETTLE is I1 register work and GI6. A
position with no independently owned Folder kind is a control record or
Task-Face act.

Each RunType performs one EPISTEMIC OPERATION and each GI control is an
AUTHORITY TRANSFER: passing GI<n> is the moment the rung below becomes citable
and nothing else does — the Climb Law read as a process instead of a
structure. That is why the aliases are verbs of knowing (scope, ask, observe,
derive, claim, hand off), not verbs of doing.

## ✚ Question Groups · partition × DIKW target

The board exposes a derived Question Group for each eligible intersection of a
partition scope and requested rung: `QG-F-D`, `QG-B-I`, `QG-C-K`, or
`QG-F-W`. The group is a scheduling/status view only. Its members are Queue
cells whose question target matches its rung and whose column matches its
partition. MT00 plus MT01-MT04 remain the record; no group Folder or state file
exists.

The CELL remains the atomic transition, so `QI5` may be ✅ in `QG-F-I`, 🟡 in
`QG-B-I`, and ⬜ in `QG-D-I` at once. A group may batch visibility but never
advance all members together. "What RunType is this board in" therefore has no
one-number answer: report the Question Groups and their member-cell frontiers.

A subgroup passes through three moments, each owned by one RunType:

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

The second named case is the COVARIATE, and it fails ① rather than ②:

```text
a covariate            a ZIP attribute, an income     fails ① → an I COLUMN, never a
                       band, a drug class, an         group · `ref/partition.md` names
                       exposure history               the failure: a board past a
                                                      handful of audiences is almost
                                                      always misreading covariates as
                                                      audiences
```

A covariate cuts ACROSS every audience instead of partitioning it, so its rows are already counted in the groups it overlaps and no arithmetic can separate them. The tell is mechanical and now checked (`partition-cross-cutting`): a candidate filtering on a column NO sibling partition filters on shares no axis with them, which is what slicing across looks like on disk. Registered anyway, it corrupts the X group specifically, because a contrast that subtracts mirrored I rows double-counts the people two overlapping groups share.

**Clause ① has an arithmetic proof, and it is now a checker rule.** Disjoint subgroups of ONE extract cannot cover more than that extract, so partition percentages summing above 100% is a breach nobody has to argue about (`partition-sum-over-100`). A00 registered two covariate partitions on 260828 and ran to 136.79% with the board checker green for the whole window; a human reader caught it, which is the case these two rules exist to remove.

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

A question id is partition-free either way (`QI5` spans all columns; there is no
`QI5-B`). Its B cell belongs to `QG-B-I`; its F cell belongs to `QG-F-I`.
"Subgroup" is never a kind of question: it is either the partition axis of a
Question Group or the subject of an X question about several groups. X is a
derived cross scope, and `QG-X-D` is invalid because X owns no raw rows.

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

This is the only authoritative Insight order; the crossing workflow delegates here.

### Pre-climbed external parent · Task RF bridge

One narrow bridge preserves the Climb Law without duplicating a
consumer-neutral chain. A settled Task Insight item Result has already climbed
`D → I → K → W → RF` under its own Task-only contract. An Application may use
that completed chain as an **external parent** for a local I5 Folder:

```text
Task instance/riNN@version/RF    Application InsightBoard          DesignBoard
R + new dataset → RI → D/I/K/W/RF ─▶ I1 QW → I5 contextual W ─✋─▶ X1 handoff
```

This is not permission to skip a rung inside an Application chain. It is a
cross-scope authority bridge with five mechanically readable assertions:

1. the source is a task-side Insight instance and the selected item execution
   has `target: wisdom`;
2. that item Result is independently CHECK-accepted against its exact source
   versions, with current applicability; unrelated open items do not block it;
3. the borrowed RF traces through named D/I/K/W rows in that exact Result;
4. the Application I1 QW row records instance, `riNN`, base-R pointer, frozen
   dataset binding, execution version, RF id, Result path/hash, and the local
   I5 W Folder; a bare R is not an RI evidence address;
5. the W Folder's Evidence Item graph binds that exact Supporting Result and
   completes its local Evidence Run. Page navigation alone is not evidence.

Legacy one-chain Page/RF references require a verified exact alias using
`haipipe-page-insight/ref/migration.md`; never select a new item by text or
`latest`.

When all five hold, GI4 reads the external chain as the K/W parent and no
local I2-I4 Folders are minted: their evidence authority remains in the Task
Page. I5 still performs the Application operation—applicability, counsel,
forbidden overreach, `serves:`, and human signature—and GI6 still settles the
I1 row. The RF itself never satisfies X1 or any Design gate. A stale,
below-Wisdom, incomplete, or untraceable item Result fails the bridge assertion
and routes through the ordinary local climb.

## 🚦 Runtime control keys · GI0-GI6

There is no standalone Gate object. Each GI key names a testable assertion;
the Runtime records its actual evaluation, authority, evidence, and resulting
route. Controls are per-CELL except GI0, which is per-board, and GI4's verdict
clause, which is per-column-set.

```text
GI0  Meta → Question      MT00 has Page CHECK/CLOSE and its sources resolve through
                          accepted Results or governed frozen local inputs · the four
                          registers exist · on partition-major the partition register
                          and the shared-threshold pointer exist
GI1  Question → Data      the cell's row carries target, raiser, what-would-answer,
                          and a state cell · its partition group exists on disk
GI2  Data → Information   the D Page reached CHECK/CLOSE; every value is bound by
                          path to an accepted source Result backed by a named run,
                          represented as a Supporting Result, frozen Local Input,
                          and ready typed local Result
GI3  Information → Knowledge   the I Page reached CHECK/CLOSE and derives only from
                          exact version/hash-pinned D parent rows (X contrast:
                          mirrored I rows, the one exception)
GI4  Knowledge → Wisdom   the local K Page reached CHECK/CLOSE and cites exact
                          version/hash-pinned I parent rows · OR the pre-climbed
                          external-parent bridge passes all five assertions above ·
                          on partition-major the X group's pooling verdict exists and
                          is current against the partition register — a late
                          partition voids this gate
GI5  Wisdom → signed      ✋ the handoff's `signed:` row reads `✅ <initials> <YYMMDD>`
                          (haipipe-insight-wisdom) · `⬜` blocks · no machine
                          writes it · under POOL a non-template W closes as a DEFERRAL
                          by id, exports no handoff, and owes no signature
GI6  settle               the register cell flips ✅, or 🚫 with a reason, or 🟡 <page>
                          final when the page states why the remainder cannot close
                          (haipipe-insight-question) — always citing the closing page ·
                          gaps remain → the next lap
```

A value produced by EXTENDING an already-used task Run binds to the new artifact
paths; the consumer records the new full Run id as a Supporting Run and reruns
its Local Run when the focal evidence changes.

The DERIVED-HEADER rule (`haipipe-insight-question`) covers every on-register
restatement of the Queue — headers, Diagrams, Openings, status words, and counts.
Reconciling one is I1 Task-Face work citing the Queue.

**The two Insight cross-RunType authority controls never have an auto mode**. A new
Supporting computation is released through the owning Page Evidence Item's
SURVEY `Decide`; there is no separate active Probe phase or lane. Handoff
signing is GI5. Page Workflow may also require local Shape approval, CITE
verification, or Page acceptance while authoring that Folder. Those nested
Page-Face controls may pause a copilot pass, but they do not create extra Insight
transitions or GI numbers. Every dispatch pins `mode: copilot`. A blocked gate
is a clean stop: report the Question Group, cell, waiting artifact, and the
person's owed decision.

For the shared Page Workflow's owner RULING, I0-I4 declare none beyond their
mechanical GI closure; I5 reuses the GI5 signature receipt. This never creates
a duplicate human tick. Historical Probe records remain read-only migration
input.

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

These are disk groups, not Question Groups. The derived projection cuts across
them: an MT02 column exposes `QG-<partition>-I`, while partition group B exposes
`QG-B-D`, `QG-B-I`, `QG-B-K`, and `QG-B-W`.

## 🚚 Dispatch: one page at a time

```text
select   the earliest RUNNABLE Question Group, then one frontier cell whose gate
         is open and whose inputs exist; prefer cells
         the register marks `⬜ calc` (computed, unauthored — I1 Question)
         before cells needing new runs, because authoring is cheaper than running
load     the matching haipipe-insight-<folder-kind> RunType skill
run      one haipipe-page-workflow PASS over that ONE Page inside the current
         Workflow Runtime · mode: copilot always;
         allocate no rpNN unless a human selected an interactive Page-writing goal
fold     move the register cell ONLY after Page CHECK emits CLOSE and the matching
         GI assertion passes; a Page Run close changes neither condition
         · every other terminal is a named
         non-settlement and the cell does not move
repeat   until every cell is settled or a gate blocks
```

A cell whose inputs do not exist is not runnable, and naming WHY is this skill's answer, never scaffolding the missing input silently.

## 🧾 Runtime records

A transition leaves one dated Runtime control record in the granting Folder's canonical
`outline/<stem>-log.md` — except a 🟡-final settle, which leaves TWO (§Marks):
MT00 records GI0 and every partition birth; the Question register records GI1
and GI6; the closing rung Folder records GI2-GI4; and the W Folder records GI5.
No embedded Page log section and no separate receipt store is authoritative.

## ⏱ Advancement is never scheduled

A gate test may be run any time; a gate may only be DECLARED passed by the human tick or CHECK verdict it names. Nothing here may be wired to a timer or a loop that advances cells on wall-clock time.

## 🔀 Resolving the Runtime frontier

Per cell: report the current RunType plus the highest GI control whose
assertion currently holds. Per Question Group:
derive `EMPTY | RUNNABLE | BLOCKED | SETTLED` from its cells. Per board: read
the register matrix whole and include the `workflow_runtime_id`. A board-level
scalar RunType is a lie this workflow refuses to mint; the crossing workflow
reports the group/cell frontier unchanged.

## 🌐 The machine is content-free

Nothing in this file names SMS, messages, or any domain. Domain content enters at exactly three declared points, and substituting all three re-instantiates the whole machine unchanged:

```text
① the EXTRACT       MT00: source, unit, grain, window — a CGM stream, a wearable
                    feed, a claims table are all one `source:` line away
② the QUESTIONS     MT01-MT04: what is asked is the board's; Question Groups are
                    their derived partition × target-rung projection
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
                   a charter: one record in the register's
                   outline/<register-stem>-log.md QUOTING the licensing sentence,
                   and one record in the ANSWERING Folder's
                   outline/<answering-stem>-log.md naming the QUESTION id and the
                   word final (the shape the checker scans) — staleness travels by
                   citation, and a citation invisible from the cited end cannot travel
```

## 🛑 Stop rules

- GI5 is the outward-export boundary: after signature, never compose or design
  in this lane. The dispatcher must still perform the I1-owned GI6 register
  settlement, leave its receipt, and only then stop that cell.
- STOP at any gate: report and end, never wait in a loop.
- STOP on contradiction: a cell that derives to two RunTypes at once (the register says answered, the page says 🔴) is reported as a defect, never repaired silently.
- **Known-stale is marked, not repaired.** A line known stale but deliberately left (a frozen handoff, a fenced page) is marked `🧊 <staling event>` where it stands, so frozen debt is distinguishable from unnoticed drift; an unmarked stale line remains a finding.
- **Refusal is convergence.** A 🚫 with a reason is a terminal state equal in rank to ✅: the lane terminates because refusing is answering, and a board rich in refusal reasons (thin, F-only, defer, no-measure) is converging, not failing. The defect is the cell that can neither answer nor refuse.

## ↩ Return

The Question Groups in MT00/rung order, their member cells and derived states,
the Pages dispatched this pass with their CHECK/CLOSE and GI outcomes, the gate
now blocking with the person's owed decision, and the next runnable cell once
that gate clears.
