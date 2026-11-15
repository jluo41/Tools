# Guide: each theme's Guide, the card Guide, sharing boundary and runtime

Part of the [Workbench base README](../README.md).

## Guide

A new workbench family fills its Guide by the checklist in `servers/README.md` § Adding a workbench.

Guide has four Views: **Description** (what the Workbench does), **Method**
(its steps, as text), **RoadMap Draw** (one drawing of its skills, method,
Workbench and folders) and **Related Paper**. Guide's UI design artifacts (once this folder's `studio/`) live in
the b10 Workbench Block (`Tools/blueprints/Project-Ladder/work/b10_project_workbench/`), not here: `s31-guide/` (the Guide tab, one screen per View, each
family's status; `method-canvas.py`; the 261002 design in its `history/`). The base's RoadMap Draw is
`s02-studio-workbench-skill/` (the frame). The Studio runtime stays.

The design follows the existing Paper and Insight studios: white surfaces,
light gray panels, blue selected tabs, and named Spaces and Views. The View
row stays directly below the Space row, leaving the content its full width.

## Each theme's Guide: guide/ and related/ (261007)

A theme's Guide lives with its server folder, and the base only reads it:

```text
servers/workbench-<theme>/            (the base: servers/workbench/; a Task type: workbench-task-<type>/)
├── <theme>_theme.py                  the theme on the frame
├── guide/                            Guide › Description · Method · RoadMap Draw
│   ├── guide.yaml                    family, label, presenter, description, method steps, spaces,
│   │                                 folders, skills, boundary, explain (its RoadMap drawing), table
│   ├── method.md                     the method page, its cards in methods/
│   ├── methods/                      one card per method
│   └── methods.excalidraw            the methods canvas (the canvas is its source)
└── related/                          Guide › Related Paper
    ├── papers.md                     group · role · key · paper · venue · doi · why here · pdf
    └── papers/                       open-licensed full texts, as the pdf column names them
```

`guide_families.py` loads every `guide/guide.yaml` it finds (that file wins over the family's old
entry there, which is deleted once the theme has moved). Paths in `guide.yaml`: `guide/…`,
`related/…` or a module (`paper.py`) are relative to the server folder; `skill:<skill>/<rest>` is
a skill's file, found by name (the Workbench Table stays in the skill: it is the run-type, agent
and skill contract); `Tools/…` is SPACE-relative (the RoadMap drawing, built in the theme's design
Block). Worked examples: `servers/workbench/guide/guide.yaml` (the base, family `shared`) and
`servers/workbench/workbench-task-draft/guide/guide.yaml` (family `page`). Check: `_host/tests` and the
Guide page `/_board/guide?family=<family>` for each of its four Views.

