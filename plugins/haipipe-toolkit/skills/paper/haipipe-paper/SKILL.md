---
name: haipipe-paper
description: >-
  The one door for planning, writing, and revising a paper as a graph of Board
  Pages. Routes Ideation, Seed, Roadmap, Venue, Narrative, Section and Round
  Pages to their contracts and runs each through the page lifecycle.
  Use for paper setup, status, drafting, compiling, or review rounds.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-28"
  # First NUMBERED version, not the first version: this door shipped unversioned
  # from 260620 through 125 commits, so it was the one family member no reader
  # could date-check. Numbering starts here; git holds everything before it.
---

# /haipipe-paper · compose a paper from evidence-bearing Pages

`haipipe-paper` is the Paper-family router. It does not implement the Page
workflow and it does not replace the specialist Page Type contracts.

Load in this order:

```text
haipipe-paper
  → haipipe-paper-workflow, when the question is the journey or a gate
  → haipipe-page
  → one Paper Page Type, when applicable
  → haipipe-page-workflow for RUN
  → the Page-local plugins actually required
```

## 🧭 The six-phase journey (JL 260828)

`haipipe-paper-workflow` owns the gates; this figure is the reading order.
Every phase is named by its authority page (the naming law), with the old
verb kept as a parenthesized alias.

```text
P0 Ideation (ideate)      💭 SD00 · the repo is minted with this page ·
│                            ideas cheap and disposable
│                            gate G0: novelty per claim + pilot + human PROCEED
P1 Seed (establish)       🌱 SD01 · venue-free · E-board with novelty column
│                            gate G1: skeleton stands · gap list readable
P2 Roadmap (route)        🗺 SD02 · BLOCK rows serving E-rows · ✋ released ·
│                            then the receipts land on its lap divisions
│                            gate G2: every 🔨/⬜ E-row has a ▶️ row or waiver
│                            gate G3: done-when holds · settle written on Seed
│  ↺ P1↔P2 = the establish loop · exits only through the Seed:
│                            gate G4: ticked outline · novelty column ·
│                            pitch sells only ✅ rows
P3 Narrative (tell)       🧭 NA · one per desk · §1 IS the venue decision
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
  story group's page zero (`SD00-ideation`), minted with the repo before any
  Seed exists; eliminated ideas stay forever; the winning idea's `went to`
  names this board's Seed (or, rarely, a sibling repo's).
- **Seed** is one venue-free identity per paper; it survives retargeting
  unchanged and binds its Ideation origin as a birth certificate.
- **Roadmap** is one paper's campaign, plan and intake on one page: BLOCK
  rows (data, model, analysis, …) each serving a Seed E-row, with executor,
  done-when, budget, and a person's block-by-block release — a block is a
  task group, its jobs are task folders, its runs are configurations,
  addressed `B<n>T<n>r<n>` — then one dispatch card per released block, the
  landed QA receipts registered lap by lap, and settle PROPOSALS the Seed
  alone writes; QA files stay the substance — register, never restate; the
  page plans and registers, and never executes.
- **Venue** is one evidence-backed desk record in the shared bank — a library
  asset outside the journey; the decision to target it lives on a Narrative.
- **Narrative** is one desk's telling: venue decision, claim system, argument
  order, and the one-row-per-section map. One desk, one page; retargeting
  mints a sibling from the same Seed.
- **Section** is one reader-ordered manuscript or appendix unit executing one
  Narrative row; the tex owns the words, the page owns the tracking.
- **Round** is one bounded feedback batch parented to a named Narrative. It
  routes every concern exactly once — to the Seed when new evidence is
  demanded, to the Narrative for retelling, to a Section for rework — and
  closes with a checked response receipt.

`/haipipe-paper status [paper] [section|probe|citation|display]` regenerates
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

There is no View layer and there are no active Literature, Value, or Display
Page Types. Probe is the evidence-acquisition family: PageX is its accepted-Page
lane, and QA Probe is its Task/Discovery lane. Every Paper Page may carry these
and the citation/display lanes it actually uses.

```text
Probe
├─ PageX      existing accepted Page → exact file and scope
└─ QA Probe   Task/Discovery → bank-owned QA answer and proof
```

```text
<page-dir>/
├── <page>.md                  human-readable argument and bindings
├── outline/                   frozen, approved shape for the current round
├── pagex/                     Probe · accepted-Page lane
├── probe/                     Probe · Task/Discovery QA cards and proof
├── bibex/                     citation cards, source notes, references.bib
├── display/                   zero or more independently accepted display units
├── latex/                     generated Page-level TeX/PDF when requested
└── word/                      generated Page-level DOCX when requested
```

The 🧮 value surface has no folder of its own. Values live in a probe card's
`## Values` block and are cited from prose as `PP<NN>.v<n>`; the value plugin
renders the two-way join and exposes unsourced or unused numbers.

