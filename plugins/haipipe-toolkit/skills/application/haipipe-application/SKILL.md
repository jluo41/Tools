---
name: haipipe-application
description: >-
  One door for building an Application as TWO boards. The InsightBoard is headed by one Meta Page saying what data exists plus four question registers saying what is asked of each rung, and holds D/I/K/W chain pages that turn Task-backed evidence into answers and a Design Handoff. The DesignBoard is headed by one Brief Page saying what is being built and for whom, and holds audience/job Design Pages that consume settled handoffs through PageX and never Probe. The Application ENDS AT ACCEPTED: building, shipping, running the experiment, and collecting data are task-layer work. Use for application setup or status, data meta, raising or checking questions, DIKW for a design need, message/intervention design, SMS/email/dashboard/checklist/report design, review, acceptance, or retargeting. Trigger: application, InsightBoard, DesignBoard, data meta, source inventory, question register, raise a question, insight need, design page, message design, artifact, SMS, email, dashboard, checklist, report, review, accept, retarget, PageX insight, /haipipe-application.
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "0.15.0"
  last_updated: "2026-08-23"
  summary: "0.15.0 is the contradiction sweep (JL 260823, four-reviewer audit): dead fn pointers cleared, the cohort rule qualified against the SPLIT-verdict licensing rule, the probe authority line corrected, and the four rung contracts + meta + question updated for partition-major in step. 0.14.0 added the sibling RUN head; 0.13.0 the partition-major layout."
---

# /haipipe-application · understand on one board, design on the other

Read `PREFERENCES.md` first. This skill is the only user-facing Application door. Resolve the Application root, select one owning Page, and hand it to `haipipe-page` with the matching Page Type and current Page phase.

## Architecture

```text
Task / Discovery evidence
          │ Probe · Task authority
          ▼
🔎 InsightBoard                            🎨 DesignBoard
Meta → Insight Page(s)  ──── PageX ────▶   Brief → Design Page(s) → ✅ accepted
        D→I→K→W                                     R<n> divisions
        + Design Handoff                            2-artifacts/ projections
```

Application owns the folders, the design need, the contextual Wisdom, and acceptance. Task rules still own how an Insight Page crosses Task/Discovery evidence. Folder ownership does not transfer evidence authority.

## Two boards, and why (JL 260820)

One board carrying both halves made one Brief Page do two jobs and gave two different readers one queue. The halves have different readers: the InsightBoard's reader checks whether the evidence holds; the DesignBoard's reader signs off that a message may reach a patient. Different question, different gate, different board.

```text
🔎 InsightBoard    reader: whoever checks the evidence     ends at: settled handoff
🎨 DesignBoard     reader: whoever approves the send       ends at: accepted version
```

PageX crosses boards unchanged, because it binds by path rather than by board.

## Page Types

```text
🔎 InsightBoard · framing asks, the chain answers, one page per LEVEL
page-type: meta         exactly one · sources, grain, freshness · holds NO question
page-type: question     exactly four · MT01-MT04, one register per rung · QD/QI/QK/QW
                        ids · asks and tracks, never concludes · no probe/, no display/
page-type: data         D · observed, run-bound, uninterpreted
page-type: information  I · rates and contrasts derived from named D rows
page-type: knowledge    K · a proposition with strength, rivals, boundary
page-type: wisdom       W · counsel + the Design Handoff · the ONLY bindable level

🎨 DesignBoard · frame, warrant, compose
page-type: brief        exactly one · outcome, venue scope, audience SET, needs
page-type: principle    P · because <W>, do <move>, within <rail> · the ONLY
                        DesignBoard layer that reads the InsightBoard
page-type: design       DS · one audience × job × venue · units as divisions

`page-type: insight` is TASK-ONLY: the consumer-neutral whole chain in one page on
the Task/Insights Board, which is where dataset-first exploration lives.
```

`page-type: intervention` and `page-type: artifact` were retired on 260820. Intervention was renamed to `design` because one concept wearing two words is what made readers ask whether Design and Artifact were the same thing. Artifact was absorbed: five of its six Content roles already existed inside a Design Page's unit division, and the sixth, acceptance, is now a per-division row.

## Verbs

```text
enter | status | board         open or scaffold the Application through fn/enter.md
meta | data | sources          create/resume the one Meta Page through fn/meta.md
question | ask | queue         register one question on the rung register it faces,
                               MT01-MT04 · haipipe-page-for-question
chain | understand | DIKW      open or extend one D→I→K→W chain through fn/chain.md
brief | opportunity | venue    create/resume the one Brief Page through fn/brief.md
design | intervention | message
  | arc | components           create/resume one Design Page through fn/design.md
artifact | project | render    generate a versioned projection through fn/render.md
review | audit | check         CHECK selected Design versions and their trace
accept                         record the per-division acceptance row · the last act
retarget                       re-pin venue or audience and reopen dependent Design
feedback | digest              run the existing family feedback procedures
workflow | run | drive         drive the whole Application forward through the
                               sibling RUN head, haipipe-application-workflow:
                               six phases in two lanes, three blocking human gates
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

A project whose sibling folders use the `<Letter><NN>_<slug>` grammar (JL 260821, e.g. `tasks/D01_*`, `discoveries/S01_*`) may prefix its runtime boards the same way, `A<NN>_` for InsightBoards and `B<NN>_` for DesignBoards, so `ls applications/` shows pipeline order: `A01_InsightBoard-SMSR2Full`, `B01_DesignBoard-RefillFraming`. The prefix is project-local ordering only; the canonical shape stays `<Kind>-<Subject>`, and the letter never appears inside pages.

```text
<application-root>/
├── InsightBoard-<Cohort>/                e.g. InsightBoard-SMSR2Full
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
└── DesignBoard-<Program>/                e.g. DesignBoard-RefillFraming
    ├── board.md
    ├── 0-BR-brief/BR00-brief/            outcome · venue scope · audience set
    ├── 1-P-principle/P<NN>-<slug>/        cites W · the only crossing
    └── 2-DS-design/DS<NN>-<slug>/         units as divisions
        ├── pagex/ outline/ display/
        └── render/                       the unit as the recipient sees it
