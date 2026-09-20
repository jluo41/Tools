---
name: haipipe-application
description: >-
  One thin door over an Application's InsightBoard and DesignBoard. Their
  Insight phases and canonical Design Folder owner govern both Folder
  faces, plugins, gates, and handoffs. The Application door owns only
  cross-board routing and ends at adopted, current Design. Trigger: application,
  InsightBoard, DesignBoard, Folder phase, data meta, question, DIKW, Brief,
  design, review, accept, retarget, signed Insight crossing, /haipipe-application.
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "3.1.0"
  last_updated: "2026-09-16"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-application · understand on one board, design on the other

Read `PREFERENCES.md` first. This skill is the only user-facing Application
door. Load `haipipe-folder`, resolve the owning Board/workflow phase, then let
that phase own the Folder's Page Face, Task Face, plugins, and closure.

## Architecture

```text
Task / Discovery Folders
          │ accepted Supporting Run Results
          ▼
🔎 InsightBoard                            🎨 DesignBoard
I0 Meta → I1-I5 Folders ── signed X1 input ─▶ Brief → stable Design Folder → ✅ adopted
        D→I→K→W                                  Commission + Design Runs + Page Runs
        + Design Handoff                         Generate Results + preview + Page CHECK
```

Application owns the folders, the design need, the contextual Wisdom, and acceptance. Task rules still own how a chain page crosses Task/Discovery evidence. Folder ownership does not transfer evidence authority.

## Two boards, and why (JL 260820)

One board carrying both halves made one Brief Page do two jobs and gave two different readers one queue. The halves have different readers: the InsightBoard's reader checks whether the evidence holds; the DesignBoard's reader signs off that a message may reach a patient. Different question, different gate, different board.

```text
🔎 InsightBoard    reader: whoever checks the evidence     ends at: settled handoff
🎨 DesignBoard     reader: whoever approves the send       ends at: adopted version
```

Insight evidence uses Supporting Run Results plus Local Input/Result. Design
freezes the exact signed handoff path, Page version, content hash, signature,
and GI6 receipt as input. PageX is not a readable Design input or Supporting
Run substitute.

## Phase-owned Folder kinds

```text
🔎 haipipe-insight-workflow
I0 Meta · I1 Question · I2 Data · I3 Information · I4 Knowledge · I5 Wisdom

🎨 haipipe-design + haipipe-design-workflow
stable Design Folder · Commission → Generate → Verify → Adopt
```

Insight retains its phase-owned contracts. Brief and Design are canonical
Folder owners; `haipipe-design-unit` is a Run worker, not a Folder phase.
Design has no D0–D5 adapter, PageX reader, promoted-principle phase, or
`page-type: brief|design` fallback.
`page-type: insight` remains Task-only for the consumer-neutral Task/Insights
Board.

## Verbs

```text
enter | status | board         open or scaffold the Application through fn/enter.md
meta | data | sources          create/resume the one Meta Page through fn/meta.md
question | ask | queue         register one question from plain words through
                               fn/question.md: level, partitions and lineage are
                               decided there · MT01-MT04 · haipipe-insight-question
chain | understand | DIKW      open or extend one D→I→K→W chain through fn/chain.md
brief | opportunity | venue    create/resume the one Brief Page through fn/brief.md
design | intervention | message
  | arc | components           create/resume one Design Folder through fn/design.md
render | project              generate a versioned projection through fn/render.md
review | audit | check         CHECK selected Design versions and their trace
accept                         record version-bound human adoption · the last act
retarget                       re-pin venue or audience and reopen dependent Design
feedback | digest              run the existing family feedback procedures
workflow | run | drive         cross the two boards through
                               haipipe-application-workflow; each board's
                               interior phases stay owned by its own workflow

insight-side verbs (meta · question · chain · partition · verdict · settle ·
handoff · check) are OWNED by the sibling door /haipipe-insight since 260827: the
one-dataset law, the Climb Law, the three pens, the two ✋ gates on that board.
The rows above remain as forwards; fn/meta.md and fn/chain.md stay as the
page-level procedures both doors share.

design-side verbs (brief · design · commission · release · generate · verify ·
render · adopt) are OWNED by the sibling door /haipipe-design: reads:/born-of:
authority, `rdNN_*` Run-backed Generate Results, independent verification, and the
unit worker. Old card/thread records are unsupported.
The rows above remain as forwards; fn/brief.md and fn/design.md stay as the
page-level procedures both doors share.
```

No-argument behavior: inside an Application, run `enter .`; outside one, ask for a path or offer to create the two board folders. Never infer an audience, behavior, or venue when that choice changes the design.

