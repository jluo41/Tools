---
name: haipipe-insight
description: >-
  InsightBoard door for the I0-I5 climb over one dataset. Meta declares the
  extract; Question registers ask; Data observes; Information derives;
  Knowledge claims; Wisdom counsels and exports a person-signed Design
  Handoff. Phase skills own each Folder and both faces; this door owns the
  one-dataset, register, climb, partition and signing laws. Ends at signed
  handoff, never designs. Trigger: InsightBoard, question register, DIKW,
  climb, chain, partition, pooling verdict, Design Handoff, /haipipe-insight.
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "1.0.5"
  last_updated: "2026-08-31"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-insight · answer as a climb, under Task-backed evidence

`haipipe-application` remains the Application umbrella (two-board pairing, PageX crossing, ends-at-ACCEPTED); this door owns the InsightBoard's own laws and verbs, symmetric to `/haipipe-design` on the other board. Physically it lives inside `skills/application/` because an InsightBoard cannot exist outside an Application; the slash name is first-class regardless.

**The name is reused; the thing is not.** A `/haipipe-insight` existed until 260717 as a knowledge-base layer and was retired (application CHANGELOG 6.6.0) because it competed with the probe → task/discovery bank for evidence authority. This door holds NO evidence: evidence lives in the bank, values bind to QA files, and the door states only how one board turns them into a signed handoff.

**Who owns what**:

```text
haipipe-insight               this door · the one-dataset/climb/register/handoff laws · the verbs
haipipe-insight-meta         the head: source inventory only, holds NO question
haipipe-insight-question     the four registers MT01-MT04: asked and tracked, never concluded
haipipe-insight-data/-information/-knowledge/-wisdom     what each rung IS
haipipe-application           the umbrella keeps ref/partition.md (the partition grammar's single
                              source) and fn/meta.md + fn/chain.md, the page-level procedures
haipipe-page-workflow         the loop every page here runs, like every page anywhere
haipipe-insight-workflow      the lane's phase machine: I0-I5, GI0-GI6,
                              the CELL frontier, dispatch, receipts, climb order
haipipe-folder                the shared two-face Folder and phase contract
haipipe-application-workflow  cross-board handoffs only; no duplicate Insight phases
```

`page-type: insight` stays TASK-ONLY: the consumer-neutral whole chain in one
Page (`/haipipe-task insight`), which is where dataset-first exploration lives.
This door never mints one—its Folders are Meta, Question, Data, Information,
Knowledge, and Wisdom. A settled Wisdom-targeted Task RF may enter only as the
workflow's pre-climbed external parent: I1 registers its exact version and a
local I5 Wisdom Folder contextualizes and signs the Application Design Handoff.
RF never reaches Design directly.

## The Climb Law · a six-level lifting chain

Authority to conclude LIFTS one rung at a time, each rung citing only named rows of the rung below — the mirror of the design side's narrowing Reads Law. Enforcement is two-sided: each rung's fixed outline shape demands its citations division (Data Cited, Information Cited, Knowledge Cited), and G1 refuses the climb into W until every value below is bound to a QA file by path.

```text
① MT00       source: <extract>            the board's ONE dataset · set at scaffold
② D page     observes, run-bound          cites the run/QA file · no interpretation
③ I page     derives from named D rows    a rate is Information, never a claim
④ K page     claims from named I rows     strength · rivals · boundary
⑤ W page     counsels from named K rows   contextual · verdict-conditioned
⑥ Handoff    exports W, signed ✋          never re-derives · the ONLY bindable level
```

Level-skipping is a CHECK routing failure, with exactly two exceptions, both inside the X cross group and both recorded in the rung contracts: the contrast I page derives from MIRRORED I rows (I-from-I), and the pooling-verdict K page cites the heterogeneity K row (K-from-K), because its subject is a claim about claims.

The pre-climbed external-parent bridge is not a third skip: the Task Insight
Page already contains and CHECK-closes the complete `D→I→K→W→RF` chain. GI4
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

