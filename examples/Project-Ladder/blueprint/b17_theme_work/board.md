# b17 · Theme: work

board-kind: task-block
package: plugins/haipipe-toolkit
theme: work
examples: work/b01_example_work, cowork/b01_example_cowork, discovery/b01_example_discovery, knowledge/b18_a2ui_learning
bands: j0N 🗄️ Earlier design · j1N 🧰 Workbench · s6N 🧰 Skills
ui-project: examples/Project-Ladder
ui-block: examples/Project-Ladder/work/b90_example_paper_results
ui-block: examples/Project-Ladder/blueprint/b16_theme_paper
ui-block: examples/Project-Ladder/cowork/b01_example_cowork
ui-block: examples/Project-Ladder/discovery/b01_example_discovery
ui-job: examples/Project-Ladder/work/b90_example_paper_results/j02_example_estimates
ui-job: examples/Project-Ladder/cowork/b01_example_cowork/j02_review_board_amendment
ui-job: examples/Project-Ladder/cowork/b01_example_cowork/j00_people
ui-job: examples/Project-Ladder/discovery/b01_example_discovery/j01_policy_effect_inquiry
ui-task: examples/Project-Ladder/work/b90_example_paper_results/j02_example_estimates/t01_example_main
ui-task: examples/Project-Ladder/work/b90_example_paper_results/j01_example_source/t01_example_source
ui-task: examples/Project-Ladder/work/b90_example_paper_results/j02_example_estimates/t03_value_tables
ui-task: examples/Project-Ladder/cowork/b01_example_cowork/j02_review_board_amendment/t01_data_use_plan
ui-task: examples/Project-Ladder/discovery/b01_example_discovery/j01_policy_effect_inquiry/t01_policy_prior_work
ui-task: examples/Project-Ladder/paper/Paper-Example/j12_writing_v0215_desk/t03_results
ui-run: examples/Project-Ladder/work/b90_example_paper_results/j02_example_estimates/t01_example_main/runs/r01_example_main
ui-run: examples/Project-Ladder/work/b90_example_paper_results/j02_example_estimates/t03_value_tables/runs/r02_build_tables
ui-run: examples/Project-Ladder/discovery/b01_example_discovery/j01_policy_effect_inquiry/t01_policy_prior_work/runs/r01_example2024_policy
ui-run: examples/Project-Ladder/paper/Paper-Example/j01_evidence_display/t02_table1-example/runs/r01_draw_table1
ui-run: examples/Project-Ladder/work/b90_example_paper_results/j02_example_estimates/t01_example_main/runs/r02_collect_example_rounding
shared-blueprint: b01_haipipe-toolkit
spine: Design the work theme: Block, Job and Task pages with results and actions together in Report, shared Studio and supporting sections, and the skills that support each level.
close: Every sNN is agreed and its delivery made: the two skills rewritten in skills/2_work/work/ and the screens named for the focus page's owner.
session: Ladder-b17-Work-v1031

## Topic

The work Theme runs bounded execution work: a Task plans, builds, executes and reports, and
each Run is one hard ticket (`rNN_<noun>_<qualifier>.sh`) with its Result and receipt. Its Block
is a task Block (`tasks/bNN_<topic>/`), a Job groups Tasks by series (j0N, j1N, j5N), and a
Block's Questions are answered by report Pages that read the Tasks' Runs.

Today the Task workbench shows it at Block level in four Spaces (Scope · Task · Check ·
Delivery): the Question groups are Views of Task. Its server is moving to
`servers/workbench-work` and its skills to `2_work/work/` (in progress, 261007).

The shared ladder (b03) gives every level the same six Spaces: Description · Idea Studio ·
Audience Report | Work Details | Runs · Delivery. This Block asks how work fits that ladder level
by level, and what it needs that no other Theme has.

Most answers here are a change to the work skills (`2_work/work/` (being set up), the work Task skills in `1_base/task`, the server `servers/workbench-work`), the Work workbench
server, or b03's shared builder, not a Task Run. A Question may have no work entries; its report
links the changed files and the drawings.

Excluded: the ladder itself and what every Theme shares (b10_project_workbench (removed 261126)); the stage pipelines a
Task runs (hai-data, -nn, -end).

## Renumbered

- 261127: the Studio Type topics run s71 to s80 with no gaps, Work first (s71 to s76; Skills s76 is s75, Theme Guide s78 is s76), then the Knowledge Band types s77 Resources, s78 Methods, s79 Applications, s80 Questions; a `sNN-studio-type-*` topic is in Studio Type whatever its decade.
- 261127: Knowledge is Block type 5 in every band: s05 Block Structure, s15 Job UI Preview (new), s63-skills-knowledge is s55-skills-knowledge.
- 261127: s60 Studio and s61 Trace are Skills topics too, one skill each; s6N continues the Skills band of s5N.
- 261127: the Studio Type topics are s71-s79 in band order (were s70-s79; each names its band on its band: line); Slide Draft has no type topic.
- 261127: the Studio Type topics are s70-s79 (were s80-s89; s77 defines Studio Type itself), the theme Guide band is s8N.
- 261127: s71-files-pane is s31-files-pane and s72-trace-section is s32-trace-section again: s3N is UI Plugin, the theme Guide moves to s7N. The Studio bands are the Studio Type topics s70-s79, not this board's bands: line.
- 261127: the second digit names the Block type in every band (1 Work, 2 Blueprint, 3 CoWork, 4 Discovery): s14-blueprint-job-preview is s12, s12-cowork-job-preview is s13, s13-discovery-job-preview is s14.
- 261127: s06-files-pane is s31-files-pane and s07-trace-section is s32-trace-section (first s31, s32; s3N stays the theme Guide), the s7N band holds the side pane topics; s51-s54 hold the skills, one per Block type.
- 261126: s07-job-page-view is s11-work-job-preview, s08-cowork-block-view is s13-cowork-job-preview, s09-discovery-block-view is s14-discovery-job-preview; the s1N band holds the Job UI Previews, one per theme.

