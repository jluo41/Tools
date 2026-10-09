s13 · Task variants
===================

**Topic:** each Task variant: its folder (one folder per Run in runs/), its skills, and where it shows on screen. One row per variant, top to bottom: folder → what it holds → skills (owns ·
works · shows) → screens. Each variant is its own frame. Its screens come in two rows:

- **proposed**: the Task tab, one screen per Space (teal, solid);
- **today**: the same variant in the current workbench, its Spaces, views and run buttons
  (gray, dashed), as the server code renders it (`Tools/plugins/haipipe-toolkit/servers/`),
  with how today differs in red.

**Source:** the trees, skills and screens are defined once, in
`../s01-overall-tree-structure/build_ladder_v4.py` (`TASK_TREES`); the screens per Space and today's
screens come from `../s01-overall-tree-structure/level_views.py`. This topic draws them on
their own canvas.

**Feeds:** `reports/` q01_bjtr_boundary · q02_bjtr_across_themes · q07_workbench_mapping.


Files
-----

```text
s13-task-variants/
├── s13-task-variants.md          this notes file
├── s13-task-variants.excalidraw           JL's own copy: JL marks and moves it; no script writes it
├── s13-task-variants-proposed.excalidraw  the proposal, drawn by the builder
├── s13-task-variants.png · -proposed.png  previews
└── build_s13_task_variants.py            draws the proposal from the shared definitions
```

Rebuild the proposal: `python build_s13_task_variants.py` (or `../_build/make.sh`). As in s11: JL marks
their copy; the agent folds the marks into the shared definitions and redraws the proposal beside it.


Decided so far
--------------

1. Proposed (261006, JL's marks on s13): the Task tab has six Spaces: Description | Idea Studio ·
   Audience Report | Work Details | Runs · Delivery. Audience Report holds the writing (Draft ·
   Evidence · Report for a Page; Draft · Report for a work Task); Work Details holds how the work is
   done (a work Task's Code · Review · Notebooks; a Page's Displays · Workflow); Runs lists the Runs,
   grouped by run type (a work Task: run · build · report). Description: Scope · Plan (· Records).
1b. (JL 261006, marks on the proposal) A work Task's Audience Report is one screen, Question │ Work │
   Report, as on the Block ("one is necessary for the task"; a task-level report is little used). Its
   Delivery has no third row: today's style, its items as cards under group headings (Reports,
   Exports).
1c. (JL 261006) A paper Section is a Page Task (`S-<desk>-<N>-<…>/` inside a version Job): the two
   rows are one, Page Task, and a Section opens in workbench-page. (JL 261007) The paper keeps its
   own pair, `servers/workbench-paper` and `skills/2_theme/paper/workbench-paper` (renamed from
   haipipe-workbench-paper); whether the two workbenches merge is still to think about.
1d. (JL 261006) A work Task's Audience Report is one screen with the subspaces Draft · Report (as
   Code · Review · Notebooks in Work Details), Report open.
1e. (JL 261006) A Page Task splits today's Draft and Evidence by who they serve. RoadMap Draw is
   Idea Studio. Audience Report, what the reader gets: Table · Reading (the Table is the Page's
   Question │ Work │ Report: paragraph │ evidence items │ state). Work Details, how the Page is
   made, each named by today's Space: Draft-Scratch · Draft-Revise · Evidence-Citation ·
   Evidence-Display · Evidence-Value · Evidence-Supporting Runs (Workflow dropped; the row wraps).
1f. (JL 261007) A discovery Task's Audience Report is Question │ Work │ Report too; its work is the
   papers it read (r01 · r02). A Page keeps its verified citations in `<stem>.bib`, which
   its `run-citation-` Runs write (today they sit in a Result's `payload/sources.bib`).
2. Proposed: each row starts with the Guide, and today's screens sit under their proposed ones
   (for a Page: Guide, Draft under Audience Report, Evidence under Work Details, Delivery; the board's Task under Work Details for a work Task).
3. A paper Section's today row is the Page workbench, where a Section opens.
4. (JL 261006, marks on the proposal) Every Task row has the blockers of the Block rows: a line down
   the row before each group of Spaces, Guide | Description | Idea Studio · Audience Report |
   Work Details | Runs · Delivery, through the proposed and today's screens.


Open
----

(write here, or mark the drawing in red)
