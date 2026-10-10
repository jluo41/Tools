s01 · paper ladder
===================

**Topic:** every paper row in one drawing, Block down to Run (JL 261007): an overview frame that
answers Q01 (the paper ladder, where each of today's Paper workbench Views moves, the run types and
gates per level, the open points in red), then the Board, version Job and Section Task rows, each
with its folder, what it holds, its skills, and its screens, the proposal (teal, solid) above
today's workbench (gray, dashed).

**Source:** the overview is this topic's own (`build_s01_paper_ladder.py`, as b12's
`s01-design/` does); the rows are defined once in `../../../b03_project_workbench/studio/s01-overall-tree-structure/`
(`build_ladder_v4.py`, `level_views.py`); edit the rows there and this drawing follows on its next
build. b03 has no paper Section tree (a Section is a Page Task, b03 s08 1c), so the Task frame draws
the Page Task tree under the paper Section's screens, and a Section screen b03 leaves out (Table,
Evidence-Citation) is the Page Task's, in memory only.

**Feeds:** `../../reports/` q01_paper_ladder (answered here, proposed) · q02 · q03 (open marks).


Files
-----

```text
s01-paper-ladder/
├── s01-paper-ladder.md            this notes file
├── s01-paper-ladder.excalidraw    the drawing; marks are kept on rebuild
├── s01-paper-ladder.png           preview
└── build_s01_paper_ladder.py      draws it: the Q01 overview, then the shared rows
```

Rebuild: `python build_s01_paper_ladder.py` (or b03's `studio/_build/make.sh`).


Proposed (261007, for JL)
-------------------------

1. Block = the paper Board `Paper-<Name>/`, face `bNN_<topic>.md`: Description (Scope · Venue ·
   Resources · Related) · Idea Studio (the RoadMap Draw and other topics) · Audience Report
   (Ideation · Spine · Questions, read from the Story) | Work Details (its Jobs: versions · grants ·
   slides, each open to its Sections) | Runs (soft) · Delivery.
2. The Ideation and the Story sit on disk in a reference Job, `j00_story/` (today `A1-Story/`), as
   cowork keeps `j00_people/`: `t00_ideation/` and one `t01_<desk>_<idea>/` Story Page per idea,
   both Page Tasks. On screen they are not a version row: the Board's Audience Report shows them.
3. A version is a Job `jNN_v<N>_<venue>/`: Description (venue, deadline, which Story it tells) ·
   Audience Report (its §8 Narrative: Section │ claim │ state, in compile order; G3 release) |
   Work Details (its Sections, Main · Appendix · Letters, each row its Section map) | Runs ·
   Delivery (G4).
4. A Section is a Page Task `S-<desk>-<N>-<Section>/` (b03 s08 1c), with the Page Task's six
   Spaces; the cover letter and the rebuttal are Page Tasks in the group Letters.
5. Every Run in a paper is soft (`run-<type>-<target>/`); facts come from hard Runs in the
   Project's work and discovery Tasks.


Open
----

(write here, or mark the drawing in red; the overview's red lines are the open points)
