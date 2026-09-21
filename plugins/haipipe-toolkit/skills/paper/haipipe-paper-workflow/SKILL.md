---
name: haipipe-paper-workflow
description: >-
  The Paper Workflow: bounded Run Specs, native Run receipts, dependencies,
  and checkable human gates across Ideation, Story, Sections and delivery. Use when asking where a paper
  is, how its research plan connects to execution, whether work may be released, or what may be
  compiled next. Trigger: paper journey, workflow, Run routing, gate,
  /haipipe-paper-workflow.
metadata:
  version: "1.3.1"
  last_updated: "2026-09-20"
---

# /haipipe-paper-workflow · read the journey, test the gate, mint the next work

For a paper-journey question, enter through `haipipe-paper`; this file is the
cross-paper authority. It says which artifact owns each decision and when the
next artifact may be released. It does not write a Page, execute a Task or
Discovery, run a Page lifecycle, or judge manuscript prose.

## Workflow = a list of Runs

A Workflow Definition lists bounded Run Specs and their dependency/Route graph.
A Workflow Runtime lists the actual owner-native Runs selected from those Specs.
Read [ref/run-workflow.md](ref/run-workflow.md) before planning, dispatch,
resume or status: it owns the Spec templates, identities, controls, Runtime
storage and completion rules. Page containers and G0–G5 gates do not become
Runs; Steps and Versions remain internal to a bounded Run.

Paper Pages hold the idea portfolio, prospective Story, manuscript Sections,
Venue reference and feedback Round. Discovery and Task remain external work
owners. A Story may have planned research, accepted evidence and released
Sections at the same time; status comes from their Runs and receipts.

Select the relevant Specs rather than executing a fixed sequence:

```text
Ideation native work / bounded idea judgments → I3 + G0 → Story work
Story claim/obligation/narrative judgments → G1 → native Supporting Runs
native accepted Results → G2 → affected Story rows / Page Evidence Runs
reviewed C8 row → G3 → selected Page Structure/Writing/Evidence/Delivery Runs
current Section deliveries → manuscript compile Run → G4 readiness control
feedback batch → response work + affected owner Runs → G5 closure
```

Arrows include control predicates, not extra Run nodes. Accepted dependencies
can be reused. Section work may proceed as soon as its row is released, while
other research continues. A compile before the intended set is ready remains
DRAFT. A full Page controller pass is a Workflow Runtime, not an RP Run.

The physical `workflow-phases/` path is a retained compatibility address for
four Paper PageType skills. P0–P4 labels are historical controller metadata;
they do not define workflow units. Each Paper Workflow remains a list of
owner-native Runs; Page controller steps and compatibility paths do not add
Run identities.

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
    Read the Ideation sync's `paper_page` surfaces separately: a current
    working projection is evidence of the latest Ideation display, while release and
    delivery are current only with their own matching Page-owned receipts. G0
    validates the latest semantic handoff and reciprocal Story binding; it does
    not silently promote a stale Page release or delivery. If
    `paper_page.state: blocked`, preserve the canonical Page path and each last
    honest surface revision, report the named gap, and create no surrogate
    Page, projection receipt, or selection receipt. A stale release surface is
    a Page publication issue, not a second I3 selection state; only apply a
    stricter G0 policy when the named Paper contract explicitly requires a
    released Ideation view.

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

### Paper Run naming

Load [`../haipipe-paper/ref/run-naming.md`](../haipipe-paper/ref/run-naming.md).
New Page work uses typed RP, RE and RD identities from the shared Page owner;
external Supporting Runs retain their native identity. Paper judgment and
compile/response profiles are declared in the Run Spec reference. Existing
`pm-/pa-/pr-`, compact `rp00/rpNN`, and `pj...` receipts stay readable without
renumbering and are not new allocation grammars. `RD<NN>` names a Round Page.

## 🧾 Receipts and work status

The existing Story `outline/` log and shared `workflow/` receipts may record
G0, G1, G2 interpretations and G3 Section releases. The Paper-side G0 record,
when present, is only a validation/projection pointer to the final Ideation
handoff and sole I3 selection receipt; it does not repeat the I3 verdict,
target, or selection. These are authoring/execution records, not additional
Story Content divisions. The
Section Page records its own Page lifecycle and CHECK. Compile writes its
build manifest and render receipt. The Round records G5 and the frozen build
hashes. The Paper-side G3 release is not a substitute for Page release or
CHECK; G4 may consume a Section only after the current Page release/CHECK
contract is satisfied. There is no separate child control-page receipt store.

Read the Runtime and exact native receipts for status. List each current
bounded goal, owner, accepted Result/version and remaining dependency or gate.
Show planned, managed and reused work distinctly. Report DRAFT/ready from the
build manifest; report response coverage from the Round ledger. A status read
neither allocates a Run nor asks for decisions already recorded.

## 🧭 Current boundary

The Story Page is the sole paper-level prospective blueprint. Its C1–C8
content is the authority for the prospective paper; Discovery and Task remain
external work owners, Section remains the manuscript owner, Compile remains a
projection, and Round remains the feedback owner. Current Paper routing does
not resolve retired child Page names or hidden compatibility paths.

## ✅ Completion checks

- The Workflow names concrete Run Specs and their routes; the Runtime indexes
  actual native Runs once, with their receipts and reuse/managed status.
- Each selected idea has one Story blueprint whose Content follows the Story contract.
- Every Story admitted through G0 traces its target/category and Venue contract
  to the final handoff and sole I3 selection receipt, and binds back to them.
- The I3 semantic owner records the intended target decision; the Paper
  Ideation Page projects it, G0 validates it, and Story confirms it as the
  operational target and owns any later human-approved rebind.
- Page Shape approval, Page CHECK acceptance, and the I3 selection receipt are
  distinct decisions; the Paper workflow creates no second selection receipt.
- When `paper_page.state: blocked`, the canonical Page path and each last honest
  surface revision remain visible; no surrogate Page, local Ideation Run, or
  fake projection receipt is made.
- Every central evidence gap has a substantive C6/C7 research need or an
  explicit scope decision; operations do not displace that explanation.
- Story CHECK evaluates the blueprint's clarity and coverage, not completion
  of its planned research. Story skill and new outlines remain v0.x pending
  the user's explicit authorization for each promotion.
- Every landed receipt points back to a Story row without copying its result.
- Every Section row is independently releasable and uses the shared Page Workflow.
- Compile reads Story's machine-readable section order and Section-owned
  delivery fragments; it never reads a retired child page.
- Static validation and a fresh-context field test pass after this skill edit.
