---
workbench: insight
dataset: demo
prototype: work/b01_topic_prototype
accumulates: '?'
versions:
- version: v1
  extract: $EXTRACTS/demo-v1
  frozen: <date>
  rows: <n>
  new: the first extract
- version: v2
  extract: $EXTRACTS/demo-v2
  frozen: <date>
  rows: <n>
  new: <what is new>
- version: v3
  extract: $EXTRACTS/demo-v3
  frozen: <date>
  rows: <n>
  new: <what is new>
---

# b01 · <topic>

One dataset, its versions, a Job per pair (Prototype version × data version).

## Questions

```yaml
questions:
- {id: Q01, title: What did each Job answer?, level: data, report: reports/q01_record/q01_record.md}
- {id: Q02, title: What moved and why?, level: information, report: reports/q02_moved/q02_moved.md}
- {id: Q03, title: What replicates across data versions?, level: knowledge, report: reports/q03_replicates/q03_replicates.md}
- {id: Q04, title: What do we counsel?, level: wisdom, report: reports/q04_counsel/q04_counsel.md}
```
