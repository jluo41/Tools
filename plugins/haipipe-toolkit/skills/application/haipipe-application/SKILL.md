---
name: haipipe-application
description: >-
  One thin door over an Application's InsightBoard and DesignBoard. Their
  native I0-I5 and D0-D5 workflow phases own each Folder kind, both Folder
  faces, plugin profile, gates, and handoffs. The Application door owns only
  cross-board routing and ends at accepted Design. Trigger: application,
  InsightBoard, DesignBoard, Folder phase, data meta, question, DIKW, Brief,
  design, review, accept, retarget, PageX crossing, /haipipe-application.
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "1.0.6"
  last_updated: "2026-08-31"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-application · understand on one board, design on the other

Read `PREFERENCES.md` first. This skill is the only user-facing Application
door. Load `haipipe-folder`, resolve the owning Board/workflow phase, then let
that phase own the Folder's Page Face, Task Face, plugins, and closure.

## Architecture

```text
Task / Discovery Folders
          │ PageX whole-Folder link · Probe when evidence is missing
          ▼
🔎 InsightBoard                            🎨 DesignBoard
I0 Meta → I1-I5 Folders ──── PageX ────▶  D0 Brief → D1-D5 Folders → ✅ accepted
        D→I→K→W                                     R<n> divisions
        + Design Handoff                            D4 divisions + delivery/render/
```

Application owns the folders, the design need, the contextual Wisdom, and acceptance. Task rules still own how a chain page crosses Task/Discovery evidence. Folder ownership does not transfer evidence authority.

## Two boards, and why (JL 260820)

One board carrying both halves made one Brief Page do two jobs and gave two different readers one queue. The halves have different readers: the InsightBoard's reader checks whether the evidence holds; the DesignBoard's reader signs off that a message may reach a patient. Different question, different gate, different board.

```text
🔎 InsightBoard    reader: whoever checks the evidence     ends at: settled handoff
🎨 DesignBoard     reader: whoever approves the send       ends at: accepted version
```

PageX crosses boards unchanged, because it binds by path rather than by board.

## Phase-owned Folder kinds

```text
🔎 haipipe-insight-workflow
I0 Meta · I1 Question · I2 Data · I3 Information · I4 Knowledge · I5 Wisdom

🎨 haipipe-design-workflow
D0 Brief · D1 Card · D2 Unit · D3 Verdict · D4 Division · D5 PageDown
```

These twelve phase skills live under `application/workflow-phases/`. Each owns
one Folder kind's Page Face, Task Face, plugin profile, gate, and handoff.
`page-type: meta|question|data|information|knowledge|wisdom|brief|design`
remains a runtime compatibility lookup only. Promoted Principle is an optional
D4 Folder role reviewed again at D5, not an independent Page Type or phase.
`page-type: insight` remains Task-only for the consumer-neutral Task/Insights
Board.

## Verbs

```text
enter | status | board         open or scaffold the Application through fn/enter.md
meta | data | sources          create/resume the one Meta Page through fn/meta.md
question | ask | queue         register one question on the rung register it faces,
                               MT01-MT04 · haipipe-insight-question
chain | understand | DIKW      open or extend one D→I→K→W chain through fn/chain.md
brief | opportunity | venue    create/resume the one Brief Page through fn/brief.md
design | intervention | message
  | arc | components           create/resume one Design Folder through fn/design.md
render | project              generate a versioned projection through fn/render.md;
                              `artifact` is a legacy command alias, never a Folder kind
review | audit | check         CHECK selected Design versions and their trace
accept                         record the per-division acceptance row · the last act
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

design-side verbs (brief · design · direction · release · realize · judge ·
render · accept) are OWNED by the sibling door /haipipe-design since 260824:
reads:/born-of:/stance laws, design cards, artifact units, the arm-agent.
The rows above remain as forwards; fn/brief.md and fn/design.md stay as the
page-level procedures both doors share.
```

No-argument behavior: inside an Application, run `enter .`; outside one, ask for a path or offer to create the two board folders. Never infer an audience, behavior, or venue when that choice changes the design.

## The Application ends at ACCEPTED

```text
🎨 DESIGN BOARD                          │  NOT THE APPLICATION
─────────────────────────────────────────┼──────────────────────────────────
brief    what we are building            │  🔧 implementation · build + ship it
design   the messages, the rails         │  🧪 experiment     · run the A/B
accept   "this exact version may go"     │  📊 collection     · gather what came back
```

