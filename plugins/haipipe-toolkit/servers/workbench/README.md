# Workbench · the base: Studio and Guide, reused by every theme

(Renamed from `workbench-shared`, 261007. Each theme is a sibling `workbench-<theme>`; the base
with no theme on top is the vanilla workbench. The `shared` route row and `/w/shared` keep
their names.)

The frame: shared Guide and Studio, five work Spaces (frame.py)
--------------------------------------------------------------

`GET /_board/workbench?path=<folder>[&space=<Space>][&sub=<subspace>][&studio=1][&theme=<name>][&format=json]`
draws any Block, Job or Task folder in one frame (`frame.py`, route `frame_view.py`):

```text
Guide · Studio | Block · Job ▾ · Task ▾                         top navigation
Description | Report | Work Details | Runs · Delivery          work mode only
<subspaces>                                                             the third row
content                                                    │ Runs panel (runs_panel.py)
```

Studio has one entry immediately after Guide and before the Block / Job / Task controls
(261010, b03 s02-D07–D09). Like Guide, it opens a shared view: only Studio is highlighted,
and the work Space and subspace rows are absent. Inside Guide, Index is the first button,
before Description, Method, RoadMap Draw and Related Paper (s02-D12). It leaves the whole
workbench for the SPACE's studio index, including from the embedded Guide. Its destination
defaults to /?view=radial&measure=studios and may be set with the host's --index-url or
INDEX_URL setting. Studio's title is `<Theme> · Studio · <Block tag> · <Block name>`.
The topics, Disk, topic sessions and new-topic prompts all use the owning Block, including
when opened from a Job or Task. A theme's Studio content is taken from its Block adapter.

`studio=1` preserves `path`, `space` and `sub` as the work context. Clicking a level returns
to that work view; an open Job or Task has a clickable level button and a sibling picker in
Studio. The older `space=Idea Studio` links open this same shared view, returning to Description
when no work Space was supplied. The plain Block button keeps its tag in the page title.
The Report button is shortened from Audience Report (s02-D10); existing `space=Audience Report`
links and theme adapters keep their names.
Studio topics may record **Tags:** (or one **Type:**) in their notes, separated by commas,
middle dots or vertical bars. One topic may have several tags. The shared list shows each
tag on its row. Current comes first, tag groups follow, and All comes last. An sNN is one
topic; a group is a set of topic references. Drag a card by its handle into Current, or use
Add to Current / Remove from Current. Current is personal to this browser and origin,
saved in localStorage under the Block's relative path, and shared across that Block's
Block, Job and Task views. It does not sync to another browser or machine. A failed save
keeps the old selection and reports the failure. Current is the default view; its empty
state points to All. The URL stores studio_group=current/all or the existing studio_tag.
Existing Job and Task topics are listed with their source until their files are moved;
a Source picker can narrow the list. Repeated sNN names use their source-qualified path
for membership and anchors, so two old topics cannot overwrite each other. All clears
the Source filter. The SPACE index counts this same list. No source files are moved or
renumbered by grouping. New topics still go into the owning Block's studio/.
A direct topic anchor reveals its row even when a saved filter would hide it.
Topic-to-Job construction, linked-topic filters and migration of existing local Studios remain
separate work in s02's Open list; this update does not move their files.

Two words keep apart: the **level** Task (a `tNN_<task>/` folder, a Task / Page in every theme)
and a **theme** (work, discovery, paper, insight, design, cowork, labeling; the old "task" theme is
work). The base owns the levels, shared Guide and Studio, the five work Spaces and their order, the third row, the
Runs panel and the look; `task-page/` holds the Page Task's own views (outline, evidence, value,
delivery, exports).

