---
name: haipipe-paper
description: >-
  The one public door for planning, writing, building, and revising a paper as a
  graph of Board Pages. It routes Seed, Venue, Narrative, Section, and Round
  Pages to their Page Type contracts and runs each through the shared
  OUTLINE–PROBE–EVIDENCE–DRAFT–REVISE/COMPILE–CHECK workflow. Use for paper
  setup, narrative and per-section outlines, evidence-backed drafting, paper
  status, compilation, export, or review rounds. The current architecture has
  no View layer and no S01–S10 paper-stage router.
---

# /haipipe-paper · compose a paper from evidence-bearing Pages

`haipipe-paper` is the Paper-family router. It does not implement the Page
workflow and it does not replace the specialist Page Type contracts.

Load in this order:

```text
haipipe-paper
  → haipipe-page
  → one Paper Page Type, when applicable
  → haipipe-page-workflow for RUN
  → the Page-local plugins actually required
```

## 🧭 The active paper model

```text
                         ┌──────── Venue A ──────── Narrative A ─┐
Paper intent ──▶ Seed ───┤                                         ├─▶ Section Pages
                         └──────── Venue B ──────── Narrative B ─┘       │
                                                                        ▼
                                                         assemble · build ──▶ Round
                                                                ▲             │
                                                                └── checked changes
```

- **Seed** is one venue-free identity per paper.
- **Venue** is one evidence-backed record per submission target.
- **Narrative** is one venue-aligned argument architecture per target. It owns
  claims, reader order, and the detailed one-row-per-section outline.
- **Section** is one reader-ordered manuscript or appendix unit executing one
  Narrative row.
- **Round** is one bounded feedback-and-response cycle against one paper build.
  It routes accepted work back to the owning Narrative and Section Pages and
  closes with a checked response/build receipt.

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
/haipipe-paper enter [paper]
/haipipe-paper status [paper] [section|probe|citation|display]
/haipipe-paper seed [paper] [phase]
/haipipe-paper venue <target> [phase]
/haipipe-paper narrative <target> [phase]
/haipipe-paper section <section-id> [phase]
/haipipe-paper round <new|id>
/haipipe-paper assemble [paper]
```

When the user names a concrete Page, prefer that Page over inferring a stage
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
├── page-types/             five active Paper Page Type contracts
├── venue/                  reusable venue playbooks and exemplars
├── _old/                   retired stages and implementations; never auto-loaded
└── README.md               architecture and maintenance boundary
```

This door owns routing and Paper composition. `haipipe-page` owns the Page
contract, `haipipe-page-workflow` owns the lifecycle, plugins own evidence
material, and `haipipe-board` owns rendering and checking machinery.
