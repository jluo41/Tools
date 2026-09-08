---
name: haipipe-paper
description: >-
  The one door for planning, writing, and revising a paper as a graph of Board
  Pages. Routes Ideation, Story, Evidence/Execution, Section and Round Pages
  to their contracts and runs each through the shared Page lifecycle.
  Use for paper setup, status, drafting, complete-paper assembly, compiling,
  or review rounds.
metadata:
  version: "1.0.0"
  last_updated: "2026-09-07"
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
  → the exact Page Type: haipipe-page-ideation · haipipe-page-story ·
    haipipe-paper-section · haipipe-paper-round, or haipipe-paper-venue
  → phase references / the Story's Section Control row and style policy
  → haipipe-run + selected workers, only where Runs exist
```

For CONTEXT, OUTLINE, and EVIDENCE, the exact material contracts are
`haipipe-plugin-outline/ref/...` files. The Page surface already installs the
shared Outline presenter; it is not a final execution dependency.

`haipipe-paper-assemble` is a separate complete-paper verb after routing; it is
not inserted into a Page phase.

## 🧭 The journey (JL 260828 · rebuilt 260907)

`haipipe-paper-workflow` owns the gates; this figure is the reading order.
Every position is named by its authority page (the naming law). Roadmap and
Narrative are no longer positions: the Story page absorbed both on 260907.

```text
P0 Ideation (ideate)       💭 Story00-ideation · the repo is minted with this page ·
│                             ideas cheap and disposable
│                             gate G0: novelty per claim + pilot + human PROCEED
P1 Story (establish)       🌱 Story-<letter> · THE ONLY CONTROL PAGE · one idea = one
│                             paper · Seed (identity) · RQ table · §6 Evidence and
│                             Work Control · §8 Section Control + compile order
│                             gate G1: approved outline · every open RQ/E-row has a
│                             typed work row or waiver · a person releases the work
P2 Evidence/Execution      🧰 a WORK LANE, not a page · Discovery blocks, Task
│                             blocks, Runs in examples/<Project>/ · receipts land
│                             back on the Story
│  ↺ P1↔P2 = the settle loop  gate G2: every released block has an owner-native
│                             receipt · the Story updates RQ/E-row state
P3 Section (realize)       📄 one page per §8 Section Control row · a person
│                             releases each row independently (gate G3) · sign-off
│                             = per-unit CHECK ✅
│  Compile                    assemble — a verb, not a phase · runs anytime from the
│                             Story's compile-order block · gate G4 marks the build
│                             SUBMISSION-READY vs DRAFT · the upload is a human act
P4 Round (respond)         🔁 routes each concern once → Story (§6 evidence or §8
                              row) / Section · gate G5: every concern ledgered and
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
  `haipipe-page-ideation` (`paper/page-types/`).
- **Story** is one idea's control center, `Story-<letter>.md` (JL 260907): the
  letter is its stable identity and the idea slug is not part of the address.
  It holds the Seed (venue-free identity, pitch, stakes, boundaries), the
  Research Question table that sends work out, §6 Evidence and Work Control
  (E-rows plus the Discovery/Task/Run register that replaced the Roadmap page),
  and §8 Section Control (one row per Section Page, the target desk, and the
  `haipipe:compile-order` block that replaced the Narrative page). It survives
  retargeting unchanged in §1–§7 and binds its Ideation origin as a birth
  certificate. `haipipe-page-story` (`paper/page-types/`; was `haipipe-paper-seed`,
  then `haipipe-page-story`).
- **Venue** is one evidence-backed desk record in the shared bank — a library
  asset outside the journey; the decision to target it lives on the Story's §8
  rows.
- **Section** is one reader-ordered manuscript or appendix unit executing one
  Story §8 Section Control row; the page owns the words and the tracking.
- **Round** is one bounded feedback batch parented to the Story and the build
  it reviewed. It routes every concern exactly once — to the Story's §6 when
  new evidence is demanded, to a §8 row for retelling, to a Section for rework
  — and closes with a checked response receipt.
