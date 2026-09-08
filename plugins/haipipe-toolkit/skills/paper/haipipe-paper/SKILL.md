---
name: haipipe-paper
description: >-
  The one door for planning, writing, and revising a paper as a graph of Board
  Pages. Routes Ideation, Story, Section and Round Pages through the shared
  Page lifecycle; Discovery and Task owners execute the external work lane.
  Use for paper setup, status, drafting, complete-paper assembly, compiling,
  or review rounds.
metadata:
  version: "1.0.2"
  last_updated: "2026-09-08"
  summary: "Story absorbs Paper planning; Discovery/Task/Run execute outside the Paper Page graph; Compile remains a verb."
---

# /haipipe-paper · compose a paper from evidence-bearing Pages

`haipipe-paper` is the Paper-family router. It does not implement the Page
workflow and it does not replace the specialist Page Type contracts.

Use two orders for two different jobs. First route the family request:

```text
haipipe-paper
  → haipipe-paper-workflow, when the question is the journey or a gate
  → resolve the concrete Page and its Page Type
```

Once one concrete Page RUN begins, use the Page router's canonical order:

```text
haipipe-page
  → haipipe-page-workflow
  → current Page phase
  → haipipe-paper-workflow (Folder-owning workflow)
  → the exact Page Type: haipipe-paper-ideation · haipipe-paper-story ·
    haipipe-paper-section · haipipe-paper-round, or haipipe-paper-venue
  → phase references / the Story's Section row and style policy
  → haipipe-run + selected workers, only where Runs exist
  → paper/haipipe-paper/ref/run-naming.md when a Paper-local Run is planned
```

For CONTEXT, OUTLINE, and EVIDENCE, the exact material contracts are
`haipipe-plugin-outline/ref/...` files. The Page surface already installs the
shared Outline presenter; it is not a final execution dependency.

`haipipe-paper-assemble` is a separate complete-paper verb after routing; it is
not inserted into a Page phase.

## 🧭 The journey (JL 260828 · rebuilt 260907)

`haipipe-paper-workflow` owns the gates; this figure is the reading order.
Every position is named by its authority page (the naming law). The Story is
the sole paper-level prospective blueprint.

```text
P0 Ideation (ideate)       💭 Story00-ideation · the repo is minted with this page ·
│                             ideas cheap and disposable
│                             gate G0: novelty per claim + pilot + human PROCEED
P1 Story (plan)            🌱 Story<Letter>-<desk>-<idea-slug> · one paper's prospective blueprint
│                             Seed C1–C5 · Discovery Roadmap C6 · Task Roadmap C7
│                             Section Narrative C8 · contract: haipipe-paper-story
│                             gate G1: a reviewed research plan and explicit
│                             release for the relevant Discovery/Task work
P2 Evidence/Execution      🧰 a WORK LANE, not a page · Discovery blocks, Task
│                             blocks, Runs in examples/<Project>/ · receipts land
│                             back on the Story
│  ↺ P1↔P2 = the settle loop  gate G2: each returning block has an owner-native
│                             receipt · the Story updates RQ/E-row state
P3 Section (realize)       📄 one page per C8 Section Narrative row · a person
│                             releases each row independently (gate G3) · sign-off
│                             = per-unit CHECK ✅
│  Compile                    assemble — a verb, not a phase · runs anytime from the
│                             Story's compile-order block · gate G4 marks the build
│                             SUBMISSION-READY vs DRAFT · the upload is a human act
P4 Round (respond)         🔁 routes each concern once → Story (C5 support,
                              C6/C7 research needs, C8 narrative) / Section · gate G5: every concern ledgered and
                              routed exactly once · a person approves the receipt

   📚 venue = library, never a phase: the QBv bank is consulted when a §8 row
      names its target, and a missing desk gets its bank page minted as a sub-step.
```

The five Page Types, one line each:

- **Ideation** is one research direction's ideas, ranked in the source
  reports' own structure (IDEA_REPORT / Novelty Check Report fields), the
  story group's page zero (`Story00-ideation`), minted with the repo before any
  Story exists; eliminated ideas stay forever; the winning idea's `went to`
  names this board's Story (or, rarely, a sibling repo's).
  `haipipe-paper-ideation` (`paper/workflow-phases/`).
