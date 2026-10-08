# Lesson 10: Route hub-and-spoke connectors through a shared bus aligned to panel centers

## The Problem
A radial figure had arrows fanning from a central hub out to columns of cards on each side. The
first pass authored them as per-item bent polylines with ad-hoc coordinates (e.g.
`[[235,244],[300,244],[352,400]]`). Rendered, they looked ragged — kinks that didn't line up, arrow
tips landing off the card edges, feeders meeting at different x's. The user flagged "the lines and
arrows are not aligned."

## The Solution
Author connectors as a **shared bus**, not independent squiggles:
- Pick one **bus x** per side (just outside the cards). Draw one straight vertical segment for the
  whole bus.
- From each card, a short **horizontal** segment at that card's exact vertical center to the bus
  (read the centers from items.json: `y = bbox.y + bbox.h/2`).
- One **arrowhead** segment from the bus into the hub (or from the bus into each card), landing on
  the card's mid-height and just touching its edge.
- Keep every segment purely horizontal or vertical; let the bus carry the turn. Reuse the same bus
  x and the same arrow sizes across the side for visual rhythm.

## Why It Works
Alignment reads as *shared reference lines*. When every spoke touches the same bus x and every
arrow lands on a computed panel center, the eye sees an intentional manifold instead of hand-placed
strokes. Deriving y from the bbox (not by eye) guarantees the tip meets the card.

## When to Apply
Any hub-and-spoke / bus / pipeline diagram: a center node feeding side columns, a data bus into
stacked cards, left-to-right stage flows. Compute endpoints from panel bboxes rather than reading
them off a grid.

## Caveats
Genuinely curved or diagonal connectors in the source should be reproduced as such — this is for the
common orthogonal "bus" layout, not free-form arrows.
