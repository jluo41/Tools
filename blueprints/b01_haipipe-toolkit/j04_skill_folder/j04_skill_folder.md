# j04 · Skill folder

job-of: b01_haipipe-toolkit (the Block `b04_skill_folder` until 261009; its questions, studio and runs moved with it)
spine: How the toolkit's skills and servers are laid out on disk: the three skill layers (0_utils · 1_base · 2_theme), the servers that pair with them (workbench-shared as the base, one workbench per theme), the paths that must follow a move, and folding the subjective-label plugin in as a theme.
close: Each recorded question has a report Page with an answer status; every move ends with no broken path (code, Markdown links, AGENTS.md) and its tests rerun.

## Topic

`plugins/haipipe-toolkit/skills/` is regrouped into three layers:

```text
skills/
├── 0_utils/    generic helpers, not tied to the Block → Job → Task ladder
├── 1_base/     what every theme is built on: project (ladder, Runs) · task (the work Task) ·
│               page (the Page Task) · question · writing · display · ideation · search
└── 2_theme/    one folder per theme: cowork · design · discovery · insight · labeling · paper,
                each its haipipe-<theme> skills and its workbench-<theme>
```

The servers follow the same split: `servers/workbench-shared` is the base (the Block / Job / Task
frame, the Guide's four Views, Studio, the Runs panel) and each `servers/workbench-<theme>` gives its
theme. The design drawings behind this are in `../b03_project_workbench/studio/` (s08 Task variants, s02 workbench-shared).

Excluded: what each skill says (its owner's); this Block asks only where things live and that every
path follows them.

## Pipeline

```text
a move on disk -> path fix (code · Markdown · AGENTS.md) -> tests rerun -> report Page
```

## Questions

```yaml
questions:
  - id: q01_skill_layers
    question: What goes in 0_utils, 1_base and 2_theme, and how do the servers pair with them?
    answer-status: open
  - id: q02_path_fix
    question: After the skills move, which paths broke, and are they all fixed?
    answer-status: open
  - id: q03_merge_subjective_label
    question: How does plugins/subjective-label fold into haipipe-toolkit as the labeling theme?
    answer-status: open
  - id: q04_theme_shape
    question: Is every theme folder the same shape (a haipipe-<theme> door, its skills named haipipe-<theme>-<thing>, workbench-<theme> at the family top, one place for agents)?
    answer-status: open
```
