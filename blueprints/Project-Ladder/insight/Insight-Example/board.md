---
board-kind: insight-board
workbench: insight
dataset: Example
prototype: work/Prototype-b91-Example
accumulates: 'yes'
versions:
- version: v1
  label: first ten days
  folder: Tools/blueprints/Project-Ladder/insight/Insight-Example/data/v1/
  frozen: '261106'
  new: 'the first extract: ten days, 600 rows'
  preview: [date, arm, group, outcome, score]
- version: v2
  label: all sixteen days
  folder: Tools/blueprints/Project-Ladder/insight/Insight-Example/data/v2/
  frozen: '261106'
  new: 'six more days: 960 rows, the first ten days unchanged'
  preview: [date, arm, group, outcome, score]
goal: What a made-up two-arm dataset says, freeze by freeze
---

# Insight · Example: what a made-up two-arm dataset says, freeze by freeze

One dataset, its data freezes, and one Job per pair (analysis plan × data freeze).

This is the insight theme's placeholder Board (the UI prototype for b11): every row of its data is made up by
`data/make_example_data.py` (seed 7), and every name in it is a placeholder. Its questions and scripts live in the
Prototype `work/Prototype-b91-Example`; this Board runs them on a data freeze and reads what they found.

## Topic

What a made-up two-arm dataset can and cannot say, by DIKW level: what the extract holds (D), the rates and the arm
gap inside each cut (I), whether the gap holds under test and whether one counsel serves both groups (K), the counsel
a person signs for Design (W), and the plain answers a leader reads first (X).

```text
Map                                              analysis plans (rows) × data freezes (columns)
j01_prototype-p1-example-questions_data-Examplev1  plan 1 × freeze 1 · the first Job, closed
j02_prototype-p1-example-questions_data-Examplev2  plan 1 × freeze 2 · the data moved, in progress
```

## Questions

The Board's own questions, over the Jobs' answers (reports/qNN_<topic>/).

```yaml
questions:
- {id: Q01, title: Does the arm gap hold from data freeze 1 to data freeze 2?, level: knowledge, report: reports/q01_gap-across-freezes/q01_gap-across-freezes.md}
```
