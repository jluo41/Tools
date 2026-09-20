---
name: haipipe-insight
description: >-
  Unified Insight door for Task-side topic/data instances and Application
  InsightBoards. Routes dataset-first requests to the Task Insight Page/RI
  contract and Application requests to the I0-I5 RunType climb. Meta declares the
  extract; Question registers ask; Data observes; Information derives;
  Knowledge claims; Wisdom counsels and exports a person-signed Design
  Handoff. Ends at the correct Insight boundary, never designs. Trigger:
  insight, InsightBoard, Insight Page, RI, question register, DIKW, climb,
  chain, partition, pooling verdict, Design Handoff, InsightBoard grooming,
  /haipipe-insight.
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "1.5.0"
  last_updated: "2026-09-16"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-insight · one public door, two Insight scopes

`/haipipe-insight` is the one user-facing entry for both kinds of Insight work.
It resolves the scope first, then loads exactly one owner:

```text
Task-side Insight       a neutral topic/data instance · item `riNN` Runs ·
                        versioned D/I/K/W/RF Results
Application Insight     a named InsightBoard · I0 Meta → I1 Question →
                        I2 Data → I3 Information → I4 Knowledge → I5 Wisdom
```

This is a router, not a third data or Page owner. Task-side execution remains
owned by `haipipe-task` + `haipipe-page-insight`; the Application route remains
owned by this door + `haipipe-insight-workflow`. The physical skill location
under `skills/application/` does not change the Task-only status of
`page-type: insight`.

**The name is reused; the thing is not.** The earlier top-level knowledge-base layer was retired. This Application door does not replace the evidence producers: values bind to named Supporting Run Results through local Evidence Runs, and this door states how one board turns bounded evidence into a signed handoff.

For an Application execution, this door creates or resumes one
`workflow_runtime_id` and routes within that Runtime. I0-I5 are Insight
RunTypes, GI0-GI6 are Runtime control keys, and the `partition × DIKW target`
Question Group remains a derived scheduling view—not a Folder, Gate, or Run.

## One public door, two routes

Use the explicit form when the scope is known. The bare form is a convenience
for a topic whose board has not yet been named:

```text
/haipipe-insight task "<topic>" [<task-board>]                         Task-side
/haipipe-insight application <application-root> <verb> [args...]        Application
/haipipe-insight "<topic>" [<task-board-or-context>]                    auto-route
```

The Application verbs (`enter`, `status`, `meta`, `sources`, `question`,
`ask`, `climb`, `chain`, `partition`, `verdict`, `settle`, `handoff`, `check`,
`review`, `workflow`, `run`) keep their existing meaning. For compatibility,
the existing verb-first form remains valid:

```text
/haipipe-insight <verb> [<application-root>] [args...]
```

Resolve the route in this order:

| Signal | Route | First owner to load | Resulting unit |
|---|---|---|---|
| explicit `task` | Task-side | `haipipe-task` → `fn/insight.md` → `haipipe-page-insight` | one topic/data Page and its `riNN` items |
| explicit `application` | Application | this door → `haipipe-insight-workflow` | one InsightBoard cell through I0-I5 |
| an existing `*-InsightBoard` or Application root | Application | same Application route | existing board status or requested verb |
| an existing Task Board, dataset-first topic, or bare topic | Task-side | same Task route | create/resume a neutral Insight Page |
| ambiguous path/context | stop and ask for the scope | neither | never create a duplicate or guess an audience |

`/haipipe-task insight "<topic>" [<board>]` is the compatibility alias for
`/haipipe-insight task "<topic>" [<board>]`; it must produce the same
`scope: task`, `insight-layout: items-v2` Page and the same RI contract. Keep
`/haipipe-discovery` separate for literature and external-evidence discovery.

The `partition × DIKW target` Question Group exists on the Application route
only: it is a derived scheduling view over one stable register question and
its partition cell. Task-side Insight work has an item-level target and dataset
binding, but does not mint Application Question Groups or I0-I5 Folders.

After routing, the boundary is equally strict:

```text
Task-side       resolve/reuse the Page → select an item → bind `riNN` to one
                normal `rNN` + new frozen dataset → execute only after its
                ticket/receipt gates; never fabricate a Result
Application     resolve the board → register/derive one Question Group cell →
                advance one I0-I5 lap through `haipipe-insight-workflow`
```