**A theme** is `servers/workbench-<theme>/<theme>_theme.py` exporting `THEME = Theme(...)`:
`name`, `label`, `icon`, `guide` (its Guide family), `levels`, `level_names`, and
`spaces(level, folder, root, sub) -> {Space name: Space(html, subspaces, open, run_types)}`.
Each run type is `{"label", "prompt", "skills"}`: every button names the skill that owns it
(b03 s21, 261007; the vanilla buttons' owners are listed in haipipe-run's
`ref/run-types-by-space.md`), and a theme's own buttons name theirs the same way.
A level with no folders shows a greyed tab, so every page keeps one tab row; a theme may set
`hide_empty_levels=True` to leave it out instead.
Anything it leaves out is the **vanilla** default, read from the standard folders: the face
`.md`, `studio/`, `reports/qNN_*/` (Question │ Work │ Report), the child `jNN_` / `tNN_`
folders, `runs/` (grouped by run type from `run.yaml`) and `delivery/`. With no theme the folder
opens as the vanilla workbench. `/w/<block>`, `/b/<block>` and every SPACE Home card open
here (261007). The page has no band line (JL 261007): the level tabs say where you are, and the
folder's path is the title's tooltip. The theme is the folder's Theme folder (`tasks/` or `work/` →
work, …) unless `theme=` names one. Example: `workbench-work/work_theme.py`. Helpers a theme may import
from `live.frame`: `Space`, `Theme`, `face`, `chain`, `children`, `runs_of`, `esc`, `link`, `reader`, `rel`,
`table`, `title`, `fields`, `studio_cards`, `pop`. Tests:

`_host/tests/test_frame.py`.

Studio and Report follow b03's `studio/s04-studio-and-report` (s02-D04, D06):

- **Studio** (`studio_cards`): one closed row per studio topic, by name, with one line:
  decided (`sNN-Dxx` lines) · open (its Open list) · sessions · feeds (Question chips, each
  popping out that report). A click opens the row in place: how it is made ("built by
  `build_*.py`", view only; or drawn by hand with Edit, which switches the canvas to the editor in
  place), the notes and any other drawings as pop-out links, the **Topic:** line, and the live
  drawing across the row, loaded only when opened. ↗ pops the topic out full size;
  `#topic-<name>` in the address opens that row. A topic's sessions are the passes of
  `runs/run-draw-<sNN>/passes/pNN-<MMDD>/` (and its older `chat/*.md` until they move), listed
  under "Save this session" in the Runs panel (`studio_sessions`).
- **Report** (`question_rows`, stored Space key `Audience Report`): one row per Question of the level's register (the
  face's `## Questions` yaml), plus any `reports/qNN_*/` not yet registered; the third row is
  All · its groups. Logic: id, title, answer-status, and "from the Studio": the topics whose
  **Feeds:** name it, each popping out its drawing. Work: the Jobs and Tasks whose face says
  `answers: <id>`, then the register's `work`. Report: the title (the Page in the pop-out), the
  Opening's first paragraph, `qNN_<topic>.png` as a thumbnail (its generated drawing, view only,
  in the pop-out) and a tag. A Task with no reports shows its own face as the report.

The frame's page carries the base's shared styles and no theme's own (JL 261007, "base styles only"):
a theme's Space html uses only base classes: the frame's `.topic` folds (`.topic.missing`: a dashed
card awaiting a Run), `.wf-table`, `.q-row`, `.chip`, `.mut`, the status marks `.st-ok` and
`.st-warn`; `SPACE_VIEW_CSS` (`task-page/space_views.py`: Space tabs and views, evidence tables, the
Supporting Runs tree) and `WORK_ITEM_CSS` (`work_items.py`: the `bj-` and `lw-` work rows). A
component a theme lacks goes into the base for every theme. `_host/tests/test_frame.py` StyleTest
keeps these styles off the frame's own parts.

A run type may carry `rows` (Runs panel cards). `pop(href, label)` opens any link in the frame's
pop-out (an in-page window with "Open in its own tab").

A theme may name its levels, pick which levels it has, name the subspaces of each Space, fill a
Space and list its run types. It may not change the levels, the six Spaces or their order, draw
its own tab rows, or carry its own look; ask the base's owner (design Block b03) for a frame change.

This folder holds what every Workbench family reuses instead of owning a copy:

| Component | Writes? | Contract | What it serves |
|---|---|---|---|
| **Studio** | Yes, through its own routes | [workbench-studio](../../skills/1_base/page/workbench-studio/SKILL.md) | The live Excalidraw editor and its save path, the chat (GUI) and terminal (TUI), the ✨ Draw it and ✨ deck pens |
| **Guide** | Never | This README | Family explanations: skills, methods, UI and folder maps, RoadMap Draw |