- **Story** is one paper's prospective blueprint, `Story<Letter>-<desk>-<idea-slug>.md`.
  `haipipe-paper-story` owns its eight Content divisions: Seed C1–C5,
  Discovery Roadmap C6, Task Roadmap C7, and Section Narrative C8. It explains
  the question, contribution, present evidence, needed knowledge and study
  outputs, and the whole-paper argument. Operational records live in the
  shared workflow and work owners. The Seed's identity survives retargeting;
  evidence and plans can evolve with substantive reasons. The Story binds
  its Ideation origin. This contract remains a v0.x design draft; this
  router's own version does not promote it.
- **Venue** is one evidence-backed desk record in the shared bank — a library
  asset outside the journey; the decision to target it lives on the Story's §8
  rows.
- **Section** is one reader-ordered manuscript or appendix unit executing one
  Story C8 Section Narrative row; the page owns the words and the tracking.
- **Round** is one bounded feedback batch parented to the Story and the build
  it reviewed. It routes every concern exactly once — to C5 for changed support,
  C6/C7 for research needs, C8 for retelling, or a Section for local rework
  — and closes with a checked response receipt.
`/haipipe-paper status [paper] [section|evidence|citation|display]` regenerates
the same rollup a Dash Page used to hold, as an optional drill-down on the
existing status command instead of a Page Type of its own: it reports every unit,
obligation, and gap in one family and never decides anything, so it earns no
lifecycle, no CHECK gate, and no `page-type:` key.

Retargeting keeps the Story's Seed divisions, binds the target's SHARED Venue
Page (creating one in the venue bank only when the desk has none), and adds a
candidate telling within C8 Section Narrative. Only the selected telling
feeds the active compile-order block (see the Story integration reference). A Venue Page is consumer-neutral and refreshes on the
desk's clock, never a paper's. Retargeting does not rewrite the stable paper
identity merely to imitate a new desk. Closed Round Pages remain bound to the
Venue, the Story version, and the build they actually reviewed.

## 🃏 Evidence belongs to the Page that uses it

There is no View layer and there are no active Literature, Value, Citation,
Display, Probe, or PageX Page Types/plugins. Every Paper Page uses typed
Evidence Items and the same Supporting-to-local Run graph.

```text
<page-dir>/
├── <page>.md                  human-readable argument and bindings
├── outline/
│   ├── <stem>-context.md      Context Workspace projection
│   ├── <stem>-outline-vN.md   Bullet Workspace authority
│   ├── <stem>-evidence-items.md  authored item/Run graph
│   └── evidence/              Evidence Workspace material by VALUE/CITE/DISPLAY
├── runs/                      Page-local or Paper-local L4 Run Tickets
├── results/                   paired local Results/runtime receipts
└── delivery/                  generated Page-level TeX/PDF/DOCX when requested
```

`haipipe-plugin-outline` presents Context, Bullet, and Evidence Workspaces.
VALUE, CITE, and DISPLAY are Result types inside Evidence Workspace, not
separate plugins. Exact numbers and citation metadata live in accepted local
Results; the Page cites their `E<NN>-<TYPE>-<slug>` and full Run/Result ids.

Paper-local Evidence/Display Runs use the semantic lane-aware ids in
[`ref/run-naming.md`](ref/run-naming.md): `pm-…` for Main, `pa-…` for
Appendix, and `pr-…` for Round. Page-local Content Runs keep the shared
`rNN_page-division-writing_cNN` grammar. The former `pjNNtNNrNN` form remains
read-only history; Paper work never silently renames it.

One Page may own many DISPLAY items. One local DISPLAY Result may contain
several artifacts or panels, but it has one message, one frozen Local Input,
and one independent acceptance state. The root paper build may copy accepted
artifacts into its compiled deliverable; the local Result remains the evidence
authority.

### 🖼 Concept-first gate for visual DISPLAY Results

For a diagram, illustration, or PowerPoint-native figure whose layout or icon
language is still open, the paper workflow freezes the visual direction before
editable authoring:

```text
visual reference → composition brief → human ruling
                 → editable reconstruction → candidate review → promotion
```

The reference may be user-provided, an existing candidate, an Image Gen
concept, or a sketch. The composition brief records the panel structure,
relationships, must-keep icons or objects, label budget, palette, and avoid
list. A generated bitmap is a design reference, not a substitute for the
editable PPT/SVG source; final labels and any real counts are re-typeset from
the admitted evidence or caller-supplied context. When a user asks to reduce
text, preserve the existing iconography and object semantics unless removal is
explicitly requested. If the user asks to discuss first, do not replace the
accepted asset or Board page before the visual ruling is recorded. Numeric
tables and plots continue through the normal intake/spec path.

