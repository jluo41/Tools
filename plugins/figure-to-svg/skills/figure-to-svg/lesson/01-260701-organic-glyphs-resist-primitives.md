# Lesson 01: Organic/interlocking glyphs resist primitive hand-authoring — switch methods after 2 rejections

## The Problem
A teal handshake icon (two clasped hands with cuffs and interlocking fingers) was hand-authored
from primitives three separate ways — abstract cuff+clasp, refined clasp, then a careful
pixel-by-pixel trace off a gridded zoom of the source. The user rejected all three ("like watch
bands", "still bad") and finally said "just download one online." Swapping in Font Awesome's
`handshake` glyph (recolored) was accepted immediately.

## The Symptom
The same shape gets rejected on visual review more than once, each retry being the *same method*
(draw-from-primitives) with better parameters. Interlocking/organic silhouettes look "off" or
"weird" no matter how the primitives are nudged.

## The Solution
For a known-hard glyph, offer the alternative route on the FIRST sign of trouble, not the fourth:
1. Pull a clean open-license glyph (Font Awesome — CC BY 4.0, Tabler, Material Symbols), recolor
   to the figure palette, drop it in at the icon's bbox.
2. Or keep the source crop as raster (`"keep_raster": true`) so fidelity is guaranteed.
3. Or ask the user which they prefer.
When feedback repeats, change the KIND of solution — don't refine the failing one.

## Why It Works
Primitive hand-authoring has a high ceiling for flat/line/solid icons (clipboards, shields,
clouds, monitors) but a LOW ceiling for organic, interlocking, or shaded shapes. A stock glyph is
a professionally drawn version of the same object; recoloring it keeps the figure's look while
buying instant fidelity. Repeated identical feedback is a signal the *method* is wrong, not the
parameters.

## When to Apply
Handshakes/clasped hands, faces, detailed animals, gestures, anything with overlapping fingers or
organic curvature — and any glyph the user rejects on look twice.

## Caveats
Recolor stock glyphs to match the palette and note the source/license. If exact fidelity to a
*specific* custom drawing matters more than cleanliness, prefer raster over a stock look-alike.
