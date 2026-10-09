s02 · Workbench shared
======================

Was b03's s08, then b02's s01, then b03's s07; s02 since the renumbering (261007), as the workbench topic of this Block.

**Topic:** what `Tools/plugins/haipipe-toolkit/servers/workbench` holds today, how every
other workbench leans on it, and whether it should own the Block / Job / Task frame (JL 261007:
"should it propose the structure of board, job, and tasks? ... what are their relationship to the
workbench shared?").

**Source:** the grid in the first frame is read off each workbench's own Python every build (an
import or link of a shared part; its own stylesheet), so it shows what the code does now. The Space
rows come from `../s01-overall-tree-structure/level_views.py` (`SERVER`, read from the server code).


Files
-----

```text
s02-workbench-shared/
├── s02-workbench-shared.md            this notes file
├── build_s02_workbench_shared.py      the builder; marks are kept on rebuild
├── s02-workbench-shared.excalidraw    the drawing
└── s02-workbench-shared.png           its picture
```


What the drawing says
---------------------

Read top to bottom, a row each (JL 261007: "arrange well the current ones"): 1 · the proposal
(frames 1-2), 2 · on screen (frames 3-4), 3 · today, what the code does now (frames 5-7), 4 · next
(frame 8). The notes below follow the drawing as it was first built.

1. Today every workbench draws its own page (header, band, Space row, stylesheet) and borrows a few
   parts: Guide (all eight), Studio (all but labeling), the Runs panel (all eight, but it lives in
   workbench-page), the BJTR tree (paper only), Related Papers (insight, design).
1b. The servers/ tree (JL 261007: "the tree-structure, like draw"): today's tree read off the disk,
   beside the proposed one: `workbench/frame/` (levels, spaces, qwr, one css) new,
   `runs_panel.py` moved in from workbench-page, one `spaces()` adapter per family (task first),
   workbench-page at Task level only, and a `workbench` skill to pair with the server (?).
2. Each workbench names its own Spaces, at one level: a Block (task, discovery, cowork, paper,
   insight, design board, labeling board) or one Page (page, design page, labeling page). No
   workbench has a Job level.
3. Proposed: workbench owns the frame (level tabs, the six Spaces and their dividers, the
   third row, Idea Studio, the Runs panel, Audience Report's Question │ Work │ Report, the BJTR tree,
   Guide, one look); a family hands it, per level, its Spaces' subspaces, content and run types.
3b. The base and a theme (JL 261007: "in the shared, the structure of the board-level, job-level
   and task-level; the workbench-xxx just gives the themes"): workbench holds Block · Job ·
   Task × the six Spaces, each cell what it reads by default from the standard folders, so a theme
   with nothing special works as is. A theme, one per Theme of the Project, is `theme.py`
   (declared: level names, which levels, subspaces, extra fields, run types, Guide) plus optional
   `views/` (code, where one Space needs its own body). Filled in: task (config only), paper
   (config + a Story view ?), page (Task only; config + its outline, evidence and export code).
   A theme may not change the levels, the six Spaces or their order, draw tab rows or carry CSS.
4. Steps: move `runs_panel.py` to shared; build the frame and move one family (task, Block level);
   the rest follow as s11 · s12 · s13 settle; old routes stay meanwhile.

5. On screen (JL 261007: "I want the real ui, just like the s04"), two frames on the right, drawn
   the s04 way: "the base, at Block, Job and Task", one full screen per level opening the Space
   that holds its children or its Runs (Block › Work Details: its Jobs; Job › Work Details: its
   Tasks; Task › Runs: its Runs), an "on disk" tree under each naming the folders it reads and the
   base files that draw it (frame.py, frame_view.py, runs_panel.py, work_items.py ?), and a Run
   pop-out; then "a theme on the base", the same Block screen under the work theme and the paper
   theme: the same frame, its own level names, third row and rows, and the theme file behind it.

6. Done (261007, JL: "add the disks as well, to show what files are associated with the content in
   the screen ... so we have both disks and runs"): the right column holds a Disk box above the
   Runs panel. It lists what the open Space reads, under the open folder, each path with what it
   feeds on screen; a glob says how many it finds, what is not there yet is greyed, a .md links
   to the reader. The base fills it per Space (`frame.vanilla_disk`); an open Page view brings its
   own (`PAGE_VIEW_DISK`); a theme sets `Space(disk=...)` per subspace, so the box always names
   what that view really reads. The live twin of the "on disk" trees under each screen here.

Open
----

- A `workbench` skill to match the server (the frame contract), as workbench-page and
  workbench-paper have theirs?
- Insight fits the frame (its session's answer, 261007): partitions are Audience Report's third row,
  the DIKW levels are Jobs, its Insight table is Question │ Work │ Report, and its question map is a
  generated, view-only Idea Studio row. Still open: its Check (a question's gates) has no Space;
  proposed as chips on each question row.
- Labeling (own host, own write door): a family's own body inside a Space?
- The paper's Job tab: workbench-paper as the version Job (s12).
- The shared README's Space order gives way to the six Spaces.
- Write the contract now; code it once s12 and s13 settle.

(write here, or mark the drawing in red)
