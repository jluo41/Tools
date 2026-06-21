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

# K03 - Validation gain does not transfer to OOD

## Claim

The new model improves validation accuracy, but the improvement does not
transfer to the tested OOD split.

## Evidence

- Validation result improved over baseline.
- OOD result did not improve under the tested split.
- Probe verdict: confirmed with caveat.

## Caveats

- Only one OOD split has been tested.
- The claim should be revisited after param-matched or multi-split probes.

## Change log

- 2026-06-21: filed from `probe:P001_model_ood`.
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

## Trigger

Use this recommendation whenever a narrative, application report, or paper
claims robustness from validation-only improvements.

## Rationale

This follows from K03: the validation gain did not transfer to OOD in the tested
probe.

## Change log

- 2026-06-21: filed from `K03`.
```

## What Did Not Become A Card

The raw run completion note did not become a D card.

Reason:

```text
It is preserved in the task folder, but it is not reusable project knowledge.
```
