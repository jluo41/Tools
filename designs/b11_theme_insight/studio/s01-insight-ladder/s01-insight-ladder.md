s01 · Insight ladder
====================

**Topic:** plan A and plan B in the workbench UI: the insight rows of b03's s11-block-variants (Blocks),
s12-job-variants (Jobs) and s13-task-variants (Tasks), each frame named for its level, with the proposed screens and today's beneath them.
Frames: Decide (the ladder and the open points ① to ⑦ with my answers); Board level A (DIKW on the
board), B (DIKW in the Jobs) and the older register board, in the same columns so A and B compare
screen by screen; Job level A (no Job tab, a note) and B (a level with the Block's six Spaces); Task
level (A and B alike).

**Colour:** red only on the open points, each note tagged with its number; a "differs:" line (today
against proposed) is gray.

**Source:** the trees, skills and screens of B and of the Task level come from b03's
`studio/s01-overall-tree-structure/build_ladder_v4.py` and `level_views.py`; option A, the Decide
frame and the cleanup (`tidy`: empty Description columns dropped, frames 300 apart, red numbered)
are this builder's own. Seed snapshot: `.s01-insight-ladder.seed.json`, beside the drawing.

**Feeds:** `reports/` q01_insight_ladder (and b03's q07_workbench_mapping).


Files
-----

```text
s01-insight-ladder/
├── s01-insight-ladder.md            this notes file
├── s01-insight-ladder.excalidraw    the drawing; marks are kept on rebuild
├── s01-insight-ladder.png           preview
└── build_s01_insight_ladder.py      draws it from b03's shared definitions
```

Rebuild: `python build_s01_insight_ladder.py` (or b03's `studio/_build/make.sh`).


Decided so far
--------------

1. (261006, JL: the levels "are in the board level, do you think in the job level") A DIKW level is
   a Job: Block › Work Details lists the four levels, and each level's Job tab takes the Block's six
   Spaces (s01-D24).
2. (261007) Today's insight question screens sit under the proposed ones: Prototype (its ask and
   needs) under Description, Insight (its partitions) under Work Details.

3. (261007, JL: "make your name of frame to be of the board level, job level and task level")
   Every frame is named for its level: Overview · Board level · Job level · Task level.
4. (261007, JL: "is DIKW in the board level or in the job level? Could you make both of them")
   Two options side by side. A · DIKW on the board: the levels are the third row of Board ›
   Work Details (Meta · Data · Information · Knowledge · Wisdom), each listing its questions;
   the level folders stay on disk with no Job tab (a note frame at the Job level). B · DIKW in
   the Jobs: Board › Work Details lists the four levels, each a Job with the Block's six Spaces.
   The Task level is the same in both. A is defined in this builder only (`define_option_a`);
   B and everything else come from b03's shared definitions. The overview frame compares them
   row by row.
5. (261007, JL: "could you reorganize this?", "make it clean and use the red color to show the one I
   should pay attention"; then "where is my original workbench UI?", "I want to see the plan A and
   plan B how to fit the workbench UI") The UI screens stay; a short text-only redraw that dropped
   them was undone. Cleaned instead: a Decide frame first, the Board rows' three empty Description
   columns dropped, frames 300 apart, "differs:" lines gray, and red only on the open points ① to ⑦.
6. (261007) The Run level follows haipipe-run 0.31.0 and b03's s05-runs: each Run is one folder in `runs/`
   (hard `rNN_<dataset>_<partition>/` with `result/`, soft `run-<type>-<target>/`), and each level's Runs
   card is one list from `run.yaml` filtered by kind or type. Insight's move to it is open point ⑦.
7. (261007, JL: "Board a column, job a column and then task a column") The frames sit in a grid under
   Decide: columns Board │ Job │ Task, a row per plan: row A = Board A · Job A (no tab) · Task (A and B
   alike), row B = Board B · Job B, then the older register board under Board. `layout()` places them.
8. (261007, JL: "why this is so thin?") Job A is drawn as screens, like Job B: the same six Spaces,
   each showing where that part of a level lives under plan A (mostly a Board screen narrowed to the
   level; "no Job tab" where A has no home). Defined here only (`define_job_a`); B is b03's row.


Open
----

① A or B: is a DIKW level a group on the Board (A), or a Job with its own tab (B)?
② Does only j04_wisdom deliver; do D · I · K hand their answers up as cite needs?
③ Does a level get its own question map, or the Block's map at its frame?
④ Today's Check (a question's gates): chips on each need in Task › Work Details?
⑤ Meta stays on the Board?
⑥ The older register boards: carry over, or keep?
⑦ Insight's Runs under the new Run contract (haipipe-run 0.31.0, b03's s05-runs): `<dataset>_<partition>.sh`
  beside `results/` and `reports/` become `runs/rNN_<dataset>_<partition>/` with `result/` inside?

(the drawing's Decide frame gives my answer to each; write here, or mark the drawing in red)
