# Delivery: Display
state: ✅ RULED
owner: JL
method: let Paper own the visual argument, caption, placement, and gate while the Display layer owns rendering

## Question
What does Paper own when a task or discovery result becomes a figure or table?

## Boundary
- ✅ Covered here
  Display request, unit, caption, label, placement, and human acceptance.
- ↪ Covered by `/haipipe-display`
  Recipe, renderer, candidates, and render promotion.

## Diagram
```text
paper request → Display renderer → unit → caption/label → section placement
```

## Content
| Field | Contract |
|---|---|
| Lifecycle | After Literature and Value have made the evidence inspectable. |
| Authority | `S-Display-*` for meaning and gate; the display unit for the promoted render. |
| Projects to | `displays/<unit>/float.tex`, assets, labels, and section references. |
| Skills | Paper Display stage plus the shared Display skill family. |
| Consumes | Display-ready task/discovery outputs and manuscript claims. |
| Gate | The human accepts what the display argues and the exact promoted render. |
| Open gaps | The shipping/working split inside a display unit remains open on QA6. |

## Items to Finish
- [x] Regroup QC3, QC4, and QD1-QD4 here.

## Where we are
The Paper/Display ownership seam is ruled and the detailed pages remain intact.

## Files
- `QC3-sentence-display-table.md`
- `QC4-sentence-display-figure.md`
- `QD1-the-display-folder.md` through `QD4-a-display-placed-in-a-section.md`

## Law
Paper owns why a Display exists, what it says, where it lands, and whether it is accepted. The Display layer makes it.

## Glossary
- **Display unit**: one figure or table's argument, render, caption, label, and working record.

## Log
260729 · Display kept as one Delivery group after Literature and Value.
