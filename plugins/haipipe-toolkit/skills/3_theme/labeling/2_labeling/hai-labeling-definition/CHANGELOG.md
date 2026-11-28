# subjective-label-definition · CHANGELOG

## [0.2.1] — 2026-10-26

Hidden from the skill listing (`disable-model-invocation: true`); reached through the `/haipipe-labeling` door, which reads this SKILL.md by path. Nothing moved; `/haipipe-labeling-definition` still works when a person types it. (hide 261026)

## 0.2.0 · 2026-10-14

- Region meanings change by a recorded revision: `job.py revise-regions` (`revise_region_meanings`), the same law
  as the label meanings; `status` checks the region chain.

## 0.1.4 · 2026-09-29

- Block G0 confirmation until every label has nonblank human-reviewable
  wording. An empty Contract now directs the user to Definition discussion.

## 0.1.3 · 2026-09-29

- Clarify the missing-G0 restore path: use an intact earlier semantic receipt,
  permit restoration after release only when it predates every round, and keep
  invalid or unbound receipts blocked. Even a matching G0 receipt fails if its
  semantic confirmation came after release. The UI names the restore action.

## 0.1.2 · 2026-09-29

- Require the discussion to close before G0 confirmation. A missing G0 receipt
  can be restored after release only from a valid earlier human attestation;
  a new confirmation cannot certify a past round.

## 0.1.1 · 2026-09-29

- Close definition discussion before releasing a round. The release,
  discussion, and direct meaning-revision writers guard the boundary, so a
  frozen round cannot outlive a retired G0 meaning receipt.

## 0.1.0 · 2026-09-29

- New: the Labeling › Definition view skill (JL 260929: one skill per view, never shared).
  Its Run text moved here from `label-building-workflow`, which keeps only the order.