Plugin folders are created only when used. Their absence means “not needed”
only when the Page says so explicitly; it must never mean “forgotten.”

One Page may own many displays. One display unit may render several artifacts
or panels, but it has one message, one frozen intake, and one independent
acceptance state. The root paper build may copy or link accepted artifacts into
its compiled deliverable; the Page-local display unit remains the evidence
authority.

Evidence evolves through the shared Page loop:

```text
① OUTLINE     mark each promised point: prose · 📮 question · 🧮 value ·
              📚 citation · 🖼 display
② PROBE       make a card for each unresolved obligation
③ EVIDENCE    land proof, values, citations, and displays; update the outline
④ DRAFT       write only from the agreed outline and landed evidence
⑤ REVISE      improve prose and bind card/display ids; COMPILE is folded here
⑦ CHECK       judge the built version; only CHECK may close the Page
```

Do not hard-code a linear advance here. Load `haipipe-page-workflow`; its
receipts and authority tests decide whether the Page repeats, branches, holds,
or returns to an earlier phase.

## 🚪 Routing

Resolve the paper root and target Page before changing anything.

| User intent | Route |
|---|---|
| brainstorm, novelty-check, eliminate an idea, or send one to a Seed | `haipipe-page-for-ideation` |
| ask where a paper is in the journey, or test a gate | `haipipe-paper-workflow` |
| create or repair paper identity | `haipipe-page-for-seed` |
| plan the campaign, release a block, register receipts, close a lap | `haipipe-page-for-roadmap` |
| inspect or record a target venue | `haipipe-page-for-venue` |
| design claims, arc, or per-section outline | `haipipe-page-for-narrative` |
| write or revise one manuscript/appendix unit | `haipipe-page-for-section` |
| triage or answer one feedback/review cycle | `haipipe-page-for-round` |
| check paper or one family's status | `/haipipe-paper status` (command, not a Page Type) |
| run one Page through its lifecycle | `haipipe-page-workflow` |
| compile or export one Page | Page-local `latex/` or `word/` plugin |
| assemble the paper | accepted Narrative/Sections plus their plugin outputs |
| respond to reviewers | a Round Page plus affected Narrative/Sections |

### Paper verbs

```text
/haipipe-paper ideate <direction|idea-id> [phase]
/haipipe-paper enter [paper]
/haipipe-paper status [paper] [section|probe|citation|display]
/haipipe-paper journey [paper]         read the journey position · test the gates ·
                                       never advances anything
/haipipe-paper seed [paper] [phase]
/haipipe-paper roadmap [paper] [phase]
/haipipe-paper venue <target> [phase]
/haipipe-paper narrative <target> [phase]
/haipipe-paper section <section-id> [phase]
/haipipe-paper round <new|id>
/haipipe-paper assemble [paper]        runs anytime · a build made while gate G6
                                       fails is watermarked DRAFT in its receipt
```

Every `[phase]` above is a PAGE phase (OUTLINE…CHECK). The journey's six
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
claims must carry Page-local evidence cards just like claims on any other Page.
Narrative does not become evidence-free merely because its output is an
outline.

## 📂 Paper folder scaffold (JL 260823 · desk rooms JL 260824 · phase groups JL 260824)

A new paper repo — created as a git submodule immediately — is one numbered
board plus one self-contained DESK ROOM per telling, in arrival order. Board
groups map onto the journey: P0–P2 in the story group, P3 in the narrative
group, P4–P5 in one group per desk:

```text
Paper-<Slug>/
├── 0-paperboard/               the board · 0 is ALWAYS the board · FIXED name,
│   ├── board.md                tooling may rely on it
│   ├── board/                  engine-generated HTML (build.py output)
│   ├── A1-SD-story/            P0-P2 · SD00-ideation · SD01-seed ·
│   │                           SD02-roadmap · venue-free head
│   ├── A2-NA-narrative/        P3 · NA<NN>-narrative-<desk> · one page per
│   │                           desk, numbered in arrival order
│   ├── Ba-<desk1>/             P4-P5 · first desk's S<D>NN main units,
│   │                           A<D>NN appendix units, AND its RD<NN> rounds
│   └── Bb-<desk2>/             second desk, same shape (may hold only RD
│                               pages for a foreign-desk round)
├── 1-<desk><year>/             first desk's ROOM (e.g. 1-ms2026/) · its number
│   ├── sections/               matches the desk's arrival order, the same order
│   ├── displays/               that assigned its lowercase B letter
│   ├── reference.bib
│   └── master tex · class/style files · compile script · the deliverable PDF
├── 2-<desk><year>/             second desk's room (e.g. 2-wise2026/) · same shape
└── README.md
```

