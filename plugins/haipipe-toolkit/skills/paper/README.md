# Paper skill family

`paper/` composes a manuscript from evidence-bearing Board Pages. The active
architecture is Page-first. The former numbered S-stage runtime was retired
and DELETED 260822. The current Paper runtime has one prospective blueprint:
the Story. Its Seed, Discovery Roadmap, Task Roadmap and Section Narrative
are defined by `haipipe-paper-story`; retired Page names are not aliases.

## Active architecture

The journey is owned by `haipipe-paper-workflow`, each position named by
its authority page; the venue bank is a library outside the journey:

```text
P0 Ideation (ideate)        Story00-ideation · the repo is minted with this page ·
                            sends one idea to its Story
P1 Story (establish)        Story<Letter>-<desk>-<idea-slug> · one idea, one prospective paper
                            Seed C1–C5 · Discovery Roadmap C6 · Task Roadmap C7
                            Section Narrative C8 · derived compile-order block
P2 Evidence/Execution       a work lane, not a page · Discovery blocks, Task
                            blocks, Runs in examples/<Project>/ · receipts land
   ↺ P1↔P2 = the settle loop   back on the Story (G2)
P3 Section (realize)        one page per §8 row · a person releases each row (G3)
   Compile (a verb)         haipipe-paper-assemble · anytime · G4 READY vs DRAFT
P4 Round (respond)          in the desk's Bc group · routes each concern once →
                            Story C5–C8 / owning Section · gates G0-G5 in
                            the workflow file
```

Each Page runs the shared workflow and owns the evidence it uses:

```text
CONTEXT → OUTLINE (SHAPE/SURVEY) ⇄ EVIDENCE (LAND/EMBED) → CONTENT (WRITE) → CHECK

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

There is no View layer and no Paper-level Literature, Value, or Display Page
Type or plugin. CITE, VALUE, and DISPLAY are typed Results presented in the
Outline Evidence Workspace of the Page that consumes them.

## Paper layout

```text
Paper-<Slug>/                        no 0-paperboard/ wrapper · board.md at the root
├── board.md                         paper-root: .
├── A1-Story/
│   ├── Story00-ideation/            the idea pool
│   └── StoryA-misq-phytrait-discretion/                     one Story = one idea · prospective blueprint
│       └── StoryA-misq-phytrait-discretion.md               Seed · Discovery / Task Roadmaps · Section
│                                    Narrative + derived compile-order block
├── Ba-<desk>-Main/  Bb-<desk>-Appendix/  Bc-<desk>-Round/
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
├── workflow-phases/          Paper journey contracts with a Page carrier
│   ├── haipipe-paper-ideation/     P0 · candidate ideas and selection
│   ├── haipipe-paper-story/        P1 · Paper Story prospective blueprint
│   ├── haipipe-paper-section/
│   └── haipipe-paper-round/
│                             (retired literature/value/display/dash Page Types deleted 260822)
├── haipipe-paper-venue/   the one non-phase Page Type: a QBv bank record
├── venue/                    the shared QBv desk bank (bank/), prose playbooks,
│                             and the literature bank
```

## Contract and validation status

Read the owning skills for current versions and gates; this index does not
duplicate their status tables. Story remains a `0.9.1` design draft. Neither
skill promotion nor outline promotion is implied by editing or passing tests.

The example `examples/Project-Personality-OpioidRx/papers/Paper-AgreeablePrescriptionDiscretion`
contains a Story and a `delivery/build.py` compile-order consumer. Inspect its
actual Page and receipts before reporting migration or approval status; a
skill edit alone does not certify the example's content.

## Complete-paper document build

There are two different Word exports. `haipipe-plugin-delivery/ref/word.md` renders one Page
for coauthor review. `haipipe-paper-assemble` builds the complete manuscript
from the Section Pages' own `delivery/latex/<page>.tex` body fragments,
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