## Pipeline

```text
chat section -> Related question -> hai-report -> skill, workbench or builder change -> report Page
                                                     -> sNN drawings beside their Jobs (shared by the questions)
```

## Structure Studios

- [s01 · Work Block Structure](s01-work-structure/s01-work-structure.md)
- [s02 · Work Block (Blueprint) Structure](s02-blueprint-structure/s02-blueprint-structure.md)
- [s03 · CoWork Block Structure](s03-cowork-structure/s03-cowork-structure.md)
- [s04 · Discovery Block Structure](s04-discovery-structure/s04-discovery-structure.md)
- [s05 · Block Structure: Knowledge](s05-knowledge-structure/s05-knowledge-structure.md)

Each structure topic has Structure / Draw / Examples / Skills. Structure contains Folder, Job-Task, and Studio. Draw shows the corresponding structural models. S11–S13 remain responsible for UI design.

The topic directories retain their existing paths. Original faces and the previous structure version are preserved in each topic’s result/; original canvases and annotations remain untouched.

## Skills Studios

- [s51 · Skill: Work](s51-skills-work/s51-skills-work.md)
- [s52 · Skill: Blueprint](s52-skills-blueprint/s52-skills-blueprint.md)
- [s53 · Skill: CoWork](s53-skills-cowork/s53-skills-cowork.md)
- [s54 · Skill: Discovery](s54-skills-discovery/s54-skills-discovery.md)
- [s55 · Skill: Knowledge](s55-skills-knowledge/s55-skills-knowledge.md)
- [s60 · Skill: Studio](s60-skill-studio/s60-skill-studio.md)
- [s61 · Skill: Trace](s61-skill-trace/s61-skill-trace.md)
- [s62 · Skill: Project](s62-skills-project/s62-skills-project.md)
- [s63 · Skill: Draw](s63-skill-draw/s63-skill-draw.md)

Each topic reads its actual skills. Shared level contracts can be referenced by
several work kinds through the same source files.

## Questions

```yaml
questions:
- id: Q01
  title: How does work climb the ladder?
  question: What do the task Block, a work Job, a work Task and a hard Run each hold
    and show on screen, and which of today's Scope, Task, Check and Delivery Views
    moves to which level?
  hypothesis: The Block keeps its Questions (Audience Report) and Job series (Work
    Details groups); a Job's Work Details = its Tasks; a Task's Runs are its tickets;
    a Question's report reads them.
  acceptance: Answered when every level names its folder and its six Spaces' content,
    drawn in studio/.
  work: []
  report: s03-cowork-structure/s03-cowork-structure.md
- id: Q02
  title: Where do Plan, Build, Execute and Report show?
  question: 'How do a Task''s four phases appear in the six Spaces: Description, Work
    Details, Runs, Audience Report?'
  hypothesis: Plan is the Task's Description; Build and Execute are its Runs (by type);
    Report is its Audience Report; the phase state is a chip on the Task's row one
    level up.
  acceptance: Answered when each phase has one place and today's Task Work tree has
    a home.
  work: []
- id: Q03
  title: How does a Question read its Runs?
  question: How does a Block Question's report Page name and read the Tasks' Runs
    that answer it, and where does that link show?
  hypothesis: By exact Run identity in the report's Evidence; the Question's row in
    Audience Report links its Tasks; the Runs Space lists the Runs per Question.
  acceptance: Answered when the link is written both ways and drawn.
  work: []
- id: Q04
  title: Which skills make the work theme?
  question: Which of today's 1_base/task skills belong to the work theme (2_work/work),
    which stay in base because every theme calls them, and what is the work theme's
    door?
  hypothesis: Base keeps hai-task (the Task folder and Plan, Build, Execute, Report
    contract other themes call) and hai-workflow (beside hai-run); work gets
    workbench-work, the task-for-* kinds and their agents; the stage pipelines stay
    out (this Block excludes them).
  acceptance: Answered when each skill in 1_base/task has a home JL agrees, drawn
    in studio/, and b04 has moved the files.
  work: []
```

## Related resources

```yaml
resources:
- title: hai-task skill (the Task door)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/3_theme/../1_base/task
  questions:
  - Q01
  - Q02
  - Q03
- title: the work Theme folder (being set up)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/2_work/work
  questions:
  - Q01
  - Q02
  - Q03
```

## Blueprint home

This Theme is an independent blueprint Block under `examples/Project-Ladder/blueprint/b17_theme_work/`
since 261010. Its studio topics, questions, reports and Runs keep their existing
identities. Shared toolkit foundations remain in [b01](../../../Project-Packages/work/b01_haipipe-toolkit/board.md).

## Earlier purpose (until 261031)

- spine: Design questions about the work Theme as one ladder: what a task Block, a work Job, a work Task and a hard Run each hold and show, how Plan, Build, Execute and Report map onto the six Spaces, and how a Question's report reads its Tasks' Runs.
- close: Each recorded question has a report Page with an answer status, and every answered question names the skill, workbench or builder change that settled it.
