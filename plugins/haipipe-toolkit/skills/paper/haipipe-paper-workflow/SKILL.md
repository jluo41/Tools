---
name: haipipe-paper-workflow
description: >-
  The paper-level journey: Ideation → Story → Evidence/Execution → Section →
  Compile → Round, with checkable human gates. Use when asking where a paper
  is, how its research plan connects to execution, whether work may be released, or what may be
  compiled next. Trigger: paper journey, workflow, phase gate,
  /haipipe-paper-workflow.
metadata:
  version: "1.1.7"
  last_updated: "2026-09-08"
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
blocks, Task blocks, and Runs keep their own native contracts. The Story
Content explains the paper's knowledge needs, evidence basis, and intended
argument through C1–C8. Assignments, releases, state and receipts remain in
the shared workflow records and native owners. Seed, Discovery Roadmap, Task
Roadmap, and Section Narrative are substantive Story content; they do not
require separate Paper Pages. `haipipe-paper-story` alone owns that shape.

## 🗺 Active paper journey

```text
position                    authority / home                 produces
──────────────────────────────────────────────────────────────────────────────
P0 Ideation                 Story00-ideation in A1-Story     ranked candidate
                                                              directions, venue fit,
                                                              and an I3-authorized
                                                              Story + target projection
P1 Story                    Story<Letter>-<desk>-<idea-slug> in A1-Story       prospective paper:
                                                              Seed + RQs + evidence
                                                              basis + Discovery/Task
                                                              Roadmaps + Section Narrative
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
Idea pool ──G0──▶ Story blueprint ──G1──▶ Discovery/Task/Run work
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
| Ideation Page | candidate projections, comparisons, venue-fit projection, projection of the final I3 handoff, and its reciprocal route to one Story | owning the I3 decision, minting another selection, evidence execution, binding desk rules, or manuscript prose |
| Venue Page | one target/category's typed and versioned external-desk contract | choosing the target or ranking Ideas |
| Story Page | Seed C1–C5, Discovery Roadmap C6, Task Roadmap C7, Section Narrative C8, selected telling and compile projection | executing Runs, replacing work records, or storing manuscript Section prose |
| Discovery block | external literature/source inquiry and its Results | changing the Story's claim state |
| Task block | jobs, configurations, and execution Runs | silently releasing itself or rewriting Story rows |
| Run receipt | what actually ran, its provenance, checks, and Result | deciding how the paper should be told |
| Section Page | local outline, evidence bindings, prose, displays, page deliverable | changing the Story's identity or RQ text |
| Compile | generated manuscript projection and build manifest | becoming a source of wording or evidence |
| Round Page | feedback ledger, dispositions, checked response package | becoming a second home for revised prose |

The Story explains the prospective paper and remains the authority for its
research meaning. A work receipt establishes what was done; C5 interprets what
the evidence supports. Accepted work can leave a proposition contradicted or
inconclusive. C3 may have an answered RQ even when its hoped-for claim fails.
Read work progress from the native owner, and preserve human decisions in the
Story's shared outline/workflow records. Do not reconstruct a release ledger
as the Story's Content outline.

## 🚪 Gates

Every gate is testable by reading named files and ends in a human receipt.

```text
G0  Ideation → Story
    Read the final handoff at handoff/paper-ideation.yaml. It must point to
    the latest projection/paper-ideation-sync.yaml, the sole I3 selection
    receipt at workflow/selection.yaml, the selected Idea, its intended
    target/category, and the exact Story path. Validate the claim-level
    novelty/feasibility bounds, pilot or explicit waiver, complete deep fit
    against the current Venue contract, and the human PROCEED or
    risk-accepted PROCEED WITH CAUTION recorded by I3.
    Validate the reciprocal binding from Story<Letter>-<desk>-<idea-slug>
    back to Story00-ideation, the final handoff, the sole I3 receipt, and the
    named Venue contract. A Paper-side G0 record is validation/projection only:
    it points to those records and never creates, requests, or overwrites a
    second selection receipt. Page Shape approval and Page CHECK acceptance
    remain separate Page decisions and cannot substitute for I3 or G0.
    If `paper_page.state: blocked`, preserve the canonical Page path and last
    actual revision, report the named gap, and create no surrogate Page,
    projection receipt, or selection receipt.

G1  Story → Evidence/Execution
    The reviewed Story plan names Seed identity and RQs, C5 evidence basis and
    boundaries, C6 external inquiries, C7 study evidence, and C8 intended
    telling. A human
    explicitly releases the relevant work in its workflow record. Other
    unstarted research needs can remain planned. A draft or content row alone
    does not release work or promote the skill/outline version.

