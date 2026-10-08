# Lesson 03: score_icon.py collapses on white-on-dark (inverted-polarity) icons — judge those by eye

## The Problem
Footer icons were WHITE glyphs meant to sit on a dark navy bar. Authored as white-on-transparent
and scored with `score_icon.py`, they came back sim≈0.05, shape=0.00 — an apparent total failure —
even though the shapes were correct.

## The Symptom
A drastically low score (near zero, `shape` especially) for an icon that visually matches fine;
or the inverse — a PASS on something that looks wrong.

## The Solution
For inverted-polarity (light-ink-on-dark) icons, don't trust the numeric gate. Verify by
compositing the SVG on its true background color and looking:
`cairosvg.svg2png(..., background_color="#001a5e")`. Use the eye for these; reserve the score for
normal dark-on-light icons.

## Why It Works
`score_icon.py` trims to content and compares filled masks assuming dark ink on light ground. A
white icon on transparent inverts the mask polarity, so the overlap metric compares opposite fills
and collapses — a measurement artifact, not a quality signal.

## When to Apply
Any icon drawn light/white for a dark panel or footer bar; any time the score contradicts a clear
visual match.

## Caveats
Also affects tiny, heavily anti-aliased crops (see Lesson 04): their mean ink samples toward a
pale midtone, capping `color`. Treat low scores on small/inverted crops as suspect, not decisive.
