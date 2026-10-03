# Workbench Shared · Guide runtime and UI design studio

This folder implements the shared **Guide Space** and holds its UI design
artifacts. Guide has four explanatory Views, a dedicated **RoadMap Draw**
View, and a predefined drawing catalog with seven starter templates.

The design follows the existing Paper and Insight studios: white surfaces,
light gray panels, blue selected tabs, and named Spaces and Views. The View
row stays directly below the Space row, leaving the content its full width.

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
│   ├── Skill set View
│   ├── Methods View
│   ├── Workbench View
│   ├── Folder map View
│   └── RoadMap Draw View                the family's explanatory diagrams
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
four explanatory Views plus RoadMap Draw; each working Space retains its
family's composition.
Guide mounts beside each family's own working Spaces. Their working content,
actions and source writers remain owned by that family.

## Runtime

The shared host mounts Guide in Paper, Task, Page, Insight, Design Board,
Design Page and Labeling Workbenches. The standalone Page host and the
dedicated Labeling Page-folder route also mount it. The Labeling family is
available only when the optional `subjective-label` package is present.

| File | Responsibility |
|---|---|
| [guide_families.py](guide_families.py) | Family-owned skill sources, methods, working Space descriptions and folder conventions. |
| [workbench_guide.py](workbench_guide.py) | Guide presenter, source resolver, deterministic Excalidraw scenes and SVG projection. |
| [assets/guide-mount.js](assets/guide-mount.js) | Guide button, the View frame directly under the Space row, and return to the native working surface. |
| [assets/guide.js](assets/guide.js) | Independent drawing folds, lazy canvas loading, fold memory and frame height. |

`/_board/guide?family=<family>&path=<native-source>&file=<source-file>` opens
Guide. `view=` selects `skill-set`, `methods`, `workbench`, `folder-map` or
`roadmap-draw`; `embed=1` renders the View row directly beneath the native
Space row. A native Workbench URL can select Guide with `guide=<view>`.
All links are origin-relative.

The family registry supplies the four explanatory diagrams. The current
instance supplies only the path-resolution context. **Source** links open
declared skill contracts; **Folder map** links resolve the declared pattern
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
reuse `../workbench-studio/excalidraw_proxy.py` and `assets/xcal-boot.js`.
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
| Task / Task / Task | Vertically stacked collapsible Questions; each open card has Logic / Work / Report columns. Report Pages live in `reports/`, beside the Block's freeform `studio/` drawings. |
| Other family-owned working Views | Place goals, design questions, Studio, evidence and checks according to the family's native workflow. |

The components may be reused across families. The layout, question semantics,
source files, actions and Run Type skill declarations stay with their owners.
This design creates no copied ledger or required `goal/`, `design/` or
`checklist/` directories. A working Studio retains its existing owner contract
for drawing and chat.

All example questions, names, counts and states are illustrative.

## Explanatory Views and RoadMap Draw

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

| Guide View | Drawing explains | Editable scene | UI preview |
|---|---|---|---|
| Skill set | Skill map: named skills, responsibilities, native owners and labeled relationships. | [Excalidraw](studio/guide-skill-set.excalidraw) | [In Guide](studio/guide-view-skill-set.png) |
| Methods | Method flow: question, reasoning, missing evidence, optional Work, interpretation, answer and remaining issues. | [Excalidraw](studio/guide-methods.excalidraw) | [In Guide](studio/guide-view-methods.png) |
| Workbench | UI map: the Guide and each family's working Space / View structure. | [Excalidraw](studio/guide-workbench.excalidraw) | [In Guide](studio/guide-view-workbench.png) |
| Folder map | Linked graph: Space / View → native owner → folder / file, with repository and external paths marked. | [Excalidraw](studio/guide-folder-map.excalidraw) | [In Guide](studio/guide-view-folder-map.png) |
| RoadMap Draw | Expand each of the four explanatory drawing rows to read its embedded canvas or open it full screen. | [View design](studio/guide-roadmap-draw.excalidraw) | [In Guide](studio/guide-view-roadmap-draw.png) |

- [All five Guide Views](studio/guide-views-with-drawings.excalidraw)
- [Vector overview of those Views](studio/guide-views-with-drawings.svg)
- [Drawing generator](studio/guide-view-drawings.py)

Each standalone drawing also has a same-named SVG and PNG. Diagram nodes are
grouped for editing. RoadMap Draw embeds the four existing diagram files in
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

## Predefined drawing types and prepared templates

[drawing-catalog.json](drawing-catalog.json) defines the drawing types. Each
entry fixes a reader question, required elements, expected source owners,
placement and an editable starter template. Diagram types are shared across
Workbench families; their concrete names, relationships, sources and states
come from the selected family or instance.

| Placement | Type | Reader question | Required content | Prepared template |
|---|---|---|---|---|
| Guide | Skill map | Which skills do what, and how do they cooperate? | Named skills, responsibilities, owners and labeled relationships. | [Template](studio/templates/guide-skill-map.excalidraw) |
| Guide | Method flow | How does this family turn a question into an answer? | Question, reasoning, evidence needs, optional work, interpretation, answer, limits and revision. | [Template](studio/templates/guide-method-flow.excalidraw) |
| Guide | UI map | Where do I go to do or read something? | Guide and working Spaces, their Views and purposes, Space row followed by View row. | [Template](studio/templates/guide-ui-map.excalidraw) |
| Guide | Folder map | Which files and owners supply each part of the UI? | Family sources, View-to-owner-to-path mapping and native work/product ownership. | [Template](studio/templates/guide-folder-map.excalidraw) |
| Owning working Draw / Studio | Question map | What matters, what is answered, and what remains open? | Goal, questions, current answer or its absence, evidence, open issues and optional Work references. | [Template](studio/templates/work-question-map.excalidraw) |
| Owning working Draw / Studio | Design map | How is the proposed solution structured, and why? | Scope, components, boundaries, flows, decisions, question references and acceptance criteria. | [Template](studio/templates/work-design-map.excalidraw) |
| Owning working Draw / Studio | Work roadmap | What comes next, what depends on what, and when is it ready? | Milestones, dependencies, deliverables, readiness criteria, related questions, native owners and available owner state. | [Template](studio/templates/work-roadmap.excalidraw) |

