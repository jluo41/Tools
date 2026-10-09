s01 · Design
============

**Topic:** the design ladder at a glance (JL 261007: "allocate all the design related things into one
excalidraw"); drawn first in b03, moved here when this Block was made (261007). One frame,
**design ladder**: each level, its folder and where it shows; the design method's six steps and where
each shows on the design Job; the 13 methods in 3 families (where the rule comes from); how an insight
Block steers a design; the open points, in red.

The Block, Job and Task frames that this drawing used to nest below the overview are now one drawing
per level (JL 261007, "instead of nesting all the things together"): `../s11-design-block/`,
`../s12-design-job/`, `../s13-design-task/`.

**Source:** the trees, skills and screens are defined once, in
`../../../b03_project_workbench/studio/s01-overall-tree-structure/build_ladder_v4.py` (`BLOCK_TREES`,
`JOB_TREES`, `TASK_TREES`) and `level_views.py` beside it; the same rows still appear in b03's s11-block-variants, s12-job-variants and s13-task-variants,
one level each. This drawing gathers one theme across the levels, as
`../../../b11_theme_insight/studio/s01-insight-ladder/` does for insight. The method itself is
`Tools/plugins/haipipe-toolkit/servers/workbench-design/guide/method.md`; the method
folders today are `haipipe-design/ref/method-folders.md` beside it.

**Feeds:** `../../reports/` q01_design_ladder · q02_design_workbench · q03_insight_steers_design.


Files
-----

```text
s01-design/
├── s01-design.md            this notes file
├── s01-design.excalidraw    the drawing; marks are kept on rebuild
├── s01-design.png           preview
└── build_s01_design.py      draws it: the overview frame
```

Rebuild: `python build_s01_design.py` (or b03's `studio/_build/make.sh`, which builds it with the rest).


Decided so far
--------------

1. (261007, JL: "a design method + design goal + N design items as a job") A design Job is one
   goal done by one method, returning N designs; each design is a Task. The Job takes the Block's
   six Spaces (see b03's s12-job-variants, decided 5).
2. (261007) The Block's Work Details groups its Jobs by method family: Internal · External · Goal
   Only, Internal first, since that is where an insight Block steers the design.
3. (261007) An insight Block steers a design through one crossing: a signed Wisdom answer is
   handed off, listed in the design Block's Resources, and read by the Jobs whose method reads
   our data (by insight · tailoring · theory and insight); each design's elements name it.


Open
----

- Generate at the Job: one Run makes the N drafts and opens N Tasks.
- `method-folders.md` makes the method alone the Job, holding every goal; it changes once agreed.
- The Brief and the principles: the Block's Description (goal list, shared rules)?
- A design's Rationale: its Task's Audience Report, or its card?
- The Task row is still a Design folder (one goal); it becomes one design once agreed (b03's s13-task-variants).
- `B00_DesignBoard-<app>/` → `bNN_<topic>/`; the old names are read until renamed.

(write here, or mark the drawing in red)