Evidence evolves through the shared Page loop:

```text
CONTEXT       collect, resolve, and freeze policy/requirements/source context
SHAPE         mark each promised point: prose · 📮 question · 🧮 value ·
              📚 citation · 🖼 display
SURVEY        specify each typed item's Supporting Runs, Local Input, and local Run
LAND · EMBED  complete the supporting/local Runs; fold accepted Results into the plan
WRITE         write only from the agreed outline and landed runs
              (revise: improve prose and bind row/display ids; COMPILE is folded here)
CHECK         judge the built version; only CHECK may close the Page
```

Do not hard-code a linear advance here. Load `haipipe-page-workflow`; its
receipts and authority tests decide whether the Page repeats, branches, holds,
or returns to an earlier phase.

## 🚪 Routing

Resolve the paper root and target Page before changing anything.

| User intent | Route |
|---|---|
| brainstorm, novelty-check, eliminate an idea, or send one to a Story | `haipipe-paper-ideation` |
| ask where a paper is in the journey, or test a gate | `haipipe-paper-workflow` |
| draft or review the whole paper, its research roadmaps or section narrative | `haipipe-paper-story` |
| release work, inspect execution progress, accept a receipt, or release a Section | `haipipe-paper-workflow` plus the exact Discovery/Task/Section owner; use Story for the resulting paper meaning |
| inspect or record a target venue | `haipipe-paper-venue` (library lane, not a phase) |
| write or revise one manuscript/appendix unit | `haipipe-paper-section` |
| triage or answer one feedback/review cycle | `haipipe-paper-round` |
| check paper or one family's status | `/haipipe-paper status` (command, not a Page Type) |
| run one Page through its lifecycle | `haipipe-page-workflow` |
| compile or export one Page | `haipipe-plugin-delivery`, using its LaTeX or Word lane |
| assemble the paper | `haipipe-paper-assemble` from the Section Pages' own `delivery/latex/` outputs and accepted bindings |
| respond to reviewers | a Round Page plus the affected Story rows and Sections |

### Paper verbs

```text
/haipipe-paper ideate <direction|idea-id> [phase]
/haipipe-paper enter [paper]
/haipipe-paper status [paper] [section|evidence|citation|display]
/haipipe-paper journey [paper]         read the journey position · test the gates ·
                                       never advances anything
/haipipe-paper story [paper] [phase]
/haipipe-paper venue <target> [phase]
/haipipe-paper section <section-id> [phase]
/haipipe-paper round <new|id>
/haipipe-paper assemble [paper]        runs anytime · a build made while gate G4
                                       fails is watermarked DRAFT in its receipt
```

Every `[phase]` above is a PAGE phase (CONTEXT…CHECK). The journey's
positions are never called by that word in a verb; `haipipe-paper-workflow`
carries the terminology law.

When the user names a concrete Page, prefer that Page over inferring a phase
from a broad verb. When a phase is omitted for an existing Page, inspect its
latest receipt and use the shared workflow's authority test.

## 📐 The Story connects study questions to the manuscript

`haipipe-paper-story` owns the Content shape and the read-through test. Routers
must load that contract rather than restating a competing outline. C8 explains
the claim system, argument arc, reader journey and detailed Section moves;
its table is a compact view of that narrative.

Each instantiated Section binds one current C8 row through `story-row:`.
A changed claim, purpose or transition reopens the affected Section; local prose
cannot redefine it. C5 records support and limits; C6/C7 describe how missing
knowledge or evidence will be obtained. Operational acceptance remains in the
workflow records.

The existing compile marker is a projection of the selected C8 telling. Read
`haipipe-paper-story/ref/integration.md` for the exact row, version and
single-target compiler interface. Planning a Section does not instantiate its
Page, authorize execution, or imply a v1 approval.

## 📂 Paper folder scaffold (JL 260823 · groups at the root and delivery/ JL 260907)

A new paper repo — created as a git submodule immediately — is one board whose
page groups sit directly at the paper root, plus one `delivery/` folder that
is a projection of the finished Section Pages. There is no `0-paperboard/`
wrapper and no hand-edited desk room. Board groups map onto the journey: P0
and P1 Story in `A1-Story/`; P3 Section and P4 Round use desk-specific groups:

