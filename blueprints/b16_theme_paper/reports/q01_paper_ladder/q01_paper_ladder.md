# How does a paper climb the ladder?
state: 🟡 DRAFT · Board/Job roles decided 2026-10-09; topic cleanup 2026-10-10; Section details remain open
answers: Q01
answer-status: partial

## Opening

A paper Board is venue-free and close to the scientific work. A Job is one version for one venue:
it selects which questions and results to report, orders its Sections and answers comments.
A Task writes one Section, Abstract or letter. The paper cites Results from the Project's work and
discovery Tasks; the Job does not call that scientific work.

**Where this Page sits:** [Q01 · How does a paper climb the ladder?](../../board.md).

## Content

### 1 · Answer

| level | holds | home |
|---|---|---|
| Board / Block | research questions, reports, related work, Ideation and tellings | `Paper-<Name>/` |
| Job | one venue's send, Section Narrative and order, version questions, comments and build | `jNN_v<MMDD>_<desk>/` |
| Task | one Section, Abstract or letter: draft, evidence, checks and fragment | `tNN_<title>/` |
| Run | one execution under its owning level; paper Runs are soft | `runs/run-<type>-<target>/` |

Every level uses Description, Idea Studio, Audience Report, Work Details, Runs and Delivery.
Work Details opens its children: Board to version Jobs, then Job to Section Tasks. Studio topics,
reports and Runs keep their own level. Story and Ideation are topics, not a reference Job.
Each version face's `## Narrative` supplies the Section order to its build.

### 2 · Evidence

- [s05 · Board, Job and Task boundary](../../studio/s05-board-job-task-boundary/s05-board-job-task-boundary.excalidraw):
  current roles, screens, communication, shared ladder (frame 8) and Story/Ideation decisions (frame 9).
- [s05 decisions](../../studio/s05-board-job-task-boundary/s05-board-job-task-boundary.md):
  JL 261009 Board/Job rules and all five carried s04 decisions, with their original ids and dates.
- [paper ladder contract](../../../../plugins/haipipe-toolkit/skills/2_theme/paper/haipipe-paper/ref/paper-ladder.md):
  the current folders; [s11](../../studio/s11-paper-block), [s12](../../studio/s12-paper-job) and
  [s13](../../studio/s13-paper-task) retain the level screens.

### 3 · Limits

The venue folder's final home, Task-level Studio and reports, a Section's upward ask, and the
Narrative question column remain open in s05. JL 261010 also asks to see Job Studio topics and
reports smoothly from the Block. That viewing proposal is recorded, not implemented.
The old migration goal is retired; this cleanup does not migrate any real paper or settle these choices.

### 4 · Next

Settle s05's remaining boundary and viewing questions before changing the live workbench.
The current Studio no longer carries s01-s04. Their full records are preserved under
`_archive/20261010/studio/`; topic numbers stay retired. Q04 keeps the Story/Ideation mapping.

### 5 · Historical outcome (2026-10-07)

This is the recorded 2026-10-07 outcome, not a new verification. References to s01 and s03 below name the retired snapshots; current design is in s05.

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
