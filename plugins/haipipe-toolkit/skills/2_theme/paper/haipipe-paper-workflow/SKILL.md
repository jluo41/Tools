---
name: haipipe-paper-workflow
description: >-
  The Paper Runs layer: bounded Run Specs, native Run receipts, dependencies,
  and checkable human gates by level: G0-G2 at the paper Board, G3-G5 in each
  version; one run card per button of each level's Spaces. Use
  when asking where a paper is, how its research plan connects to execution,
  whether work may be released, or what may be compiled next. Trigger: paper
  journey, paper-runs, workflow, Run routing, gate, /haipipe-paper-workflow.
metadata:
  version: "1.8.1"
  last_updated: "2026-10-09"
---

# /haipipe-paper-workflow · govern Paper Runs, test gates, and route next work

For a paper-journey question, enter through `haipipe-paper`; this file is the
cross-paper authority. It says which artifact owns each decision and when the
next artifact may be released. It does not write a Page, execute a Task or
Discovery, run a Page lifecycle, or judge manuscript prose.

## Paper Runs = a list of Runs

`paper-runs` is the Paper-scoped execution layer. This skill owns its Run Specs,
dependencies, native receipts, and G0–G5 controls. A PageType skill defines the
content and ownership contract that a Run operates on; it is not itself a Run.

A Workflow Definition lists bounded Run Specs and their dependency/Route graph.
A Workflow Runtime lists the actual owner-native Runs selected from those Specs.
Read [ref/run-workflow.md](ref/run-workflow.md) before planning, dispatch,
resume or status: it owns the Spec templates, identities, controls, Runtime
storage and completion rules. Page containers and G0–G5 gates do not become
Runs; Steps and Versions remain internal to a bounded Run.
[ref/run-cards.md](ref/run-cards.md) is the compact card per Run: the button and
prompt each level's Space shows in its Runs panel, keyed `<Level> › <Space>`
(Block · Job); a Section's buttons are the Page workflow's.

On the ladder (`haipipe-paper/ref/paper-ladder.md`) the Board holds the idea pool
and the tellings as studio topics with their Board Questions, the venues and the
related work; each version holds its Narrative, its Section, Abstract and letter
Tasks, its comments reports and its build. Discovery and Task remain external
work owners. A Story may have planned research, accepted evidence and released
Sections at the same time; status comes from their Runs and receipts.

Select the relevant Specs rather than executing a fixed sequence:

```text
Ideation native work / bounded idea judgments → I3 + G0 → Story work
Story claim/task/narrative judgments → G1 → native Supporting Runs
native accepted Results → G2 → affected Story rows / Page Evidence Runs
reviewed Section Narrative row → G3 → selected Page Structure/Writing/Evidence/Delivery Runs
current Section deliveries → manuscript compile Run → G4 readiness control
feedback batch → response work + affected owner Runs → G5 closure
```

Arrows include control predicates, not extra Run nodes. Accepted dependencies
can be reused. Section work may proceed as soon as its row is released, while
other research continues. A compile before the intended set is ready remains
DRAFT. A full Page controller pass is a Workflow Runtime, not a Page Run.

The former `workflow-phases/` path was only a compatibility address for the
four Paper PageType skills; those skills now sit beside the other Paper
entrypoints. P0–P4 labels are historical controller metadata and do not define
workflow units. Each Paper Workflow remains a list of owner-native Runs; Page
controller steps and compatibility labels do not add Run identities.

## 🧩 Ownership map