## The Application ends at ADOPTED + CURRENT

```text
🎨 DESIGN BOARD                          │  NOT THE APPLICATION
─────────────────────────────────────────┼──────────────────────────────────
brief    what we are building            │  🔧 implementation · build + ship it
design   the messages, the rails         │  🧪 experiment     · run the A/B
adopt    "this exact candidate may go"   │  📊 collection     · gather what came back
```

Adopting an exact candidate is a Design judgment and stays here. Its receipt is
also the Page's domain ruling; Page CHECK then verifies the current projection.
Building, shipping, experimenting, and collecting remain Task work. The
Application has no `deploy/` folder and no native round folder.

## Runtime folders

A board's folder name SAYS ITS SUBJECT (JL 260820). `InsightBoard/` and `DesignBoard/` alone tell a reader the kind and nothing else, and a reader opening an Application wants to know which data and which topic before opening anything.

```text
<DataSubject>-InsightBoard/     the subject is the DATA    SmsClickR4-InsightBoard/
<DesignTopic>-DesignBoard/      the subject is the TOPIC   YoungMaleRefill-DesignBoard/
```

The subject is PascalCase; the suffix is the literal kind, so `ls *InsightBoard*`
finds them all. The two subjects are named independently, which is what makes
the count free: an Application may hold several InsightBoards when it reads
distinct data and several DesignBoards when it designs for distinct topics.
A DesignBoard may consume any authorized signed W handoff as an exact frozen
input. Two boards is the common case, not the limit. No date suffix: the
`<NN>-<topic>-<YYMMDD>` rule governs boards newly opened under `diagram/`, and
these are runtime boards.

A project whose executable Task folders use a stage-letter grammar such as `tasks/D01_*` may prefix its runtime boards the same way, `A<NN>_` for InsightBoards and `B<NN>_` for DesignBoards, so `ls applications/` shows pipeline order: `A01_SMSR2Full-InsightBoard`, `B01_RefillFraming-DesignBoard`. Discovery uses its own explicit `bNN_/jNN_/tNN_/rNN_` address and does not supply a board prefix. The Application prefix is project-local ordering only; the canonical shape stays `<Subject>-<Kind>`, and the letter never appears inside pages.

```text
<application-root>/
├── <Cohort>-InsightBoard/                e.g. SMSR2Full-InsightBoard
│   ├── board.md
│   ├── 0-MT-meta/
│   │   ├── MT00-meta/                    sources · grain · freshness · NO question
│   │   ├── MT01-question-data/           QD<n> · asks of 1-D-data/
│   │   ├── MT02-question-information/    QI<n> · asks of 2-I-information/
│   │   ├── MT03-question-knowledge/      QK<n> · asks of 3-K-knowledge/
│   │   └── MT04-question-wisdom/         QW<n> · asks of 4-W-wisdom/ + board rollup
│   ├── 1-D-data/D<NN>-<slug>/            observed · run-bound
│   ├── 2-I-information/I<NN>-<slug>/     derived · cites D
│   ├── 3-K-knowledge/K<NN>-<slug>/       claimed · cites I
│   └── 4-W-wisdom/W<NN>-<slug>/          counsel + handoff · cites K
└── <Program>-DesignBoard/                e.g. RefillFraming-DesignBoard
    ├── board.md                          reads: · the evidence whitelist
    ├── 0-BR-brief/BR00-brief/            outcome · venue scope · audience set
    └── 2-Design/Design-<NN>-<audience>-<job>-<venue>/  one stable Design Folder
        ├── runs/                         caller-authored YAML Run Tickets
        ├── results/                      Generate and Verify Results; results/rdNN_commission|adopt_*/decision.yaml
        ├── scripts/config/               frozen per-Run configuration
        ├── delivery/render/              the Adopt preview: the exact draft, copied
        ├── workflow/                    Page workflow receipts (when used)
        ├── outline/<stem>-design-items.md  the Design Item register (goal and rules)
        ├── outline/evidence/            Page-owned typed evidence
        └── delivery/web|latex|word/     released Page projections
```

The InsightBoard tree above is the RUNG-MAJOR layout; the next section gives the partition-major alternative, and a page's path depends on which one its board uses.

A board is **one head page's scope**: one Meta is one source scope (one prepared extract), one Brief is one program scope (one outcome, venue and promise). A new source extract is a new InsightBoard; a new question is a new chain inside it. A SUBGROUP of an existing extract is never a new board by default: it is a partition (next section), and it may become its own board only by citing a SPLIT verdict (`ref/partition.md`). A new program is a new DesignBoard; a new audience is a new line in the Brief and a new Design Folder inside it.