The four Guide diagrams are the expected family introduction. The three
working types are **optional starter templates**. Their required content
describes the chosen template; the shared drawing component imposes no type
selection, source binding, status field or metadata form on a working Studio.
Each family owns its working Space and View composition and drawing semantics.

The shared catalog describes both groups in successive single-column sections.
Guide's drawing list offers its four explanatory types. Working types are used
in their owning working Spaces when that owner chooses a template.
A Question map can reference reasoning or a Report without BJTR execution;
a Work roadmap can name human review or design work as well as native Runs.

**Task alignment:** Task's Roadmap Studio is a freeform single-column list,
with freely named Drawing 1 / Drawing 2 / Drawing 3 rows and an Add drawing
action. Opening a row embeds its Excalidraw; several rows may stay open. It
requires no Topic hierarchy, registered type or template content fields.
The shared capability is the folding row and embedded drawing surface.
Guide's Folder map explains the family's folder conventions; a Task drawing
may freely sketch a current Question's actual folders and paths. Question
cards retain their own Logic / Work / Report columns. A single-column
drawing list does not require the contents of every working View to use one
column. Task's working UI and its save actions are implemented by the Task
Workbench; Guide supplies its family explanations and folder conventions.

### Preparation and use

The following steps apply to Guide and deliberately chosen typed templates.
Freeform working drawings can be created directly without these steps.

1. Select a defined diagram type and the family or native instance owner.
2. Bind its source records. Keep a missing drawing visible as **Not prepared**,
   naming the missing source. **Not applicable** includes a concise reason.
3. Fill the prepared template or redraw the existing scene. Keep its reader
   question and required content; node counts and concrete layout can adapt.

The seven starter templates are prepared, with explicit replacement slots.
Their availability does not mean the corresponding family or instance drawing
has been filled. Unknown answers, sources or states stay explicit. Each arrow
names its relationship. Current question state and native execution state keep
their respective owner meanings.

A family-specific extension declares an id, reader question, required
elements, sources, placement and starter template before becoming a standard
template. Freeform working drawings need no type registration. Generated
diagrams remain owned by their generators; preserve separately
edited scenes before regenerating.

- [Drawing type catalog design](studio/drawing-type-catalog.excalidraw)
- [Catalog preview](studio/drawing-type-catalog.png)
- [Template generator](studio/drawing-templates.py)

Each template also has a same-named SVG and PNG preview. This is a design
contract and prepared artifact set; it does not create an instance ledger or
change native skill contracts.

## Current artifacts · Guide v4

- [Editable Excalidraw scene](studio/workbench-shared-guide-v4.excalidraw)
- [Vector overview](studio/workbench-shared-guide-v4.svg)
- [Guide / Workbench](studio/v4-01-guide.png)
- [Paper / Story / collapsed Questions](studio/v4-02-paper-questions.png)
- [Paper / expanded Question and Work](studio/v4-03-paper-question-work.png)
- [Insight / Questions](studio/v4-04-insight-questions.png)
- [Generator](studio/workbench-shared-guide-v4.py)

The generator owns these generated artifacts. Keep independently edited
Excalidraw copies under another filename before regenerating.

```sh
python3 plugins/haipipe-toolkit/servers/workbench-shared/studio/workbench-shared-guide-v4.py
python3 plugins/haipipe-toolkit/servers/workbench-shared/studio/guide-view-drawings.py
python3 plugins/haipipe-toolkit/servers/workbench-shared/studio/drawing-templates.py
```

This writes the scene and SVG using the Python standard library. Add
`--previews` with Pillow installed to render PNG previews. Optional `--font`
and `--mono-font` paths control preview fonts; the scene uses the same
Excalidraw font IDs as the existing Paper and Insight drawings.

## Earlier proposals · superseded

These remain for comparison. Their sharing boundaries do not describe the
current proposal:

- [v3 scene](studio/workbench-shared-guide-v3.excalidraw): horizontal Views;
  explanatory and instance Views were both in Guide.
- [v2 scene](studio/workbench-shared-guide-v2.excalidraw): the earlier grouped
  sidebar, with both kinds of Views in Guide.
- [Original scene](studio/workbench-shared-design.excalidraw): the initial
  proposal before the Guide boundary was settled.

## References

- [Workbench design principle](../../../../principle/WORKBENCH-DESIGN.md)
- [Paper Workbench implementation](../workbench-paper/paper.py)
- [Paper workflow contract](../../skills/paper/haipipe-paper-workflow/SKILL.md)
- [Paper Story contract](../../skills/paper/haipipe-paper-story/SKILL.md)
- [Paper Workbench contract](../../skills/paper/haipipe-workbench-paper/SKILL.md)
- [Paper design studio](../workbench-paper/studio/paper-workbench-design.excalidraw)
- [Insight Workbench implementation](../workbench-insight/insightboard.py)
- [Insight design studio](../workbench-insight/studio/insight-workbench-design.excalidraw)
- [Studio contract](../../skills/page/haipipe-workbench-studio/SKILL.md)