```text
Paper-<Slug>/
├── board.md                    the board · paper-root: .
├── board/                      engine-generated HTML (build.py output)
├── A1-Story/
│   ├── Story00-ideation/       P0 · the idea pool · exactly one
│   └── StoryA-misq-phytrait-discretion/                P1 · one paper's prospective blueprint
│       └── StoryA-misq-phytrait-discretion.md          Seed · Discovery Roadmap · Task Roadmap ·
│                               Section Narrative + selected compile order
│   (a second surviving idea is Story-B/, same shape; no roadmap/narrative children)
├── Ba-<desk1>-Main/            P3 · first desk's named Main sections
├── Bb-<desk1>-Appendix/        P3 · its named Appendix sections
├── Bc-<desk1>-Round/           P4 · its RD<NN> rounds, one page per batch ·
│   └── RD<NN>-<event>-<date>/  each holds sent/ · feedback/ · released/ (the
│                               frozen PDF+DOCX that drew comments, what came
│                               back, the PDF+DOCX that answered them)
├── Bd-<desk2>-Main/ …          second desk continues at the next free letter
│                               (a foreign-desk round mints only its -Round)
├── delivery/                   GENERATED · never hand-edited
│   ├── paper-build.toml        reading order · venue profile · output names
│   ├── latex/                  master.tex + sections/ + appendices/ (the pages'
│   │                           <page>.tex fragments) + displays/ + reference.bib,
│   │                           all copied from the pages · the compiled paper PDF
│   └── word/                   .docx converted from latex/
└── README.md
```

**No `tasks/` here (JL 260828)**: a C7 evidence block's Task group lives in the
TASK LAYER's own home, `examples/<Project>/tasks/{G}{NN}_<name>/`, never inside
the paper repo. The symmetry is with discoveries — evidence layers are
consumer-neutral and a page binds them by path, so a task inside the paper
would make the paper both the consumer of its evidence and the executor of it.
C7 states the evidence need; `haipipe-task` owns reuse/extend/new matching,
project placement, job design and execution.

**The delivery law (JL 260907; replaces the room law of 260824)**: the words
live on the Section Pages. Each Section Page compiles its own
`delivery/latex/<page>-complete.tex` (with its `.bib` and `.pdf`) through the
page-level delivery plugin, and that PDF is the page's own deliverable; the
body fragment beside it, `delivery/latex/<page>.tex`, is what the paper
build `\input`s. The paper's `delivery/latex/` is built FROM those fragments,
in the Story's compile order (the C8 `haipipe:compile-order` projection): `master.tex` is generated, `sections/`
and `appendices/` are copies of the fragments, `displays/` holds copies of
accepted page-local DISPLAY floats and assets, and `reference.bib` is merged
from the pages' `outline/evidence/bibex/<page>.bib`. Generated delivery artifacts
are not hand-edited; `paper-build.toml` and the declared adapter remain maintained
inputs. A prose or evidence correction goes
back to the owning page and the folder is regenerated whole. `delivery/word/`
is converted from `delivery/latex/` and never edited either. On send, a copy
of the current build is frozen in the Round it opens (`RD<NN>/sent/`); on that
Round's close, the answering build is frozen in `RD<NN>/released/`
(`haipipe-paper-round`). Evidence
AUTHORITY never moves into `delivery/`: it holds copies, the pages hold the
Results. The milestone that admits a page into the build is per Section Page:
its outline table is approved, every display unit has its preview PDF, and its
own page PDF compiles. Old self-contained desk rooms (`<N>-<desk><year>/` with
`sections/*.tex` as source of record) are outside the current runtime and must
be migrated before current Paper commands are used.

