# b01 · haipipe-toolkit

board-kind: task-block
spine: Shared toolkit foundations: utilities, base skills, the project ladder and workbench frame, skill layout, and chat; one Job per area. Theme design belongs to the peer b11–b17 Blocks.
close: Every Job's questions have a report Page with an answer status, and every answered question names the skill, server or file change that settled it.

## Topic

The shared foundations of `plugins/haipipe-toolkit`: utility and base skills,
the project ladder and workbench frame, skill folders, and chat. Each area is a
Job inside this Block. Each Theme has its own peer Block under `blueprints/`
(261010), with its own questions, reports, studio topics and Runs.

`b02_haipipe-utils` and `b03_inlab-human` remain the other package blueprints.
Blueprint Blocks describe a coherent area; a package can have a shared Block
and several Theme Blocks.

## Jobs

```text
j01_utils               utility skills and small helpers
j02_base                base skill families
j03_project_workbench   the project ladder and shared workbench frame
j04_skill_folder        skill and server layout
j05_chat                chat and workbench Runs
```

## Theme Blocks

| Block | Focus |
|---|---|
| [b11_theme_insight](../b11_theme_insight/board.md) | insight |
| [b12_theme_design](../b12_theme_design/board.md) | design |
| [b13_theme_cowork](../b13_theme_cowork/board.md) | cowork |
| [b14_theme_discovery](../b14_theme_discovery/board.md) | discovery |
| [b15_theme_labeling](../b15_theme_labeling/board.md) | labeling |
| [b16_theme_paper](../b16_theme_paper/board.md) | paper |
| [b17_theme_work](../b17_theme_work/board.md) | work |

## Questions

The Block's questions span shared Jobs and the peer Theme Blocks. Each Theme keeps its own questions in its board.md.

```yaml
questions:
- id: Q01
  title: How are the toolkit's blueprints organized?
  question: 'How does Tools/blueprints/ map the toolkit: shared foundation Jobs in b01,
    independent Theme Blocks b11–b17, and what belongs to each level?'
  hypothesis: b01 holds shared foundation Jobs and cross-theme questions; each
    Theme Block keeps its own studio, questions, reports and runs. Package membership
    does not determine the number of blueprint Blocks.
  acceptance: Answered when the current shared and Theme layout, the 261010
    promotion paths, and preserved question, studio and Run identities are documented
    and their references resolve.
  work: []
  report: reports/q01_blueprints_organized/q01_blueprints_organized.md
- id: Q02
  title: Does every theme follow one ladder?
  question: Do the seven themes (insight, design, cowork, discovery, labeling, paper,
    work) put the same things at Block, Job, Task and Run, show them in the same Spaces,
    and name their Runs and skills the same way?
  hypothesis: They share the ladder and the six Spaces; they differ in what a Job
    pins and in their own Runs; the theme matrix shows where they drift.
  acceptance: Answered when the theme matrix (studio s02) lists each theme per level
    and every difference is kept on purpose or opened as a fix.
  work: []
  report: reports/q02_one_ladder/q02_one_ladder.md
- id: Q03
  title: How do sessions share this repo and machine safely?
  question: 'Several sessions edit Tools and run hosts on one machine at once: how
    do they avoid clobbering each other''s edits, branches and processes?'
  hypothesis: Main only, one Block per session at a time with a handoff brief, git
    add of named paths only, and a process is stopped only by its own task or PID,
    never by a pattern.
  acceptance: Answered when the rules are written where every session reads them and
    the 261009 incident (a pattern kill that stopped six hosts and open apps) is recorded
    with its cause.
  work: []
  report: reports/q03_sharing_safely/q03_sharing_safely.md
- id: Q04
  title: What do we track for a studio drawing?
  question: 'A studio topic has a builder, a drawing, a seed snapshot and a preview:
    which are tracked in git, which stay local, and how big may a drawing get?'
  hypothesis: Track the builder and the drawing (it holds a person's marks); keep
    seeds local; write compact JSON and embed screenshots as small JPEGs; studio PNG
    previews are optional.
  acceptance: Answered when the tracking rule is in .gitignore and haipipe-studio,
    and the largest drawings are rebuilt under a size target.
  work: []
  report: reports/q04_studio_drawings/q04_studio_drawings.md
```
