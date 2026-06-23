---
date: 2026-06-23
status: open
source: user
scope: haipipe-paper-claims / 2-claims template
---

# Claims should start with Claim 0: dataset description

Before any hypothesis testing, the claims ledger should have a "Claim 0" or
"Research Question 0" that describes the dataset:
- What is the dataset? (N, structure, coverage)
- How were the variables constructed? (LLM extraction → 5-level ordinal)
- What is the quality of the measurement? (sufficiency, consistency)
- What are the correlations between measures?

This is standard in empirical IS papers: the first result is always "here is
the data, here is the measurement quality." Without this, reviewers don't know
what they're looking at when they see H1-H4 results.

In the PhyTraitNudging paper, this matters especially because:
- The Big Five scores are 5-level ORDINAL (not continuous) — this constrains method choices
- Coverage varies: Agree 100%, Neuroticism 72% — the sample shrinks per trait
- Only 49% of prescribers have ALL scores — intersection coverage is low
- Agreeableness correlates .74 with overall_score and .87 with IQC — is it
  personality or just "being a good doctor"?
- EmotionStability = exactly -1.0 × Neuroticism — they're the same measure inverted

Fix: add to the haipipe-paper-claims template:
- C0 (data description) as a required claim row before H1
- The claims skill should check: does a data description exist?
- The display skill should link: is there a Table 1 / dataset overview?