**Group-name grammar (JL 260824; Section IDs re-ruled 260901)** — one `A` group
carries the per-paper journey: `A1-Story` holds `Story00-ideation` (the pool)
and one `Story<Letter>-<desk>-<idea-slug>` per surviving idea, the paper's prospective blueprint
(JL 260907: the letter is the stable Story identity);
`B` groups run in lowercase
letter order across the board, ONE LETTER PER GROUP (JL 260831 "Ba to be Main,
Bb to be Appendix, Bc to be Round"): the first desk takes `Ba-<desk>-Main` for
the named Main units, `Bb-<desk>-Appendix` for its named Appendix units, and
`Bc-<desk>-Round` for the `RD` pages; a second desk continues at the next free
letter (`Bd-<desk2>-Main`, …). Section Pages use full semantic IDs that carry the section index (JL 260908):
`S-<desk>-Main-<N>-<Title>` and `S-<desk>-Appendix-<L>-<Title>`, N and L from the
page H1; an unnumbered page keeps title only (`S-MISQ-Main-Abstract`). Thus a Round
routes to `S-MISQ-Main-5-Results`, not to an opaque `SM05`; the selected Story C8
compile-order block supplies reader order; `board.md` indexes the Pages. The
`<desk>` name keeps its own capitals (`Ba-MISQ-Main`); only
the group letter is lowercase.
Current boards use one group letter per family and do not add compatibility
groups or shadow Page names.
No old SD/SA/NA prefix reservation or collision table participates in current
routing. Review letters live inside their Round page's folder, never at the
repo root. Historical paper layouts are outside the current runtime. An
explicit migration must produce the current group grammar and pass the current
Page, Section, and delivery checks before a Paper command is used; the router
reads no compatibility alias, shadow Page, or fallback source.
`Paper-AgreeablePrescriptionDiscretion` is the first repo using the current single-Story
layout; its Story content must still be inspected against the Story draft
before assuming that it implements every draft requirement.

## 📦 Assembly and delivery

Paper assembly is a source-driven projection, governed by
`haipipe-paper-assemble`. It does not silently mine raw Task or Discovery
folders, and it does not use a previous Word file as a template or input.

```text
Board/Page authority                  Section Pages' own deliverables
boundary · claims · evidence         <page>/delivery/latex/<page>.tex (body)
acceptance · display bindings        + .bib · accepted display assets
             \                         /
              accepted bindings + delivery/paper-build.toml
                               ↓
             delivery/latex/ regenerated whole: master.tex ·
             sections/ · appendices/ · displays/ · reference.bib
                               ↓
             shared assembly engine + venue profile
                               ↓
       main DOCX/PDF · supplement · snapshots · manifest · CHECK result
```

The Page-local `delivery/word/` snapshot remains useful for a coauthor
reading one Section Page. It is not the complete-paper input. The complete
paper builder reads each Section Page's `delivery/latex/<page>.tex`
in the Story's compile order, regenerates `delivery/latex/` from them, and
converts `delivery/word/` from that. The pages own the wording; `delivery/`
is a projection and is never edited by hand.

The paper declares one `delivery/paper-build.toml` containing the page groups
and the Story page whose compile-order block orders them, the display and bibliography sources,
output names, and venue profile. The reusable engine owns parsing, document events, rendering,
manifests, and deterministic build checks; the paper contributes configuration and only a narrowly
scoped adapter for unusual constructs. See
`haipipe-paper-assemble/SKILL.md` for the full contract.

Assembly may run before G4. Such an output is a `DRAFT`; it becomes a
`SUBMISSION-READY` candidate only when the Section CHECK bindings, source
manifest, build-check result, and human decision required by the workflow all hold.
Generated DOCX/PDF/snapshots are derived artifacts and are overwritten by a
rebuild; corrections must return to the source Section/config.

## 🚦 Submission-readiness gate (G4 · before submission)

Use this gate after assembly and before labeling any PDF/DOCX
`SUBMISSION-READY`. Read [`ref/submission-readiness.md`](ref/submission-readiness.md)
and the target venue's current author instructions. A clean render is necessary
but never sufficient: the gate must close evidence, story, reporting, files, and
human approval together.

Run the gate in this order:

1. **Freeze evidence.** Name one primary estimand and one primary claim. Bind
   every number, interval, sample size, display, and consequential sentence to
   accepted evidence. Mark provisional, exploratory, unrecomputed, and
   unsupported items explicitly; do not promote them through polished prose.
2. **Check the story.** Confirm that the title, Key Points, abstract, lead
   Results paragraph, Discussion opening, and Conclusion make the same claim.
   Keep inherited methods or upstream features as enablers unless the paper's
   evidence supports a separate methodological claim. Keep distinct papers,
   diseases, estimands, and causal interpretations separate.
3. **Check reporting and displays.** Reconcile design labels, dates, eligibility,
   missingness, analytic N, uncertainty, clustering, multiplicity, ethics, and
   prespecified versus secondary analyses. Confirm that every table, figure,
   supplement item, legend, and checklist is final, cited, and rendered.
4. **Check submission files.** Apply the venue's current limits and required
   structure to the title page, abstract, Key Points, main text, references,
   tables, figures, supplement, cover letter, reporting checklist, and metadata.
   Fill authorship, funding, conflicts, data/code sharing, consent/IRB, and AI
   disclosure fields; never leave placeholders in a submission package.
5. **Run the final human pass.** Read the assembled document linearly for
   clinical clarity, claim strength, citation support, AI-like promotional
   language, unexplained abbreviations, repetition, and formatting. A person
   must approve the evidence scope and the final build before G4 closes.

The build remains `DRAFT` when any hard blocker is open, even if the document
compiles and passes visual checks. A human may explicitly waive a noncritical
item; the waiver belongs in the build receipt and does not waive venue rules,
unsupported claims, missing evidence, or required disclosures.

## 🧱 Current architecture boundary

The former S01–S10 stage contracts, stage resolver, S-page creator, S03/S04
topic-entry tooling, stage-specific craft, and their helper scripts are outside
the current Paper runtime. This door does not load them.

The current Paper graph has one Story prospective blueprint. Its C1–C5 Seed
content, C6 Discovery Roadmap, C7 Task Roadmap, and C8 Section Narrative remain
substantive Story content; the corresponding execution, Section, Compile, and
Round records stay with their native owners. The router reads no retired child
Page, compatibility alias, or fallback source.

## ✅ Completion checks

Before reporting Paper work complete:

Apply these checks to the requested operation. A discussion, draft Story
proposal, or planning handoff needs its semantic checks and explicit open
decisions; it does not start a Page RUN, release a Section, require rendered
deliverables, or close G4. The Page, evidence and assembly checks below apply
when those artifacts are actually authored, executed or built.

- The active Page Type and Page phase are explicit.
- The Story passes its eight-division read-through test and preserves the
  user's version/approval boundary.
- The selected C8 Section Narrative states the venue telling and every
  Section's ordered moves, claims, evidence/display role and reader transition.
  Its compile projection lists only real Section ids when assembly is requested.
- Every Section resolves to one Story Section Narrative row and every consequential sentence
  resolves to evidence or is visibly marked as an unsupported obligation.
- Citation, value, and display bindings live on the consuming Page; each one
  resolves to a typed Evidence Item, full local Run id, and accepted Result.
- Every display has its own intake, artifacts, bindings, and acceptance state.
- For a visual DISPLAY whose composition was open, the accepted unit records a
  concept reference and composition ruling before editable reconstruction; the
  promoted asset still follows the normal candidate and evidence gates.
- Every Round covers one feedback batch, routes every item exactly once, and
  names checked target-Page versions plus an approved response/build receipt.
- The complete-paper PDF/DOCX is regenerated from the Section Pages' own
  `delivery/latex/` outputs, accepted Page bindings/versions, and the declared
  `delivery/paper-build.toml` config.
- The build manifest records the source/config/profile/engine versions and the
  output CHECK result; no generated Word file is used as an input.
- G4 submission-readiness is either closed or explicitly recorded as a DRAFT
  with named hard blockers and a human owner.
- Static skill validation, repository checks, and a fresh-context skill test
  have passed after any skill edit.

## 📂 Family map

```text
paper/
├── haipipe-paper/          public door; one routing contract
├── haipipe-paper-workflow/ the journey gate machine (Ideation → Story →
│                           Evidence/Execution → Section → Compile → Round);
│                           owns transitions only
├── haipipe-paper-assemble/  complete-paper DOCX/PDF/supplement build contract
├── workflow-phases/        Paper journey contracts with a Page carrier:
│                           haipipe-paper-ideation · haipipe-paper-story ·
│                           haipipe-paper-section ·
│                           haipipe-paper-round
├── haipipe-paper-venue/ the one non-phase Page Type: a QBv bank record
├── venue/                  the shared QBv desk bank (bank/), prose playbooks,
│                           and the literature bank
└── README.md               architecture and maintenance boundary
```

This door owns routing and Paper composition. `haipipe-page` owns the Page
contract, `haipipe-page-workflow` owns the lifecycle, Runs/Results own evidence
artifacts, `haipipe-plugin-outline` presents them, and `haipipe-board` owns
rendering and checking machinery.
