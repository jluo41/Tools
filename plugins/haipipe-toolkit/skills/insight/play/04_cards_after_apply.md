# Cards After Apply

This file shows the kind of cards created after applying
`03_INSIGHT_REVIEW.example.yaml`.

The exact IDs may differ in a real project.

## K Card

```markdown
---
id: K03
layer: K
title: "Validation gain does not transfer to OOD"
status: active
created: 2026-06-21
updated: 2026-06-21
sources:
  - probe:P001_model_ood
refs:
  - task:T001_validation
  - task:T002_ood_split
confidence: medium
---

# K03 - Validation gain does not generalize to OOD

## Claim

The validation-set gain found in-sample does NOT generalize to the tested
out-of-distribution split. (A generalization claim — note the in-sample gain
itself, the +X on val, is an I card; whether it carries over is this K.)

## Generalization basis

- The val gain did not reproduce on the OOD split (the inferential test that
  would let it generalize fails there). p / CI of the OOD comparison go here.
- Cites the in-sample I card(s) for the val gain.

## Counter-evidence

- Only one OOD split has been tested; a different split might behave differently.

## Confidence rationale

medium — the non-transfer is clean on the one split tested, but a single split is
the statistical tier only, not robustness across splits. Multi-split would raise it.

## Scope

The tested OOD split; current training schedule. Does not speak to other shifts.

## Change log

- 2026-06-21: filed from `probe:P001_model_ood` (one possible basis; no probe is required).
```

## W Card

```markdown
---
id: W02
layer: W
title: "Do not use validation gain as OOD evidence"
status: active
created: 2026-06-21
updated: 2026-06-21
sources:
  - K03
confidence: medium
---

# W02 - Do not use validation gain as OOD evidence

## Recommendation

When reporting model quality, separate validation gains from OOD evidence.

## How to act

In any results table or claim, label val-set and OOD-set numbers separately, and
do not state OOD robustness unless an OOD test backs it.

## Risk posture

K03 is medium-confidence (non-transfer shown on one OOD split only). That medium
confidence justifies a conservative rule — "do not claim OOD robustness from val
gains" — rather than a strong "the model fails OOD" assertion. If a multi-split
probe later raises K03 to high, the rule can harden.

## Why now

Narratives and papers are most tempted to over-read a val gain at write-up time;
the rule is needed before the claim is drafted.

## Decay condition

- A multi-split OOD probe lands (re-evaluate K03 and this rule), OR
- the project stops reporting val-only improvements.

## Change log

- 2026-06-21: filed from `K03`.
```

## What Did Not Become A Card

The raw run completion note did not become a D card.

Reason:

```text
It is preserved in the task folder, but it is not reusable project knowledge.
```
