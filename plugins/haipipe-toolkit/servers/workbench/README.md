# Workbench · the base: Studio and Guide, reused by every theme

(Renamed from `workbench-shared`, 261007. Each theme is a sibling `workbench-<theme>`; the base
with no theme on top is the vanilla workbench. The `shared` route row and `/w/shared` keep
their names.)

This folder holds what every Workbench family reuses instead of owning a copy:

| Component | Writes? | Contract | What it serves |
|---|---|---|---|
| **Studio** | Yes, through its own routes | [hai-studio](../../skills/1_base/project/hai-studio/ref/screen.md) | The live Excalidraw editor and its save path, the chat (GUI) and terminal (TUI), the ✨ Draw it and ✨ deck pens |
| **Guide** | Never | [ref/guide.md](ref/guide.md) | Family explanations: skills, methods, UI and folder maps, RoadMap Draw |

Any Workbench that shows a drawing (Paper Story › RoadMap Draw, Task Scope ›
RoadMap Draw, a Page's 🎨 Studio tab, Guide's own canvases) opens it through
Studio's `xcal.py` and `excalidraw_proxy.py`. A family owns *which* drawing
and *where* it lives; Studio owns how a scene is opened, minted and saved.
Guide embeds the same canvas in its isolated viewing mode and never saves.

## Folders

One folder per Task of the b17 work Block (`examples/Project-Ladder/blueprint/b17_theme_work`): a file's
folder names the Task that owns it. Every code folder is listed in `_host/host_registry.py` `BASE_GROUPS`,
so a module is `live.<module>` wherever it sits; the Draft Task's module folders are `TASK_GROUPS`.

| Folder | Job · Task | What it draws |
|---|---|---|
| `page/block_index_page/` | j11 · t01 | the Block as the one index page: Main, view buttons, bands, folds |
| `page/job_task_views/` | j11 · t02 | a Job's views on the Block page: Main and one per Task |
| `page/element_marks/` | j11 · t03 | each element's info, comments and 🙋 marks; the 🙋 tray |
| `page/parts_and_map/` | j11 · t04 | shared page parts, themes, page rules; with `ref/` and `assets/` |
| `home/` | j11 · t05 | the SPACE Home and Project pages |
| `side_pane/files_tree/` | j12 · t01 | the Files tree in the side pane, its scope and traces |
| `side_pane/rail_sections/` | j12 · t02 | the rail sections opened in the side pane |
| `studio/tabs/` | j13 · t01 | Studio read like Main: a page's topics, each a fold |
| `guide/` | j13 · t02 | the Guide pages |
| `studio/canvas/` | j13 · t04 | the Excalidraw canvas, linked drawings, ✨ Draw it and ✨ deck |
| `chat_drawer/` | j15 · t01 | the chat drawer: the Claude session, its context, rules and transcript |
| `terminal/` | j15 · t02 | the terminal in a page |
| `workbench-task-draft/page_shell/` | j14 · t01 | the Draft Task page: its tabs and Steps view |
| `workbench-task-draft/plan_outline/` | j14 · t02 | the Plan step: outline, plan cards, feedback, scratch |
| `workbench-task-draft/evidence_steps/` | j14 · t03 | the Evidence step: items, cite cards, displays, values |
| `workbench-task-draft/revise_steps/` | j14 · t04 | the Revise step: cards, notes, history, rubric |
| `workbench-task-draft/run_views/` | j14 · t05 | the Runs tab: Runs, cards, receipts, results |
| `workbench-task-draft/delivery_export/` | j14 · t06 | Delivery and the exports, with `exporters/` |
| `workbench-task-draft/reader/` | j14 · t07 | the standalone Page server and the reader look |

`focus-assets/` (the page's one css and js) is shared: the shell is j11 t01's, the 🙋 tray j11 t03's,
the side pane j12 t01's.

A Task's tests sit in its folder's own `tests/` (`page/job_task_views/tests/`), beside the code they
check; a `tests/` folder is not a live folder. `tests/` here keeps only `focus_page_fixtures.py`, the
shared fixtures, which a test finds from any depth. Run one Task's tests with
`cd servers && PYTHONPATH=_host python -m pytest -q workbench/page/job_task_views/tests`, or all of
them with `workbench`.

A focus page takes `mark=<part>[,<part>]` (a class, or `jsub=main` for `[data-jsub="main"]`): `focus-assets/focus.js`
outlines those parts in red, so a UI preview's live views of one page differ only in what they mark.

A focus page is built once into a file and served from it (`page/block_index_page/page_cache.py`):
the build records every file and folder the page reads, and the next open checks their modified times,
the loaded code's and the date, building again only when one changed (a repeat open of a large Block:
0.9 s to 0.03 s). Built pages are kept in `~/.cache/haipipe/pages/`; `PAGE_CACHE=0` turns it off. A
page that runs a command other than `git log` is never kept.

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

- Workbench design principle (b10, removed 261126)
- [Paper Workbench implementation](../workbench-paper/paper.py)
- [Paper workflow contract](../../skills/3_theme/paper/hai-paper-workflow/SKILL.md)
- [Paper Story contract](../../skills/3_theme/paper/hai-paper-story/SKILL.md)
- [Paper Workbench contract](../../skills/3_theme/paper/workbench-paper/SKILL.md)
- [Paper design studio](../../../../examples/Project-Ladder/blueprint/b16_theme_paper/s01-paper-tree-concept/s01-paper-tree-concept.excalidraw)
- [Insight Workbench implementation](../workbench-insight/insightboard.py)
- [Insight design studio](../workbench-insight/studio/insight-workbench-design.excalidraw)
- [Studio contract](../../skills/1_base/project/hai-studio/ref/screen.md)