Deciding a version may ship is a design judgment and stays here. Building it, shipping it, running the experiment, and collecting the result are separate work the task layer already owns through Plan → Build → Execute → Report. The Application has no `deploy/` folder and no round folder.

## Runtime folders

A board's folder name SAYS ITS SUBJECT (JL 260820). `InsightBoard/` and `DesignBoard/` alone tell a reader the kind and nothing else, and a reader opening an Application wants to know which data and which topic before opening anything.

```text
<DataSubject>-InsightBoard/     the subject is the DATA    SmsClickR4-InsightBoard/
<DesignTopic>-DesignBoard/      the subject is the TOPIC   YoungMaleRefill-DesignBoard/
```

The subject is PascalCase; the suffix is the literal kind, so `ls *InsightBoard*` finds them all. The two subjects are named independently, which is what makes the count free: an Application may hold several InsightBoards when it reads distinct data, several DesignBoards when it designs for distinct topics, and any DesignBoard may PageX-bind any InsightBoard. Two boards is the common case, not the limit. No date suffix: the `<NN>-<topic>-<YYMMDD>` rule governs boards newly opened under `diagram/`, and these are runtime boards.

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
    ├── 1-P-principle/P<NN>-<slug>/        optional subordinate D4 promotion
    └── 2-DS-design/DS<NN>-<audience>-<job>-<venue>/  units as divisions
        ├── design/                       card + unit · one thread per Folder
        ├── delivery/render/              the unit as the recipient sees it
        ├── evidence/pagex/              cross-Folder relationships
        ├── evidence/display/            Page-owned displays, when selected
        └── outline/                     human plan and decision record
```

The InsightBoard tree above is the RUNG-MAJOR layout; the next section gives the partition-major alternative, and a page's path depends on which one its board uses.

A board is **one head page's scope**: one Meta is one source scope (one prepared extract), one Brief is one program scope (one outcome, venue and promise). A new source extract is a new InsightBoard; a new question is a new chain inside it. A SUBGROUP of an existing extract is never a new board by default: it is a partition (next section), and it may become its own board only by citing a SPLIT verdict (`ref/partition.md`). A new program is a new DesignBoard; a new audience is a new DS page inside it.

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

Do not create the legacy descriptions/themes/claims/advice ladder, a flat Application-wide `1-probes/`, a `4-deploy/`, or a `5-rounds/`. Each rung page owns its own bounded `evidence/probe/`; Meta, the registers, Brief, and Design Pages own none.

## The two authorities

```text
InsightBoard
  may PROBE Task/Discovery under each rung phase's Task Face
  (page-type: insight itself remains task-only)
  owns D→I→K and application-contextual W

DesignBoard
  may use PageX only
  owns selection, inline/promoted warrants, message roles, concrete content,
  and acceptance
```

The law: **Design Pages own no Probe; rung pages may Probe under Task-backed evidence authority.**

## Page flow

```text
Meta
  says what data exists, at what grain, how fresh, with what limits
    ↓
Question registers (MT01-MT04)
  hold what is asked of each rung · a Brief need or a board-raised curiosity
    ↓
D→I→K→W chain pages
  settle each question rung by rung and publish a Design Handoff at W
    ↓ PageX exact file/scope binding, across boards
Brief
  states the opportunity, audience, outcome, venue scope, and the needs it raises
    ↓
Design Folder(s)
  translate handoffs into cards, judged units, optional promoted warrants,
  R<n> divisions, and rails
    ↓
Review → ✅ accepted · STOP
```

Brief and Meta are both head pages and may be written in either order. Meta may exist alone with four empty registers, because data can land before anyone knows what it is for; the registers fill as the Brief raises needs or as a reader of the inventory becomes curious, and a source landing in Meta may raise no question at all.

## Dataset-first: where exploration goes before a Brief exists

An InsightBoard chain page must serve a question registered on MT01-MT04 — raised by a Brief need or by a reader's curiosity, the two births `/haipipe-insight` rules. What no chain page may serve is no question at all: exploration with no register row belongs on the **Task/Insights Board**, as a `scope: task` Page opened through `/haipipe-task insight`.

```text
a dataset lands, no Brief yet
        │
        ▼
🧪 /haipipe-task insight          scope: task · consumer-neutral · no serves:
   D → I → K → W → Reusable Findings
        │
        │  ... later, a Brief raises a need this already answers
        ▼
