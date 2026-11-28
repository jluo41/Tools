---
board-kind: insight-board
workbench: insight
dataset: Example
prototype: insight/InsightQuestionBook-Example
accumulates: 'yes'
versions:
- version: data-v1
  label: first ten days
  folder: Tools/examples/Project-Ladder/insight/Insight-Example/data/data-v1/
  frozen: '261106'
  new: 'the first extract: ten days, 600 rows'
  preview:
  - date
  - arm
  - group
  - outcome
  - score
  raw: Tools/examples/Project-Ladder/insight/Insight-Example/data/data-v1
  cut: {}
  params: {}
- version: data-v2
  label: all sixteen days
  folder: Tools/examples/Project-Ladder/insight/Insight-Example/data/data-v2/
  frozen: '261106'
  new: 'six more days: 960 rows, the first ten days unchanged'
  preview:
  - date
  - arm
  - group
  - outcome
  - score
  raw: Tools/examples/Project-Ladder/insight/Insight-Example/data/data-v2
  cut: {}
  params: {}
goal: What a made-up two-arm dataset says, version by version
dataprep: insight/InsightDataPrep-Example
---

# Insight · Example: what a made-up two-arm dataset says, version by version

One dataset, its data versions, and one Job per pair (analysis plan × data version).

This is the insight theme's placeholder Board (the UI prototype for b11): every row of its data is made up by
`data/make_example_data.py` (seed 7), and every name in it is a placeholder. Its questions and scripts live in the
Question Book `insight/InsightQuestionBook-Example`; this Board runs them on a data version and reads what they found.

## Topic

What a made-up two-arm dataset can and cannot say, by DIKW level: what the extract holds (D), the rates and the arm
gap inside each segment (I), whether the gap holds under test and whether one counsel serves both groups (K), the counsel
a person signs for Design (W), and the plain answers a leader reads first (X).

```text
Map                                              analysis plans (rows) × data versions (columns)
j01_question-v1-example-questions_data-v1  question-v1 × data-v1 · the first Job, closed
j02_question-v1-example-questions_data-v2  question-v1 × data-v2 · the data moved, in progress
```

## Questions

The Board's own questions, over the Jobs' answers (each answered in a Studio topic, sNN-qNN-<topic>/).

```yaml
questions:
- {id: Q01, title: Does the arm gap hold from data-v1 to data-v2?, level: knowledge, report: s04-q01-gap-across-data-versions/s04-q01-gap-across-data-versions.md}
```
