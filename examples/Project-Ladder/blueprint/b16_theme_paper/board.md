# b16 · Theme: paper

board-kind: task-block
package: plugins/haipipe-toolkit
theme: paper
shared-blueprint: b01_haipipe-toolkit
spine: Design questions about the paper Theme as one ladder: what a paper Board, a version Job and a Section Task each hold and show, where Ideation and the Story sit among the six Spaces, where venues, related papers and the built paper live, and how review rounds and letters appear.
close: Each recorded question has a report Page with an answer status, and every answered question names the skill, workbench or builder change that settled it.
session: Ladder-b16-Paper-v1031
ui-block: examples/Project-Ladder/paper/Paper-Example
ui-block: examples/Project-Ladder/paper/Idea-Example
ui-block: examples/Project-Ladder/paper/Grant-Example
ui-job: examples/Project-Ladder/paper/Paper-Example/j11_writing_v1130_desk
ui-job: examples/Project-Ladder/paper/Paper-Example/j12_writing_v0215_desk
ui-job: examples/Project-Ladder/paper/Paper-Example/j01_evidence_display
ui-job: examples/Project-Ladder/paper/Paper-Example/j02_evidence_value
ui-job: examples/Project-Ladder/paper/Paper-Example/j03_evidence_cite
ui-job: examples/Project-Ladder/paper/Paper-Example/j21_submission_v1130_desk
ui-task: examples/Project-Ladder/paper/Paper-Example/j11_writing_v1130_desk/t01_introduction
ui-task: examples/Project-Ladder/paper/Paper-Example/j11_writing_v1130_desk/t31_cover-letter
ui-task: examples/Project-Ladder/paper/Paper-Example/j12_writing_v0215_desk/t32_response
ui-task: examples/Project-Ladder/paper/Paper-Example/j01_evidence_display/t02_table1-example
ui-task: examples/Project-Ladder/paper/Paper-Example/j02_evidence_value/t01_values-sample
ui-task: examples/Project-Ladder/paper/Paper-Example/j03_evidence_cite/t01_cite-prior-work
ui-task: examples/Project-Ladder/paper/Paper-Example/j21_submission_v1130_desk/t02_portal-walk
ui-task: examples/Project-Ladder/paper/Paper-Example/j11_writing_v1130_desk/t00_summary
ui-task: examples/Project-Ladder/paper/Paper-Example/j02_evidence_value/t02_raw-value-tables
ui-task: examples/Project-Ladder/paper/Paper-Example/j02_evidence_value/t99_paper_value_check
ui-task: examples/Project-Ladder/paper/Paper-Example/j03_evidence_cite/t99_paper_citation_check
ui-task: examples/Project-Ladder/paper/Paper-Example/j21_submission_v1130_desk/t01_cover-letter
ui-task: examples/Project-Ladder/paper/Paper-Example/j21_submission_v1130_desk/t03_portal-fill

## Current Block Structure

| Studio | Subject | Job organization |
| --- | --- | --- |
| [s01 Idea Block Structure](s01-idea-block-structure/s01-idea-block-structure.md) | Candidate ownership and assessment | Ideas → named candidate Jobs → ideation Tasks |
| [s02 Grant Block Structure](s02-grant-block-structure/s02-grant-block-structure.md) | A funding application project | Story / Evidence / Display / Writing / Presentation |
| [s03 Paper Block Structure](s03-paper-block-structure/s03-paper-block-structure.md) | A manuscript project | Story / Evidence / Display / Writing / Presentation |

Each Structure entry names Job Type, Job Name, Task Type and Task Name, with topic/group separately. The drawing uses the same concrete names. Review and Submission are Task groups inside the appropriate Writing Job. Unregistered or conflicting type contracts remain explicit; the existing Paper-Example is not silently migrated.

The shared Studio reader supplies the Block Structure type views. Idea-Example, Grant-Example and Paper-Example provide actual Folder, Jobs and Studio sources for their Examples views. The first two are authored demonstration Blocks; their scientific assessment and submission are not implied. Skills opens the owning skill files.

The user authorized replacing old s01–s03. Their complete files, historical decisions and annotations are retained under `_archive/20261127/`; old decision ids continue to refer to those archived topics. New s01/s02/s03 subjects do not reassign their historical decisions. Receipt: [named structures](trace/261127/1049_named_block_structures.md).

## Earlier design context

The following records the previous ladder and compatibility examples. Current target structures are linked above.

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

Most answers here are a change to the paper skills (`3_theme/paper/hai-paper` and its sub-skills, `workbench-paper`), the Paper workbench
server, or b03's shared builder, not a Task Run. A Question may have no work entries; its report
links the changed files and the drawings.

Excluded: the ladder itself and what every Theme shares (b10_project_workbench (removed 261126)); the Page workflow every
Section uses (hai-draft-workflow).

## Pipeline

```text
chat section -> Related question -> hai-report -> skill, workbench or builder change -> report Page
                                                     -> studio/ drawings (shared by the questions)
```

## Pages

One Job, `j01_paper_workbench_pages` (the paper pages, level by level: a Task per level, three UI sNN
in each). Block Studio topics (reorganized 261011, JL: "you just propose it"), one per view with b10's
numbers, so the same number means the same view in every theme Block; groups in `studio/_groups.txt`:

```text
group          topic                  holds                                         stage    Q
Structure      s01-idea-block-structure     Candidate Jobs and assessment Tasks       explore  Q01/Q04
Structure      s02-grant-block-structure    Grant application structure               explore  Q01/Q02
Structure      s03-paper-block-structure    Paper groups, types, names and ownership  explore  Q01/Q02/Q04
Levels         s11 · s12 · s13        the Board, version and Section tabs           -        Q01
Run and Skill  s53-paper-skills    the paper's Runs and skills                   explore  Q05
Guide          s81-paper-guide        the Guide, cut by level                       explore
UI             s32 to s40 in j01      the 3 x 3: Board, version, Section × Report,  explore
                                      Work, Studio (one sNN per cell, in its Task)
```

