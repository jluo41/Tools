# How are the toolkit's blueprints organized?
state: 🔴 OPEN
answers: Q01
answer-status: open

## Opening

The 261010 layout promotes each Theme to its own blueprint Block. The migration
is implemented; the broader organization question remains open for review.

## Content

### Current layout

- [b01](../../board.md) keeps shared foundations as j01–j05, its package map,
  theme matrix, and questions that span shared Jobs or Themes.
- b11–b17 are peer Theme Blocks: insight, design, cowork, discovery, labeling,
  paper and work. Each has board.md and its existing studio, reports and Runs.
- b02 and b03 keep the utilities and human-study package blueprints.

### Migration record · 261010

`blueprints/b01_haipipe-toolkit/jNN_theme_<name>/` moved to
`blueprints/bNN_theme_<name>/` for NN 11–17. The former jNN_theme_<name>.md
faces became board.md. Topic, question and Run numbers, frozen history, and
existing local work were carried with their Theme. Skill links, Guide drawing
paths and builder roots follow the promoted Blocks. The live toolkit map and
theme matrix now show the shared Jobs and independent Theme Blocks.

### Evidence

- [the shared foundations and Theme index](../../board.md)
- [toolkit map](../../studio/s01-toolkit-map/s01-toolkit-map.md)
- [theme matrix](../../studio/s02-theme-matrix/s02-theme-matrix.md)
