# subjective-label-contract · CHANGELOG

## 0.1.1 · 2026-09-29

Clarify that Contract consumes prepared labeling units. Raw transcript
normalization and unitization are upstream work; the current item-level sealed
draw is not safe when multiple items share one conversation.

## 0.1.0 · 2026-09-29

- New: the Data › Contract view skill (JL 260929: one skill per view, never shared).
  Its Run text moved here from `label-building-workflow`, which keeps only the order.
