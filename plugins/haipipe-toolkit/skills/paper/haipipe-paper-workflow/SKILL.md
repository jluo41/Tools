---
name: haipipe-paper-workflow
description: >-
  The paper-level journey: Ideation → Story → Evidence/Execution → Section →
  Compile → Round, with checkable human gates. Use when asking where a paper
  is, what the Story controls, whether work may be released, or what may be
  compiled next. Trigger: paper journey, workflow, phase gate,
  /haipipe-paper-workflow.
metadata:
  version: "1.0.0"
  last_updated: "2026-09-07"
---

# /haipipe-paper-workflow · read the journey, test the gate, mint the next work

For a paper-journey question, enter through `haipipe-paper`; this file is the
cross-paper authority. It says which artifact owns each decision and when the
next artifact may be released. It does not write a Page, execute a Task or
Discovery, run a Page lifecycle, or judge manuscript prose.

## 🔤 Two meanings of workflow

A **journey phase** is one position in the paper journey below. A **Page phase**
is one step of the shared Page lifecycle:

```text
Page lifecycle:   00 CONTEXT → 01 OUTLINE → 02 EVIDENCE → 03 CONTENT → 04 CHECK
Paper journey:    P0 Ideation → P1 Story → P2 Evidence/Execution →
                  P3 Section → Compile → P4 Round
```

`P2 Evidence/Execution` is a work lane, not a Paper Page Type. Discovery
blocks, Task blocks, and Runs keep their own native contracts; the Story page
records their assignment, state, receipt, and effect on the paper. There is no
active Paper Roadmap Page and no active Paper Narrative Page.

## 🗺 Active paper journey

```text
position                    authority / home                 produces
──────────────────────────────────────────────────────────────────────────────
P0 Ideation                 Story00-ideation in A1-Story     ranked candidate
                                                              directions and a
                                                              human-selected Story
P1 Story                    Story-<letter> in A1-Story       one paper's control
                                                              center: Seed + RQ +
                                                              evidence/work board +
                                                              section/compile map
P2 Evidence / Execution     external Discovery blocks,        released and landed
                            Task blocks, and Run receipts     evidence; no Paper
                                                              phase page is minted
P3 Section                  Ba/Bb Section Pages               one checked manuscript
                                                              or appendix unit per row
Compile                     haipipe-paper-assemble             generated delivery
                                                              projection; DRAFT or
                                                              SUBMISSION-READY
P4 Round                    Bc Round Pages                     frozen feedback cycle,
                                                              response, and next route
```

The live shape is deliberately overlapping:

```text
Idea pool ──G0──▶ Story control ──G1──▶ Discovery/Task/Run work
                         ▲                       │
                         └──────G2 receipts─────┘
                                  │ G3, per Section row
                                  ▼
                           Section Page 00–04
                                  │
                     Compile anytime; G4 for ready status
                                  │
                                  ▼
                              Round ──▶ Story or Section
```

The former “run to 70%” is a useful human readiness signal, not a global
arithmetic gate. A person may release a Section as soon as that row has a
stable reader question, claim/evidence bindings, and a workable outline;
other Discovery/Task/Run work may continue in parallel. A compile made before
all intended Sections are CHECK-closed is explicitly a DRAFT.

## 🧩 Ownership map

| Artifact | Owns | Does not own |
|---|---|---|
| Ideation Page | candidate directions, comparisons, handoff to one Story | evidence execution or manuscript prose |
| Story Page | Seed, RQs, E-rows, Discovery/Task/Run assignments, section rows, compile order | executing Runs or storing section prose |
| Discovery block | external literature/source inquiry and its Results | changing the Story's claim state |
| Task block | jobs, configurations, and execution Runs | silently releasing itself or rewriting Story rows |
| Run receipt | what actually ran, its provenance, QA, and Result | deciding how the paper should be told |
| Section Page | local outline, evidence bindings, prose, displays, page deliverable | changing the Story's identity or RQ text |
| Compile | generated manuscript projection and build manifest | becoming a source of wording or evidence |
| Round Page | feedback ledger, dispositions, checked response package | becoming a second home for revised prose |

The Story is the control center. It links outward to work and Sections, then
receives receipts back. A link is not a Result: a Story row may become
`✅ answered` only after the named Discovery/Task/Run receipt is accepted and a
person records the settlement.

## 🚪 Gates

Every gate is testable by reading named files and ends in a human receipt.

