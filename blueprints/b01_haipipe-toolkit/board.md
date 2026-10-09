# b01 · haipipe-toolkit

board-kind: task-block
spine: The blueprint of the `plugins/haipipe-toolkit` package: its skill layers, its project ladder and workbench, each theme, and the chat; one Job per area.
close: Every Job's questions have a report Page with an answer status, and every answered question names the skill, server or file change that settled it.

## Topic

One blueprint Block per package in `plugins/` (261009): this one is `plugins/haipipe-toolkit`; `b02_haipipe-utils`
and `b03_inlab-human` are the others. Until 261009 each Job here was a Block of its own in `Tools/blueprints/`
(`b11_theme_insight` is now `j11_theme_insight`, the same number); each kept its questions (`reports/`), its
studio topics (`studio/`) and its Runs (`runs/`), now at the Job level.

## Jobs

```text
j01_utils               the 0_utils skills: reply format, questions, small helpers
j02_base                the 1_base skill layer: project, page, task, question, display families
j03_project_workbench   a Project from root to Run, and the shared workbench frame
j04_skill_folder        how skills and servers are laid out on disk
j05_chat                the chat: the old in-page chat, and how a workbench Run reaches Claude Code
j11_theme_insight       the insight theme          j15_theme_labeling   the labeling theme
j12_theme_design        the design theme           j16_theme_paper      the paper theme
j13_theme_cowork        the cowork theme           j17_theme_work       the work theme
j14_theme_discovery     the discovery theme
```

## Questions

The Block's own questions, across its Jobs. None yet; each Job keeps its own.

```yaml
questions:
- id: Q01
  title: How are the toolkit's blueprints organized?
  question: 'How does Tools/blueprints/ map the toolkit: one Block per package, one
    Job per area with the old Block numbers, and what lives at the Block level versus
    in a Job?'
  hypothesis: One Block per package in plugins/; a Job per area keeps its own studio,
    reports and runs; the Block keeps only the package map and questions that span
    Jobs.
  acceptance: Answered when the layout, the renames (designs to blueprints, Blocks
    to Jobs) and the Block-level rule are written down with the paths they changed.
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