## Two InsightBoard layouts (JL 260823)

The tree above is the default, RUNG-MAJOR: groups are the four rungs, and a subgroup is at most a column inside an I page. When subgroup analysis is first-class, the same ladder climbed per subgroup under identical thresholds, each subgroup producing its own K claims, the board lays out PARTITION-MAJOR instead:

```text
├── 0-MT-meta/            same head · the registers gain one Queue COLUMN per partition
├── 1-F-full/             FD→FI→FK→FW · the template ladder on the whole extract
├── 2-<L>-<slug>/         one group per partition · mirrors 1-F-full slug for slug
└── X-cross/              contrast · heterogeneity · the POOL/SPLIT verdict
                          (index-free: letters sort last · legacy: 9-X-cross/)
```

Page id = partition letter + rung letter + NN (`BK01` is partition B,
Knowledge, first page); phase ownership is unchanged. The grammar's single
source is `ref/partition.md`: the mirror rule, MT00 partition register,
shared-threshold rule, X-only comparison law, and SPLIT verdict.

Do not create the legacy descriptions/themes/claims/advice ladder, a flat Application-wide run bank, a `4-deploy/`, or a `5-rounds/`. Each rung page declares typed Evidence Items and binds Supporting/Local Runs; Meta, the registers, Brief, and Design Pages own none.

## The two authorities

```text
InsightBoard
  may commission bounded Supporting Runs from Task/Discovery under each rung
  phase's Task Face (page-type: insight itself remains task-only)
  owns D→I→K and application-contextual W

DesignBoard
  may consume authorized frozen inputs; never launches upstream work invisibly
  owns selection, inline/promoted warrants, message roles, concrete content,
  and acceptance
```

The law: **Design Pages own no upstream execution; rung pages may commission
Supporting Runs under Task-backed evidence authority.**

## Page flow

```text
Meta
  says what data exists, at what grain, how fresh, with what limits
    ↓
Question registers (MT01-MT04)
  hold what is asked of each rung · their partition columns derive
  Question Groups = partition × DIKW target
    ↓
D→I→K→W chain pages
  settle each question rung by rung and publish a Design Handoff at W
    ↓ exact signed W path/Page-version/hash + GI6 receipt, frozen by Design
Brief
  states the opportunity, audience, outcome, venue scope, and the needs it raises
    ↓
Design Folder(s)
  freeze Commission bets → generate immutable DUs → independently verify
  → render previews → person adopts exact versions
    ↓
Page release → fresh CHECK of the same adoption/projection → ✅ current · STOP
```

Brief and Meta are both head pages and may be written in either order. Meta may exist alone with four empty registers, because data can land before anyone knows what it is for; the registers fill as the Brief raises needs or as a reader of the inventory becomes curious, and a source landing in Meta may raise no question at all.

## Dataset-first: where exploration goes before a Brief exists

An InsightBoard chain page must serve a question registered on MT01-MT04 — raised by a Brief need or by a reader's curiosity, the two births `/haipipe-insight` rules. What no chain page may serve is no question at all: exploration with no register row belongs on the **Task/Insights Board**, as a `scope: task` Page opened through `/haipipe-insight task` (`/haipipe-task insight` remains the compatibility alias).

```text
a dataset lands, no Brief yet
        │
        ▼
🧪 /haipipe-insight task           scope: task · consumer-neutral · no serves:
   topic instance → item Runs → versioned D/I/K/W/RF Results
        │
        │  ... later, a Brief raises a need this already answers
        ▼
🔎 Application I1 QW              pins instance/item/version/RF + Result hash
        │
        ▼ Supporting Result · pre-climbed external parent
🔎 Application I5 W               contextual counsel + forbidden overreach
        │ ✋ signed local Design Handoff · then GI6
        ▼
🎨 Design Page                    binds only the signed Application W
```

The chain verb (`fn/chain.md`, step 2) searches the Task/Insights Board FIRST
and treats an accepted `scope: task` instance item's Wisdom-targeted RF as a **pre-climbed
external parent** rather than recomputing D/I/K locally. The Application still
owns the commission and consequence: I1 registers one QW row, a local I5 W
Folder binds the exact item Result through its Evidence graph, contextualizes it, and earns a human
signature before GI6. A Task RF is consumer-neutral evidence, never a signed
Design Handoff and never direct Design authority. The normal local I2-I5 climb
remains the route when the selected item Result is incomplete, stale, below Wisdom, or
does not answer the registered need.

