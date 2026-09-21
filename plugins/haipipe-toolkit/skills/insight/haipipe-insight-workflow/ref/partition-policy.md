# Partition decisions and cross-partition dependencies

Load for partition registration, X routing, pooling, or late arrivals.
The disk/config grammar is [partition.md](../../haipipe-insight/ref/partition.md);
Question Group membership is [question-groups.md](../../haipipe-insight/ref/question-groups.md).

## Question Groups and audience routing

The board exposes a derived Question Group for each eligible intersection of a
partition scope and requested rung: `QG-F-D`, `QG-B-I`, `QG-C-K`, or
`QG-F-W`. The group is a scheduling/status view only. Its members are Queue
cells whose question target matches its rung and whose column matches its
partition. MT00 plus MT01-MT04 remain the record; no group Folder or state file
exists.

The CELL remains the atomic register-settlement target, so `QI5` may be ✅ in `QG-F-I`, 🟡 in
`QG-B-I`, and ⬜ in `QG-D-I` at once. A group may batch visibility but never
advance all members together. Report the actual Run inventory and blockers first, then the derived
Question Groups and member-cell states.

Partition proposals have three resource owners:

```text
noticed   Information/Knowledge   an I page's partition column diverges, or a K boundary names a cut
asked     Question      a register row: does this cut deserve its own ladder?
born      Meta      one MT00 partition-register row (letter · filter · config) +
                  one group folder beside X · the door's `partition` verb
```

The ladder notices, the register asks, Meta births — a partition is born at Meta and nowhere else, and it is a CONFIG, never a code change (`../../haipipe-insight/ref/partition.md`).

**The partition test, at Meta.** A partition is an AUDIENCE stratum: a grouping of the unit the counsel is FOR — in an SMS application, the humans receiving it. Not every cut of the data qualifies; birth requires three yeses, each mechanically checkable:

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
                                                  , a design bet
time as pattern        engagement over the window  an I column, never a group
time as epoch          a new window / next round   a NEW EXTRACT → a NEW InsightBoard
                                                   (the one-dataset law), with MT00's
                                                   freshness rule owning the seam
```

The second named case is the COVARIATE, and it fails ① rather than ②:

```text
a covariate            a ZIP attribute, an income     fails ① → an I COLUMN, never a
                       band, a drug class, an         group · `../../haipipe-insight/ref/partition.md` names
                       exposure history               the failure: a board past a
                                                      handful of audiences is almost
                                                      always misreading covariates as
                                                      audiences
```

A covariate cuts ACROSS every audience instead of partitioning it, so its rows are already counted in the groups it overlaps and no arithmetic can separate them. The tell is mechanical and now checked (`partition-cross-cutting`): a candidate filtering on a column NO sibling partition filters on shares no axis with them, which is what slicing across looks like on disk. Registered anyway, it corrupts the X group specifically, because a contrast that subtracts mirrored I rows double-counts the people two overlapping groups share.

Disjoint subgroup shares cannot sum above 100%; the checker reports
`partition-sum-over-100`. The cross-cutting-column check is a screening signal;
verify actual membership disjointness before registering a proposed audience.

The deep reason: the partition axis exists so the pooling verdict can ask "one counsel or several," and counsel is PER-AUDIENCE — the insight lane's partition columns mirror the design lane's DS-page audience axis. A dimension that could never become an audience can never split the counsel, so making it a partition buys mirrors nobody will consume.

**The routing test, at Question.** The two axes never mix inside one question because registration classifies it once, by one mechanically checkable property — how many partition groups its `what-would-answer` field needs rows from:

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
                    even produce every column's numbers at once
a PARTITION         scripts/config/<partition>.yaml over the same code · needing DIFFERENT
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
XK  pooling verdict K-from-K: a claim about claims — POOL, SPLIT, or
                    UNDETERMINED, from the predeclared shared-threshold source
                    └─▶ conditions EVERY W page: POOL routes non-template W
                        to an explicit deferral; SPLIT permits evidenced local
                        counsel; UNDETERMINED permits only full-extract template
                        counsel and a licensed partial-final non-answer for an
                        unanswered subgroup W
```

At verdict time, cite the shared-threshold file and its version/hash, the
compared partitions and outcome rows, and the differences that would change
counsel. The threshold source must predate the compared Results and be the same
for F and every partition config. POOL needs evidence precise enough to rule
out a difference material to the registered counsel question; a non-significant
test or a failure to detect a difference is not that evidence. SPLIT requires a
predeclared, decision-relevant difference supported by current X evidence.
If a completed comparison is too imprecise, conflicting, or otherwise unable
to support either result, record `UNDETERMINED` and say what evidence or
decision could resolve it. If inputs, threshold definitions, or comparisons
are missing or stale, do not write any verdict; GI4 stays held.

`UNDETERMINED` is not shorthand for `POOL`, `SPLIT`, or a statistical null. It
does not authorize a partition-specific handoff or a child board. The template
W can answer only at the full-extract scope and must keep subgroup applicability
open. A requested partition W that cannot answer under this restriction may
settle only as `🟡 <page> final`, under the existing partial-final receipt rule,
when its page names the unresolved question, the exact blocker, and the
evidence or decision that could change the result. It writes no handoff and
does not pass GI5; Question records the licensed partial exit at GI6. If that
resolution is still in scope and feasible, keep the target waiting and run the
required work instead of settling it early.

Every such answering Page states and licenses this exact non-answer sentence;
the register receipt quotes it verbatim:

> The current, threshold-bound comparison cannot establish whether these partitions support common or separate counsel; it authorizes neither pooling nor subgroup-specific counsel or handoff.

**The escalation ladder.** A subgroup earns first-class standing in three steps, each with its own trigger, and skipping one is the defect:

```text
L0  a segment column inside an I page      rung-major default · costs one column
      │ trigger: readers keep asking K questions about the segment
L1  a PARTITION with its own ladder        partition-major · born at Meta · mirrors F
      │ trigger: a SPLIT verdict + the subgroup has its OWN consumer
L2  a child InsightBoard                   the verdict page is its birth certificate
```

**Late arrival** (a partition added after siblings have climbed) has four consequences, all mechanical:

```text
① its cells are born ⬜ and NEVER inherit a sibling's refusal — a 🚫 reason is
  re-earned per partition
② the X group REOPENS: contrast, heterogeneity and the pooling verdict must be
  recomputed with the new column
③ a reopened verdict stales every W page's verdict citation, template included —
  the W pages are re-conditioned; changed signed payloads (including source/
  verdict pins) require a new person signature even if counsel wording is unchanged
④ every OTHER partition's D/I/K pages are untouched
```

A partition may become its own board only by citing a SPLIT verdict; `../../haipipe-insight/ref/partition.md` stays the grammar's single source.
