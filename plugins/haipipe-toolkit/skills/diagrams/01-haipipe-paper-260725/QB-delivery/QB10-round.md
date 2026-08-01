# Delivery: Round
state: 🟡 PARTIAL
owner: JL
method: keep each batch of review, rebuttal, revision, and resubmission as one dated round record

## Opening
How should the paper represent repeated response batches after an initial submission?

Scope: This page covers Submission response and later review/revision batches as Round pages. Build covers The artifact diff, compile, and shipment for a round.

## Diagram
```text
submission → Round 1 → Round 2 → … → accepted/retired
                review · rebuttal · revision · resubmission
```

## Content
| Field | Contract |
|---|---|
| Lifecycle | Submission and every later batch of external feedback and revision. |
| Authority | One `S-Round-*` page per batch, with dated decisions and applied changes. |
| Projects to | Rebuttal, response letter, revised manuscript, diff, and resubmission package. |
| Skills | `haipipe-paper-round`, rebuttal, diff, compile, and ship leaves. |
| Consumes | Reviewer/editor input plus the accepted prior submission. |
| Gate | A human verifies every response is applied or explicitly declined and the resubmission matches the round record. |
| Open gaps | Board filename resolution still needs `Round` added as a first-class family. |

## Items to Finish
- [x] Rename the Delivery group from Response to Round.
- [ ] Make `Round` resolvable in Board family tooling.

## Where we are
The concept and name are ruled; the Board family implementation remains open.

## Files
- `0-lifecycle/7-round/`

## Law
Use Round, not Response. One batch is one round, and every round keeps its review, decision, applied change, and shipped artifact together.

## Glossary
- **Round**: one externally triggered batch of review, rebuttal, revision, and resubmission.

## Log
260729 · JL renamed Response to Round and defined it as batch/iteration ownership.