Where things stand (261007): every family (shared, page, task, paper, labeling, discovery, cowork,
design, insight) reads from its `guide/guide.yaml`; `guide_families.py` keeps no family entry of
its own, only the loader and the fallback for a family that has none yet. A theme
may keep its methods canvas in its design Block instead of `guide/` (design keeps it in its b12
studio, and `guide.yaml`'s `method_drawing` names it there). The b03 script
`s31-guide/method-canvas.py` reads both layouts: it titles `<server>/guide/method.md`
from the server folder's name and finds the Workbench Table from `guide.yaml`'s `table:`.

## The card Guide: by level, as cards (levels.yaml, 261007)

The design is b03's `s31-guide` (s31-D05 to D09). A family whose `guide/guide.yaml` declares
`levels:` is drawn as the card Guide; the others keep the Guide described above until they move
(the conformance test's `GAPS` lists them, rule `levels`). The work family moved first.

```text
Guide › <View>
  <lead line>                         Description: the family's paragraph; others: the View's question
  ▾ Block   <its role>                a heading, not a box; a click folds it
     ┌ card ┐ ┌ card ┐ …              one card shape per View, the same in every theme
  ▸ Job     6 Spaces                  folded: one line of what it holds
  ▸ Task    5 steps
  ▸ All levels                        the View as it was before the levels, closed
```

| View | card | title line | second line | from |
|---|---|---|---|---|
| Description | a Space card | Space · what it is at this level | sub · reads · runs | words: `levels.yaml` + `levels:`; sub, runs: the frame, live |
| Method | a step card | N · step · what happens | where · methods · signs | `method.md`: one step table per level |
| RoadMap Draw | a drawing card | drawing · what it shows | source · builder · ↗ full size; opens to the drawing, view only | `guide.yaml` `roadmap:` |
| Related Paper | a paper card | title · author year · venue | role · why here · ↗ doi | `papers.md` `level` column |

- **Words.** `servers/workbench/guide/levels.yaml` holds the base's words: each level's `role` and,
  per Space, `is` (what it is at that level) and `reads` (what it reads). A theme's `guide.yaml`
  `levels:` has the same shape and overrides only the words that differ (`guide_families.merge_levels`).
- **Live parts.** A Space card's `sub` (the third row) and `runs` (its run types) are never written:
  `frame.space_cards(theme, level, folder, root)` reads them through `spaces_for`, the base then
  the theme, for the open folder's own Block, Job or Task (`frame.level_folders`); a level with no
  folder shows the theme's defaults. So the Guide and the tabs cannot disagree.
- **Steps.** `method.md` gives each level a heading (`**Block · …**`, `## Job …`, or an underlined
  line) over a table `step | what happens | methods | where in the workbench | who signs`; "where"
  names one of the six Spaces (`workbench_guide.level_steps`).
- **Drawings.** `roadmap:` maps each level to a list of `{title, shows, board}`; `board` is a
  `Tools/…` drawing, served view only as `roadmap-<level>-<n>`; its builder is a `build_*.py` or
  `<stem>.py` beside it.
- **Papers.** `papers.md` leads its table with `level` (`Block`, `Job`, `Task`, `all`, several split
  by `;`); `table-papers`' check accepts it as an optional first column.
- **Folds.** The frame passes the level it shows (`context.level`, `frame.render` → `mount_guide`);
  that section starts open and the other two folded (no level: Block). `assets/guide.js` keeps a
  person's folds per family, instance and View, the level sections with the drawing cards.
- **Family key.** The work family is `work`; `guide_families.ALIASES` keeps `task` answering. A
  frame folder with no face file still opens its family's Guide, its cards read from the folder.
- **Tests.** `_host/tests/test_guide_levels.py`; the status of every family is frame 6 of
  `Tools/blueprints/Project-Ladder/work/b10_project_workbench/s31-guide/s31-guide.excalidraw`, read off the code.

## Revised sharing boundary

**Guide keeps kind 1 only:** explanations of the Workbench family's skills,
methods, UI design and mapping to folders. These documents are shared across
instances of that family. They describe how the family works.

**The former kinds 2 and 3 belong together in each family's working Spaces.**
Instance goals, design, Studio, question progress and checks appear where the
family's workflow needs them. Families can reuse UI components without sharing
an obligatory roster of Goal / Design / Studio / Progress / Checklist Views.

```text
Workbench
├── Guide Space                         family explanations
│   ├── Description View                what this Workbench does
│   ├── Method View                     its steps, as text
│   ├── RoadMap Draw View               skills · method · Workbench · folders, one drawing
│   └── Related Paper View              the papers it builds on
└── Family-owned working Spaces         this instance's work
    └── Their own Views
        ├── Questions, answers and evidence
        ├── Related Work and native receipts
        └── Goals, design, Studio and checks where needed
```

| Earlier kind | Current placement | Content scope |
|---|---|---|
| 1 · Shared explanation | Guide | The family's skill set, methods, design rationale and folder mapping. An active path may provide context. |
| 2 · Shared structure, instance content | The owning family's working Spaces and Views | This instance's goals, design, Studio, questions and checks. Reusable presentation can follow the family's native contracts. |
| 3 · Specialized instance work | The same family-owned working Spaces and Views | Domain-specific questions, evidence, work and products. |

Selecting a Space replaces the View row with that Space's Views. Guide has
its four Views; each working Space retains its
family's composition.
Guide mounts beside each family's own working Spaces. Their working content,
actions and source writers remain owned by that family.

## Runtime

The shared host mounts Guide in Paper, Task, Page, Insight, Design Board,
Design Page and Labeling Workbenches. The standalone Page host and the
dedicated Labeling Page-folder route also mount it. The Labeling family is
available only when the optional `haipipe-labeling` package is present.

| File | Responsibility |
|---|---|
| [guide_families.py](../guide/guide_families.py) | Family-owned skill sources, methods, working Space descriptions and folder conventions. |
| [workbench_guide.py](../guide/workbench_guide.py) | Guide presenter (`guide_html`), Guide › Method's family page (`method_page_html`), the HTTP mixin, and re-exports of the modules below. |
| [guide_core.py](../guide/guide_core.py) | Paths, Views, URLs, a family's profile, declared sources and `mount_guide`. |
| [guide_drawing.py](../guide/guide_drawing.py) | Deterministic Excalidraw scenes (the RoadMap) and their SVG projection. |
| [guide_tables.py](../guide/guide_tables.py) | The Workbench Table, its rows and the Guide Space's Runs panel. |
| [guide_level_cards.py](../guide/guide_level_cards.py) | The card Guide (Block · Job · Task) and `level_steps`. |
| [shared_workbench.py](../guide/shared_workbench.py) | The Shared Workbench's own site, laid out like the other workbenches, with Guide as its only Space. |
| [assets/guide-mount.js](../assets/guide-mount.js) | Guide button, the View frame directly under the Space row, and return to the native working surface. |
| [assets/guide.js](../assets/guide.js) | Independent drawing folds, lazy canvas loading, fold memory and frame height. |

`/_board/guide?family=<family>&path=<native-source>&file=<source-file>` opens
Guide. Without `path` and `file` it is the family-only Guide: drawings and
explanations come from the registry and folder patterns stay unresolved.
`/_board/shared?guide=<view>` is the Shared Workbench's own site: the same
header, band and Space row as the other workbenches, with Guide mounted as
its only Space and explaining this Workbench (the `shared` family entry).
`view=` selects `description`, `method`, `roadmap-draw` or `related-paper`;
the earlier keys (`skill-set`, `methods`, `workbench`, `folder-map`) still open
the View that now holds their content, and a family's `explain` pages for those
keys appear there. `embed=1` renders the View row directly beneath the native
Space row. A native Workbench URL can select Guide with `guide=<view>`.
All links are origin-relative.

The family registry supplies the Description, Method steps, RoadMap and
`papers`. The current instance supplies only the path-resolution context.
**Source** links open declared skill contracts; folder links resolve the declared pattern
within the selected instance. Missing or private paths explain why there is
no accessible source. Paths outside the served root and native private lanes
remain under their existing custodians. Guide creates no instance ledger.

Each drawing has **Download Excalidraw** and **Open full screen** actions.
Embedded and full-screen canvases use the existing isolated viewing mode;
Guide never calls a drawing save API. Collapsing keeps an already loaded
canvas alive, and fold state is remembered per family, instance and View.
Change family definitions in `guide_families.py`; native working Studio
files continue to use their own writers.

### Dependencies

The runtime is hosted through `../_host` and its `live` namespace. Canvases
reuse this folder's Studio `excalidraw_proxy.py` and `assets/xcal-boot.js`.
The proxy defaults to the existing local Excalidraw service on port 5610;
`EXCALIDRAW_ORIGIN` can select another existing service. An unavailable
service displays the proxy's startup instruction. SVG and Excalidraw
downloads remain available from Guide independently of that service.
The standalone Page host reuses the read-only proxy without importing Board
grammar or adding Studio writers.
