# Lesson 17: Measure panel/background/gradient colours from the source — don't guess

## The Problem
Composed a section with a **guessed** gray-blue panel fill and flat teal headers. The user flagged
the background as wrong: the real panels were **white**, the banner a **darker navy**, and the
headers were **left→right gradients**.

## The Solution
Sample actual pixels from the source for backgrounds too, not just icons:
- panel-body fill — sample an *empty interior* point (not a text pixel),
- the banner colour,
- header **gradient endpoints** — sample the left and right of the band.
Use the measured hex values and real `<linearGradient>`s.

## Why It Works
Backgrounds carry "same figure" recognition more than icons do — a wrong panel tint or a missing
gradient is immediately visible. Guessing fills is as unreliable as guessing icon colours; the
skill already says sample icon colours — extend that to panels, banners, and gradients.

## When to Apply
Composing any panel/banner/section replica. Sample fill, stroke, and both gradient endpoints of
each coloured band.

## Caveats
Sampling a text pixel instead of the fill returns the text colour — pick an empty region. A single
sample can hit an icon or anti-aliased edge; take a few and take the median.
