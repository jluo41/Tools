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
external supporting work; Page Runs (`run-<kind>-…`) own writing, local evidence and Page
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
├── draft/       plan + nested Evidence Workspace (CITE/VALUE/DISPLAY + Run lineage)
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

Every Run has a full name: Page Runs `run-<kind>-<slug>`, Paper judgment
Runs `run-paper-<judgment>-<slug>`. Read `haipipe-paper/ref/run-naming.md`
for the names and owner/worker boundaries. Older short names are retired; reused
Results keep their exact native address.

There is no View layer and no Paper-level Literature, Value, or Display Page
Type or workbench. CITE, VALUE, and DISPLAY are typed Results presented in the
Outline Evidence Workspace of the Page that consumes them.

## Paper layout

The paper is a Board on the ladder (`haipipe-paper/ref/paper-ladder.md`; b16 Q01, Q04, Q05):

```text
Paper-<Slug>/                        Block: board.md · studio/ (s01-ideation, sNN-story-<desk>-<idea>) ·
│                                    reports/qNN_ · runs/ · venues/<venue>/ · related/related.md
└── jNN_v<MMDD>_<desk>/              Job: one send · its face (## Narrative, ## Questions) · studio/ reports/ runs/
    ├── t00_abstract · t0N_<title>   Tasks: the Abstract and the Main Sections; t2N_ the Appendix
    ├── t3N_<title>                  letters: t31_cover-letter · t32_response
    ├── reports/qNN_<kind>-<MMDD>/   a comments report
    └── delivery/                    GENERATED from the Sections' own delivery/latex/<page>.tex fragments
```

An older Board (`A1-Story/`, `Ba-`/`Bb-`/`Bc-<desk>-…` groups, a root `delivery/`) is still read; the carry-over
scripts (`haipipe-paper/scripts/carry_over/`) move it onto the ladder once.

## Active files

```text
paper/                              by the level each serves
├── haipipe-paper/                  all: the door, the ladder contract (ref/paper-ladder.md), the scaffold
│                                   (scripts/paper_ladder.py), the one-time carry-over (scripts/carry_over/)
├── haipipe-paper-workflow/         all: the run cards by <Level> › <Space>, gates G0-G2 (Board) and G3-G5 (version)
├── workbench-paper/                all: the paper theme on the shared frame; ref/workbench-table.md
├── haipipe-paper-ideation/         Board: studio/s01-ideation/ and the ideation Questions
├── haipipe-paper-story/            Board: each telling as a studio topic, its Questions, the Narrative
├── haipipe-paper-venue/            Board: venues/<venue>/ and the shared Venue Pages (QBv bank)
├── haipipe-paper-comments/         version: comments reports, Review Items (scripts/review_items.py)
├── haipipe-paper-assemble/         version: the build, the cover letter, send and release
├── haipipe-paper-section/          Section: one Section, the Abstract or a letter (a Page Task)
├── tests/                          the family's tests (the ladder scaffold, run naming)
└── venue/                          the shared QBv desk bank, prose playbooks and the literature bank
```

## Contract and validation status

Read the owning skills for current versions and gates; this index does not
duplicate their status tables. Story remains a v0.x design draft. Neither
skill promotion nor outline promotion is implied by editing or passing tests.

A paper Board in a Project's `paper/` folder is the working example. Inspect its actual Pages and receipts
before reporting migration or approval status; a skill edit alone does not certify any paper's content.

## Complete-paper document build

There are two different Word exports. `workbench-page/ref/delivery.md` renders one Page
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
