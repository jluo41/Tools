---
name: haipipe-design-pagedown
description: >-
  DesignBoard workflow phase D5 and Folder contract for PageDown: reread every
  Folder changed by a round as a document, repair stale prose without changing
  decisions, run a milestone cold read, and seal the round. Trigger: page down,
  seal design round, stale design prose, D5, /haipipe-design-pagedown.
metadata:
  version: "1.0.4"
  last_updated: "2026-09-01"
  workflow: haipipe-design-workflow
  phase: D5
  folder_kind: design-pagedown
  primary_face: page
  page_ruling: none
---

# /haipipe-design-pagedown · make the grown board read true

Load `haipipe-folder`, the Design door/workflow, `haipipe-page`, and the fresh
Board reviewer at milestone rounds.

## Position

D5 starts after all D4 threads are terminal and ends at GD6. It seals one
round, then stops. It never starts fielding or another round automatically.

## Folder Kind

PageDown is the round's cross-Folder truth pass. Its subject is the set of
Folders changed by the round: BR00, Design Pages, promoted principles, and
`board.md`. It materializes one minimal
`workflow/rounds/R<NN>-pagedown/` receipt Folder so the pass itself has two
faces, status, and a testable close. It is not a new Page Type or an editorial
cleanup lane, and its receipt never competes with the affected Folders as the
authority for their prose or decisions.

## Input

The round's cards, units, verdicts, terminals, renders, emitted needs,
promoted principles, receipts, and the current prose of every affected Folder.

## Page Face

The receipt Page Face names the round, affected Folder addresses, before/after
versions, findings, repairs, cold-read result, and GD6 seal. Reread title,
Opening, Diagram, Content roles, scope/law prose, state lines,
Files, and board Topic/close as one document. Counts must equal rows on disk;
era-frozen explanations must not survive a changed decision. Optional promoted
principles must still state their promotion reason, pinned warrant, rail, scope,
and affected divisions.

## Task Face

Write the receipt Folder's plan/report while repairing prose and stale
references only. Do not alter cards, unit content,
verdicts, `accepted:`, `emitted:`, `killed`, or human signatures. At milestones
or before outside review, dispatch a fresh zero-background cold read: a stranger
must identify what the board is, what it produced, and what remains open.

## Plugins

- `outline` required to inspect human plan/receipts;
- `folder` live surface required to inspect material and staleness;
- `pagex` read-only for resolving references;
- no private PageDown, Task, or Runs plugin.

## Gate and Closure

GD6 passes when all grown Pages read true, counts and references resolve, the
round receipt is complete, and any required cold read passes. A decision-level
defect is reported into the next round; D5 never repairs it in place.

## Handoff

Seal the round and stop. Accepted artifacts may be handed to the task layer for
building/fielding; emitted needs cross to the Insight workflow; measured
effects later return as new Data Folders.

## Files

- Receipt Folder: `workflow/rounds/R<NN>-pagedown/`
- Receipt Page Face: `<receipt>/<receipt>.md`
- Task Face: `<receipt>/workflow/plan.yaml`, `report.yaml`, and `receipts/`
- Surfaces read: `BR00`, `DS*`, optional `P*`, and `board.md`
- Domain receipts remain in each affected Brief/Design Folder's
  `outline/<stem>-log.md`.
