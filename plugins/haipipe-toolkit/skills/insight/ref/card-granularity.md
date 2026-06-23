Insight Card Granularity Policy
================================

This file controls how large or small an insight card should be.

The principle:

```text
One card = one reusable knowledge unit.
```

A card is not a raw note, not a whole report, and not a folder substitute. It
should be small enough to cite from a narrative or paper, but rich enough that
a future reader understands the evidence, caveats, and scope without reopening
every upstream artifact.


Folder Rule
===========

DIKW folders stay flat:

```text
insights/
├── D_data/
│   ├── D01_*.md
│   └── D02_*.md
├── I_information/
├── K_knowledge/
└── W_wisdom/
```

Do not create topic subfolders such as `K_knowledge/film/` or
`D_data/ood/`. Topic membership is many-to-many and belongs in metadata:

```yaml
tags: [film, ood, generalization, cgm]
sources: [probe:P.0619_film_ood, I02]
ref_by: [W01, narrative:N01.C2]
```

Navigation belongs in derived views:

```text
insights/views/by_topic.md
insights/views/by_source.md
insights/views/by_narrative.md
insights/views/by_status.md
```


Granularity Tests
=================

Before filing a new card, the INSIGHT_REVIEW.yaml MUST answer these tests.

```text
1. Reuse test
   Will a future narrative, paper, ask session, or decision cite this exact unit?

2. One-sentence test
   Can the card's contribution be stated in one sentence without "and also"?

3. Evidence-coherence test
   Do all sources support the same observation / pattern / claim / action?

4. Merge test
   Would this be better as new evidence inside an existing card?

5. Split test
   Does the candidate contain multiple independent claims, patterns, or actions?
```

If the reuse test fails, `action: skip`.
If the merge test passes, `action: merge`.
If the split test passes, split into multiple candidate cards.


Layer Grain
===========

```text
D — one named dataset's profile (in-sample)
    What the dataset looks like; not every metric, seed, table row, or log line.

I — one in-sample pattern inside ONE dataset
    Cites that dataset's D card(s); no p/CI. Not a whole topic summary, and not a
    cross-dataset regularity (that is robust generalization → a K).

K — one generalization claim with scope and confidence
    Does the pattern hold beyond the sample. p/CI/confidence live here. Not an
    entire theory, research area, or paper section. Low-confidence/negative K are valid.

W — one actionable recommendation, risk-tuned to its K's confidence
    Not a vague strategy memo; it should imply a concrete command or decision.
```


Examples
========

Too fine:

```text
D01: seed 1 MAE = 3.2
D02: seed 2 MAE = 3.4
D03: seed 3 MAE = 3.3
```

Good:

```text
D01: FiLM validation MAE is lower across 3 seeds
```

Too coarse:

```text
K01: Everything we know about FiLM
```

Good:

```text
K01: FiLM improves in-distribution forecasting but does not establish OOD transfer
```

Too vague:

```text
W01: Think more about OOD generalization
```

Good:

```text
W01: Stop treating validation gains as OOD evidence until test-od probe passes
```


Size Budgets
============

These are review targets, not hard parser limits.

```text
D body: 30-70 lines
I body: 40-90 lines
K body: 60-140 lines
W body: 40-90 lines

Most files: <= 160 lines total
Absolute max: 200 lines total
```

If a candidate exceeds the target, first try:

1. move raw detail back to the source artifact and cite it
2. split independent units into separate cards
3. merge redundant evidence into an existing card


INSIGHT_REVIEW.yaml Fields
===================

Every `candidate_cards[]` item SHOULD include:

```yaml
granularity:
  unit: observation | pattern | claim | recommendation
  decision: file | merge | split | skip | blocked
  rationale: "<why this is the right-sized unit>"
  merge_target: K03       # only when decision/action is merge
  split_into: [C4a, C4b]  # only when decision/action is split
```

The action and granularity decision should agree:

```text
granularity.decision=file   -> action=file
granularity.decision=merge  -> action=merge
granularity.decision=split  -> action=blocked until split candidates exist
granularity.decision=skip   -> action=skip
```


Reviewer Gate
=============

Per-card reviewers should fail or block a card when:

- it is too fine: raw row / isolated seed / transient note with no reuse value
- it is too broad: multiple independent claims or recommendations
- it duplicates an active card and should have been `merge`
- it exceeds the size budget without a clear reason
- it uses a folder/subfolder to encode topic instead of tags/views

When in doubt, prefer fewer, stronger cards with better evidence trails.
