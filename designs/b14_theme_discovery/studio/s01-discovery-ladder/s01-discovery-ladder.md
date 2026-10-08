s01 · discovery ladder
=======================

**Topic:** every discovery row in one drawing, Block down to Run (JL 261007): an overview frame that
answers Q01 (the ladder one line per level, where each of today's Discovery Views goes, what discovery
has that no other Theme has, the open points in red), then the Board, Job and Task levels, each row
with its folder, what it holds, its skills and its screens, the proposal (teal, solid) above today's
workbench (gray, dashed), and a Run-level frame: a Paper Run opened from Task › Runs.

**Source:** the Board, Job and Task rows are defined once in
`../../../b03_project_workbench/studio/s01-overall-tree-structure/` (`build_ladder_v4.py`, `level_views.py`; the
discovery entries are this Block's, marked `b14 Q01`); edit them there and this drawing and b03's s06,
s07, s08 follow on their next build. The overview and the Run frame are drawn by this topic's builder.

**Feeds:** `../../reports/` q01 (the ladder question); q02 and q03 pick up its open points.


Files
-----

```text
s01-discovery-ladder/
├── s01-discovery-ladder.md            this notes file
├── s01-discovery-ladder.excalidraw    the drawing; marks are kept on rebuild
├── s01-discovery-ladder.png           preview
└── build_s01_discovery_ladder.py      the overview and Run frames; the rows come from b03
```

Rebuild: `python build_s01_discovery_ladder.py` (or b03's `studio/_build/make.sh`).


Proposed (261007, for JL)
-------------------------

1. **Block** `discovery/bNN_<topic>/`: the folder of a work Block (s01-D19). Description = Scope ·
   Resources (where it searches) · Related; Idea Studio = `studio/`; Audience Report = `reports/`, one
   Question │ Work │ Report row each; Work Details = its Jobs, each open to its Tasks; Runs = its soft
   Runs (draw, report, check, delivery-bib); Delivery (optional) = `<block>.bib` and built reports.
2. **Job** `jNN_<inquiry>/`: one inquiry, with the Block's six Spaces (as the DIKW level and the design
   method). Description = its face `jNN_<inquiry>.md`; Audience Report = its Tasks' answers, a view
   with no `reports/`; Work Details = its sub-question Tasks, each open to its papers, third row by
   specialist (Search · Review · Synthesize); Runs = soft only (plan-tasks, delivery-bib) plus its Tasks'
   Runs from below; Delivery (optional) = `jNN_<inquiry>.bib`, merged.
3. **Task** `tNN_<task>/`: one sub-question, one `discovery_type`. A Page that makes facts: hard Paper
   Runs, and its Page's soft Runs (structure, section, citation, check). Description = Scope ·
   Admission · Records; Audience Report = Table (Question │ Work │ Report, as b03's s08 decided) · Reading; Work
   Details = Papers (the Result Cards) · Intake (screened candidates) · Draft (the plan); Runs grouped
   read · write · check · delivery; Delivery = the built article and the Evidence Bib, as cards.
4. **Run** `runs/rNN_<author><year>_<subject>/`: hard, one Subject; the Paper Run contract kept (Result
   Card, facts, runtime receipt, one Bib entry); opens as a pop-out from Task › Runs or a paper row.
5. Today's Views, all on the Block, each have a place: see the overview frame's table.


Open
----

1. A Job face `jNN_<inquiry>.md` (today the `job:` block is copied into each Task's discovery.yaml).
2. A synthesis across a Job's Tasks: a Task of its own, or the Block's report?
3. A Paper Run's receipt: `result/runtime.yaml` (today) or `passes/pNN-<MMDD>/runtime.yaml` (s01-D15)?
4. Screened candidates: `draft/records/search/` (today `results/search/`, which merges into `runs/`)?
5. The Evidence Bib: `draft/evidence/bibex/tNN_<task>.bib` (today) or `tNN_<task>.bib`, as a Page Task's?
6. Papers grouped by role, and the citation chip: Q02.

(write here, or mark the drawing in red)
