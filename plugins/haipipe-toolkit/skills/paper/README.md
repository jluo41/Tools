# Paper skill family

`paper/` composes a manuscript from evidence-bearing Board Pages. The active
architecture is Page-first. The former numbered S-stage runtime was retired
and DELETED 260822. The current Paper runtime has one prospective blueprint:
the Story. Its Seed, Discovery Roadmap, Task Roadmap and Section Narrative
are defined by `haipipe-paper-story`; retired Page names are not aliases.

## Active architecture

`haipipe-paper` routes requests to the relevant owner. The Paper Runs layer is
owned by `haipipe-paper-workflow`: `ref/run-workflow.md` defines bounded Specs,
dependencies, routes and completion; the Runtime indexes actual native Runs.
Ideation/Story/Section/Round/Venue Pages hold content. G0–G5, sync, routing and
Page controller passes are controls. Step and Version stay inside a Run.

Use `haipipe-ideation` for generation/testing/selection and
`haipipe-paper-ideation` for the Paper Page projection. Both Paper and Page
entrypoints load the adapter when that Page is involved. Discovery/Task execute
external supporting work; Page RP/RE/RD own writing, local evidence and Page
delivery. The assembler composes Section outputs; Round routes feedback back
to its exact owner. Skills are loaded as needed, not all at once.

Each Page runs the shared workflow and owns the evidence it uses:

```text
CONTEXT → OUTLINE (SHAPE/SURVEY) ⇄ EVIDENCE (LAND/EMBED) → CONTENT (WRITE) → CHECK

Evidence Item graph
├─ Supporting Runs   Execution/Discovery 0..N · planned at SURVEY
└─ Local Run         Page · Evidence Item exactly 1 · executed at LAND

<page-dir>/
├── <page>.md
├── outline/     plan + nested Evidence Workspace (CITE/VALUE/DISPLAY + Run lineage)
├── workflow/    controller/Run receipts
├── scripts/     optional owned implementation
├── runs/        optional Page-owned interaction or Paper-local Run tickets
├── results/     Folder-local Results
├── delivery/    page-level render outputs (latex/ · word/ · render/)
└── studio/      human chat and drawing room
```

Evidence Items are typed (`CITE`, `VALUE`, `DISPLAY`) and live in the nested
Evidence Workspace. Supporting Run Results and the single Page-local Run
provide the material; no `pagex/`, `probe/`, or standalone value lane is a
current write target.

New local work uses the shared typed RP/RE/RD grammar. Read
`haipipe-paper/ref/run-naming.md` for Paper judgment IDs, owner/worker boundaries
and historical `pm-/pa-/pr-/pj...` or compact `rp00/rpNN` records. Existing
identities are not renamed; reused Results keep their exact native address.

There is no View layer and no Paper-level Literature, Value, or Display Page
Type or workbench. CITE, VALUE, and DISPLAY are typed Results presented in the
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
├── haipipe-workbench-paper/
│   ├── SKILL.md              the Paper Board-level work console contract
│   └── ref/                   Space mapping and presentation references
├── haipipe-paper-workflow/
│   └── SKILL.md              Run Spec list, native Runtime index and G0–G5 controls
├── haipipe-paper-assemble/
│   ├── SKILL.md              complete-paper source-driven DOCX/PDF contract
│   └── ref/                   config example and assembly references
├── haipipe-paper-ideation/  research-question Ideas PageType projection
├── haipipe-paper-story/     Paper Story PageType / prospective blueprint
├── haipipe-paper-section/   manuscript Section PageType
├── haipipe-paper-round/     feedback Round PageType
│                             (retired literature/value/display/dash PageTypes deleted 260822)
├── haipipe-paper-venue/   shared Venue PageType: a QBv bank record
├── venue/                    the shared QBv desk bank (bank/), prose playbooks,
│                             and the literature bank
```

## Contract and validation status

Read the owning skills for current versions and gates; this index does not
duplicate their status tables. Story remains a v0.x design draft. Neither
skill promotion nor outline promotion is implied by editing or passing tests.

The example `examples/Project-Personality-OpioidRx/papers/Paper-AgreeablePrescriptionDiscretion`
contains a Story and a `delivery/build.py` compile-order consumer. Inspect its
actual Page and receipts before reporting migration or approval status; a
skill edit alone does not certify the example's content.

## Complete-paper document build

There are two different Word exports. `haipipe-workbench-page/ref/delivery.md` renders one Page
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
