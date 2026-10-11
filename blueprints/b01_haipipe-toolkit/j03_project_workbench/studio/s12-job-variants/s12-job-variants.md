s12 · Job variants
==================

**Tags:** `Structure`

**Topic:** each Job variant: its folder, what it holds, its skills, and where it shows on screen. One row per variant, top to bottom: folder → what it holds → skills (owns ·
works · shows) → screens. Each variant is its own frame. Its screens come in two rows:

- **proposed**: the Job tab, one screen per Space (teal, solid);
- **today**: the same variant in the current workbench, its Spaces, views and run buttons
  (gray, dashed), as the server code renders it (`Tools/plugins/haipipe-toolkit/servers/`),
  with how today differs in red.

**Source:** the trees, skills and screens are defined once, in
`../s01-overall-tree-structure/build_ladder_v4.py` (`JOB_TREES`); the screens per Space and today's
screens come from `../s01-overall-tree-structure/level_views.py`. This topic draws them on
their own canvas.

**Feeds:** `reports/` q02_bjtr_across_themes · q07_workbench_mapping.


Files
-----

```text
s12-job-variants/
├── s12-job-variants.md          this notes file
├── s12-job-variants.excalidraw  the drawing; marks are kept on rebuild
├── s12-job-variants.png         preview
└── build_s12_job_variants.py   draws it from the shared definitions
```

Rebuild: `python build_s12_job_variants.py` (or `../_build/make.sh`).


Decided so far
--------------

1. (261006, as on the Block and Task rows) Every Job row has the blockers: a line down the row
   before each group of the Job tab's Spaces, Overview · Studio · Reports | its children |
   Runs · Delivery, through the proposed and today's screens. They are read off the Spaces row,
   so they move if the Job tab takes the Block's Spaces.
2. (261006, JL: "make a job level DIKW") The DIKW level row takes the Block's six Spaces, the
   first Job row to: Description · Idea Studio · Audience Report | Work Details | Runs ·
   Delivery, filled from today's Prototype DIKW level view and the Insight table. A note under each
   screen says where it comes from; red = open. The other Job rows keep Overview · Studio ·
   Reports | children | Runs · Delivery until JL decides.
3. (261006) Today's screens sit under the proposed screen doing the same job (Scope under
   Overview, Task under Tasks, Check under Runs, Prototype under Work Details).
4. (261007, as on the Block's Work Details) A paper version's Sections rows each carry the
   Section's map (excalidraw-section), embedded and view only.
5. (261007, JL: "a design method + design goal + N design items as a job") The design row is
   now "design method": one goal done by one method (design-method.md's 13 cards, 3
   families), returning N designs, each design a Task. It takes the Block's six Spaces, like the
   DIKW level: Description (Goal · Method · Resources: the Brief's row and the frozen
   method.md) | Idea Studio · Audience Report (the element matrix: which elements the N designs
   changed) | Work Details (the N designs) | Runs (commission · generate · verify · revise) ·
   Delivery (step 5, Release). The same goal by another method is a sibling Job, so methods
   compare side by side; the Block's Work Details groups its Jobs by method family, Internal
   (steered by an insight Block's Wisdom) first.


Open
----

- Generate at the Job: one Run makes the N drafts and opens N Tasks (red on the Runs screen).
- `haipipe-design/ref/method-folders.md` today makes the method alone the Job, holding every
  goal; a goal is a Design folder (the Task). The skill changes only once this is settled.
- The Task row (s13) still shows a design folder (one goal), not one design.

(write here, or mark the drawing in red)
