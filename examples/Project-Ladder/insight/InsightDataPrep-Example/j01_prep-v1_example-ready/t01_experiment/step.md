---
step: experiment
script: experiment
goal: 'Write the experiment card from the raw export: arms, groups, days'
reads: 'ctx.raw example.parquet'
writes: 'experiment_card.json and .md'
checks:
- the raw export holds example.parquet with date, arm, group, outcome, score
cut: []
params: []
agreed: ✅ 261126
---

# experiment

The card comes first (rule 7); a later step and every question read what it found about the arms and the days.
