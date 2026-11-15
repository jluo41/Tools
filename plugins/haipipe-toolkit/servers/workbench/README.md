# Workbench · the base: Studio and Guide, reused by every theme

(Renamed from `workbench-shared`, 261007. Each theme is a sibling `workbench-<theme>`; the base
with no theme on top is the vanilla workbench. The `shared` route row and `/w/shared` keep
their names.)

This folder holds what every Workbench family reuses instead of owning a copy:

| Component | Writes? | Contract | What it serves |
|---|---|---|---|
| **Studio** | Yes, through its own routes | [haipipe-studio](../../skills/1_base/project/haipipe-studio/ref/screen.md) | The live Excalidraw editor and its save path, the chat (GUI) and terminal (TUI), the ✨ Draw it and ✨ deck pens |
| **Guide** | Never | [ref/guide.md](ref/guide.md) | Family explanations: skills, methods, UI and folder maps, RoadMap Draw |

Any Workbench that shows a drawing (Paper Story › RoadMap Draw, Task Scope ›
RoadMap Draw, a Page's 🎨 Studio tab, Guide's own canvases) opens it through
Studio's `xcal.py` and `excalidraw_proxy.py`. A family owns *which* drawing
and *where* it lives; Studio owns how a scene is opened, minted and saved.
Guide embeds the same canvas in its isolated viewing mode and never saves.

## Topics

- [ref/focus-views.md](ref/focus-views.md): focus page views, Around the Work, Files, UI examples, Delivery storage
- [ref/frame.md](ref/frame.md): the frame (`frame.py`), Studio's folding parts, Studio tags and Current, levels, Task types, themes
- [ref/guide.md](ref/guide.md): Guide's four Views, each theme's `guide/`, the card Guide (`levels.yaml`), sharing boundary, runtime files and routes
- [ref/studio-files.md](ref/studio-files.md): Studio's files and routes (editor, chat, terminal, autodraw, autodeck)
- [ref/questions-lead-progress.md](ref/questions-lead-progress.md): Questions lead progress, family examples
- [ref/guide-design-history.md](ref/guide-design-history.md): the earlier five-View design, folder map, predefined drawing types (Task alignment), Guide v4, superseded proposals
- [ref/use-cases.md](ref/use-cases.md): linked use cases and UI walkthroughs

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
| Insight | Scope (the data) · Question Book (the questions and their scripts) | Insight · Check | Delivery |
| Labeling | Data | Labeling · Quality | Delivery |
| Design (page) | Design Task | Design Item | Delivery |
| Paper | none | Ideation · Story · Sections | Delivery |
| Page | none | Draft · Evidence | Delivery |
| Task | Scope (the Block, its Questions, data and drawings) | Task · Check | Delivery |

"Setup" names a role, not a tab: tabs keep their family's own words.

## References

- [Workbench design principle](../../../../blueprints/Project-Ladder/work/b10_project_workbench/board.md)
- [Paper Workbench implementation](../workbench-paper/paper.py)
- [Paper workflow contract](../../skills/2_theme/paper/haipipe-paper-workflow/SKILL.md)
- [Paper Story contract](../../skills/2_theme/paper/haipipe-paper-story/SKILL.md)
- [Paper Workbench contract](../../skills/2_theme/paper/workbench-paper/SKILL.md)
- [Paper design studio](../../../../blueprints/Project-Ladder/work/b16_theme_paper/s01-paper-tree-concept/s01-paper-tree-concept.excalidraw)
- [Insight Workbench implementation](../workbench-insight/insightboard.py)
- [Insight design studio](../../../../blueprints/Project-Ladder/work/b11_theme_insight/s02-insight-workbench/insight-workbench-design.excalidraw)
- [Studio contract](../../skills/1_base/project/haipipe-studio/ref/screen.md)
