# QB0 · paper board layout · PLAN, MAIN, and APPENDIX

state: 🟡 PARTIAL · three-group design ruled · MISQ migration not yet executed
owner: JL
method: define the smallest paper-owned board after value, citation, probe, display, and pagex become standard page capabilities
session: d6d8c7f4-4e8d-4ebe-b16c-2d11a8f20e9e

## Opening

What must remain as a page when evidence, display, and transport are no longer separate page families?
The answer is the paper's story and the manuscript sections that realize it.
The paper board therefore has three groups: `PLAN`, `MAIN`, and `APPENDIX`.
`Opening` tells the venue-free canonical story, and `Narrative` retells that story for one selected venue.
The section pages then execute the Narrative without recreating its planning work.

## Writing Style

Name a page only when it owns a distinct decision, artifact, or human gate.
Treat `Opening`, `Narrative`, and `Section` as paper roles carried by Stage Pages, not as new Page Types.
Keep the venue catalog on the shared PaperSkillBoard and keep the selected venue explicit on the paper's Narrative page.
Write one page per line in every inventory so the board can be counted by eye.

## Diagram

**The two-board relationship**: the shared board supplies contracts and venue knowledge; the paper board owns this paper's choices and prose plan.

```text
SHARED PaperSkillBoard
  Venue catalog
    QBv1 · MISQ ───────────────────────────────┐
  Role contracts                              │ pagex borrows
    Opening · Narrative · Section             │ selected Venue
                                               ▼
PAPER BOARD
  ① PLAN
    Opening       venue-free canonical story
    Narrative     Opening × selected Venue

  ② MAIN
    Abstract
    Introduction
    Literature Review
    Theory
    Measurement
    Empirical Strategy
    Results
    Discussion
    Conclusion

  ③ APPENDIX
    Appendix A
    Appendix B
    Appendix C
    Appendix D
    Appendix E
    Appendix F
```

The target contains **17 paper pages**: 2 Plan pages, 9 Main section pages, and 6 Appendix section pages.
That count excludes generated board surfaces and per-page plugins.

## Content

### 1 · PLAN owns the story before it owns prose

**The Plan handoff**: the venue-free story closes before venue alignment begins.

```text
Opening · canonical story
   │ requires: the paper's phenomenon, puzzle, claims, and evidence
   ▼
Narrative · canonical story × selected Venue
   │ outputs: argument order + section obligations
   ▼
MAIN and APPENDIX
```

**Opening** is the canonical, venue-free account of why the phenomenon matters, what tension or puzzle organizes it, what the paper can claim, and how the evidence resolves the story.
It may absorb material formerly scattered across Seed, Pitch, Claim, and resource-planning pages, but it must not mention a target journal as the reason for the story's shape.

**Narrative** requires the Opening plus one selected Venue.
It records the selected venue explicitly and uses `pagex` to borrow the venue page from the shared PaperSkillBoard.
Its output is the venue-aligned argument order and the obligations handed to Main and Appendix sections.

Both are Stage Pages.
`Stage` answers how work closes: inputs, outputs, checks, and the human gate.
`Opening` and `Narrative` answer what kind of paper decision the stage owns.

### 2 · MAIN owns the reader-facing manuscript

**The Main inventory**: nine reader-facing section pages in manuscript order.

```text
M1 Abstract                 M6 Empirical Strategy
M2 Introduction             M7 Results
M3 Literature Review        M8 Discussion
M4 Theory                   M9 Conclusion
M5 Measurement
```

MAIN contains the nine reader-facing section stages in manuscript order.
Each page owns the plan, evidence obligations, displays, and revision state for one section.
Citation, value, probe, display, and pagex are capabilities available on the page rather than reasons to create neighboring page families.

MAIN is a separate group because these sections form the journal-facing argument a reader must traverse in sequence.

### 3 · APPENDIX owns support without becoming a second narrative

**The Appendix inventory**: six stable lettered pages whose visible titles may evolve.

```text
A · supplementary theory or derivation
B · measurement detail
C · identification and robustness
D · additional results
E · data and implementation detail
F · remaining required material
```

APPENDIX contains Appendix A through F as six section stages.
They use the same Section role contract as MAIN, but they form a separate group because their reading order, cross-references, and submission treatment differ.
The letters are stable board identities; the visible appendix titles may change as the paper develops.

Those descriptions are defaults, not fixed MISQ contents.
Each appendix page must state what Main claim it supports and whether the appendix is required for the current submission package.

### 4 · What is no longer a page family

**Concern-to-capability collapse**: former page families move onto the Stage Page that consumes them.

```text
Literature ─┬─ citation
Value ──────┼─ value record
Probe ──────┼─ probe
Display ────┼─ display
Venue ──────┴─ pagex reference on Narrative
```

| Former family | New home |
|---|---|
| Venue page on the paper board | selected Venue reference on Narrative; source page remains on PaperSkillBoard |
| Seed, Pitch, and Claims | divisions or records inside Opening and Narrative |
| Literature pages | citations, value records, probes, and pagex attached to the section that uses them |
| Value pages | per-page value records |
| Display pages | per-page display plugin |
| Round and Build pages | board workflow and generated surfaces, created only when they own a real gate |

The rule is not that these concerns disappear.
They cease to justify permanent top-level page families because every relevant Stage Page can now carry them.

