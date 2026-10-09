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
questions: []
```