The router does not execute a whole Task merely because a topic was named, and
it does not create an Application board merely because a dataset was named.

**Who owns what**:

```text
haipipe-insight               public Insight router + Application one-dataset/climb/register/
                              handoff laws · Application verbs
haipipe-task/fn/insight       Task-side route procedure (compatibility alias included)
haipipe-page-insight          Task-side topic/data Page, item, RI, and DIKW/RF Result contract
haipipe-insight-meta         the head: source inventory only, holds NO question
haipipe-insight-question     the four registers MT01-MT04: asked and tracked, never concluded
haipipe-insight-data/-information/-knowledge/-wisdom     what each rung IS
haipipe-page-workflow         the loop every page here runs, like every page anywhere
haipipe-insight-workflow      the lane's RunType/Runtime controller: I0-I5,
                              GI0-GI6, the CELL frontier, dispatch, receipts, climb order
haipipe-folder                the shared two-face Folder contract
```

Read `ref/page-v2-adapter.md` whenever creating, reopening, or checking a rung
Page. Read `ref/question-groups.md` for question registration, status, or
dispatch. The first separates Page closure from epistemic advancement; the
second defines the derived `partition × DIKW target` grouping without adding a
Folder or second Queue.

`page-type: insight` stays TASK-ONLY: a consumer-neutral topic/data instance
with item Runs, each carrying a versioned DIKW/RF Result. The unified Task
route delegates to `/haipipe-task insight` and `haipipe-page-insight`; this
Application route never mints a Task-side Page or RI. Its own Folders are Meta,
Question, Data, Information, Knowledge, and Wisdom. A settled Wisdom-targeted
Task RF may enter only as the workflow's pre-climbed external parent: I1
registers its exact instance/item/execution-version/RF reference and a local I5
Wisdom Folder contextualizes and signs the Application Design Handoff.
RF never reaches Design directly.

## The Climb Law · a six-level lifting chain

Authority to conclude lifts one rung at a time, each rung citing named rows below it. Each rung's fixed outline demands its citations division (Data Cited, Information Cited, Knowledge Cited); the climb into W requires exact source Result bindings and accepted local Evidence Items.

```text
① MT00       source: <extract>            the board's ONE dataset · set at scaffold
② D page     observes, run-bound          cites the exact Run Result · no interpretation
③ I page     derives from named D rows    a rate is Information, never a claim
④ K page     claims from named I rows     strength · rivals · boundary
⑤ W page     counsels from named K rows   contextual · verdict-conditioned
⑥ Handoff    exports W, signed ✋          never re-derives · the ONLY bindable level
```

Level-skipping is a CHECK routing failure, with exactly two exceptions, both inside the X cross group and both recorded in the rung contracts: the contrast I page derives from MIRRORED I rows (I-from-I), and the pooling-verdict K page cites the heterogeneity K row (K-from-K), because its subject is a claim about claims.

The pre-climbed external-parent bridge is not a third skip: the selected Task
Insight `riNN` item's accepted Result CHECK-closes the complete
`D→I→K→W→RF` chain. Its packet carries the RI execution id, the base-R pointer,
dataset binding, Result path/hash, and RF id; a bare `rNN` cannot identify the
rebound data execution. Historical items-v1 `#rNN@vNNN` packets remain
readable under their recorded contract.
Open sibling items do not invalidate that Result. GI4
verifies that authority before local I5 performs the new Application-contextual
operation; see `haipipe-insight-workflow`.

**One dataset, one board.** The chain's ① is a scope, not a suggestion:

```text
a new source extract        ──▶ a NEW InsightBoard
a new question              ──▶ a new chain INSIDE the board
a subgroup of the extract   ──▶ a PARTITION inside the board, never a board
a subgroup + SPLIT verdict  ──▶ MAY become a child board · the verdict is its birth
                                certificate, necessary and not sufficient: the child
                                still needs its own consumer (ref/partition.md)
```

Re-extracting a subgroup's rows into their own parquet does not make them "a new source extract": a new extract is new SCOPE — rows or fields the old one did not carry — never the same rows re-cut. The child-board path always runs through the SPLIT verdict, and a re-extract cannot launder around it.

## The two births of a question

