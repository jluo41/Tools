---
name: paper-edit-values
description: "Reconcile every numeric value in an existing LaTeX draft against its 0-display/ source. Topic ② of the 4-edit cycle. Self-contained numeric-consistency checks. STUB — scope defined, checklist to be filled. Trigger: check numbers, numeric consistency, reconcile values, verify stats."
metadata:
  version: "0.0.1"
  status: stub
  stage: 4-edit
  topic: "② values"
---

# paper-edit-values  (stub)

Topic ② of the `4-edit` cycle. Runs **after** content has settled for a section.
Self-contained: it carries its own numeric-reconciliation logic rather than
delegating to `6-review`.

Read `../_shared/` first — especially `comment-protocol.md`. Like every 4-edit
sub-skill it is **comment-first**: Round 1 inserts `%% {CC-values-vMMDD}: finding
| suggestion ========>` and changes no text; apply waits for the human
`========> {XX}:` reply.

## Scope

Every number in the prose, tables, and captions matches the artifact it came
from. Ground truth is `0-display/` (figures, tables, computed stats) and the
analysis outputs — never the prose's memory of a number.

## Intended checks (to be written)

- [ ] Each `% TODO[values]` flag from the content pass is resolved against source.
- [ ] Every reported statistic (means, $r$, CIs, $n$, $p$, $\beta$, $R^2$) traces
      to a `0-display/` value or a logged computation.
- [ ] In-text numbers agree with the same number in tables/figure captions.
- [ ] Rounding/precision is consistent within a section and across the paper.
- [ ] Units and scales are correct and consistent.
- [ ] Derived/aggregate figures (totals, percentages, deltas) recompute correctly.

## Done means

- [ ] No `% TODO[values]` left in the section.
- [ ] Every number sourced and cross-agreeing; the section's ② cell → `done`.

> **Status:** stub. Fill the checklist into `ref/` when topic ② is activated.