Any Workbench that shows a drawing (Paper Story › RoadMap Draw, Task Scope ›
RoadMap Draw, a Page's 🎨 Studio tab, Guide's own canvases) opens it through
Studio's `xcal.py` and `excalidraw_proxy.py`. A family owns *which* drawing
and *where* it lives; Studio owns how a scene is opened, minted and saved.
Guide embeds the same canvas in its isolated viewing mode and never saves.

## Each theme's Guide: guide/ and related/ (261007)

A theme's Guide lives with its server folder, and the base only reads it:

```text
servers/workbench-<theme>/            (the base: servers/workbench/; the Page Task: workbench/task-page/)
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
`servers/workbench/task-page/guide/guide.yaml` (family `page`). Check: `_host/tests` and the
Guide page `/_board/guide?family=<family>` for each of its four Views.

Where things stand (261007): every family (shared, page, task, paper, labeling, discovery, cowork,
design, insight) reads from its `guide/guide.yaml`; `guide_families.py` keeps no family entry of
its own, only the loader and the fallback for a family that has none yet. A theme
may keep its methods canvas in its design Block instead of `guide/` (design keeps it in its b12
studio, and `guide.yaml`'s `method_drawing` names it there). The b03 script
`studio/s31-guide/method-canvas.py` reads both layouts: it titles `<server>/guide/method.md`
from the server folder's name and finds the Workbench Table from `guide.yaml`'s `table:`.

## The card Guide: by level, as cards (levels.yaml, 261007)

The design is b03's `studio/s31-guide` (s31-D05 to D09). A family whose `guide/guide.yaml` declares
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
  `Tools/blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/s31-guide.excalidraw`, read off the code.

## Studio

| File | Responsibility |
|---|---|
| [xcal.py](xcal.py) | `/_board/excalidraw` editor routes, scene minting (`mint_board_scene`) and `/_board/excalidraw-save`. |
| [excalidraw_proxy.py](excalidraw_proxy.py) | Proxy to the local Excalidraw service; injects [assets/xcal-boot.js](assets/xcal-boot.js), which arms a save only after the first gesture. |
| [autodraw.py](autodraw.py) | `/_board/autodraw`: `claude -p` authors a scene from the Page's `.md`. |
| [chat.py](chat.py), [turnring.py](turnring.py) | The GUI chat: sessions, the SDK turn, context priming, the turn ring. |
| [term.py](term.py) | The TUI: PTYs, parking, and the vendored xterm under `assets/vendor/xterm/`. |
| [autodeck.py](autodeck.py) | `/_board/autodeck`: `claude -p` authors the Page's slide deck. |
| `assets/js/10-drawer/`, `assets/css/86-*.css` | Drawer parts, concatenated into `board.js` / `board.css` by `_host/host_assets.py`. |

Its routes form the `shared` row of `_host/host_registry.WORKBENCH_ROUTES`;
a `--only` host without `shared` serves no terminal, chat or drawing save.
The lane contracts are [ref/draw.md](../../skills/1_base/page/workbench-studio/ref/draw.md)
and [ref/chat.md](../../skills/1_base/page/workbench-studio/ref/chat.md).

## Guide

A new workbench family fills its Guide by the checklist in `../README.md` § Adding a workbench.

Guide has four Views: **Description** (what the Workbench does), **Method**
(its steps, as text), **RoadMap Draw** (one drawing of its skills, method,
Workbench and folders) and **Related Paper**. Guide's UI design artifacts (once this folder's `studio/`) live in
the b03 design Block (`Tools/blueprints/b01_haipipe-toolkit/j03_project_workbench/`), not here: `studio/s31-guide/` (the Guide tab, one screen per View, each
family's status; `method-canvas.py`; the 261002 design in its `history/`). The base's RoadMap Draw is
`studio/s02-workbench-shared/` (the frame). The Studio runtime stays.

The design follows the existing Paper and Insight studios: white surfaces,
light gray panels, blue selected tabs, and named Spaces and Views. The View
row stays directly below the Space row, leaving the content its full width.

## Space order

Every workbench lists its Spaces in one order (JL 261003):

```text
Guide  ->  setup  ->  work  ->  Delivery
shared     the input      the processing     shared
name       and its        and its output     name
           design
