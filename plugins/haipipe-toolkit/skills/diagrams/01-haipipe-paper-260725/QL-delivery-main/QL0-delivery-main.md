# Delivery: Main
state: 🟡 PARTIAL
owner: JL
method: treat each Main S page as the authoritative manuscript unit and its LaTeX/Word forms as projections

## Question
How do authoritative Main pages become the journal's main manuscript without becoming a second authoring tree?

## Boundary
- ✅ Covered here
  Main-page authority and projection role.
- ↪ Covered by Build
  Candidate generation, checking, and promotion.

## Diagram
```text
S-Main-* ## Content → candidate → sections/ → master
```

## Content
| Field | Contract |
|---|---|
| Lifecycle | Main manuscript work after the evidence/display lanes. |
| Authority | `0-lifecycle/4-main/S-Main-*.md`. |
| Projects to | `sections/*.tex`, Word handoffs, and the root master. |
| Skills | Section-edit stages plus `haipipe-paper-project`. |
| Consumes | Opening, Work, Literature, Value, and Display contracts. |
| Gate | The owning S page is explicitly GATED and projection checks pass. |
| Open gaps | Only MISQ Main-1 currently passes G1; the rest remain open or partial. |

## Items to Finish
- [ ] Add detailed Main-unit pages only when a cross-paper rule needs one.

## Where we are
Authority is ruled; the first candidate-only projection exercised Main-1.

## Files
- `0-lifecycle/4-main/`
- `sections/`

## Law
Main S pages are authored. `sections/` is a submission projection and is never edited as the independent source.

## Glossary
- **Main unit**: one authoritative S page and the manuscript files it projects.

## Log
260730 · Main-1 candidate passed G0-G3 in the first runtime trial.