- `_archive/20261127/s01-paper-tree-concept/`: the current ladder and Board, Job and Task boundaries; each level's Studio,
  reports and communication; shared ladder overview and all five Story/Ideation decisions (s01-D06..D10,
  carried from the retired s04). The Job-to-Block viewing proposal stays open here.
- `_archive/20261127/s02-paper-studio/` to `s05-paper-report/`: what paper puts in each of the Block's views (Studio,
  Delivery, Related, Report), each starting from b10's rule for every Block, its open points in red.
- `s11-paper-block/`, `s13-paper-job-preview/`, `s13-paper-task/`: one level each (s11 explore; s12 and s13
  shaping): the level's tab on the shared frame, each Space a full screen with "on disk" under it, then
  Guide › Method opened from that tab. Drawn by `studio/_build/paper_ui.py`.
- `s53-paper-skills/`: Q05, every Run each level's buttons make with its skill, agent and signs,
  the paper skills and the base skills they borrow, the skill folders before → after. Read from disk by
  `build_s53_paper_skills.py`. Run by `goals/g04-paper-skills.md`.
- `s81-paper-guide/`: the paper Guide cut by level, read live from the paper Guide's files; one file
  per level (guide_block · guide_job · guide_task), one shared builder.
- `j01_paper_workbench_pages/`: the paper's UI as a 3 x 3 (JL 261031: "I think it should be 3 x 3"); `t01_board_page`
  holds s32 · s33 · s34, `t02_version_page` s35 · s36 · s37, `t03_section_page` s38 · s39 · s40 (Report · Work ·
  Studio), each drawn in five parts by `j01_paper_workbench_pages/paper_ui_cells.py`. They replace `s32-paper-ui`
  (the old frame's element gallery), moved to `_archive/20261031/` (JL 261031: "你把这个 UI 删了重做吧").
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
  report: _archive/20261127/s01-paper-tree-concept/s01-paper-tree-concept.md
- id: Q02
  title: Where do venues, related papers and the built paper live?
  question: 'Where on disk and on screen do the venue folders, the related-papers table and the built
    paper (LaTeX, Word, cover letter) sit: at the Board, or in each version''s Job?'
  hypothesis: Venues and related papers are the Board's Description; the built paper is the version
    Job's Delivery, since each version targets one venue.
  acceptance: Answered when each has one home and the open ? in b03's paper rows is settled.
  work: []
  report: _archive/20261127/s01-paper-tree-concept/s01-paper-tree-concept.md
- id: Q03
  title: How do review rounds show?
  question: 'Where do a review round, its responses, the rebuttal and the revised Sections appear:
    a new version Job, Tasks in the same Job, or Runs?'
  hypothesis: A round is Tasks in the same version Job (tNN_rebuttal, the revised Sections' Runs);
    a resubmission elsewhere is a new version Job.
  acceptance: Answered when a round's place is written and the workbench shows it.
  work: []
  report: _archive/20261127/s05-paper-report/s05-paper-report.md
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
  report: _archive/20261127/s01-paper-tree-concept/s01-paper-tree-concept.md
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
  report: s53-paper-skills/s53-paper-skills.md
```

## Related resources

```yaml
resources:
- title: hai-paper skill (the Paper door)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper
  questions:
  - Q01
  - Q02
  - Q03
- title: workbench-paper skill (the Paper workbench)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper
  questions:
  - Q01
  - Q02
  - Q03
```

## Renumbered (261127)

Studio bands follow the Studio Type topics (b17 s70-s79); each title starts with its band's name.

```text
s14-idea-job-preview   → s11-idea-job-preview    👀 Block Job UI Preview, under s01 Idea
s12-paper-job          → s13-paper-job-preview   👀 Block Job UI Preview, under s03 Paper
s21-paper-run-skill    → s53-paper-skills        🧰 Skills; its sNN-D codes stay s21-D
s31-paper-guide        → s81-paper-guide         🗺️ Theme Guide; its sNN-D codes stay s31-D
s11-paper-block, s13-paper-task, s04-paper-related, s05-paper-report → _archive/20261127/
```

## Renumbered (261011)

JL 261011: b16 takes b10's view numbers. A decision id moved with its topic.

```text
studio topic           was                            decision ids
s01-paper-tree-concept         s05-board-job-task-boundary    s05-D01..D10 → s01-D01..D10
s02-paper-studio       new                            from s02-D01
s03-paper-delivery     new                            from s03-D01
s04-paper-related      new                            from s04-D06; archived 261127 (_archive/20261127/)
s05-paper-report       new                            from s05-D01; archived 261127 (_archive/20261127/)
s32-paper-ui           s32-paper-element-ui + s33-ui-issue   s32-D unchanged (archived 261031)
s32 to s40 (j01)       s32-paper-ui (261031)          from sNN-D01, one per cell
runs/run-draw-s01      runs/run-draw-s05
runs/run-draw-s32      runs/run-draw-s33
```

## Blueprint home

This Theme is an independent blueprint Block under `examples/Project-Ladder/blueprint/b16_theme_paper/`
since 261010. Its studio topics, questions, reports and Runs keep their existing
identities. Shared toolkit foundations remain in [b01](../../../Project-Packages/work/b01_haipipe-toolkit/board.md).

## Design

### 🧭 High-level design
embed: design.md
