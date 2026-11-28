---
step: prepare
script: prepare
goal: 'Write the ready folder the questions read: the rows, their manifest and dictionary'
reads: 'ctx.prev rows.parquet'
writes: 'example.parquet, manifest.json, data_dictionary.csv (the ready folder)'
checks:
- the rows hold exactly the five dictionary columns
- the dictionary holds no record value
cut: []
params: []
agreed: ✅ 261126
---

# prepare

The ready folder has the shape of a data version folder, so question-v1's scripts read it unchanged.