- **Retired 260907**: Roadmap (plan to collect) and Narrative (plan to show)
  are no longer Page Types. Their contracts are parked at
  `paper/_old/retired-workflow-phases-260907/`, a paper's old child pages at that
  paper's `_archive/`; both are migration history, never current authority.

`/haipipe-paper status [paper] [section|evidence|citation|display]` regenerates
the same rollup a Dash Page used to hold, as an optional drill-down on the
existing status command instead of a Page Type of its own: it reports every unit,
obligation, and gap in one family and never decides anything, so it earns no
lifecycle, no CHECK gate, and no `page-type:` key (retired 260820, JL: it
covered four families and only one of them — section — was ever
Narrative-shaped; folding it into Narrative would have stranded the other
three with no owner).

Retargeting keeps the Story's Seed divisions, binds the target's SHARED Venue
Page (creating one in the venue bank only when the desk has none), and adds a
sibling set of §8 Section Control rows with the new target and its own
compile-order block. A Venue Page is consumer-neutral and refreshes on the
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
| brainstorm, novelty-check, eliminate an idea, or send one to a Seed | `haipipe-page-ideation` |
| ask where a paper is in the journey, or test a gate | `haipipe-paper-workflow` |
| start a paper, read where one idea stands, repair its identity or RQ table | `haipipe-page-story` (`seed` still routes here) |
| release a work block, register a receipt, settle an E-row, release a Section row | `haipipe-page-story` (§6 Work Control · §8 Section Control) |
| inspect or record a target venue | `haipipe-paper-venue` (library lane, not a phase) |
| write or revise one manuscript/appendix unit | `haipipe-paper-section` |
| triage or answer one feedback/review cycle | `haipipe-paper-round` |
| check paper or one family's status | `/haipipe-paper status` (command, not a Page Type) |
| run one Page through its lifecycle | `haipipe-page-workflow` |
| compile or export one Page | Page-local `latex/` or `word/` plugin |
| assemble the paper | `haipipe-paper-assemble` from the Section Pages' own `delivery/latex/` outputs and accepted bindings |
| respond to reviewers | a Round Page plus the affected Story rows and Sections |

### Paper verbs

```text
/haipipe-paper ideate <direction|idea-id> [phase]
/haipipe-paper enter [paper]
/haipipe-paper status [paper] [section|evidence|citation|display]
/haipipe-paper journey [paper]         read the journey position · test the gates ·
                                       never advances anything
/haipipe-paper story [paper] [phase]    (`seed` accepted as alias)
/haipipe-paper venue <target> [phase]
/haipipe-paper section <section-id> [phase]
/haipipe-paper round <new|id>
/haipipe-paper assemble [paper]        runs anytime · a build made while gate G6
                                       fails is watermarked DRAFT in its receipt
```

Every `[phase]` above is a PAGE phase (CONTEXT…CHECK). The journey's
positions are never called by that word in a verb; `haipipe-paper-workflow`
carries the terminology law.

When the user names a concrete Page, prefer that Page over inferring a phase
from a broad verb. When a phase is omitted for an existing Page, inspect its
latest receipt and use the shared workflow's authority test.

## 📐 The Story's Section Control controls the paper

The Story page's §8 Section Control is not a paragraph summary. Its governing
artifact is a table with one row per reader-ordered section, plus a
machine-readable compile order:

```text
target | order | section-id | reader question | claim / E ids | evidence/run ids |
state | open risk
<!-- haipipe:compile-order:start --> main: … appendix: … <!-- …:end -->
```

Every Section Page points to exactly one current row (`story-row:` on the
Section; `narrative-row:` is the pre-260907 name and reads as an alias). A
changed row reopens the affected Section; a prose draft never outranks the
current row. The compile-order block is an order projection of the table, read
by `haipipe-paper-assemble`; it never carries prose.