**No `tasks/` here (JL 260828)**: a roadmap block's task group lives in the
TASK LAYER's own home, `examples/<Project>/tasks/{G}{NN}_<name>/`, never inside
the paper repo. The symmetry is with discoveries — evidence layers are
consumer-neutral and a page binds them by path, so a task inside the paper
would make the paper both the consumer of its evidence and the executor of it.
`haipipe-page-for-roadmap` carries the law and the which-project test.

**The room law (JL 260824)**: a desk room is self-contained — its tex reads
only its own `sections/`, includes only from its own `displays/`, cites only
its own `reference.bib`, and compiles alone. Rooms never reach into each
other. Evidence AUTHORITY never moves into a room: `displays/` holds COPIES of
accepted page-local `display/` units, and `reference.bib` is assembled from
the consuming pages' `bibex/` — reuse across tellings goes through the board
(pagex, page display units), never through a shared folder. The old shared
top-level `sections/`, `displays/`, and root `reference.bib` are retired for
new repos: a second telling that wants the first telling's figure copies it
from the owning page into its own room, with the page as provenance.

**Group-name grammar (JL 260824)** — `A` groups carry the per-paper journey
(`A1-SD-story` for P0–P2, `A2-NA-narrative` for P3); `B` groups are one per
desk in lowercase arrival order (`Ba`, `Bb`, `Bc`…), each hosting that desk's
three token families together: `S<D>` main units, `A<D>` appendix units, and
`RD` rounds — so `RD01 lands in SM05 and SW01` reads without a legend.
**Collision rule**: `<D>` is the first distinctive letter of the desk not
already claimed on this board; `D` is never available (`SD` is the story
token) and `A`/`N`/`R` initials watch for clashes with the `A<D>`/`NA`/`RD`
tokens; two desks sharing an initial resolve by the later arrival taking its
next distinctive letter. Review letters live inside their Round page's
folder, never at the repo root. Existing repos (`0-<Slug>PaperBoard/`, bare
`paperboard/`, `0-sections/`, `0-display/`, a shared root `reference.bib`,
`SC`/`SA` tokens, narratives inside the SD story group, a lone `C1-RD-round`
group, a story group holding a separate `SD03-collection` page) are
grandfathered and migrate only on explicit request, because the
rename touches tex `\input` paths, pagex symlinks, and compile scripts.

## 📦 Assembly and delivery

Paper assembly reads accepted Page outputs; it does not silently mine raw Task
or Discovery folders.

```text
accepted Narrative + accepted Sections + accepted display units
                              ↓
        the desk room: sections/ · displays/ copies · room TeX
                              ↓
                     PDF · DOCX · Overleaf package
```

Paper does not maintain a second build engine. Page-local `latex/` and `word/`
plugins build the accepted Page; the Paper assembly reads those accepted,
versioned outputs and the display artifacts they bind. Generated prose and
build artifacts are never a second authority.

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
- Seed contains no venue-specific promise.
- Each Narrative names its venue and carries claims plus one detailed row per
  Section.
- Every Section resolves to one Narrative row and every consequential sentence
  resolves to evidence or is visibly marked as an unsupported obligation.
- Citation, value, and display bindings live on the consuming Page; each value
  resolves to a probe-card value id rather than a second storage folder.
- Every display has its own intake, artifacts, bindings, and acceptance state.
- Every Round covers one feedback batch, routes every item exactly once, and
  names checked target-Page versions plus an approved response/build receipt.
- The built PDF/DOCX is regenerated from the accepted Page versions.
- Static skill validation, repository checks, and a fresh-context skill test
  have passed after any skill edit.

## 📂 Family map

```text
paper/
├── haipipe-paper/          public door; one routing contract
├── haipipe-paper-workflow/ the seven-phase gate machine; owns transitions only
├── page-types/             eight active Paper Page Type contracts
├── venue/                  the shared QBv desk bank (bank/), prose playbooks,
│                           and the literature bank
├── TODO.md                 deferred design work, one entry per item
└── README.md               architecture and maintenance boundary
```

This door owns routing and Paper composition. `haipipe-page` owns the Page
contract, `haipipe-page-workflow` owns the lifecycle, plugins own evidence
material, and `haipipe-board` owns rendering and checking machinery.
