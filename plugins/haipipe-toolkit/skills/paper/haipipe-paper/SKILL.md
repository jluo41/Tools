---
name: haipipe-paper
description: >-
  The one door for planning, writing, and revising a paper as a graph of Board
  Pages. Routes Ideation, Story, Roadmap, Venue, Narrative, Section and Round
  Pages to their contracts and runs each through the page lifecycle.
  Use for paper setup, status, drafting, complete-paper assembly, compiling,
  or review rounds.
metadata:
  version: "0.8.1"
  last_updated: "2026-09-07"
  summary: "page-types/ replaced by workflow-phases/: six haipipe-paper-<phase> skills; venue contract moved beside its bank."
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
  → exact haipipe-paper-<phase> Page Type, or haipipe-paper-venue
  → phase references / narrative-style policy
  → haipipe-run + selected workers, only where Runs exist
```

For CONTEXT, OUTLINE, and EVIDENCE, the exact material contracts are
`haipipe-plugin-outline/ref/...` files. The Page surface already installs the
shared Outline presenter; it is not a final execution dependency.

`haipipe-paper-assemble` is a separate complete-paper verb after routing; it is
not inserted into a Page phase.

## 🧭 The six-phase journey (JL 260828)

`haipipe-paper-workflow` owns the gates; this figure is the reading order.
Every phase is named by its authority page (the naming law), with the old
verb kept as a parenthesized alias.

```text
P0 Ideation (ideate)      💭 Story00 · the repo is minted with this page ·
│                            ideas cheap and disposable
│                            gate G0: novelty per claim + pilot + human PROCEED
P1 Story (establish)      🌱 Story<NN>-<idea> · THE STORY PAGE · one idea = one
│                            paper · holds the Seed (identity) · RQ table · E-board
│                            gate G1: skeleton stands · gap list readable
P2 Roadmap (route)        🗺 Story<NN>-roadmap · child of its Story · plan to
│                            COLLECT · BLOCK rows serving RQ/E-rows · ✋ released ·
│                            then the receipts land on its lap divisions
│                            gate G2: every 🔨/⬜ E-row has a ▶️ row or waiver
│                            gate G3: done-when holds · settle written on Seed
│  ↺ P1↔P2 = the establish loop · exits only through the Seed:
│                            gate G4: ticked outline · novelty column ·
│                            pitch sells only ✅ rows
P3 Narrative (tell)       🧭 Story<NN>-narrative-<desk> · child of its Story ·
│                            plan to SHOW · one per desk · §1 IS the venue decision
│                            gate G5: bank page bound · claims parented ·
│                            map rows budgeted
P4 Section (realize)      📄 one per map row · sign-off = per-unit CHECK ✅
│  P4.9                      assemble — a verb, not a phase · runs anytime;
│                            G6 marks the build SUBMISSION-READY vs DRAFT ·
│                            the upload is a human act
P5 Round (respond)        🔁 routes each concern once → seed / narrative /
                             section · gate G7: every concern ledgered and
                             routed exactly once · a person approves the
                             response receipt

   📚 venue = library, never a phase: the QBv bank is consulted at P3 §1,
      and a missing desk gets its bank page minted as a sub-step.