```

1. **Guide** comes first and has the same name everywhere: it explains the family.
2. **Setup** Spaces follow: what is fixed before the work starts. Each keeps its own
   name, because each family sets up something different; a family without a setup step
   starts with its work.
3. **Work** Spaces come next, in the order the work flows: input, then processing,
   then output.
4. **Delivery** comes last and has the same name everywhere: what is finished leaves here.

| Family | Setup | Work | Delivery |
|---|---|---|---|
| Insight | Scope (the data) · Prototype (the questions and their scripts) | Insight · Check | Delivery |
| Labeling | Data | Labeling · Quality | Delivery |
| Design (page) | Design Task | Design Item | Delivery |
| Paper | none | Ideation · Story · Sections | Delivery |
| Page | none | Draft · Evidence | Delivery |
| Task | Scope (the Block, its Questions, data and drawings) | Task · Check | Delivery |

"Setup" names a role, not a tab: tabs keep their family's own words.

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
| [guide_families.py](guide_families.py) | Family-owned skill sources, methods, working Space descriptions and folder conventions. |
| [workbench_guide.py](workbench_guide.py) | Guide presenter, source resolver, deterministic Excalidraw scenes and SVG projection. |
| [shared_workbench.py](shared_workbench.py) | The Shared Workbench's own site, laid out like the other workbenches, with Guide as its only Space. |
| [assets/guide-mount.js](assets/guide-mount.js) | Guide button, the View frame directly under the Space row, and return to the native working surface. |
| [assets/guide.js](assets/guide.js) | Independent drawing folds, lazy canvas loading, fold memory and frame height. |

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

## Questions lead progress

The primary reading is: **what is the question, what answer do we have, what
supports it, and what remains open?** Related execution is shown as Work.
Question progress can come from design reasoning, an Insight report, a paper
claim, evidence review or other records owned by that workflow.

Paper's existing folding layout is the reference:

```text
Question                                  closed: answer + remaining issue
└── Expanded question
    ├── Answer and reasoning               hypotheses / claims / evidence
    └── Related Work
        ├── Shared preparation             also for another question
        └── Expanded Work
            └── Block
                └── Job
                    ├── Task               expands its Runs
                    │   └── Run            receipt + Result
                    └── Another Task
