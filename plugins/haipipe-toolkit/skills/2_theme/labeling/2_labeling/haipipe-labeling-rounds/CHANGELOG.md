# subjective-label-rounds · CHANGELOG

## [0.1.4] — 2026-10-26

Hidden from the skill listing (`disable-model-invocation: true`); reached through the `/haipipe-labeling` door, which reads this SKILL.md by path. Nothing moved; `/haipipe-labeling-rounds` still works when a person types it. (hide 261026)

## 0.1.3 · 2026-09-29

- Document `calibration.py finalize` for a fully judged batch whose final
  Result write was interrupted. It closes the existing running Ticket after
  event verification without replaying a human judgment.

## 0.1.2 · 2026-09-29

- Recover an interrupted first/lock sequence on `open_item` without asking
  for a second first answer, and refuse writes to a closed calibration Run.

## 0.1.1 · 2026-09-29

- Clarify that `+ New Run` opens the first request, its `Copy` button copies it,
  and `Resume` copies an updated request after `open_item` allocates the Run.

## 0.1.0 · 2026-09-29

- New: the Labeling › Rounds view skill (JL 260929: one skill per view, never shared).
  Its Run text moved here from `label-building-workflow`, which keeps only the order.
