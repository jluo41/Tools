# Paper skill family

`paper/` composes a manuscript from evidence-bearing Board Pages. The active
architecture is Page-first. The former numbered S-stage runtime was retired
and DELETED 260822 rather than parked. On 260907 the Roadmap and Narrative
journey phases were retired too; their contracts are parked, not deleted, at
`_old/retired-workflow-phases-260907/` as migration history.

## Active architecture

The journey (haipipe-paper-workflow 1.0.0, JL 260907), each position named by
its authority page; the venue bank is a library outside the journey:

```text
P0 Ideation (ideate)        Story00-ideation · the repo is minted with this page ·
                            sends one idea to its Story
P1 Story (establish)        Story-<letter> · THE ONLY CONTROL PAGE · one idea = one
                            paper · Seed (identity) · RQ table · §6 Evidence and
                            Work Control (E-rows + Discovery/Task/Run register) ·
                            §8 Section Control + haipipe:compile-order block
P2 Evidence/Execution       a work lane, not a page · Discovery blocks, Task
                            blocks, Runs in examples/<Project>/ · receipts land
   ↺ P1↔P2 = the settle loop   back on the Story (G2)
P3 Section (realize)        one page per §8 row · a person releases each row (G3)
   Compile (a verb)         haipipe-paper-assemble · anytime · G4 READY vs DRAFT
P4 Round (respond)          in the desk's Bc group · routes each concern once →
                            Story §6 / Story §8 row / Section · gates G0-G5 in
                            the workflow file
```

Each Page runs the shared workflow and owns the evidence it uses:

```text
SHAPE ⇄ SURVEY ⇄ LAND ⇄ EMBED (the OUTLINE part) → WRITE → CHECK (the DRAFT part)

Evidence Item graph
├─ Supporting Runs   Execution/Discovery 0..N · planned at SURVEY
└─ Local Run         Page · Evidence Item exactly 1 · executed at LAND

<page-dir>/
├── <page>.md
├── outline/     plan + nested Evidence Workspace (CITE/VALUE/DISPLAY + Run lineage)
├── workflow/    machine-readable phase receipts
├── scripts/     optional owned implementation
├── runs/        optional authored Run tickets
├── results/     Folder-local Results
├── delivery/    page-level render outputs (latex/ · word/ · render/)
└── studio/      human chat and drawing room
```

Evidence Items are typed (`CITE`, `VALUE`, `DISPLAY`) and live in the nested
Evidence Workspace. Supporting Run Results and the single Page-local Run
provide the material; no `pagex/`, `probe/`, or standalone value lane is a
current write target.

There is no View layer. Literature, Value, and Display are Page-local plugin
lanes, not Page Types.

## Paper layout (1.0.0 · JL 260907)

```text
Paper-<Slug>/                        no 0-paperboard/ wrapper · board.md at the root
├── board.md                         paper-root: .
├── A1-Story/
│   ├── Story00-ideation/            the idea pool
│   └── Story-A/                     one Story = one idea · the only control page
│       └── Story-A.md               seed + RQ table + §6 Work Control + §8 Section
│                                    Control + compile-order block
├── Ba-<desk>-Main/  Bb-<desk>-Appendix/  Bc-<desk>-Round/
├── _archive/                        history only · e.g. retired-workflow-pages-260907/
└── delivery/                        GENERATED from the Section Pages' own
    ├── paper-build.toml             delivery/latex/<page>.tex fragments
    ├── latex/                       master.tex · sections/ · displays/ · .bib · PDF
    └── word/                        .docx converted from latex/
```

## Active files