```text
need-first        a Brief raises the need OUT; it lands on the rung register it faces,
                  carrying the Brief's need id, and G4 later checks the round trip
curiosity-first   a reader of the inventory becomes curious; the register row names the
                  raiser and no consumer, because data may land before anyone knows its use
```

Either way the question is written ONCE, on the one register facing its rung
(QD/QI/QK/QW ids), with target, raiser, what-would-answer and a state cell. Its
derived Question Group is `partition × target rung`: `QI3` under B belongs to
`QG-B-I`, while the same `QI3` under F belongs to `QG-F-I`. The id is never
duplicated or partition-suffixed (`QK1` spans all eligible partitions; there is
no `QK1-B`). `ref/question-groups.md` owns membership, X routing, state, and
sorting.

## The three pens · who may write what

The workflow drives the lap; this door states the pens, and they never cross:

```text
register     writes STATE, never a finding         MT01-MT04 cells, including the
                                                   ⬜ annotations (`⬜ calc`) — notes
                                                   about work ARE state · haipipe-insight-question's
                                                   vocabulary · ✅/🚫/🟡-final settle
chain page   writes FINDINGS, never its own cell   the rung pages
handoff      EXPORTS, never re-derives             the W page's signed division
```

The join is a round trip through one question id: the register row's cell cites the closing page by id, and that page's handoff SERVES row names the register's question id back. `board.md`'s spine and close are DERIVED HEADERS of the same record: the registers are authoritative, a header that disagrees with them is stale, and reconciling it is register-pen work, citing the registers it was reconciled to. Its `## Pages` roster and group counts derive from DISK instead: completing them is part of the MINT act, in the same lap as the page they name. The loop's only exit is through the register at G3, so a Design page reads a signed handoff and never a D, I or K page's prose — two consumers can never keep separate books.

## The board, concretely

```text
<DataSubject>-InsightBoard/                RUNG-MAJOR · canonical
(optional A<NN>_ ordering prefix before the subject)
├── board.md                               spine · close · store:
├── 0-MT-meta/MT00-meta/ + MT01-MT04/      inventory + the four registers
├── 1-D-data/D<NN>-<slug>/                 observed · run-bound
├── 2-I-information/I<NN>-<slug>/          derived · cites D
├── 3-K-knowledge/K<NN>-<slug>/            claimed · cites I
└── 4-W-wisdom/W<NN>-<slug>/               counsel + handoff · cites K

PARTITION-MAJOR · when each subgroup must produce its OWN K claims and W counsel
├── 0-MT-meta/                             same head · registers gain one column per partition
├── 1-F-full/F<rung><NN>-<slug>/           the TEMPLATE ladder · the whole extract
├── 2-<L>-<slug>/<L><rung><NN>-<slug>/     one group per partition · mirrors F slug for slug
└── X-cross/X<rung><NN>-<slug>/            the ONLY comparing group · no index,
                                           letters sort last (legacy: 9-X-cross/)
```

The layout is chosen once, at scaffold; `ref/partition.md` stays the partition grammar's single source (the mirror rule, reserved letters F/X/Q/S/M, the index-free X seat, the shared-threshold file, the POOL/SPLIT verdict conditioning every W — under POOL a non-template W page DEFERS by id and exports no handoff). Each rung page declares its typed Evidence Items in `outline/` and binds Supporting and Local Runs; Meta and the four registers own none, and no flat run bank exists. Legacy probe paths are read-only migration input and are never created by new work. `A<NN>_` is only a project-local ordering option before the subject; the canonical shape stays `<DataSubject>-InsightBoard` (umbrella §Runtime folders).

## The Folder RunTypes this door owns

```text
MT00        haipipe-insight-meta          what data EXISTS · one per board
MT01-MT04   haipipe-insight-question      what is ASKED of one rung · four per board
D rung      haipipe-insight-data          observed · run-bound · never compares
I rung      haipipe-insight-information   derived from named D rows · never claims
K rung      haipipe-insight-knowledge     claimed from named I rows · never advises
W rung      haipipe-insight-wisdom        counsel + the signed Design Handoff
```

These are six workflow RunTypes, not six configuration/Page-Type skills. Each
named skill owns its Folder kind's Page Face, Task Face, plugins, control
policy, and handoff. Legacy `page-type:` keys resolve to these skills during
migration.

