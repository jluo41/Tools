# How do review rounds show?
state: 🟡 DRAFT · the 2026-10-07 comments rule, checked against b10's every-level Report (261011); one Board applied
answers: Q03
answer-status: partial

## Opening

A review round is a report, not a Task and not a new Board: the reviewers' comments are one batch,
kept as a report of type comments in the version that answers them. The response is that version's
letter Task, and the revised Sections are the next version, which starts as a copy of the last
one's authored files. b10 gave every level its own Report (s09-D02), so the round shows in the
version's Report, where a reader of that send expects it.

**Where this Page sits:** [Q03 · Where do a review round, its responses, the rebuttal and the revised Sections appear: a new version Job, Tasks in the same Job, or Runs?](../../board.md).

**Why it matters:** each point a reviewer raises has to be answered exactly once and traced to the
change that answers it; if the round sat in Runs or in loose Tasks, the workbench could not show
which points are still open.

## Content

### 1 · Answer

| part of a round | on disk | on screen |
|---|---|---|
| the comments (one batch) | `<answering version>/reports/qNN_review-<MMDD>/`, `page-type: comments` | version › Report › Comments |
| each point | a row of that report's item table: cites · lands on · work · reply · state | the Section it lands on: Report › Comments |
| the response letter | `<answering version>/t32_response/` (letters are `t3N_`; t31 the cover letter) | version › Work › Letters |
| the revised Sections | the next version `jNN_v<MMDD>_<desk>/`, copied from the last one's faces, drafts and drawings | its own tab in Version ▾ |
| a resubmission elsewhere | a new version Job for the new venue | the same |
| a coauthor's pass | `<the version drafted>/reports/qNN_coauthor-<MMDD>/` | version › Report |
| a meeting's comments | the Board's `reports/qNN_meeting-<MMDD>/`, its notes in `related/meetings/` | Board › Report |
| the built resubmission | the Board's `delivery/jNN_<version>/` | top row › Delivery |

### 2 · Evidence

- [haipipe-paper-comments](../../../../plugins/haipipe-toolkit/skills/2_theme/paper/haipipe-paper-comments/SKILL.md)
  (1.1.0, JL 261007: "comments … are a special type of report"): the batch kinds and where each lands.
- [Q01 §5](../q01_paper_ladder/q01_paper_ladder.md): the 2026-10-07 outcome, with the version face and
  the Section numbers (t3N_ letters).
- [b10 s09-D02](../../../b10_project_workbench/studio/s01-overall-tree-structure/s01-overall-tree-structure.md):
  every level writes its own Report, in its own `reports/`.
- Applied on one Board, TestToLearn: `j02_v1007_mansci` answers `reports/q01_editor-decision-0916`;
  the paper workbench shows Report › Comments, Work › Letters and the routed items on each Section.
- [b16 s05-paper-report](../../studio/s05-paper-report/): the topic that owns review rounds now.

### 3 · Limits

Only one Board has a round in this shape. Whether a past send keeps its Run names, and how a
revised Section rebuilds its LaTeX (from its draft, or after its evidence is bound), are still open
in s05-paper-report. ScalingGlucose has no round yet.

### 4 · Next

JL confirms the shape; then haipipe-paper-comments and workbench-paper name the top-row Delivery for
the built resubmission, and the next real round is taken in this way.