### 5 · Migration from the current MISQ board

**The group migration**: every current family lands on one persistent target group or on an owner-page capability.

```text
CURRENT MISQ BOARD                         TARGET
SN · 9 narrative-related pages      ──▶   PLAN · Opening + Narrative
SD1 · main dashboard + sections     ──▶   MAIN · 9 section pages
SD2 · appendix control + A-F        ──▶   APPENDIX · 6 section pages
SE1 · value pages                   ──▶   plugins/records on owner pages
SE2 · literature pages              ──▶   citations/pagex on owner pages
SE3 · display pages                 ──▶   display plugin on owner pages
SR · round/build pages              ──▶   workflow surfaces when needed
```

The current MISQ board is historical evidence, not the target schema.
Its migration is archive-first and must preserve every substantive claim, citation, display, discussion, and human decision before collapsing pages.

The local MISQ Venue page retires only after Narrative resolves `QBv1 · MISQ` through pagex and carries the selected-venue decision in readable form.

## Aims

### 1 · PLAN owns the story before it owns prose

- A1.1 · Define Opening as the venue-free canonical story.
  **Done when:** Opening has no selected-venue dependency.
- A1.2 · Define Narrative as Opening plus one selected Venue.
  **Done when:** its required input and section handoff are explicit.

### 2 · MAIN owns the reader-facing manuscript

- A2.1 · Inventory the nine Main section pages.
  **Done when:** every reader-facing manuscript section is countable here.

### 3 · APPENDIX owns support without becoming a second narrative

- A3.1 · Inventory Appendix A through F under the same Section role contract as Main.
  **Done when:** six stable appendix identities are countable here.

### 4 · What is no longer a page family

- A4.1 · Place citation, value, probe, display, and pagex on their consuming Stage Pages.
  **Done when:** none remains a permanent top-level paper-board family.
- A4.2 · Keep Venue on the shared PaperSkillBoard.
  **Done when:** the paper board carries a reference and selection, not a duplicate Venue page.

### 5 · Migration from the current MISQ board

- A5.1 · Produce a page-by-page keep, merge, plugin, and archive manifest.
  **Done when:** every current MISQ page has one destination and no content is orphaned.
- A5.2 · Materialize the 17-page target board.
  **Done when:** the rebuilt MISQ board exposes PLAN, MAIN, and APPENDIX and passes its gates.

## States

### 1 · PLAN owns the story before it owns prose

- ✅ A1.1 · Built here on 260817.
- ✅ A1.2 · Built here on 260817.

### 2 · MAIN owns the reader-facing manuscript

- ✅ A2.1 · Built here on 260817: Main has nine pages.

### 3 · APPENDIX owns support without becoming a second narrative

- ✅ A3.1 · Built here on 260817: Appendix has six pages.

### 4 · What is no longer a page family

- ✅ A4.1 · Ruled here on 260817.
- 🟡 A4.2 · Design is explicit here; the live MISQ Narrative still needs its pagex reference.

### 5 · Migration from the current MISQ board

- ⬜ A5.1 · Not started; this page supplies the group-level mapping only.
- ⬜ A5.2 · Not started; the live 59-page board remains intact.

## Files

- `5-QBv-venue-packs/QBv1-misq/QBv1-misq.md`
  The shared MISQ venue page Narrative should borrow through pagex.
- `4-QBt-page-types/QBt15-for-narrative/QBt15-for-narrative.md`
  The existing Narrative specimen; it must be aligned to the Opening-first rule.
- `2-QB-delivery/QB1-opening/QB1-opening.md`
  The existing Opening contract page; it must be narrowed to the venue-free canonical story.
- `examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-MISQPhyTraitOpioidPaperBoard/board.md`
  The live MISQ paper board to migrate after its page-level manifest is reviewed.
- `2-QB-delivery/QB0-paper-board-layout/_archive/QB0-paper-board-layout-pre-three-group-260817.md`
  The complete pre-redesign ten-group contract retained for provenance.

## Law

1. A persistent paper board has exactly three groups: `PLAN`, `MAIN`, and `APPENDIX`.
2. `Opening`, `Narrative`, and `Section` are paper roles carried by Stage Pages; they are not separate Page Types.
3. Opening is venue-free. Narrative equals Opening plus one explicitly selected Venue borrowed from the shared PaperSkillBoard through pagex.
4. MAIN holds nine reader-facing section pages. APPENDIX holds six lettered section pages. Both use the Section role contract.
5. Citation, value, probe, display, and pagex are page capabilities, not permanent top-level paper-board families.
6. No live page may be collapsed until a migration manifest assigns all of its content to a surviving page, plugin, generated surface, or archive.

## Discussion

> JL: I think here one challenge is how to build these pages.
> Like for writing one pages, you might need to load other pages, or first write other pages and do the current pages. I think we might need to think clear about what we are doing.

The three-group design answers the ownership half of that challenge.
Execution order remains explicit: Opening closes before Narrative, Narrative closes before section planning, and each section declares its own upstream requirements.

## Log

260817 · JL · split manuscript sections into MAIN and APPENDIX; retained Opening as the venue-free canonical story and defined Narrative as Opening × selected Venue.
260817 · CC · archived the complete ten-group QB0 and replaced it with the three-group, 17-page target contract; the live MISQ board was deliberately left unchanged pending a page-level migration manifest.