## Verbs

```text
task | topic | instance
                    dispatch a dataset-first request to the Task Insight Page/RI route ·
                    create/resume a neutral topic/data instance, never an Application board
application | board  resolve an Application root, then use the Application verbs below
enter | status      resolve the board · derive Question Groups from MT00 × the four
                    rung registers · report each group's member-cell frontier
meta | sources      create/resume the one MT00 (the umbrella's fn/meta.md)
question | ask      register one question from plain words: the verb decides level, partitions
                    and lineage, then writes the row (the umbrella's fn/question.md) ·
                    NEVER answer it there
climb | chain       open or extend the frontier rung for one question (the umbrella's fn/chain.md) ·
                    Evidence Items planned · ✋ a person releases each Run before dispatch
partition           register a partition on MT00 and insert its group before X
                    (the umbrella's ref/partition.md)
verdict             drive the X group XI → XK → the POOL/SPLIT verdict page
                    (the umbrella's fn/verdict.md) · every W waits for it
settle              flip the register cell ✅, 🚫 with a reason, or 🟡 <page> final
                    (haipipe-insight-question's exit), citing the closing page
handoff             draft the W page's Design Handoff division · ✋ a person signs its
                    `signed:` row — `signed: ✅ <initials> <YYMMDD>`, never a machine ·
                    the door RECORDS a signature the person states, never decides one
check | review      CHECK selected rung pages in a fresh context through haipipe-page-check
workflow | run      drive laps (§The lap): gap → climb (✋release inside) → ✋sign → settle · STOP
```

The two Insight cross-RunType ✋ controls never have an auto mode: releasing a
bounded Run and signing a handoff are a person's, and every page dispatched into
`haipipe-page-workflow` pins `mode: copilot`. Page-local outline/read/verified
ticks remain nested controls rather than new Insight control identities. With
the Design door's two cross-RunType controls (card release, acceptance), they are the
Application's four domain authority transfers, two per door.

## The lap, step by step

The `run` verb's procedure. These six are VERBS, not RunTypes: none can name an
authority page beyond the pages already on the board, which is the naming-law
test — the design door's realize and
judge are verbs by the same test. The lane's RunTypes are the rungs themselves,
named in `haipipe-insight-workflow`; a lap is how one register cell moves
through them.

```text
lap entry: pick one frontier question, a register cell not yet settled
           (anything but ✅, 🚫, or 🟡 final)
────────────────────────────────────────────────────────────────────────────
① STATE    read the register row: what is asked, what would      pen: register
           answer it, which rung it faces
② MINT     open the NEXT rung page only, D before I before       pen: chain page
           K before W; partition-major: resolve the partition        + register
           group from the register cell · the register pen
           records the allocation, `⬜ <id>`, in the same lap
③ CLIMB    run that ONE page through one haipipe-page-workflow   pen: chain page
           PASS, mode: copilot — Evidence Items and their Run/Result records are
           declared in the outline table (this door points, it does not
           restate their shape) · MATCH existing
           Supporting Run Results BEFORE raising and AGAIN at dispatch — a
           released card whose numbers are already held reuses the immutable
           Run and dispatches NOTHING, because a re-run reproducing known
           numbers under a new timestamp muddies the run identity closed pages
           already bind · ✋ a person releases each · focal evidence lands in
           the consumer-owned Local Run/Result · I/K/W semantic parents use the
           exact row-lineage grammar in ref/page-v2-adapter.md · only Page CHECK
           may emit CLOSE; a Page Run close never advances the rung
④ SIGN     only when the rung was W: draft the Design Handoff    pen: W page
           division · ✋ a person signs at that page's CHECK (G2)
⑤ SETTLE   flip the register cell ✅, 🚫 with a reason, or        pen: register
           🟡 <page> final when its page licenses the exit,
           citing the page that closed it (G3)
⑥ EXIT     gaps remain → next lap at ② · every cell settled → the lane is done
────────────────────────────────────────────────────────────────────────────
```