```

The seven Page Types, one line each:

- **Ideation** is one research direction's ideas, ranked in the source
  reports' own structure (IDEA_REPORT / Novelty Check Report fields), the
  story group's page zero (`Story00-ideation`), minted with the repo before any
  Seed exists; eliminated ideas stay forever; the winning idea's `went to`
  names this board's Seed (or, rarely, a sibling repo's).
- **Story** is one idea's control center, `Story<NN>-<idea-slug>.md` (JL
  260907): it holds the Seed (venue-free identity, pitch, stakes, boundaries),
  the Research Question table that drives the work, the Establishment Board
  that records what came back, and the handoff to its two child plans; it
  survives retargeting unchanged and binds its Ideation origin as a birth
  certificate. `haipipe-paper-story` (was `haipipe-paper-seed`).
- **Roadmap** is one paper's plan to COLLECT, a child page of its Story
  (`Story<NN>-roadmap`), campaign and intake on one page: BLOCK
  rows (data, model, analysis, …) each serving a Seed E-row, with executor,
  done-when, budget, and a person's block-by-block release — a block is a
  task group, its jobs are task folders, its runs are configurations,
  addressed `B<n>T<n>r<n>` — then one dispatch card per released block, the
  landed QA receipts registered lap by lap, and settle PROPOSALS the Seed
  alone writes; QA files stay the substance — register, never restate; the
  page plans and registers, and never executes.
- **Venue** is one evidence-backed desk record in the shared bank — a library
  asset outside the journey; the decision to target it lives on a Narrative.
- **Narrative** is one desk's telling and the paper's plan to SHOW, a child
  page of its Story (`Story<NN>-narrative-<desk>`): venue decision, claim
  system, argument order, and the one-row-per-section map. One desk, one page;
  retargeting mints a sibling child from the same Story.
- **Section** is one reader-ordered manuscript or appendix unit executing one
  Narrative row; the tex owns the words, the page owns the tracking.
- **Round** is one bounded feedback batch parented to a named Narrative. It
  routes every concern exactly once — to the Seed when new evidence is
  demanded, to the Narrative for retelling, to a Section for rework — and
  closes with a checked response receipt.

`/haipipe-paper status [paper] [section|evidence|citation|display]` regenerates
the same rollup a Dash Page used to hold, as an optional drill-down on the
existing status command instead of a Page Type of its own: it reports every unit,
obligation, and gap in one family and never decides anything, so it earns no
lifecycle, no CHECK gate, and no `page-type:` key (retired 260820, JL: it
covered four families and only one of them — section — was ever
Narrative-shaped; folding it into Narrative would have stranded the other
three with no owner).

Retargeting keeps Seed, binds the target's SHARED Venue Page (creating one in
the venue bank only when the desk has none), and creates a new Narrative. A
Venue Page is consumer-neutral and refreshes on the desk's clock, never a
paper's. Retargeting does not rewrite the stable paper identity merely to
imitate a new desk. Closed Round Pages remain bound to the Venue, Narrative,
and build they actually reviewed.

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
├── runs/                      Page-local L4 Run Tickets
├── results/                   paired local Results/runtime receipts
└── delivery/                  generated Page-level TeX/PDF/DOCX when requested
```

`haipipe-plugin-outline` presents Context, Bullet, and Evidence Workspaces.
VALUE, CITE, and DISPLAY are Result types inside Evidence Workspace, not
separate plugins. Exact numbers and citation metadata live in accepted local
Results; the Page cites their `E<NN>-<TYPE>-<slug>` and full Run/Result ids.

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
| brainstorm, novelty-check, eliminate an idea, or send one to a Seed | `haipipe-paper-ideation` |
| ask where a paper is in the journey, or test a gate | `haipipe-paper-workflow` |
| start a paper, read where one idea stands, repair its identity or RQ table | `haipipe-paper-story` (`seed` still routes here) |
| plan the campaign, release a block, register receipts, close a lap | `haipipe-paper-roadmap` |
| inspect or record a target venue | `haipipe-paper-venue` (library lane, not a phase) |
| design claims, arc, or per-section outline | `haipipe-paper-narrative` |
| write or revise one manuscript/appendix unit | `haipipe-paper-section` |
| triage or answer one feedback/review cycle | `haipipe-paper-round` |
| check paper or one family's status | `/haipipe-paper status` (command, not a Page Type) |
| run one Page through its lifecycle | `haipipe-page-workflow` |
| compile or export one Page | Page-local `latex/` or `word/` plugin |
| assemble the paper | `haipipe-paper-assemble` from the Section Pages' own `delivery/latex/` outputs and accepted bindings |
| respond to reviewers | a Round Page plus affected Narrative/Sections |