```

Jobs, Tasks and Runs stay together in this hierarchy. The reader can open a
Question, then its Work, then a Task's Runs without switching between separate
execution tabs. Closed Questions lead with the current answer and open issue;
closed Work keeps its role and references visible.

- A Question can have reasoning or a Report before it has any BJTR work.
- Work can support several Questions. Its native owner is retained; other
  Questions refer to it.
- Work without a Question remains visible under Paper's existing
  **Not under a question** fold.
- A completed Run contributes an execution receipt. The question's answer,
  evidence and remaining review are read from the owning Question / Report.
- The answer states in the drawing are illustrative. Each family keeps its
  native marks and acceptance rules; this proposal introduces no universal
  question-status enum or question database.

## Family examples

| Family / Space / View | Proposed reading |
|---|---|
| Paper / Story / High-level logic + low-level work | Collapsible Questions. An open Question shows reasoning beside Work; BJTR is nested together inside that Work. |
| Insight / Insight / Questions | Keep the partition's Logic / Work / Report columns and DIKW folds. The Question and its answer lead; related Runs and Reports stay alongside it. |
| Task / Task / each group | Insight's partition table: one View per register `group:`, a row per Question with Logic / Work / Report columns. Report Pages live in `reports/`; the Block's drawings, the generated question map first, are Scope › RoadMap Draw (`studio/`). |
| Other family-owned working Views | Place goals, design questions, Studio, evidence and checks according to the family's native workflow. |

The components may be reused across families. The layout, question semantics,
source files, actions and Run Type skill declarations stay with their owners.
This design creates no copied ledger or required `goal/`, `design/` or
`checklist/` directories. A working Studio retains its existing owner contract
for drawing and chat.

All example questions, names, counts and states are illustrative.

## Explanatory Views and RoadMap Draw · earlier five-View design

The scenes in this section record the earlier design, with Skill set, Methods,
Workbench and Folder map as separate Views. Guide now shows them as one
RoadMap drawing; see **Guide** above.

The design studio supplies editable Excalidraw examples. Each explanatory View's drawing is a
collapsible row above vertically stacked written explanations.
**RoadMap Draw** is an additional View under Guide with a **single-column
list**, one row per explanatory drawing. The **Diagram types** catalog uses
the same layout. Space and View navigation remain two horizontal rows.

- A collapsed row shows the drawing name, purpose and preparation state.
- Clicking its header expands requirements, the embedded canvas and sources
  directly beneath that same header. Clicking again collapses the row.
- Rows open independently; several drawings may stay open together.
- **Open full screen** opens the same drawing and returns to its row.
- Collapsing preserves the drawing file, content and local editing state.
  A missing drawing keeps its row and names what still needs preparation.

The design artifacts below use the Paper family, matching v4's Guide example. They explain
family roles and structure. Switching Paper instances keeps these explanations;
another Workbench family supplies diagrams based on its own contracts.

| Guide View | Drawing explains | Editable scene |
|---|---|---|
| Skill set | Skill map: named skills, responsibilities, native owners and labeled relationships. | [Excalidraw](../../../../blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/history/guide-views/parts/guide-skill-set.excalidraw) |
| Methods | Method flow: question, reasoning, missing evidence, optional Work, interpretation, answer and remaining issues. | [Excalidraw](../../../../blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/history/guide-views/parts/guide-methods.excalidraw) |
| Workbench | UI map: the Guide and each family's working Space / View structure. | [Excalidraw](../../../../blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/history/guide-views/parts/guide-workbench.excalidraw) |
| Folder map | Linked graph: Space / View → native owner → folder / file, with repository and external paths marked. | [Excalidraw](../../../../blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/history/guide-views/parts/guide-folder-map.excalidraw) |
| RoadMap Draw | Expand each of the four explanatory drawing rows to read its embedded canvas or open it full screen. | [View design](../../../../blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/history/guide-views/parts/guide-roadmap-draw.excalidraw) |

- [All five Guide Views, as they appear in Guide](../../../../blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/history/guide-views/s02-guide-views.excalidraw)
- [Drawing generator](../../../../blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/history/guide-views/build_s02_guide_views.py)

Diagram nodes are grouped for editing. RoadMap Draw embeds the four existing diagram files in
their own rows. It explains the
family's skill and Workbench design; instance-owned working roadmaps stay with
their family's working Spaces. The runtime creates family-specific scenes from
the source bindings above; the design studio remains the editable reference.

### Folder map reading and navigation

Folder map uses connected nodes. Start at a Space or View, follow **reads**
to its native owner, then **defined in** or **stored at** to the folder or
file that supplies it. Repository definitions, instance-relative paths and
external work homes are explicitly distinguished. The Paper example uses
the existing storage and writer contracts; its folder patterns are relative
to `Paper-<Slug>/` unless marked otherwise.

In the runtime, a folder or file node opens its resolved native
source. Guide explains the family's conventions; actual paths resolve from
the selected instance's existing records, such as Paper's `board.md`. A
missing source retains its node and preparation reason. Changing the map
does not move folders or change record ownership. The same source links also
appear below the diagram for keyboard and screen-reader access. External
stores are named as conventions; Guide does not follow them outside the root.

## Predefined drawing types

[drawing-catalog.json](../../../../blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/history/guide-views/drawing-catalog.json) defines the drawing types. Each
entry fixes a reader question, required elements, expected source owners and
placement. Diagram types are shared across Workbench families; their concrete
names, relationships, sources and states come from the selected family or
instance. Guide draws its four types at run time from `guide_families.py`.

| Placement | Type | Reader question | Required content |
|---|---|---|---|
| Guide | Skill map | Which skills do what, and how do they cooperate? | Named skills, responsibilities, owners and labeled relationships. |
| Guide | Method flow | How does this family turn a question into an answer? | Question, reasoning, evidence needs, optional work, interpretation, answer, limits and revision. |
| Guide | UI map | Where do I go to do or read something? | Guide and working Spaces, their Views and purposes, Space row followed by View row. |
| Guide | Folder map | Which files and owners supply each part of the UI? | Family sources, View-to-owner-to-path mapping and native work/product ownership. |
| Owning working Draw / Studio | Question map | What matters, what is answered, and what remains open? | Goal, questions, current answer or its absence, evidence, open issues and optional Work references. |
| Owning working Draw / Studio | Design map | How is the proposed solution structured, and why? | Scope, components, boundaries, flows, decisions, question references and acceptance criteria. |
| Owning working Draw / Studio | Work roadmap | What comes next, what depends on what, and when is it ready? | Milestones, dependencies, deliverables, readiness criteria, related questions, native owners and available owner state. |

The four Guide diagrams are the expected family introduction. The three
working types are optional references; the shared drawing component imposes
no type selection, source binding, status field or metadata form on a working
Studio. Each family owns its working Space and View composition and drawing
semantics. A missing Guide drawing stays visible as **Not prepared**, naming
the missing source.

**Task alignment:** Task's Scope › RoadMap Draw is a freeform single-column list (after its generated question map),
with freely named Drawing 1 / Drawing 2 / Drawing 3 rows and an Add drawing
action. Opening a row embeds its Excalidraw; several rows may stay open. It
requires no Topic hierarchy, registered type or content fields.
The shared capability is the folding row and embedded drawing surface.
Guide's Folder map explains the family's folder conventions; a Task drawing
may freely sketch a current Question's actual folders and paths. Question
cards retain their own Logic / Work / Report columns. A single-column
drawing list does not require the contents of every working View to use one
column. Task's working UI and its save actions are implemented by the Task
Workbench; Guide supplies its family explanations and folder conventions.

A family-specific extension declares an id, reader question, required
elements, sources and placement before becoming a standard type. Freeform
working drawings need no type registration. Generated diagrams remain owned
by their generators; preserve separately edited scenes before regenerating.

## Current artifacts · Guide v4

- [Editable Excalidraw scene](../../../../blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/history/guide-design/s04-guide-design.excalidraw)
- [Generator](../../../../blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/history/guide-design/build_s04_guide_design.py)

The generator owns these generated artifacts. Keep independently edited
Excalidraw copies under another filename before regenerating.

```sh
python3 blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/history/guide-design/build_s04_guide_design.py
python3 blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/history/guide-views/build_s02_guide_views.py
```

`studio/` keeps only the Excalidraw scenes and their generators. Each generator
writes its scene with the Python standard library. Add `--previews` with Pillow
installed to render local PNG previews; `studio/.gitignore` keeps PNG and SVG
out of git. Optional `--font`
and `--mono-font` paths control preview fonts; the scene uses the same
Excalidraw font IDs as the existing Paper and Insight drawings.

## Earlier proposals · superseded

These remain for comparison. Their sharing boundaries do not describe the
current proposal:

- [v3 scene](../../../../blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/history/guide-design/workbench-shared-guide-v3.excalidraw): horizontal Views;
  explanatory and instance Views were both in Guide.
- [v2 scene](../../../../blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/history/guide-design/workbench-shared-guide-v2.excalidraw): the earlier grouped
  sidebar, with both kinds of Views in Guide.
- [Original scene](../../../../blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s31-guide/history/guide-design/workbench-shared-design.excalidraw): the initial
  proposal before the Guide boundary was settled.

## References

- [Workbench design principle](../../../../blueprints/b01_haipipe-toolkit/j03_project_workbench/j03_project_workbench.md)
- [Paper Workbench implementation](../workbench-paper/paper.py)
- [Paper workflow contract](../../skills/2_theme/paper/haipipe-paper-workflow/SKILL.md)
- [Paper Story contract](../../skills/2_theme/paper/haipipe-paper-story/SKILL.md)
- [Paper Workbench contract](../../skills/2_theme/paper/workbench-paper/SKILL.md)
- [Paper design studio](../../../../blueprints/b16_theme_paper/studio/s05-board-job-task-boundary/s05-board-job-task-boundary.excalidraw)
- [Insight Workbench implementation](../workbench-insight/insightboard.py)
- [Insight design studio](../../../../blueprints/b11_theme_insight/studio/s02-insight-workbench/insight-workbench-design.excalidraw)
- [Studio contract](../../skills/1_base/page/workbench-studio/SKILL.md)