```text
G0  Ideation → Story
    The selected idea has claim-level novelty/feasibility bounds, a pilot or
    explicit waiver, a human PROCEED decision, and a reciprocal link between
    Story00-ideation and Story-<letter>.

G1  Story → Evidence/Execution
    Story has an approved outline containing the Seed identity, stable RQ
    text, one E-row per proposition/RQ, typed Discovery/Task/Run work rows for
    open debts, and visible Section placeholders. A human releases the work.

G2  Evidence/Execution → Story
    Every released block has an owner-native Run/Discovery receipt, a
    done-when/acceptance reading, and a full path or id. The Story updates the
    work state, RQ state, and E-row status; unsupported claims stay open.
    This is a repeatable settle loop, not an automatic phase advance.

G3  Story → Section
    A person releases each Section row independently. The row names its
    reader question, claim role, entry/exit state, required evidence/display
    ids, target desk if any, and open risks. No fixed percentage is required.

G4  Section → Compile
    Every Section admitted to a ready build has an approved outline, accepted
    evidence bindings, current delivery output, and Page CHECK closure. The
    assembler may run earlier, but the receipt must say DRAFT until the full
    intended set is closed; only a human may label the build ready.

G5  Round → next route
    Each concern in the feedback batch appears once, is routed once to the
    Story or owning Section, and returns with a checked version or explicit
    disposition. The Round freezes both the build that drew feedback and the
    answering build.
```

Gates do not run on timers. An agent may report that G2 or G3 is still open;
only the named human receipt can release or close it.

## 🗃 File-system projection

```text
Paper-<Slug>/
├── board.md
├── A1-Story/
│   ├── Story00-ideation/
│   └── Story-A/
│       ├── Story-A.md                 Story control center
│       ├── outline/                    Page 00–04 records
│       └── studio/                     optional Story-local presentation lanes
├── Ba-<desk>-Main/                     Section Pages
├── Bb-<desk>-Appendix/                 Section Pages
├── Bc-<desk>-Round/                    Round Pages
└── delivery/                           generated Compile projection
```

Evidence execution remains outside the Paper folder:

```text
examples/<Project>/
├── discoveries/<discovery-block>/      Discovery block + inquiry Results
└── tasks/<task-block>/                 Task block + jobs + Run receipts
```

The Story stores pointers and status, not copied evidence tables or raw PHI. A
Section's Page workflow still uses the common Evidence graph:
`Supporting Run → Local Input → Local Run → typed Result`.

## 🧾 Receipts and phase reading

The Story Log records G0, G1, G2 settlements, and G3 Section releases. The
Section Page records its own Page lifecycle and CHECK. Compile writes its
build manifest and render receipt. The Round records G5 and the frozen build hashes. No
separate Roadmap or Narrative receipt store exists.

The current position is read, not guessed from a folder name:

- before G0: P0 Ideation;
- after G0 but before work release: P1 Story;
- while released work lacks settled receipts: P2 Evidence/Execution;
- once individual rows are released: P3 Section may run in parallel;
- after a build: read its DRAFT/ready receipt, not a phase number;
- after feedback arrives: P4 Round, with each concern routed back to Story or
  a Section.

## 🧳 Retired phase machinery

The following names are removed from the active Paper router on 2026-09-07:

```text
haipipe-paper-roadmap       → paper/_old/retired-workflow-phases-260907/
haipipe-paper-narrative     → paper/_old/retired-workflow-phases-260907/
Story-A-roadmap             → paper instance _archive/retired-workflow-pages-260907/
Story-A-narrative-<desk>    → paper instance _archive/retired-workflow-pages-260907/
```

They are preserved as migration history, never loaded as current authority.
“Narrative” may still occur as an ordinary writing concept or in frozen
historical/venue material; it is no longer a Paper Page Type or a journey
phase. “Roadmap” may occur in venue prose as a reader-facing organization
paragraph; it is no longer a Paper control page.

## ✅ Completion checks

- The active journey names only Ideation, Story, Evidence/Execution, Section,
  Compile, and Round.
- Story-A is the only active Paper control page after Ideation.
- Every open RQ/E-row has a typed Discovery or Task/Run work row, or an
  explicit human waiver.
- Every landed receipt points back to a Story row without copying its result.
- Every Section row is independently releasable and runs Page 00–04.
- Compile reads Story's machine-readable section order and Section-owned
  delivery fragments; it never reads a retired child page.
- Static validation and a fresh-context field test pass after this skill edit.
