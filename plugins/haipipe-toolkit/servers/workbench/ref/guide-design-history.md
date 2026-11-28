# Guide design history: the five-View design, drawing types, v4 and earlier

Part of the [Workbench base README](../README.md).

## Explanatory Views and RoadMap Draw · earlier five-View design

The scenes in this section record the earlier design, with Skill set, Methods,
Workbench and Folder map as separate Views. Guide now shows them as one
RoadMap drawing; see [guide.md](guide.md).

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
| Skill set | Skill map: named skills, responsibilities, native owners and labeled relationships. | Excalidraw (b10, removed 261126) |
| Methods | Method flow: question, reasoning, missing evidence, optional Work, interpretation, answer and remaining issues. | Excalidraw (b10, removed 261126) |
| Workbench | UI map: the Guide and each family's working Space / View structure. | Excalidraw (b10, removed 261126) |
| Folder map | Linked graph: Space / View → native owner → folder / file, with repository and external paths marked. | Excalidraw (b10, removed 261126) |
| RoadMap Draw | Expand each of the four explanatory drawing rows to read its embedded canvas or open it full screen. | View design (b10, removed 261126) |

- All five Guide Views, as they appear in Guide (b10, removed 261126)
- Drawing generator (b10, removed 261126)

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

drawing-catalog.json (b10, removed 261126) defines the drawing types. Each
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

- Editable Excalidraw scene (b10, removed 261126)
- Generator (b10, removed 261126)

The generator owns these generated artifacts. Keep independently edited
Excalidraw copies under another filename before regenerating.

```sh
python3 b10_project_workbench/s31-guide/history/guide-design/build_s04_guide_design.py (removed 261126)
python3 b10_project_workbench/s31-guide/history/guide-views/build_s02_guide_views.py (removed 261126)
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

- v3 scene (b10, removed 261126): horizontal Views;
  explanatory and instance Views were both in Guide.
- v2 scene (b10, removed 261126): the earlier grouped
  sidebar, with both kinds of Views in Guide.
- Original scene (b10, removed 261126): the initial
  proposal before the Guide boundary was settled.
