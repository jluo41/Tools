---
name: haipipe-paper
description: >-
  The one public door for planning, writing, building, and revising a paper as a
  graph of Board Pages. It routes Explore, Seed, Venue, Narrative, Section, and
  Round Pages to their Page Type contracts, reads the five-phase journey
  (Explore → Establish → Tell → Realize → Respond) through
  haipipe-paper-workflow's gates, and runs each Page through the shared
  OUTLINE–PROBE–EVIDENCE–DRAFT–REVISE/COMPILE–CHECK workflow. Use for idea
  exploration, paper setup, narrative and per-section outlines, evidence-backed
  drafting, paper status, compilation, export, or review rounds. The current
  architecture has no View layer and no S01–S10 paper-stage router.
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

## 🧭 The five-phase journey (JL 260823)

`haipipe-paper-workflow` owns the gates; this figure is the reading order.

```text
P0 Explore    💭 explore page · standing IdeaBoard · ideas cheap and disposable
│                gate G0: novelty judged per claim + pilot receipt + human PROCEED
P1 Establish  🌱 seed · venue-free · E-board with novelty column
│                gate G1: human-ticked outline · pitch sells only ✅ rows
P2 Tell       🧭 narrative · one per desk · §1 IS the venue decision
│                gate G2: bank page bound · claims parented · map rows budgeted
P3 Realize    📄 sections · one per map row · sign-off = per-unit CHECK ✅
│  P3.9          assemble — a verb, not a phase · runs anytime; G3 marks the
│                build SUBMISSION-READY vs DRAFT · the upload is a human act
P4 Respond    🔁 round · routes each concern once → seed / narrative / section

   📚 venue = library, never a phase: the QBv bank is consulted at P2 §1,
      and a missing desk gets its bank page minted as a sub-step.
```

The six Page Types, one line each:

- **Explore** is one research direction's idea ledger on a standing IdeaBoard;
  killed ideas stay forever; graduates become Seeds.
- **Seed** is one venue-free identity per paper; it survives retargeting
  unchanged and binds its Explore origin as a birth certificate.
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
existing status command instead of a sixth Page Type: it reports every unit,
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
| brainstorm, novelty-check, kill, or graduate an idea | `haipipe-page-for-explore` |
| ask where a paper is in the journey, or test a gate | `haipipe-paper-workflow` |
| create or repair paper identity | `haipipe-page-for-seed` |
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
/haipipe-paper explore <direction|idea-id> [phase]
/haipipe-paper enter [paper]
/haipipe-paper status [paper] [section|probe|citation|display]
/haipipe-paper journey [paper]         read the journey position · test the gates ·
                                       never advances anything
/haipipe-paper seed [paper] [phase]
/haipipe-paper venue <target> [phase]
/haipipe-paper narrative <target> [phase]
/haipipe-paper section <section-id> [phase]
/haipipe-paper round <new|id>
/haipipe-paper assemble [paper]        runs anytime · a build made while gate G3
                                       fails is watermarked DRAFT in its receipt
```

Every `[phase]` above is a PAGE phase (OUTLINE…CHECK). The journey's five
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

## 📂 Paper folder scaffold (JL 260823)

A new paper repo — created as a git submodule immediately — takes plain,
prefix-free top-level names and a fixed board address:

```text
Paper-<Slug>/
├── paperboard/                 the board · FIXED name, tooling may rely on it
│   ├── board.md
│   ├── board/                  engine-generated HTML (build.py output)
│   ├── A1-SD-story/            seed + one narrative per desk
│   ├── Ba1-SM-ms-main/         first desk's main units
│   ├── Ba2-AM-ms-appendix/     first desk's appendix units
│   ├── Bb1-SW-wise-main/       second desk's main units (pair may be single)
│   └── C1-RD-round/            RD<NN>-<desk>-<event>/ · letters live inside
├── sections/                   the words · tex reader units
├── displays/                   the figures and tables · shared by all tellings
├── <desk><year>/               one deliverable room per desk (e.g. wise2026/)
├── reference.bib · class files · compile scripts
└── README.md
```

**Group-name grammar** — three characters, three meanings: UPPERCASE category
(`A` story, `B` tellings, `C` rounds), lowercase desk-pair letter within `B`
(`a`, `b`, `c`… in arrival order), digit for the member (`1` main, `2`
appendix). Page tokens carry the desk too: `S<D>` main units, `A<D>` appendix
units, `<D>` the desk's letter — so `C1 lands in SM05 and SW01` reads without
a legend. **Collision rule**: `<D>` is the first distinctive letter of the desk
not already claimed on this board, and `D` itself is never available because
`SD` is the story group's token; two desks sharing an initial resolve by the
later arrival taking its next distinctive letter. Review letters live inside their Round page's folder, never at the
repo root. Existing boards (`0-<Slug>PaperBoard/`, `0-sections/`, `SC`/`SA`
tokens) are grandfathered and migrate only on explicit request, because the
rename touches tex `\input` paths, pagex symlinks, and compile scripts.

## 📦 Assembly and delivery

Paper assembly reads accepted Page outputs; it does not silently mine raw Task
or Discovery folders.

```text
accepted Narrative + accepted Sections + accepted display units
                              ↓
                generated sections/ · appendices/ · paper TeX
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
├── haipipe-paper-workflow/ the five-phase gate machine; owns transitions only
├── page-types/             six active Paper Page Type contracts
├── venue/                  reusable venue playbooks and exemplars
├── _old/                   retired stages and implementations; never auto-loaded
└── README.md               architecture and maintenance boundary
```

This door owns routing and Paper composition. `haipipe-page` owns the Page
contract, `haipipe-page-workflow` owns the lifecycle, plugins own evidence
material, and `haipipe-board` owns rendering and checking machinery.
