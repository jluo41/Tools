# How does an inquiry climb the ladder?
state: 🔴 OPEN
answers: Q01
answer-status: open

## Opening

Proposed (261007), waiting on JL: a discovery Block holds the inquiries and the Questions; a Job is one
inquiry with the Block's six Spaces, its Work Details its sub-question Tasks; a Task is one Page that
makes facts (hard Paper Runs, and its Page's soft Runs), its Work Details its papers; a Paper Run is
hard, one per source. Every one of today's sixteen Discovery Views has a place. The hypothesis holds,
with one addition: the Task is both a Page and a maker of facts, which no other Theme's Task is.

**Where this Page sits:** [Q01 · What do the Discovery Block, an inquiry Job, a sub-question Task and a Paper Run each hold and show on screen, and which of today's Discovery Views moves to which level?](../../board.md).

**Why it matters:** the skill contract, its scaffold and the workbench views are built from this
answer, level by level.

## Content

### Answer

```text
level   folder                                what its tab shows
-----   ------                                ------------------
Block   discovery/bNN_<topic>/                Description (Scope · Resources · Related) · Idea Studio
                                              · Audience Report (the Questions) | Work Details (its
                                              Jobs, each open to its Tasks) | Runs (soft) · Delivery
Job     jNN_<inquiry>/                        one inquiry, the six Spaces: Audience Report = its
                                              Tasks' answers (a view); Work Details = its Tasks, by
                                              Search · Review · Synthesize; Delivery = merged Bib
Task    tNN_<task>/                           one sub-question, one discovery_type: Audience Report =
                                              Table (Question │ Work │ Report) · Reading; Work Details
                                              = Papers · Intake · Draft; Runs = read · write · check
Run     runs/rNN_<author><year>_<subject>/    hard, one Subject: Result Card · facts · receipt · one
                                              Bib entry; a pop-out from Task › Runs or a paper row
```

Where today's Views go (all sixteen are on the Block today):

```text
today                          proposed
-----                          --------
Guide › all four               the Guide tab, unchanged
Scope › Block                  Block › Description › Scope; its Jobs and Tasks: Block › Work Details
Scope › Questions              Block › Audience Report
Scope › Resources              Block › Description › Resources
Scope › RoadMap Draw           Block › Idea Studio
Work › Papers                  Task › Work Details › Papers (each Task its own)
Work › Tasks                   Job › Work Details
Work › Questions               Block › Audience Report (merged with Scope › Questions)
Check › Runs                   the Runs Space of each level
Check › Citations              a chip on its paper row, Task › Work Details › Papers (Q02)
Check › Reports                the state on each report row; Check a report is a Run
Delivery › Reports             Block › Delivery, and each Task's built article from below
Delivery › BibTeX              Delivery at each level: the Task's Evidence Bib, merged at Job, Block
```

What discovery has that no other Theme has: a Task that is a Page and makes facts; one Run per
admitted Subject (a Trigger resolves to Subjects first); Intake, the screened candidates; Tasks grouped
by `discovery_type`'s specialist; the Bib climbing from one entry per Result to the Block.

### Evidence

- [discovery ladder](../../studio/s01-discovery-ladder/s01-discovery-ladder.excalidraw)

### Limits

- A proposal only: no skill, scaffold, server or real Block has changed. The rows are b03's shared
  definitions (the discovery entries in `Tools/designs/b03_project_workbench/studio/s01-overall-tree-structure/`
  `build_ladder_v4.py` and `level_views.py`); b03's s06, s07 and s08 drawings follow on their next build.
- Five points change real folders and wait on JL: a Job face `jNN_<inquiry>.md`; a synthesis across a
  Job's Tasks; the Paper Run receipt in `result/` or in `passes/`; where screened candidates live once
  `results/` merges into `runs/`; the Evidence Bib's path.
- Papers grouped by role, the citation chip and the Bib at each level are Q02's; the synthesis handoff
  is Q03's.

### Next

- JL settles the open points (red in the drawing); then the skill contract and its scaffold (new
  Block, Job, Task, Run) follow, then the workbench views on a demo Block, on the shared base frame.