### Paper verbs

```text
/haipipe-paper ideate <direction|idea-id> [phase]
/haipipe-paper enter [paper]
/haipipe-paper status [paper] [section|evidence|citation|display]
/haipipe-paper journey [paper]         read the journey position · test the gates ·
                                       never advances anything
/haipipe-paper story [paper] [phase]    (`seed` accepted as alias)
/haipipe-paper roadmap [paper] [phase]
/haipipe-paper venue <target> [phase]
/haipipe-paper narrative <target> [phase]
/haipipe-paper section <section-id> [phase]
/haipipe-paper round <new|id>
/haipipe-paper assemble [paper]        runs anytime · a build made while gate G6
                                       fails is watermarked DRAFT in its receipt
```

Every `[phase]` above is a PAGE phase (CONTEXT…CHECK). The journey's six
positions are never called by that word in a verb; `haipipe-paper-workflow`
carries the terminology law.

When the user names a concrete Page, prefer that Page over inferring a phase
from a broad verb. When a phase is omitted for an existing Page, inspect its
latest receipt and use the shared workflow's authority test.

## 📐 The Narrative contract controls the paper

The Narrative Page is not a paragraph summary. Its governing artifact is a
detailed section map with one row per reader-ordered section:

```text
section-id | reader question | claim role | must establish | evidence ids |
display ids | paragraph/move outline | enters from | hands to | open risk
```

Every Section Page points to exactly one current row. A changed Narrative row
reopens the affected Section; a prose draft never outranks the current map.

Narrative itself may make factual claims—for example, that a result is the
paper's peak claim or that a mechanism is sufficiently established. Those
claims must carry typed Evidence Items and accepted local Results just like
claims on any other Page.
Narrative does not become evidence-free merely because its output is an
outline.

## 📂 Paper folder scaffold (JL 260823 · groups at the root and delivery/ JL 260907)

A new paper repo — created as a git submodule immediately — is one board whose
page groups sit directly at the paper root, plus one `delivery/` folder that
is a projection of the finished Section Pages. There is no `0-paperboard/`
wrapper and no hand-edited desk room. Board groups map onto the journey: P0
and the Stories in `A1-Story/`, P4–P5 in one group per desk:

```text
Paper-<Slug>/
├── board.md                    the board · paper-root: .
├── board/                      engine-generated HTML (build.py output)
├── A1-Story/
│   ├── Story00-ideation/       P0 · the idea pool · exactly one
│   └── Story01-<idea-slug>/    P1 · ONE STORY = ONE IDEA · the Story page carries
│       │                       the Seed and the Research Question table
│       ├── Story01-roadmap/            P2 · child · plan to COLLECT
│       └── Story01-narrative-<desk>/   P3 · child · plan to SHOW · one per desk
│   (a second surviving idea is Story02-<slug>/, same shape)
├── Ba-<desk1>-Main/            P4 · first desk's named Main sections
├── Bb-<desk1>-Appendix/        P4 · its named Appendix sections
├── Bc-<desk1>-Round/           P5 · its RD<NN> rounds, one page per batch ·
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

**No `tasks/` here (JL 260828)**: a roadmap block's task group lives in the
TASK LAYER's own home, `examples/<Project>/tasks/{G}{NN}_<name>/`, never inside
the paper repo. The symmetry is with discoveries — evidence layers are
consumer-neutral and a page binds them by path, so a task inside the paper
would make the paper both the consumer of its evidence and the executor of it.
`haipipe-paper-roadmap` carries the law and the which-project test.

**The delivery law (JL 260907; replaces the room law of 260824)**: the words
live on the Section Pages. Each Section Page compiles its own
`delivery/latex/<page>-complete.tex` (with its `.bib` and `.pdf`) through the
page-level delivery plugin, and that PDF is the page's own deliverable; the
body fragment beside it, `delivery/latex/<page>.tex`, is what the paper
build `\input`s. The paper's `delivery/latex/` is built FROM those fragments,
in the Narrative's section-map order: `master.tex` is generated, `sections/`
and `appendices/` are copies of the fragments, `displays/` holds copies of
accepted page-local DISPLAY floats and assets, and `reference.bib` is merged
from the pages' `bibex/<page>.bib`. Nothing under `delivery/` is hand-edited; a correction goes
back to the owning page and the folder is regenerated whole. `delivery/word/`
is converted from `delivery/latex/` and never edited either. On send, a copy
of the current build is frozen in the Round it opens (`RD<NN>/sent/`); on that
Round's close, the answering build is frozen in `RD<NN>/released/`
(`haipipe-paper-round`). Evidence
AUTHORITY never moves into `delivery/`: it holds copies, the pages hold the
Results. The milestone that admits a page into the build is per Section Page:
its outline table is approved, every display unit has its preview PDF, and its
own page PDF compiles. The old self-contained desk rooms (`<N>-<desk><year>/`
with `sections/*.tex` as source of record) are retired for new repos and
grandfathered where they exist.

**Group-name grammar (JL 260824; Section IDs re-ruled 260901)** — one `A` group
carries the per-paper journey: `A1-Story` holds `Story00-ideation` (the pool)
and one `Story<NN>-<idea-slug>` per surviving idea, each holding its
`Story<NN>-roadmap` and `Story<NN>-narrative-<desk>` children (JL 260907: the
number is the idea counter; `SD`/`NA` tokens are retired); `B` groups run in lowercase
letter order across the board, ONE LETTER PER GROUP (JL 260831 "Ba to be Main,
Bb to be Appendix, Bc to be Round"): the first desk takes `Ba-<desk>-Main` for
the named Main units, `Bb-<desk>-Appendix` for its named Appendix units, and
`Bc-<desk>-Round` for the `RD` pages; a second desk continues at the next free
letter (`Bd-<desk2>-Main`, …). Section Pages use full semantic IDs:
`S-<desk>-Main-<kind>` and `S-<desk>-Appendix-<slug>`. Thus a Round routes to
`S-MISQ-Main-Results`, not to an opaque `SM05`; `board.md` alone supplies
reader order. The `<desk>` name keeps its own capitals (`Ba-MISQ-Main`); only
the group letter is lowercase.
Grandfathered: three groups sharing one desk letter, and a single
`B<x>-<desk>` group holding all three families.
**Collision rule**: `<D>` is the first distinctive letter of the desk not
already claimed on this board; `D` is never available (`SD` is the story
token), `A` is never available (`SA` is the appendix token), and `N`/`R`
initials watch for clashes with the `NA`/`RD` tokens; two desks sharing an initial resolve by the later arrival taking its
next distinctive letter. Review letters live inside their Round page's
folder, never at the repo root. Existing repos (`0-<Slug>PaperBoard/`, bare
`paperboard/`, `0-sections/`, `0-display/`, a shared root `reference.bib`,
`SC`/`A<D>`/`SD`/`NA` tokens, a separate `A2-NA-narrative` group, a lone `C1-RD-round`
group, a story group holding a separate `SD03-collection` page, the
`0-paperboard/` wrapper with `<N>-<desk><year>/` desk rooms beside it, and the
flat phase-numbered story group `Story01-seed` / `Story02-roadmap` /
`Story03-narrative-<desk>`) are grandfathered and migrate only on explicit
request, because the rename touches tex `\input` paths, legacy PageX
symlinks, and compile scripts. `Paper-AgreeablePrescription` is the first
repo on the 0.8.0 layout.

## 📦 Assembly and delivery

Paper assembly is a source-driven projection, governed by
`haipipe-paper-assemble`. It does not silently mine raw Task or Discovery
folders, and it does not use a previous Word file as a template or input.

```text
Board/Page authority                  Section Pages' own deliverables
boundary · claims · evidence         <page>/delivery/latex/<page>-complete.tex
acceptance · display bindings        + .bib · accepted display assets
             \                         /
              accepted bindings + delivery/paper-build.toml
                               ↓
             delivery/latex/ regenerated whole: master.tex ·
             sections/ · appendices/ · displays/ · reference.bib
                               ↓
             shared assembly engine + venue profile
                               ↓
       main DOCX/PDF · supplement · snapshots · manifest · QA
```

The Page-local `delivery/word/` snapshot remains useful for a coauthor
reading one Section Page. It is not the complete-paper input. The complete
paper builder reads each Section Page's `delivery/latex/<page>-complete.tex`
in the Narrative's order, regenerates `delivery/latex/` from them, and
converts `delivery/word/` from that. The pages own the wording; `delivery/`
is a projection and is never edited by hand.

The paper declares one `delivery/paper-build.toml` containing the page groups
and the Narrative that orders them, the display and bibliography sources,
output names, and venue profile. The reusable engine owns parsing, document events, rendering,
manifests, and QA; the paper contributes configuration and only a narrowly
scoped adapter for unusual constructs. See
`haipipe-paper-assemble/SKILL.md` for the full contract.

Assembly may run before G6. Such an output is a `DRAFT`; it becomes a
`SUBMISSION-READY` candidate only when the Section CHECK bindings, source
manifest, build QA, and human decision required by the workflow all hold.
Generated DOCX/PDF/snapshots are derived artifacts and are overwritten by a
rebuild; corrections must return to the source Section/config.

## 🚦 Submission-readiness gate (G6 · before submission)

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
   must approve the evidence scope and the final build before G6 closes.

The build remains `DRAFT` when any hard blocker is open, even if the document
compiles and passes visual checks. A human may explicitly waive a noncritical
item; the waiver belongs in the build receipt and does not waive venue rules,
unsupported claims, missing evidence, or required disclosures.

## 🧱 Retired architecture boundary

The former S01–S10 stage contracts, stage resolver, S-page creator, S03/S04
topic-entry tooling, stage-specific craft, and their helper scripts are
retired, and were DELETED 260822 rather than parked; this door never loaded them.

An existing paper that still uses those files is migrated only on explicit
request. Migration reads the old pages as evidence, creates current Seed,
Venue, Narrative, and Section Pages, verifies the new build, and preserves the
old tree under that paper's archive. Ordinary writing never silently revives a
retired stage lane.

## ✅ Completion checks

Before reporting Paper work complete:

- The active Page Type and Page phase are explicit.
- The Story page contains no venue-specific promise, no prose, no run.
- Each Narrative names its venue and carries claims plus one detailed row per
  Section.
- Every Section resolves to one Narrative row and every consequential sentence
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
  output QA result; no generated Word file is used as an input.
- G6 submission-readiness is either closed or explicitly recorded as a DRAFT
  with named hard blockers and a human owner.
- Static skill validation, repository checks, and a fresh-context skill test
  have passed after any skill edit.

## 📂 Family map

```text
paper/
├── haipipe-paper/          public door; one routing contract
├── haipipe-paper-workflow/ the six-phase gate machine; owns transitions only
├── haipipe-paper-assemble/  complete-paper DOCX/PDF/supplement build contract
├── workflow-phases/        six journey-phase skills, haipipe-paper-ideation
│                           … haipipe-paper-round; each owns its page-type key
├── haipipe-paper-venue/ the one non-phase Page Type: a QBv bank record
├── venue/                  the shared QBv desk bank (bank/), prose playbooks,
│                           and the literature bank
├── TODO.md                 deferred design work, one entry per item
└── README.md               architecture and maintenance boundary
```

This door owns routing and Paper composition. `haipipe-page` owns the Page
contract, `haipipe-page-workflow` owns the lifecycle, Runs/Results own evidence
artifacts, `haipipe-plugin-outline` presents them, and `haipipe-board` owns
rendering and checking machinery.