G2  Evidence/Execution → Story
    Each returning block has an accepted owner-native Result, limitations and
    a full path/id. Record that return without requiring every other released
    block to finish. Update C5 support and C3 answers as justified, then the
    affected C6/C7 needs and C8 narrative. Preserve null, contradictory and
    inconclusive outcomes. G2 is repeatable and does not grant a version promotion.

G3  Story → Section
    A person releases each Section row independently. The row names its
    reader question, ordered moves, claim role, entry/exit state, required
    evidence/displays, current target/category and Venue contract, transitions,
    cut rules and open risks. A proposed C8 row may precede its Section file;
    release binds the exact Section identity and human decision. No fixed
    percentage or automatic v1 promotion is required.

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
│   └── StoryA-misq-phytrait-discretion/
│       ├── StoryA-misq-phytrait-discretion.md                 Story prospective blueprint
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

The Story states research questions, bounded evidence interpretations and
prospective plans, with concise source links. Detailed execution and raw
evidence remain with the owners. A
Section's Page workflow still uses the common Evidence graph:
`Supporting Run → Local Input → Local Run → typed Result`.

### 🪪 Paper Run naming

The Paper-specific Run dialect is defined in
[`../haipipe-paper/ref/run-naming.md`](../haipipe-paper/ref/run-naming.md).
Use `pm-<page>-<target>-rNN`, `pa-<page>-<target>-rNN`, or
`pr-<round>-<target>-rNN` for new Paper-local Evidence/Display Runs. The
Section's Page-local Paragraph Writing Run follows `haipipe-page-content`:
`rNN_page-writing_cNN-pNN.md`; its owning semantic Page supplies the Main or
Appendix meaning. `Ba`/`Bb`/`Bc` are shelf tokens, and `RD<NN>` is the Round
Page token, not a Run id. Existing `pjNNtNNrNN` files are read-only historical
Runs and are never bulk-renamed.

## 🧾 Receipts and phase reading

The existing Story `outline/` log and shared `workflow/` receipts may record
G0, G1, G2 interpretations and G3 Section releases. The Paper-side G0 record,
when present, is only a validation/projection pointer to the final Ideation
handoff and sole I3 selection receipt; it does not repeat the I3 verdict,
target, or selection. These are authoring/execution records, not additional
Story Content divisions. The
Section Page records its own Page lifecycle and CHECK. Compile writes its
build manifest and render receipt. The Round records G5 and the frozen build
hashes. There is no separate child control-page receipt store.

The current position is read, not guessed from a folder name:

- before G0: P0 Ideation;
- after G0 but before work release: P1 Story;
- while released work lacks settled receipts: P2 Evidence/Execution;
- once individual rows are released: P3 Section may run in parallel;
- after a build: read its DRAFT/ready receipt, not a phase number;
- after feedback arrives: P4 Round, with each concern routed back to Story or
  a Section.

## 🧭 Current boundary

The Story Page is the sole paper-level prospective blueprint. Its C1–C8
content is the authority for the prospective paper; Discovery and Task remain
external work owners, Section remains the manuscript owner, Compile remains a
projection, and Round remains the feedback owner. Current Paper routing does
not resolve retired child Page names or hidden compatibility paths.

## ✅ Completion checks

- The active journey names only Ideation, Story, Evidence/Execution, Section,
  Compile, and Round.
- Each selected idea has one Story blueprint whose Content follows the Story contract.
- Every Story admitted through G0 traces its target/category and Venue contract
  to the final handoff and sole I3 selection receipt, and binds back to them.
- The I3 semantic owner records the intended target decision; the Paper
  Ideation Page projects it, G0 validates it, and Story confirms it as the
  operational target and owns any later human-approved rebind.
- Page Shape approval, Page CHECK acceptance, and the I3 selection receipt are
  distinct decisions; the Paper workflow creates no second selection receipt.
- When `paper_page.state: blocked`, the canonical Page path and last actual
  revision remain visible and no surrogate Page or projection receipt is made.
- Every central evidence gap has a substantive C6/C7 research need or an
  explicit scope decision; operations do not displace that explanation.
- Story CHECK evaluates the blueprint's clarity and coverage, not completion
  of its planned research. Story skill and new outlines remain v0.x pending
  the user's explicit authorization for each promotion.
- Every landed receipt points back to a Story row without copying its result.
- Every Section row is independently releasable and runs Page 00–04.
- Compile reads Story's machine-readable section order and Section-owned
  delivery fragments; it never reads a retired child page.
- Static validation and a fresh-context field test pass after this skill edit.