| Artifact | Owns | Does not own |
|---|---|---|
| Ideation (`studio/s01-ideation/` + Questions) | candidate projections, comparisons, venue-fit projection, projection of the final I3 handoff, and its reciprocal route to one Story | owning the I3 decision, minting another selection, evidence execution, binding desk rules, or manuscript prose |
| Venue (`venues/<venue>/`) | one target/category's typed and versioned external-desk contract | choosing the target or ranking Ideas |
| Story (a telling's studio topic, its Board Questions and reports) | seed, research questions, Discovery and Task Roadmaps, the selected telling | executing Runs, replacing work records, or storing manuscript Section prose |
| version face (`## Narrative`, `## Questions`) | one send's Section Narrative and compile order, its standing questions | changing the telling's research meaning |
| Discovery block | external literature/source inquiry and its Results | changing the Story's claim state |
| Task block | jobs, configurations, and execution Runs | silently releasing itself or rewriting Story rows |
| Run receipt | what actually ran, its provenance, checks, and Result | deciding how the paper should be told |
| Section Task | local outline, evidence bindings, prose, displays, page deliverable | changing the Story's identity or RQ text |
| Compile | generated manuscript projection and build manifest | becoming a source of wording or evidence |
| comments report (`reports/qNN_<kind>-<MMDD>/`) | Review Items, dispositions, checked response package | becoming a second home for revised prose |

A version face's `## Questions` opens with five standing questions every send answers (b16 s12), each a Question
│ Work │ Report row until its report exists: J1 what is the one-minute story · J2 why this venue · J3 which writing
principles it follows · J4 is it ready to send (G4) · J5 what changed since the last send (a revision only).

The Story explains the prospective paper and remains the authority for its
research meaning. A work receipt establishes what was done; §5 interprets what
the evidence supports. Accepted work can leave a proposition contradicted or
inconclusive. §3 may have an answered RQ even when its hoped-for claim fails.
Read work progress from the native owner, and preserve human decisions in the
Story's shared draft/ and workflow/ records. Do not reconstruct a release table
as the Story's Content outline.

## 🚪 Gates

Every gate is testable by reading named files and ends in a human receipt. Each
gate is signed at one level (b16 Q05), on the run card that names it:

```text
Board    G0 the admitted idea (Select idea) · G1 release of Task work (Task review) ·
         G2 the claim state and the answer (Claim review · Review the report)
version  G3 release of one Section (Narrative review · Release a Section) ·
         G4 submission readiness (Check) · G5 every response answered (Response)
```

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
    `paper_page.state: blocked`, preserve the Page path and each last
    honest surface revision, report the named gap, and create no surrogate
    Page, projection receipt, or selection receipt. A stale release surface is
    a Page publication issue, not a second I3 selection state; only apply a
    stricter G0 policy when the named Paper contract explicitly requires a
    released Ideation view.

G1  Story → Evidence/Execution
    The reviewed Story plan names Seed identity and RQs, §5 evidence basis and
    boundaries, §6 external inquiries, §7 study evidence, and §8 intended
    telling. A human
    explicitly releases the relevant work in its workflow record. Other
    unstarted research needs can remain planned. A draft or content row alone
    does not release work or promote the skill/outline version.

G2  Evidence/Execution → Story
    Each returning block has an accepted owner-native Result, limitations and
    a full path/id. Record that return without requiring every other released
    block to finish. Update §5 support and §3 answers as justified, then the
    affected §6/§7 needs and §8 narrative. Preserve null, contradictory and
    inconclusive outcomes. G2 is repeatable and does not grant a version promotion.

G3  Narrative → Section
    A person releases each Section row of the version face's `## Narrative` independently. The row names its
    reader question, ordered moves, claim role, entry/exit state, required
    evidence/displays, current target/category and Venue contract, transitions,
    cut rules and open risks. A proposed §8 row may precede its Section file;
    release binds the exact Section identity and human decision. No fixed
    percentage or automatic v1 promotion is required.

G4  Section → Compile
    Every Section admitted to a ready build has an approved outline, accepted
    evidence bindings, current delivery output, and Page CHECK closure. The
    assembler may run earlier, but the receipt must say DRAFT until the full
    intended set is closed; only a human may label the build ready. At the final
    G4 pass, apply the Paper submission-readiness reference: Section Pages own
    the `SUB-INTRO-*`, `SUB-METHOD-*`, `SUB-RESULT-*`, and `SUB-DISC-*` rows;
    Paper owns `SUB-COVER-*` and `SUB-WHOLE-*` after assembly. These rows reuse
    the shared four-axis rubric and do not add a Workflow unit or numeric score.

G5  Comments → next route
    Each Review Item of the comments report appears once, is routed once to the
    telling or the owning Section, and returns with a checked version or explicit
    disposition. The report freezes both the build that drew the comments (sent/)
    and the answering build (released/).
```

Gates do not run on timers. An agent may report that G2 or G3 is still open;
only the named human receipt can release or close it.

## 🗃 File-system projection

Layout: the ladder (the Story as `studio/` topics and `reports/` Questions, `jNN_v<MMDD>_<desk>/` per version) is current; the layout below is still read. Both are in `haipipe-paper/ref/paper-ladder.md`.

```text
Paper-<Slug>/                           Board: board.md · studio/ · reports/ · runs/ · venues/ · related/
└── jNN_v<MMDD>_<desk>/                 a version: its face (## Narrative · ## Questions), studio/ · reports/ · runs/
    ├── t00_abstract/ · t0N_<title>/    Section Tasks (Main), t2N_<title>/ (Appendix)
    ├── t3N_<title>/                    letters: t31_cover-letter · t32_response
    ├── reports/qNN_<kind>-<MMDD>/      a comments report
    └── delivery/                       generated Compile projection
```

Evidence execution remains outside the Paper folder:

```text
examples/<Project>/
├── discovery/<discovery-block>/      Discovery block + inquiry Results
└── work/<task-block>/                 Task block + jobs + Run receipts
```

The Story states research questions, bounded evidence interpretations and
prospective plans, with concise source links. Detailed execution and raw
evidence remain with the owners. A
Section's Page workflow still uses the common Evidence graph:
`Supporting Run → Local Input → Local Run → typed Result`.

### Paper Run naming

Load [`../haipipe-paper/ref/run-naming.md`](../haipipe-paper/ref/run-naming.md).
New Page work uses the shared Page Run names (`run-<kind>-<slug>`);
Paper judgment Runs are `run-paper-<judgment>-<slug>`; external Supporting
Runs retain their native identity. Paper judgment and compile/response profiles
are declared in the Run Spec reference. Older short names are retired.
A comments batch is a report, `reports/qNN_<kind>-<MMDD>/`, never a Run family.

## 🧾 Receipts and work status

The existing Story `draft/records/` log and shared `workflow/` receipts may record
G0, G1, G2 interpretations and G3 Section releases. The Paper-side G0 record,
when present, is only a validation/projection pointer to the final Ideation
handoff and sole I3 selection receipt; it does not repeat the I3 verdict,
target, or selection. These are authoring/execution records, not additional
Story Content divisions. The
Section Page records its own Page lifecycle and CHECK. Compile writes its
build manifest and render receipt. The comments report records G5 and the frozen build
paths and `built` times. The Paper-side G3 release is not a substitute for Page release or
CHECK; G4 may consume a Section only after the current Page release/CHECK
contract is satisfied. There is no separate child control-page receipt store.

Read the Runtime and exact native receipts for status. List each current
bounded goal, owner, accepted Result/version and remaining dependency or gate.
Show planned, managed and reused work distinctly. Report DRAFT/ready from the
build manifest; report response coverage from the comments report's Review Items. A status read
neither allocates a Run nor asks for decisions already recorded.

## 🧭 Current boundary

The current telling (its studio topic and Board Questions) is the paper-level
prospective blueprint, and each version face's `## Narrative` is how that send
tells it; Discovery and Task remain external work owners, the Section Task remains
the manuscript owner, Compile remains a projection, and the comments report
remains the feedback owner. Current Paper routing does
not resolve retired child Page names or hidden compatibility paths.

## ✅ Completion checks

- The Workflow names concrete Run Specs and their routes; the Runtime indexes
  actual native Runs once, with their receipts and reuse/managed status.
- Each selected idea has one Story blueprint whose Content follows the Story contract.
- Every Story admitted through G0 traces its target/category and Venue contract
  to the final handoff and sole I3 selection receipt, and binds back to them.
- The I3 semantic owner records the intended target decision; the Paper
  Ideation projects it, G0 validates it, and Story confirms it as the
  operational target and owns any later human-approved rebind.
- Page Shape approval, Page CHECK acceptance, and the I3 selection receipt are
  distinct decisions; the Paper workflow creates no second selection receipt.
- When `paper_page.state: blocked`, the Page path and each last honest
  surface revision remain visible; no surrogate Page, local Ideation Run, or
  fake projection receipt is made.
- Every central evidence gap has a substantive §6/§7 research need or an
  explicit scope decision; operations do not displace that explanation.
- Story CHECK evaluates the blueprint's clarity and coverage, not completion
  of its planned research. Story skill and new outlines remain v0.x pending
  the user's explicit authorization for each promotion.
- Every landed receipt points back to a Story row without copying its result.
- Every Section row is independently releasable and uses the shared Page Workflow.
- Compile reads the version face's machine-readable section order and Section-owned
  delivery fragments; it never reads a retired child page.
- Static validation and a fresh-context field test pass after this skill edit.
