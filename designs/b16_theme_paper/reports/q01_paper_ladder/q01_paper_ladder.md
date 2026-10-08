# How does a paper climb the ladder?
state: 🟡 DRAFT · proposed 2026-10-07 from b03's ladder decisions and today's paper skills; JL to settle
answers: Q01
answer-status: open

## Opening

Proposed: a paper is one Block (the paper Board); its thinking, the Ideation and the Story, is a
reference Job `j00_story/` that the Board's Audience Report shows; each version for a venue is a
Job `jNN_v<N>_<venue>/` whose Work Details are its Sections; a Section is a Page Task; and every
Run inside a paper is soft. The hypothesis holds on screen (the Board keeps Ideation and the Story
in its Audience Report) and changes on disk (they move from `A1-Story/` into `j00_story/`).

**Where this Page sits:** [Q01 · What do the paper Board, a version Job and a Section Task each hold and show on screen, and which of today's Ideation, Story, Sections and Delivery Views moves to which level?](../../board.md).

**Why it matters:** the paper skill's contract, its scaffold and the paper workbench's level tabs
are built from this answer.

## Content

### 1 · Answer

**The ladder, level by level**

```text
Block  Paper-<Name>/ (face bNN_<topic>.md)   one paper
  Job  j00_story/            ?               reference Job: t00_ideation/ · t01_<desk>_<idea>/ (Page Tasks)
  Job  jNN_v<N>_<venue>/                     one version for one venue
  Job  jNN_grant_<funder>/ · jNN_slides_<talk>/   the same Story as a grant or a talk
 Task  S-<desk>-<N>-<Section>/               a Section = a Page Task (Main · Appendix · Letters)
  Run  runs/run-<type>-<target>/             soft only; facts come from work/discovery hard Runs
```

**The six Spaces at each level**

```text
             Description          Idea Studio     Audience Report        | Work Details              | Runs              · Delivery
Board        Scope·Venue·          RoadMap Draw,   Ideation · Spine ·     | Jobs: versions · grants · | run-venue-        · from below,
             Resources·Related     other topics    Questions (RQ→reports) |   slides, open to Sections|   run-question- … |   by version
version Job  venue · deadline ·    optional        §8 Narrative: Section  | Sections: Main · Appendix | run-narrative-    · the built
             which Story it tells                  │ claim │ state (G3)   |   · Letters, each its map |   run-compile- …  |   version (G4)
Section Task S-<…>.md: its job,    roadmap ·       Table · Reading        | Draft-… · Evidence-…      | run-structure-    · latex/S-<…>.tex
             claim, group, plan    Section map                            |                           |   run-section- …  |   (its fragment)
```

**Where today's Paper workbench Views go**

```text
Guide (4 Views)                          → Guide tab, unchanged
Ideation                                 → Block › Audience Report › Ideation (reads j00_story/t00_ideation)
Story › Spine                            → Block › Audience Report › Spine
Story › High-level logic + Low-level work→ Block › Audience Report › Questions (RQ → claim → work → reports/qNN)
Story › RoadMap Draw                     → Block › Idea Studio (a drawing topic)
Story › Related Papers                   → Block › Description › Related (related/related.md, b03 s01-D27)
Story §8 Narrative · Sections › Narrative→ version Job › Audience Report        ?
Sections › Main · Appendix               → version Job › Work Details (Main · Appendix · Letters)
a Section (opens in the Page workbench)  → Task tab (the Page Task's six Spaces)
Delivery › LaTeX · Word                  → version Job › Delivery               ? (Q02)
Delivery › Cover letter                  → version Job › Work Details › Letters (a Page Task)
Delivery › Rounds                        → ? (Q03)
```

**Run types and gates per level:** Board `runs/`: run-venue-, run-question-, run-draw-,
run-version-, run-status (G2 answers). Story Pages: run-idea-, run-claim-, run-task-,
run-structure-, run-section- (G0 pick, G1 release work, G2 claim). Version `runs/`:
run-narrative-, run-compile-, run-check-submit, run-delivery- (G3 release a Section, G4 submit).
Section `runs/`: the Page Task's soft Runs and its CHECK. No hard `rNN_` Run sits in a paper:
`support.<target>` work runs in the Project's work and discovery Tasks.

### 2 · Evidence

- [paper ladder](../../studio/s01-paper-ladder/s01-paper-ladder.excalidraw): the overview frame
  (this answer) and the Board, version and Section rows, proposed above today
- b03's decisions: `Tools/designs/b03_project_workbench/studio/s01-overall-tree-structure/s01-overall-tree-structure.md`
  (s01-D10, D15, D19-D22, D25-D27) and s07 decided 4, s08 decided 1c, 1e
- today's paper layout and Run Specs: `Tools/plugins/haipipe-toolkit/skills/2_theme/paper/haipipe-paper/ref/paper-structure.md`,
  `.../workbench-paper/ref/space-mapping.md`, `.../workbench-paper/ref/workbench-table.md`

### 3 · Limits

- A proposal: nothing on disk has moved, and no skill or server has changed yet.
- `A1-Story/ → j00_story/` renames folders in real paper Projects; it waits for JL.
- The Section folder name keeps `S-<desk>-<N>-<Section>/` (JL 261006, s08 1c), which is not the
  `tNN_` name other Tasks carry (s01-D15).

### 4 · Next

Open for JL (red in the drawing):

1. `A1-Story/` → `j00_story/`, a reference Job: yes, or keep the Story folder at the Board root?
2. Several Stories in one Board: does the Board show the one `j00_story.md` names (the G0 pick)?
3. The §8 Narrative moves from the Story Page to each version (one Story, many tellings)?
4. Block › Work Details groups: versions · grants · slides (b03 lists main · appendix · grants ·
   slides; main · appendix are a version's Section groups)?
5. Drop the Audience Report's Design group (s01-D22), since RoadMap Draw is a drawing and lives in
   Idea Studio?
6. The version face `jNN_v<N>_<venue>.md` (b03's tree says `jNN_v<N>.md`)?

Then: Q02 (venues, related, the built paper) and Q03 (rounds); then the build: the skill contract
and scaffold, and the workbench views, level by level, on a demo fixture Block.

### 5 · Outcome so far (2026-10-07)

JL's decisions on the open points, as applied; answer-status stays open until JL settles the whole answer.

```text
point                          decided (2026-10-07)                                      where it shows
1 A1-Story/ → j00_story/       no: the Story is not a Job; its Pages become studio         Q04 · s01 · s03 · s11
                               topics, studio/s01-ideation/ · studio/sNN-story-<telling>/,
                               and its research questions Board Questions with reports/
2 several Stories              each telling is its own studio topic; the version face's    Q04 · s11
                               tells: names the one it tells
3 §8 Narrative                 the version face's ## Narrative; the build reads its order   s12 · paper-structure.md
6 the version face             jNN_v<MMDD>_<desk>.md: a version dated by its send          s12 · haipipe-paper 1.8.0
  a Section's name             t00_abstract · t0N_ Main · t2N_ Appendix (A = t21)          s12 · s13 · rename_tasks.py
                               · t3N_ letters (t31 cover letter, t32 response)
  a version's folders          studio/ · reports/ · runs/ beside its Tasks and delivery/   s12
  Q03 the review               a comments batch is a report of type comments,              s12 · haipipe-paper-comments 1.1.0
                               <answering version>/reports/qNN_<kind>-<MMDD>/; never a Task
  a revision                   the next version starts as a copy of the last one's         TestToLearn j02_v1007_mansci
                               authored files (faces, drafts, drawings)
```

Still open: 4 (the Block's Work Details groups), 5 (no Design group), Q02 (venues and the built
paper), whether past sends keep their Run names, and how the renamed Sections rebuild their LaTeX
(draft exports, or bind the evidence first).

Applied on one Board, TestToLearn: `j01_v0429_mansci` (the April send, the record) and
`j02_v1007_mansci` (the revision, answering `reports/q01_editor-decision-0916`). The paper
workbench's version tab reads both: Questions (the register, then the send's standing questions),
Draft-Main · Draft-Appendix (the face's ## Narrative), Comments (the comments report's items),
Cover letter, Work Details › Letters (the t3N_ letters and the comments they answer), and
Delivery as item cards.