```

A board is **one head page's scope**: one Meta is one source scope (one prepared extract), one Brief is one program scope (one outcome, venue and promise). A new source extract is a new InsightBoard; a new question is a new chain inside it. A SUBGROUP of an existing extract is never a new board by default: it is a partition (next section), and it may become its own board only by citing a SPLIT verdict (`ref/partition.md`). A new program is a new DesignBoard; a new audience is a new DS page inside it.

## Two InsightBoard layouts (JL 260823)

The tree above is the default, RUNG-MAJOR: groups are the four rungs, and a subgroup is at most a column inside an I page. When subgroup analysis is first-class, the same ladder climbed per subgroup under identical thresholds, each subgroup producing its own K claims, the board lays out PARTITION-MAJOR instead:

```text
├── 0-MT-meta/            same head · the registers gain one Queue COLUMN per partition
├── 1-F-full/             FD→FI→FK→FW · the template ladder on the whole extract
├── 2-<L>-<slug>/         one group per partition · mirrors 1-F-full slug for slug
└── 9-X-cross/            contrast · heterogeneity · the POOL/SPLIT verdict (pinned at 9)
```

Page id = partition letter + rung letter + NN (`BK01` is partition B, Knowledge, first page); page types are unchanged. The grammar's single source is `ref/partition.md`: the mirror rule, the MT00 partition register, the shared-threshold rule, the X-only comparison law, and the SPLIT verdict as the only birth certificate a per-partition child board may cite. The choice of layout is made once, at scaffold.

Do not create the legacy descriptions/themes/claims/advice ladder, a flat Application-wide `1-probes/`, a `4-deploy/`, or a `5-rounds/`. Each Insight Page owns its own bounded `probe/`; Meta, Brief, and Design Pages own none.

## The two authorities

```text
InsightBoard
  may PROBE Task/Discovery under Task-backed evidence authority
  (the rung contracts inherit haipipe-page-for-task; page-type: insight itself is task-only)
  owns D→I→K and application-contextual W

DesignBoard
  may use PageX only
  owns selection, design principles, message roles, concrete content, and acceptance
```

The law: **Design Pages own no Probe; Insight Pages may Probe under Task-backed evidence authority.**

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
Design Page(s)
  translate handoffs into principles, message architecture, R<n> divisions, and rails
    ↓
Review → ✅ accepted · STOP
```

Brief and Meta are both head pages and may be written in either order. Meta may exist alone with four empty registers, because data can land before anyone knows what it is for; the registers fill as the Brief raises needs or as a reader of the inventory becomes curious, and a source landing in Meta may raise no question at all.

## Dataset-first: where exploration goes before a Brief exists

An InsightBoard Page must serve a named need, so it cannot be opened before a Brief raises one. That is deliberate, and it is not a dead end: exploration with no consumer yet belongs on the **Task/Insights Board**, as a `scope: task` Page opened through `/haipipe-task insight`.

```text
a dataset lands, no Brief yet
        │
        ▼
🧪 /haipipe-task insight          scope: task · consumer-neutral · no serves:
   D → I → K → W → Reusable Findings
        │
        │  ... later, a Brief raises a need this already answers
        ▼
   PageX binding                  borrowed straight into the Application
        │
        ▼
🎨 Design Page                    no local Insight Page needed at all
```

The chain verb (`fn/chain.md`, step 2) searches the Task/Insights Board FIRST and binds a settled `scope: task` Page rather than reopening the same question locally. A local chain is for what that search does not answer: the reading that only makes sense for this audience, this venue, this promise.

The two scopes share one contract and one key, `page-type: insight`, with `scope:` picking the instance. Read `haipipe-page-for-insight` before writing either.

## Insight-to-design handoff

An Insight Page keeps D/I/K evidence-led and lets W become Application-contextual only after K settles:

```text
Application Need → neutral Question → D → I → K → contextual W → Design Handoff
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
                🧪 task folder · Plan → Build → Execute → Report
                      │
                      ▼
                🔎 Insight Page refreshes · handoff v2
                      │  PageX binding goes stale
                      ▼
                🎨 Design division reopens
```

The Application may propose the measurement question. Task owns execution; the InsightBoard's Insight Page owns the refreshed DIKW reading and source staleness; the Design Page owns the response. An experiment run is a task folder, its result reading is a task page, and its synthesis is an Insight Page. Check that the task layer does not already cover a need before proposing a new board family for it.

## Legacy compatibility

Existing Applications remain readable. Do not delete or bulk-rewrite their folders without a separate migration request.

```text
legacy Seed + Venue + Pitch                    → Brief input
legacy Descriptions + Themes + Claims + Advice → candidate Insight Pages
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
fn/principle.md         one because/do/within rule, citing one W handoff
fn/design.md            one audience/job/venue design, units as divisions
fn/render.md            render a unit through the page's render/ plugin
fn/feedback.md          family feedback
fn/digest.md            session feedback digestion

ref/partition.md        the partition-major layout grammar · a REFERENCE, not a verb:
                        fn/ holds procedures someone runs; a grammar is consulted
```

The old stage specialists under `_old/` are compatibility readers during migration and are not the target architecture.
