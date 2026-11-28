---
step: source
script: source
goal: 'Read the raw export, cut each date to its day, and check its keys before anything uses it'
reads: 'ctx.raw example.parquet'
writes: 'rows.parquet (dates cut to the day); metrics.json with its counts and checks'
checks:
- no key column is empty
- arms are A or B
- groups are group_1, group_2 or group_3
- outcome is 0 or 1
cut: []
params: []
agreed: ✅ 261126
---

# source

A row with an unknown arm or group stops the Run here, not inside a question.