Either way the question is written ONCE, on the one register facing its rung (QD/QI/QK/QW ids), with target, raiser, what-would-answer and a state cell; on a partition-major board it is asked per partition as Queue COLUMNS, never re-registered (`QK1` spans all partitions; there is no `QK1-B`).

## The three pens · who may write what

The workflow drives the lap; this door states the pens, and they never cross:

```text
register     writes STATE, never a finding         MT01-MT04 cells, including the
                                                   ⬜ annotations (`⬜ calc`) — notes
                                                   about work ARE state · for-question's
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

The layout is chosen once, at scaffold; `ref/partition.md` stays the partition grammar's single source (the mirror rule, reserved letters F/X/Q/S/M, the index-free X seat, the shared-threshold file, the POOL/SPLIT verdict conditioning every W — under POOL a non-template W page DEFERS by id and exports no handoff). Each rung page owns its own bounded `evidence/probe/`; Meta and the four registers own none, and no flat `1-probes/` exists. A flat `probe/` on an unmigrated Page is a compatibility alias, never the shape new work writes. `A<NN>_` is only a project-local ordering option before the subject; the canonical shape stays `<DataSubject>-InsightBoard` (umbrella §Runtime folders).

## The Folder phases this door owns

```text
MT00        haipipe-insight-meta          what data EXISTS · one per board
MT01-MT04   haipipe-insight-question      what is ASKED of one rung · four per board
D rung      haipipe-insight-data          observed · run-bound · never compares
I rung      haipipe-insight-information   derived from named D rows · never claims
K rung      haipipe-insight-knowledge     claimed from named I rows · never advises
W rung      haipipe-insight-wisdom        counsel + the signed Design Handoff
```

These are six workflow phases, not six configuration/Page-Type skills. Each
named skill owns its Folder kind's Page Face, Task Face, plugins, gate, and
handoff. Legacy `page-type:` keys resolve to these skills during migration.

## Verbs

```text
enter | status      resolve the board · derive frontier from disk · count register cells by state
meta | sources      create/resume the one MT00 (the umbrella's fn/meta.md)
question | ask      register one question on the rung register it faces · NEVER answer it there
climb | chain       open or extend the frontier rung for one question (the umbrella's fn/chain.md) ·
                    probes raised · ✋ a person releases each card before dispatch
partition           register a partition on MT00 and insert its group before X (ref/partition.md)
verdict             drive the X group to its pooling K page · POOL or SPLIT
settle              flip the register cell ✅, 🚫 with a reason, or 🟡 <page> final
                    (for-question's exit), citing the closing page
handoff             draft the W page's Design Handoff division · ✋ a person signs its
                    `signed:` row — `signed: ✅ <initials> <YYMMDD>`, never a machine ·
                    the door RECORDS a signature the person states, never decides one
check | review      CHECK selected rung pages in a fresh context
workflow | run      drive laps (§The lap): gap → climb (✋release inside) → ✋sign → settle · STOP
```

The two Insight cross-phase ✋ gates never have an auto mode: releasing a probe
card and signing a handoff are a person's, and every page dispatched into
`haipipe-page-workflow` pins `mode: copilot`. Page-local outline/read/verified
ticks remain nested controls rather than new Insight gates. With the Design
door's two cross-phase gates (card release, acceptance), they are the
Application's four domain authority transfers, two per door.

## The lap, step by step

The `run` verb's procedure. These six are VERBS, not phases: none can name an authority page beyond the pages already on the board, which is the naming-law test (`haipipe-application-workflow` 0.4.0) — the design door's realize and judge are verbs by the same test. The lane's PHASES are the rungs themselves, named in `haipipe-insight-workflow`; a lap is how one register cell moves through them.

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
③ CLIMB    run that ONE page through haipipe-page-workflow,      pen: chain page
           mode: copilot — cards raised at PROBE (a card is the
           probe plugin's `evidence/probe/PP<NN>-<slug>/card.md`, states
           and shape per board/haipipe-plugin/ref/roster.md —
           this door POINTS, it does not restate) · MATCH the
           QA bank BEFORE raising and AGAIN at dispatch — a
           released card whose numbers the bank already holds
           reuses them and dispatches NOTHING, because a re-run
           reproducing known numbers under a new timestamp
           muddies the run identity closed pages already bind ·
           ✋ a person releases each · answers land at EVIDENCE
           bound to QA paths · the rung closes CHECK
④ SIGN     only when the rung was W: draft the Design Handoff    pen: W page
           division · ✋ a person signs at that page's CHECK (G2)
⑤ SETTLE   flip the register cell ✅, 🚫 with a reason, or        pen: register
           🟡 <page> final when its page licenses the exit,
           citing the page that closed it (G3)
⑥ EXIT     gaps remain → next lap at ② · every cell settled → the lane is done
────────────────────────────────────────────────────────────────────────────
```

The pens own their steps — ① and ⑤ write STATE, ② and ③ write FINDINGS, ④
exports — and the lap's two cross-phase ✋ are the door's two domain gates; no
third GI transfer appears. A ZERO-CARD ③ is a legal quiet pass: when every
value the page owes already exists in the store, PROBE raises nothing, there is
nothing to release, and the lap proceeds — a skipped phase is a phase that had
cards and ignored them, not a phase that had none. A quiet pass is DECLARED,
never silent: the run states "PROBE: zero cards (quiet pass)" where it would
have presented cards, because from the operator's side an undeclared quiet pass
and a skipped phase look identical. SIGN precedes SETTLE because a W question's
"what would answer it" includes the signed handoff: the cell cites a page whose
person's tick already exists. GI5 forbids outward composition; GI6 then records
the settlement before the cell stops.

**Serial in a chain, parallel across.** One chain is strictly serial — each rung cites only the rung below, so there is nothing inside it to parallelize. Parallelism lives ACROSS: questions each on their own lap, partition mirrors climbing side by side. The design door is the opposite shape: its fan-out is per-card INSIDE one page, one arm-agent each.

## The journey, mapped onto existing machinery

The lane has its own phase machine, `haipipe-insight-workflow`: six
phase-owned Folder kinds — I0 Meta, I1 Question, I2 Data, I3 Information, I4
Knowledge, I5 Wisdom — with gates GI0-GI6 and the register CELL (question ×
partition) as the frontier unit. The division of labor with this door:

```text
this door        the LAW: one dataset, the Climb Law, the pens, the two ✋ · and the
                 LAP, which is HOW one cell moves
insight-workflow the PHASES: where a cell is, which gate it faces, the climb order
                 (template, mirrors in parallel, X, every W), receipts, stop rules
application-wf   cross-board receipts and handoffs; it never renames these phases
page-workflow    OUTLINE…CHECK inside every single page RUN
```

## The auto charter · standing authorization, signed once per run

The two ✋ gates never gain an auto mode, but a person may PRE-AUTHORIZE classes of decisions for one bounded run by signing a CHARTER at its start — the difference between a machine passing a gate and a person opening a class of gates in advance:

```text
charterable        vocabulary re-marks under a ruled grammar · 🟡 final flips whose
                   licensing sentence the machine QUOTES in the receipt · header
                   re-derivations citing their Queue
never charterable  handoff signatures · releasing a probe card that runs NEW
                   computation · any write the charter does not name
```

A charter names the run, the classes, and the expiry (the run's close); its receipt quotes it; anything outside its classes stops at the gate exactly as before. Batching, not bypassing: the person's remaining appearances are the charter's signature and the run-close review.

## Ends at a signed handoff

A signed Design Handoff is an insight decision, not a design: it names finding, strength, boundary, source versions, design consequence and forbidden overreach, and never message copy. Composing from it is the DesignBoard's, through PageX; shipping and measuring are task-layer work; and the effect read back lands HERE — a refreshed source row on MT00, a reopened chain, a handoff v2 whose staleness reopens exactly the design divisions that cited it.
