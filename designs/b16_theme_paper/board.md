# b16 · Theme: paper

board-kind: task-block
spine: Design questions about the paper Theme as one ladder: what a paper Board, a version Job and a Section Task each hold and show, where Ideation and the Story sit among the six Spaces, where venues, related papers and the built paper live, and how review rounds and letters appear.
close: Each recorded question has a report Page with an answer status, and every answered question names the skill, workbench or builder change that settled it.

## Topic

The paper Theme plans, writes and revises one paper as Board Pages: Ideation, the Story (its
research questions, claims, roadmaps and Section Narrative), one Page per Section, and review
rounds. On the ladder its Block is the paper Board, a Job is one version for a venue (or a grant,
or a talk), and a Task is a Section, a Page Task, or a cover letter and rebuttal.

Today the Paper workbench shows it at Board level in four Spaces (Ideation · Story · Sections ·
Delivery); a Section opens in the Page workbench.

The shared ladder (b03) gives every level the same six Spaces: Description · Idea Studio ·
Audience Report | Work Details | Runs · Delivery. This Block asks how paper fits that ladder level
by level, and what it needs that no other Theme has.

Most answers here are a change to the paper skills (`2_theme/paper/haipipe-paper` and its sub-skills, `workbench-paper`), the Paper workbench
server, or b03's shared builder, not a Task Run. A Question may have no work entries; its report
links the changed files and the drawings.

Excluded: the ladder itself and what every Theme shares (b03_project_workbench); the Page workflow every
Section uses (haipipe-page-workflow).

## Pipeline

```text
chat section -> Related question -> haipipe-question -> skill, workbench or builder change -> report Page
                                                     -> studio/ drawings (shared by the questions)
```

## Pages

No Jobs yet. Studio topics:

- `studio/s01-paper-ladder/s01-paper-ladder.excalidraw`: every paper row, Block to Run, proposed
  and today, with Q01's proposed answer in its first frame. Drawn by its own
  `build_s01_paper_ladder.py` from b03's shared definitions
  (`b03_project_workbench/studio/s01-overall-tree-structure/`), and rebuilt by b03's `studio/_build/make.sh`.
- `studio/s02-paper-workbench/paper-workbench-design.excalidraw`: the Paper workbench as built
  today (moved from `servers/workbench-paper/studio/`, 261007); Guide › RoadMap Draw shows it.
- `studio/s03-paper-migration/`: how the old paper folders and the old paper workbench move to the
  new ladder and frame: the Boards today (counted), the folder map, the readers, the phases.
- `studio/s04-story-to-topics/`: Q04, the Story and Ideation into studio topics and Questions: where
  each part of a Story goes, the Board after, the readers that change. Drawn by its own builder.
- `studio/s11-paper-block/`, `s12-paper-job/`, `s13-paper-task/`: one level each, as b11 does: the
  level's tab on the shared frame, each Space a full screen with "on disk" under it, then Guide ›
  Method opened from that tab (its level's section open). Drawn by `studio/_build/paper_ui.py`.
- `studio/s21-paper-run-skill/s21-paper-run-skill.excalidraw`: Q05, the paper theme's skills and Runs:
  every Run each level's buttons make (run-<type>-<target>) with its skill, agent and signs, one
  version in order, the 9 paper skills and the base skills they borrow, the skill folders before →
  after with each change's reason, skill × Run, the Runs on disk, and the skill update plan. Read
  from disk by `build_s21_paper_run_skill.py`, in b12's s21 style. Run by `goals/g04-paper-skills.md`.
- `studio/s31-paper-guide/s31-paper-guide.excalidraw`: the paper Guide cut by level (s03's style):
  the four Views opened from each level's tab, read live from the paper Guide's files, each level's
  proposals in red; one file per level (guide_block · guide_job · guide_task), one shared builder.
- `studio/s32-paper-element-ui/s32-paper-element-ui.excalidraw`: the paper theme's element gallery, after b03's
  s32: every element as the frame draws it at Block, Job and Task (every Space and view) and on the old pages
  (flagged OLD), each with its proposed look (b03's picks) beside it, and the Theme elements list with its gaps
  in red. Shot live and drawn by `build_s32_paper_element_ui.py` (b03's helpers imported).

## Questions

```yaml
questions:
- id: Q01
  title: How does a paper climb the ladder?
  question: What do the paper Board, a version Job and a Section Task each hold and show on screen,
    and which of today's Ideation, Story, Sections and Delivery Views moves to which level?
  hypothesis: The Board keeps Ideation and the Story in its Audience Report groups; a version is a
    Job whose Work Details = its Sections (Main · Appendix · Letters); a Section is a Page Task.
  acceptance: Answered when every level names its folder and its six Spaces' content, drawn in studio/.
  work: []
  report: reports/q01_paper_ladder/q01_paper_ladder.md
- id: Q02
  title: Where do venues, related papers and the built paper live?
  question: 'Where on disk and on screen do the venue folders, the related-papers table and the built
    paper (LaTeX, Word, cover letter) sit: at the Board, or in each version''s Job?'
  hypothesis: Venues and related papers are the Board's Description; the built paper is the version
    Job's Delivery, since each version targets one venue.
  acceptance: Answered when each has one home and the open ? in b03's paper rows is settled.
  work: []
  report: reports/q02_venues_related_built/q02_venues_related_built.md
- id: Q03
  title: How do review rounds show?
  question: 'Where do a review round, its responses, the rebuttal and the revised Sections appear:
    a new version Job, Tasks in the same Job, or Runs?'
  hypothesis: A round is Tasks in the same version Job (tNN_rebuttal, the revised Sections' Runs);
    a resubmission elsewhere is a new version Job.
  acceptance: Answered when a round's place is written and the workbench shows it.
  work: []
  report: reports/q03_review_rounds/q03_review_rounds.md
- id: Q04
  title: Where do the Story and Ideation live?
  question: 'Once a paper Board takes b03''s shape (studio topics, Questions with reports), where does
    each part of the Story and Ideation Pages go, which readers change, and how do the Story and
    Ideation skills work from there?'
  hypothesis: Ideation and each telling are studio topics; each research question is a Board Question
    grouped by its topic, with a report; the Section Narrative and order go to the version.
  acceptance: Answered when every Story part has one home, the workbench, the build and the skills read
    it, and one paper Board has moved and still opens and builds.
  work: []
  report: reports/q04_story_into_topics/q04_story_into_topics.md
- id: Q05
  title: Which skills and Runs make the paper theme?
  question: 'Which Runs does each level''s buttons make, which skill owns each one, where do the
    paper skills fall short today, and how do their folders change to close the gap?'
  hypothesis: A Section's Runs are the Page workflow's; the Board's and the version's are the paper
    skills', named run-<type>-<target>; the skills take one ladder contract and one scaffold, as the
    design theme's do.
  acceptance: Answered when every button's Run has a card naming its skill, agent and sign, and the
    skill folders match s21's after tree.
  work: []
  report: reports/q05_skills_and_runs/q05_skills_and_runs.md
```

## Related resources

```yaml
resources:
- title: haipipe-paper skill (the Paper door)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/2_theme/paper/haipipe-paper
  questions:
  - Q01
  - Q02
  - Q03
- title: workbench-paper skill (the Paper workbench)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/2_theme/paper/workbench-paper
  questions:
  - Q01
  - Q02
  - Q03
```
