# b16 · Theme: paper

board-kind: task-block
package: plugins/haipipe-toolkit
theme: paper
shared-blueprint: b01_haipipe-toolkit
spine: Design questions about the paper Theme as one ladder: what a paper Board, a version Job and a Section Task each hold and show, where Ideation and the Story sit among the six Spaces, where venues, related papers and the built paper live, and how review rounds and letters appear.
close: Each recorded question has a report Page with an answer status, and every answered question names the skill, workbench or builder change that settled it.

## Topic

The paper Theme plans, writes and revises one venue-free paper Board. Ideation and each telling
are Studio topics; its research questions have reports. A Job is one version for one venue,
selecting questions and results, ordering Sections and answering comments. A Task is one Section,
Abstract or letter, written as a Page Task. Scientific work runs in the Project's work and discovery Tasks.

The shared ladder (b10) gives every level the same screen: Guide · Studio | Block · Job · Task | Delivery
on top (Studio and Delivery are the Board's own, opened from every level, with Related folded inside
Studio, b10 s04-D05), and Description · Report | Work | Runs below; a version and a Section keep no
related/, studio/ or delivery/ of their own (JL 261011) (every level writes its own Report). This Block asks how paper fits that ladder level
by level, and what it needs that no other Theme has.

Most answers here are a change to the paper skills (`2_theme/paper/haipipe-paper` and its sub-skills, `workbench-paper`), the Paper workbench
server, or b03's shared builder, not a Task Run. A Question may have no work entries; its report
links the changed files and the drawings.

Excluded: the ladder itself and what every Theme shares (b10_project_workbench); the Page workflow every
Section uses (haipipe-draft-workflow).

## Pipeline

```text
chat section -> Related question -> haipipe-report -> skill, workbench or builder change -> report Page
                                                     -> studio/ drawings (shared by the questions)
```

## Pages

No Jobs yet. Studio topics (reorganized 261011, JL: "you just propose it"), one per view with b10's
numbers, so the same number means the same view in every theme Block; groups in `studio/_groups.txt`:

```text
group          topic                  holds                                         stage    Q
Structure      s01-paper-tree         Board · version · Section boundaries (was s05) shaping  Q01
Views          s02-paper-studio       Story and Ideation as studio topics           explore  Q04
Views          s03-paper-delivery     the built paper, per version                  explore  Q02
Views          s04-paper-related      venues and related papers (ids from s04-D06)  explore  Q02
Views          s05-paper-report       research questions and review rounds          explore  Q03
Levels         s11 · s12 · s13        the Board, version and Section tabs           -        Q01
Run and Skill  s21-paper-run-skill    the paper's Runs and skills                   explore  Q05
Guide          s31-paper-guide        the Guide, cut by level                       explore
UI             s32-paper-ui           elements and issues (s33-ui-issue merged in)  shaping
```

- `studio/s01-paper-tree/`: the current ladder and Board, Job and Task boundaries; each level's Studio,
  reports and communication; shared ladder overview and all five Story/Ideation decisions (s01-D06..D10,
  carried from the retired s04). The Job-to-Block viewing proposal stays open here.
- `studio/s02-paper-studio/` to `s05-paper-report/`: what paper puts in each of the Block's views (Studio,
  Delivery, Related, Report), each starting from b10's rule for every Block, its open points in red.
- `studio/s11-paper-block/`, `s12-paper-job/`, `s13-paper-task/`: one level each (s11 explore; s12 and s13
  shaping): the level's tab on the shared frame, each Space a full screen with "on disk" under it, then
  Guide › Method opened from that tab. Drawn by `studio/_build/paper_ui.py`.
- `studio/s21-paper-run-skill/`: Q05, every Run each level's buttons make with its skill, agent and signs,
  the paper skills and the base skills they borrow, the skill folders before → after. Read from disk by
  `build_s21_paper_run_skill.py`. Run by `goals/g04-paper-skills.md`.
- `studio/s31-paper-guide/`: the paper Guide cut by level, read live from the paper Guide's files; one file
  per level (guide_block · guide_job · guide_task), one shared builder.
- `studio/s32-paper-ui/`: the element gallery (`s32-paper-ui.excalidraw`, shot live by
  `build_s32_paper_ui.py`) and the served UI's issues (`ui-issue.excalidraw`, review 261008, by
  `build_ui_issue.py`), one topic since 261011.
- Retired s01-s04 stay frozen under `_archive/20261010/studio/`; they are not current build inputs.

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

## Renumbered (261011)

JL 261011: b16 takes b10's view numbers. A decision id moved with its topic.

```text
studio topic           was                            decision ids
s01-paper-tree         s05-board-job-task-boundary    s05-D01..D10 → s01-D01..D10
s02-paper-studio       new                            from s02-D01
s03-paper-delivery     new                            from s03-D01
s04-paper-related      new                            from s04-D06 (s04-D01..D05: retired Story, in s01)
s05-paper-report       new                            from s05-D01
s32-paper-ui           s32-paper-element-ui + s33-ui-issue   s32-D unchanged
runs/run-draw-s01      runs/run-draw-s05
runs/run-draw-s32      runs/run-draw-s33
```

## Blueprint home

This Theme is an independent blueprint Block under `blueprints/b16_theme_paper/`
since 261010. Its studio topics, questions, reports and Runs keep their existing
identities. Shared toolkit foundations remain in [b01](../b01_haipipe-toolkit/board.md).