The pens own their steps — ① and ⑤ write STATE, ② and ③ write FINDINGS, ④
exports — and the lap's two cross-RunType ✋ controls are the door's two domain
authority transfers; no
third GI transfer appears. A ZERO-CARD ③ is a legal quiet pass: when every
value the page owes already exists in the store, SURVEY raises nothing, there is
nothing to release, and the lap proceeds — a skipped RunType is a RunType that
had work and ignored it, not a RunType with no work. A quiet pass is DECLARED,
never silent: the run states "SURVEY: zero cards (quiet pass)" where it would
have presented cards, because from the operator's side an undeclared quiet pass
and an absent RunType work unit look identical. SIGN precedes SETTLE because a W question's
"what would answer it" includes the signed handoff: the cell cites a page whose
person's tick already exists. GI5 forbids outward composition; GI6 then records
the settlement before the cell stops.

**Serial in a chain, parallel across.** One chain is strictly serial — each rung cites only the rung below, so there is nothing inside it to parallelize. Parallelism lives ACROSS: questions each on their own lap, partition mirrors climbing side by side. The design door is the opposite shape: its fan-out is per-card INSIDE one page, one arm-agent each.

A Question Group is the schedulable view across those cells, not a wider
transition. `QG-B-I` may expose several runnable Information cells, but the
dispatcher still advances one cell and one Page at a time. Group state is
always derived from its member cells and is never written independently.

## The journey, mapped onto existing machinery

The lane has its own Workflow Runtime controller,
`haipipe-insight-workflow`: six RunType-owned Folder kinds — I0 Meta, I1
Question, I2 Data, I3 Information, I4 Knowledge, I5 Wisdom — with GI0-GI6
control keys and the register CELL (question × partition) as the frontier unit.
The division of labor with this door:

```text
this door        the LAW: one dataset, the Climb Law, the pens, the two ✋ · and the
                 LAP, which is HOW one cell moves
insight-workflow the RunTypes/Runtime: where a cell is, which control it faces,
                 the climb order (template, mirrors in parallel, X, every W),
                 receipts, stop rules
application-wf   cross-board receipts and handoffs; it never renames these RunTypes
page-workflow    CONTEXT…CHECK inside one bounded Page workflow pass; interactive
                 Page Runs are optional sibling records and never GI transitions
```

## The auto charter · standing authorization, signed once per run

The two ✋ gates never gain an auto mode, but a person may PRE-AUTHORIZE classes of decisions for one bounded run by signing a CHARTER at its start — the difference between a machine passing a gate and a person opening a class of gates in advance:

```text
charterable        vocabulary re-marks under a ruled grammar · 🟡 final flips whose
                   licensing sentence the machine QUOTES in the receipt · header
                   re-derivations citing their Queue
never charterable  handoff signatures · releasing a Run that starts NEW
                   computation · any write the charter does not name
```

A charter names the run, the classes, and the expiry (the run's close); its receipt quotes it; anything outside its classes stops at the gate exactly as before. Batching, not bypassing: the person's remaining appearances are the charter's signature and the run-close review.

## Board grooming is an audit, not a hidden writer

When a user asks to groom an InsightBoard, first identify the real board path
and read its `board.md`, MT01–MT04 registers, current D/I/K/W pages, and the
mechanical Insight checks. Report the current frontier, partial or open
register cells, dead or malformed references, and the Wisdom Handoffs that
are actually bindable. Keep the report linked to the exact source paths so a
demo is evidence-backed rather than generated from an empty fixture.

The board-level Insight plugin presents this as the read-only Check Space.
It may propose the next Question Group or identify a safe repair, but it does
not rewrite a finding, promote a register cell, overwrite evidence, or write a
person's `signed:` row. Those are explicit owner actions in the Insight
workflow. The Page-level Design plugin reads only the DesignBoard's declared
`reads:` InsightBoard and accepts only a person-signed Wisdom Handoff; it never
binds directly to D, I, or K.

## Ends at a signed handoff

A signed Design Handoff is an insight decision, not a design: it names finding,
strength, boundary, source versions, design consequence and forbidden
overreach, and never message copy. Design consumes its exact frozen
path/version/hash and GI6 settlement receipt under `ref/page-v2-adapter.md`; it
does not create a new PageX lane or synthetic Run. Shipping and measuring are
task-layer work, and the effect read back lands HERE — a refreshed source row
on MT00, a reopened chain, and a handoff v2 whose staleness reopens exactly the
design divisions that cited it.