A Story row may make factual claims — that a result is the paper's peak claim,
that a mechanism is sufficiently established. Those claims resolve to the
Story's §6 E-rows and their accepted receipts, like claims on any other Page.
A control table does not become evidence-free merely because its output is an
order.

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
│   └── Story-A/                P1 · ONE STORY = ONE IDEA · the only control page:
│       └── Story-A.md          Seed · RQ table · §6 Evidence and Work Control ·
│                               §8 Section Control + haipipe:compile-order block
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
├── _archive/                   HISTORY only, read by nothing · e.g.
│                               retired-workflow-pages-260907/ (old child pages)
└── README.md
```

**No `tasks/` here (JL 260828)**: a roadmap block's task group lives in the
TASK LAYER's own home, `examples/<Project>/tasks/{G}{NN}_<name>/`, never inside
the paper repo. The symmetry is with discoveries — evidence layers are
consumer-neutral and a page binds them by path, so a task inside the paper
would make the paper both the consumer of its evidence and the executor of it.
The Story's §6 Work Control (`haipipe-page-story`) carries the law and the which-project test.

**The delivery law (JL 260907; replaces the room law of 260824)**: the words
live on the Section Pages. Each Section Page compiles its own
`delivery/latex/<page>-complete.tex` (with its `.bib` and `.pdf`) through the
page-level delivery plugin, and that PDF is the page's own deliverable; the
body fragment beside it, `delivery/latex/<page>.tex`, is what the paper
build `\input`s. The paper's `delivery/latex/` is built FROM those fragments,
in the Story's compile order (the §8.2 `haipipe:compile-order` block): `master.tex` is generated, `sections/`
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
and one `Story-<letter>` per surviving idea, the paper's only control page (JL
260907: the letter is the stable Story identity; `SD`/`NA` tokens are retired;
the roadmap/narrative children retired the same day into `_archive/`);
`B` groups run in lowercase
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
`0-paperboard/` wrapper with `<N>-<desk><year>/` desk rooms beside it, the
flat phase-numbered Story/Seed/Roadmap/Narrative sibling group, and a Story
still holding `Story-<letter>-roadmap` / `-narrative-<desk>` children) are
grandfathered and migrate only on explicit
request, because the rename touches tex `\input` paths, legacy PageX
symlinks, and compile scripts. `Paper-AgreeablePrescription` is the first
repo on the 1.0.0 single-Story layout.

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
in the Story's compile order, regenerates `delivery/latex/` from them, and
converts `delivery/word/` from that. The pages own the wording; `delivery/`
is a projection and is never edited by hand.

The paper declares one `delivery/paper-build.toml` containing the page groups
and the Story page whose compile-order block orders them, the display and bibliography sources,
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
request. Migration reads the old pages as evidence, creates the current Story,
Venue, and Section Pages, verifies the new build, and preserves the old tree
under that paper's archive. Ordinary writing never silently revives a retired
stage lane.

On 2026-09-07 the Roadmap and Narrative journey phases were retired as well:
`haipipe-paper-roadmap` and `haipipe-paper-narrative` moved to
`paper/_old/retired-workflow-phases-260907/`, and their duties moved onto the
Story page (§6 Evidence and Work Control, §8 Section Control with the
compile-order block). A paper still carrying `Story-<letter>-roadmap` /
`-narrative-<desk>` child pages is grandfathered and migrates on explicit
request, the children going to that paper's `_archive/`; `board.md`, Section
`story-row:` fields, and `delivery/paper-build.toml` `order` then point at the
Story page.

## ✅ Completion checks

Before reporting Paper work complete:

- The active Page Type and Page phase are explicit.
- The Story page contains no venue-specific promise, no prose, no run.
- The Story's §8 Section Control names the target desk and carries one row per
  Section, and its compile-order block lists only real Section ids.
- Every Section resolves to one Story Section Control row and every consequential sentence
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
├── haipipe-paper-workflow/ the journey gate machine (Ideation → Story →
│                           Evidence/Execution → Section → Compile → Round);
│                           owns transitions only
├── haipipe-paper-assemble/  complete-paper DOCX/PDF/supplement build contract
├── page-types/             the two Paper Page Types, named like every other
│                           haipipe-page-<type> (JL 260907): haipipe-page-ideation ·
│                           haipipe-page-story; each owns its page-type key
├── workflow-phases/        the two journey-phase skills that are also Page Types:
│                           haipipe-paper-section · haipipe-paper-round
├── _old/                   retired-workflow-phases-260907/ (roadmap, narrative) ·
│                           history only, never loaded
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
