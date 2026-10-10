s01 · work ladder
==================

**Topic:** every work row in one drawing, Block down to Run (JL 261007). First the frame
"work ladder · Q01": this Block's proposed answer to Q01, a grid with one row per level (Block, Job,
Task, Run), its folder on the left and one column per Space (Description | Idea Studio · Audience
Report | Work Details | Runs · Delivery | the Run types panel); under it, where each of today's Task
workbench views goes, and the open points in red. Then the Board, Job and Task levels, each row
with its folder, what it holds, its skills, and its screens, the proposal (teal, solid) above
today's workbench (gray, dashed).

**Source:** the Q01 frame is this folder's own (`build_s01_work_ladder.py`, the `GRID`, `MOVES` and
`OPEN` tables). The rows below it are defined once in `../../../b03_project_workbench/studio/s01-overall-tree-structure/`
(`build_ladder_v4.py`, `level_views.py`); edit them there and this drawing follows on its next build.

**Feeds:** `../../reports/` q01 (the ladder question).


Files
-----

```text
s01-work-ladder/
├── s01-work-ladder.md            this notes file
├── s01-work-ladder.excalidraw    the drawing; marks are kept on rebuild
├── s01-work-ladder.png           preview
└── build_s01_work_ladder.py
```

Rebuild: `python build_s01_work_ladder.py` (or b03's `studio/_build/make.sh`).

Decided so far
--------------

(none yet: Q01 is proposed, 261007, and open until JL settles it)


Open
----

The nine red points of the Q01 frame, listed in `../../reports/q01_work_ladder/` under Limits. The
first decides the rest of the drawing: if the work Job takes the Block's six Spaces, b03's work Job
row follows (its owner, b03, changes it).

(write here, or mark the drawing in red)
