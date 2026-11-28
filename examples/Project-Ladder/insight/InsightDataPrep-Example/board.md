---
board-kind: insight-dataprep
workbench: insight
set: Example
store: _WorkSpace/insight-ready
serves:
- insight/Insight-Example
references: []
goal: 'Example: the made-up two-arm export, made ready, one signed prep version at
  a time'
---

# InsightDataPrep-Example · Example: the made-up two-arm export, made ready

The code that turns a raw export into a folder ready for insight, one Job per prep version
(`jNN_prep-vK_<slug>/`), frozen once a person signs it. It runs nothing: each Board it serves runs a signed
prep version on its own dataset, in a data Job, and adds the folder as its next data version.

## Background

The rows are made up by `insight/Insight-Example/data/make_example_data.py` (seed 7): two arms assigned at random,
three groups, a 0/1 outcome. Nothing is wrong or missing by design; the example has no documents.