```text
paper/
├── haipipe-paper/
│   └── SKILL.md              one public Paper door and routing contract
├── haipipe-paper-workflow/
│   └── SKILL.md              the journey gate machine (Ideation → Story →
│                             Evidence/Execution → Section → Compile → Round)
├── haipipe-paper-assemble/
│   ├── SKILL.md              complete-paper source-driven DOCX/PDF contract
│   └── ref/                   config example and assembly references
├── page-types/               the two Paper Page Types (JL 260907: named like
│   ├── haipipe-page-ideation/      every other haipipe-page-<type>) · P0 · was
│   │                               workflow-phases/haipipe-paper-ideation
│   └── haipipe-page-story/         P1 · was haipipe-paper-seed, then haipipe-paper-story
├── workflow-phases/          two journey-phase skills, each owning its page-type key
│   ├── haipipe-paper-section/
│   └── haipipe-paper-round/
│                             (retired literature/value/display/dash Page Types deleted 260822)
├── _old/
│   └── retired-workflow-phases-260907/   haipipe-paper-roadmap · haipipe-paper-narrative ·
│                                          parked 260907, history only, never loaded
├── haipipe-paper-venue/   the one non-phase Page Type: a QBv bank record
├── venue/                    the shared QBv desk bank (bank/), prose playbooks,
│                             and the literature bank
└── TODO.md                   open issues future sessions pick up (task-family format)
```

## Family status

as of 2026-09-07 22:40 · regenerate with `/workflow-table paper` · this block is a dated receipt, never a second authority

```text
Part      Phase / Cycle            skill                    ver     L3 content it changes                        L4 Runs               human gate
A1-Story  P0 Ideation              haipipe-page-ideation    0.7.3   Story00-ideation.md                          Discovery 0..N        G0 PROCEED
A1-Story  P1 Story (seed alias)    haipipe-page-story       0.9.x   Story-<letter>.md · §3 RQ · §6 E-rows + work   Page Evidence 0..N    G1 release work
                                                                    register · §8 Section Control + compile order
external  P2 Evidence/Execution    haipipe-task ·           —       none on the paper · receipts land on Story §6  Execution/Discovery   G2 settle (person
                                   haipipe-discovery                                                                                    records it)
Ba/Bb     P3 Section               haipipe-paper-section    0.9.0   S-<desk>-*.md · delivery/latex/<page>.tex    Page Evidence/Writing  G3 row release ·
                                                                                                                                       outline v1.0 mint
delivery  Compile (verb)           haipipe-paper-assemble   0.4.x   none · writes one build-manifest               Delivery 1 per build  G4 decide to send
Bc        P4 Round                 haipipe-paper-round      0.6.0   RD<NN>.md · sent/ feedback/ released/        none                  G5 dispositions
gates     all                      haipipe-paper-workflow   1.0.0   none                                         none                  —
door      all                      haipipe-paper            1.0.0   none                                         none                  —
library   consulted by §8 rows     haipipe-paper-venue      0.6.x   QBv bank page                                none                  —
```

First repo on this layout: `examples/Project-Personality-OpioidRx/papers/Paper-AgreeablePrescription` (migrated 260907: `Story-A.md` carries §6.4 Work Control and §8 Section Control; its old roadmap/narrative children sit in `_archive/retired-workflow-pages-260907/`; `delivery/build.py` reads the compile-order block). A fresh-context field test of the 1.0.0 journey is still owed.

## Complete-paper document build

There are two different Word exports. `haipipe-plugin-delivery/ref/word.md` renders one Page
for coauthor review. `haipipe-paper-assemble` builds the complete manuscript
from the Section Pages' own `delivery/latex/<page>-complete.tex` files,
regenerating the paper's `delivery/latex/` whole (0.4.0). The latter is
deterministic and source-driven: generated Word files and section snapshots
are outputs only, never inputs. New papers should provide a small
`paper-build.toml` and select a venue profile; they should not copy a large
paper-specific `build_word.py`.

## Retired architecture policy

The S01–S10 folders, stage resolver, S-page creator, and S03/S04 probe tooling
are archive material. New work must not reference them. An old paper is migrated
only on explicit request, with the old files preserved and the new build checked.

After changing a Paper skill, run the static validators, repository checks, and
a realistic fresh-context agent test before calling it complete.