These routes do not share a Page Type. Task owns the topic-instance Page and
item Run contract in `haipipe-page-insight`. An accepted item can be reused
while siblings remain open. An Application owns an I1 Question
register plus separate I2 Data, I3 Information, I4 Knowledge, and I5 Wisdom
Folder contracts under `haipipe-insight-workflow`.

## Insight-to-design handoff

A chain keeps D/I/K evidence-led and lets W become Application-contextual only after K settles:

```text
Application Need → neutral Question → D → I → K → contextual W → Design Handoff
                                     or
Application Need → QW → exact Task RF → contextual W → Design Handoff
                         pre-climbed      local + signed
```

The Design Handoff names finding, strength, boundary, source versions, design consequence, forbidden overreach, and the Brief/Design need it serves. It does not write final message copy.

Design Pages pin the exact signed handoff file/scope and hash in their Run
inputs. PageX is invalid. Never copy upstream Run artifacts, invent an Insight
Run identity, or inspect raw Task results from a Design Page.

## Review, adoption, and Page gate

A Design candidate is adoptable only when all are true:

```text
trace         every evidence-informed move reaches a settled Insight Design Handoff;
              a brief-only item says it rests on the Brief alone
applicability the borrowed K/W actually covers this audience, context, and outcome
venue         format, length, timing, interaction, and audience rules pass
safety        prohibited moves and uncertainty language pass
version       adoption names the exact draft hash, its Verify Result, and the preview
              copy; the Commission and run records pin the insight versions
human         the exact visible candidate is explicitly adopted
```

Adoption is an immutable Design decision receipt, not a Page prose tick. One
candidate may be adopted while a sibling remains historical or under revision.
A changed handoff, candidate, venue constraint, verification, or render stales
only the affected binding. `page_ruling: domain-gate` makes Page CHECK consume
the same receipt; it never asks the person to select twice.

## Iteration is a handoff, not a stage

```text
✅ adopted + Page-current ──▶ 🔧 shipped elsewhere
                      │
                      ▼
                🧪 executable Folder · Plan → Build → Execute → Report
                      │
                      ▼
                🔎 Insight Folder refreshes · handoff v2
                      │  frozen signed-input pin goes stale
                      ▼
                🎨 dependent Design candidate reopens
```

The Application may propose the measurement question. Task owns execution; the InsightBoard's chain owns the refreshed DIKW reading and source staleness; the Design Page owns the response. An experiment run is a task folder, its result reading is a task page, and its synthesis is a chain page. Check that the task layer does not already cover a need before proposing a new board family for it.

## Legacy non-Design inputs

Some pre-Design Application inputs may still be inspected under their own
contracts. This does not apply to old Design formats.

```text
legacy Seed + Venue + Pitch                    → Brief input
legacy Descriptions + Themes + Claims + Advice → candidate chain pages
legacy 1-probes/                               → historical bindings, read-only
legacy 0-lifecycle/ single-folder Applications → read and fold into the two boards
external Task/Insights Board Results           → valid Supporting Results when exactly pinned;
                                                  do not move them automatically
```

Design D0–D5/GD0–GD6, PageX, `design/DU*/`, old card/thread/plugin records,
v1 Tickets/Results, `rNN_design_*`, `page-type: intervention|artifact|design`,
and old acceptance rows are rejected. They are never read-and-folded.

## Status

Derive status from disk, not prose:

```text
frontier: meta | insight:<id> | brief | design:<id> | review | adopted | page-current
maturity: scoped | understood | designed | authored | reviewed | adopted | current
```

Also report Question Groups in MT00 partition order then D→I→K→W, their open
member cells from the four registers (the wisdom register's rollup remains the
one-view source), stale Supporting Run or frozen handoff inputs, the Design Run
and Page Run frontiers separately, and adopted member/render versions.

## Internal procedures

```text
fn/enter.md             open an Application, or scaffold both boards from nothing
fn/meta.md              Meta Page create/resume and the Source Inventory
fn/chain.md             open or extend one D→I→K→W chain for one question
fn/question.md          register one question from plain words: level, partitions, lineage
fn/verdict.md           drive the X group XI → XK → the POOL/SPLIT verdict
fn/brief.md             Brief create/resume and the needs it raises
fn/design.md            one audience/job/venue Design Folder, units as Results
fn/render.md            render a unit through the page's delivery/render/ plugin
fn/feedback.md          family feedback
fn/digest.md            session feedback digestion

ref/partition.md        the partition-major layout grammar · a REFERENCE, not a verb:
                        fn/ holds procedures someone runs; a grammar is consulted
```

The `_old/` directory is documentation history only and is never a runtime
reader or migration source.
