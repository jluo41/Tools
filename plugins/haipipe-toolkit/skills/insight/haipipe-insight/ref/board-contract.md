# InsightBoard resource and citation laws

Read when scaffolding, authoring an answer Page, or settling a register.

## The Climb Law · a six-level lifting chain

Authority to conclude lifts one rung at a time, each rung citing named rows below it. Each rung's fixed outline demands its citations division (Data Cited, Information Cited, Knowledge Cited); the climb into W requires exact source Result bindings and accepted local Evidence Items.

```text
① MT00       source: <extract>            the board's ONE dataset · set at scaffold
② D page     observes exact sources      cites the accepted evidence · no interpretation
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
verifies that authority before local Wisdom performs the new InsightBoard-contextual
operation; see `haipipe-insight-workflow`.

**One dataset, one board.** The chain's ① is a scope, not a suggestion:

```text
a new source extract        ──▶ a NEW InsightBoard
a new question              ──▶ a new chain INSIDE the board
a subgroup of the extract   ──▶ a PARTITION inside the board, never a board
a subgroup + SPLIT verdict  ──▶ MAY become a child board · the verdict is its birth
                                certificate, necessary and not sufficient: the child
                                still needs its own consumer (partition.md)
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
no `QK1-B`). `question-groups.md` owns membership, X routing, state, and
sorting.

## The three pens · who may write what

The workflow coordinates Runs and control actions; this door states the pens, and they never cross:

```text
register     writes STATE, never a finding         MT01-MT04 cells, including the
                                                   ⬜ annotations (`⬜ calc`) — notes
                                                   about work ARE state · haipipe-insight-question's
                                                   vocabulary · ✅/🚫/🟡-final settle
chain page   writes FINDINGS, never its own cell   the rung pages
handoff      EXPORTS, never re-derives             the W page's signed division
```

The join is a round trip through one question id: the register row's cell cites the closing page by id, and that page's handoff SERVES row names the register's question id back. `board.md`'s spine and close are DERIVED HEADERS of the same record: the registers are authoritative, a header that disagrees with them is stale, and reconciling it is register-pen work, citing the registers it was reconciled to. Its `## Pages` roster and group counts derive from DISK instead: completing them is part of the MINT act, in the same lap as the page they name. Final settlement is recorded in the register at GI6, so a Design page reads a signed handoff and never a D, I or K page's prose — two consumers can never keep separate books.

## The board, concretely

```text
<DataSubject>-InsightBoard/                RUNG-MAJOR · canonical
(optional A<NN>_ ordering prefix before the subject)
├── board.md                               spine · close · store:
├── 0-MT-meta/MT00-meta/ + MT01-MT04/      inventory + the four registers
├── 1-D-data/D<NN>-<slug>/                 observed · exact source provenance
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

The layout is chosen once, at scaffold; `partition.md` stays the partition grammar's single source, including the predeclared shared thresholds and the `POOL | SPLIT | UNDETERMINED` consequences for W. Under POOL, non-template W defers by id. Under UNDETERMINED, the template W is full-extract only and an unanswered partition W may use the licensed partial-final route; neither route exports a new handoff. Answer Pages and Meta declare any owed typed Evidence Items in `outline/` and bind Supporting and local Evidence Runs. Question registers record identity and state; they own no analytical evidence. Any selected Page Writing/Delivery Runs remain native to their Page, and no flat Run bank exists. Legacy probe paths are read-only migration input and are never created by new work. `A<NN>_` is only a project-local ordering option before the subject; the canonical shape stays `<DataSubject>-InsightBoard` (umbrella §Runtime folders).

## Folder owners

```text
MT00        haipipe-insight-meta          what data EXISTS · one per board
MT01-MT04   haipipe-insight-question      what is ASKED of one rung · four per board
D rung      haipipe-insight-data          observed · exact source provenance · never compares
I rung      haipipe-insight-information   derived from named D rows · never claims
K rung      haipipe-insight-knowledge     claimed from named I rows · never advises
W rung      haipipe-insight-wisdom        counsel + the signed Design Handoff
```

These are resource contracts. Each named skill owns its Folder kind's Page
Face, Task Face, plugins, closure and handoff. They live under `folder-kinds/`.
Actual work selects the Run Specs defined by the controller; a Folder kind
never creates a Run identity. Legacy `page-type:` keys resolve to these owners.