🔎 Application I1 QW              registers the need and exact RF version
        │
        ▼ PageX · pre-climbed external parent
🔎 Application I5 W               contextual counsel + forbidden overreach
        │ ✋ signed local Design Handoff · then GI6
        ▼
🎨 Design Page                    binds only the signed Application W
```

The chain verb (`fn/chain.md`, step 2) searches the Task/Insights Board FIRST
and treats a settled `scope: task`, Wisdom-targeted RF as a **pre-climbed
external parent** rather than recomputing D/I/K locally. The Application still
owns the commission and consequence: I1 registers one QW row, a local I5 W
Folder PageX-binds the exact RF version, contextualizes it, and earns a human
signature before GI6. A Task RF is consumer-neutral evidence, never a signed
Design Handoff and never direct Design authority. The normal local I2-I5 climb
remains the route when the Task Page is incomplete, stale, below Wisdom, or
does not answer the registered need.

These routes do not share a Page Type. Task owns the one-page
`haipipe-page-for-insight` contract. An Application owns an I1 Question
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

Design Pages borrow the exact handoff file/scope through PageX. PageX answers "which Page material"; the Design Page answers "which move follows here." Never copy probe cards or inspect Task `results/` from a Design Page.

## Review and acceptance gates

A Design division is acceptable only when all are true:

```text
trace         every substantive move reaches a settled Insight Design Handoff
applicability the borrowed K/W actually covers this audience, context, and outcome
venue         format, length, timing, interaction, and audience rules pass
safety        prohibited moves and uncertainty language pass
version       acceptance names design/handoff and visible render versions
human         the exact visible version is explicitly accepted
```

Acceptance is written on the division, not the page, so one unit may be accepted while a sibling is mid-revision. A changed Insight handoff, content edit, venue constraint, or re-render clears the affected division's `accepted:` row and only that row.

## Iteration is a handoff, not a stage

```text
✅ accepted ──▶ 🔧 shipped elsewhere
                      │
                      ▼
                🧪 executable Folder · Plan → Build → Execute → Report
                      │
                      ▼
                🔎 Insight Folder refreshes · handoff v2
                      │  PageX binding goes stale
                      ▼
                🎨 Design division reopens
```

The Application may propose the measurement question. Task owns execution; the InsightBoard's chain owns the refreshed DIKW reading and source staleness; the Design Page owns the response. An experiment run is a task folder, its result reading is a task page, and its synthesis is a chain page. Check that the task layer does not already cover a need before proposing a new board family for it.

## Legacy compatibility

Existing Applications remain readable. Do not delete or bulk-rewrite their folders without a separate migration request.

```text
legacy Seed + Venue + Pitch                    → Brief input
legacy Descriptions + Themes + Claims + Advice → candidate chain pages
legacy Narrative + Display + Section-edit      → Design Page input
legacy 1-probes/                               → historical bindings, read-only
legacy 0-lifecycle/ single-folder Applications → read and fold into the two boards
page-type: intervention on an existing page    → rename the key to design
page-type: artifact on an existing page        → fold into its Design Page as a division
external Task/Insights Board Pages             → valid PageX inputs; do not move them automatically
```

Compatibility means read-and-fold into the new target, not copy-and-continue the old stage spine.

## Status

Derive status from disk, not prose:

```text
frontier: meta | insight:<id> | brief | design:<id> | review | accepted
maturity: scoped | understood | designed | authored | reviewed | accepted
```

Also report open questions from the four registers (the wisdom register's rollup is the one-view source), stale Probe/PageX bindings, Design Page and division counts, and accepted render versions per division.

## Internal procedures

```text
fn/enter.md             open an Application, or scaffold both boards from nothing
fn/meta.md              Meta Page create/resume and the Source Inventory
fn/chain.md             open or extend one D→I→K→W chain for one question
fn/brief.md             Brief create/resume and the needs it raises
fn/principle.md         compatibility verb for an optional subordinate D4 warrant
fn/design.md            one audience/job/venue Design Folder, units as divisions
fn/render.md            render a unit through the page's delivery/render/ plugin
fn/feedback.md          family feedback
fn/digest.md            session feedback digestion

ref/partition.md        the partition-major layout grammar · a REFERENCE, not a verb:
                        fn/ holds procedures someone runs; a grammar is consulted
```

The old stage specialists under `_old/` are compatibility readers during migration and are not the target architecture.
