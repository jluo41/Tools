# Lesson 02: Trademarked wordmarks and photographic elements → keep_raster from the start

## The Problem
A figure card contained brand wordmarks (dexcom, ŌURA, fitbit, ZIO, Epic, FHIR, FDA) and product
photos (a smartwatch, a ring, a biosensor patch). These do not reduce to a handful of clean
primitives without becoming a confidently-wrong redraw of a trademarked mark.

## The Solution
Tag such items `"keep_raster": true` in items.json from the FIRST pass. `crop_bboxes.py` still
cuts them, and `compose_svg.py` embeds the PNG crop in place — so the master stays honest and the
rest of the figure stays vector/editable. Say explicitly which items you kept as raster.

## Why It Works
The skill's fidelity bar: "honesty about a weak match beats a confident wrong one." A logo redrawn
by hand reads as a *different* logo (brand/legal problem); a photo traced to primitives loses its
texture. Embedding the original crop is both faithful and cheap.

## When to Apply
Any brand wordmark/logo, any photographic or richly-shaded element, tiny rendered text/numbers
(e.g. "120/80"). Decide raster-vs-vector during Analyze, not after a failed vectorization.

## Caveats
Raster crops don't scale/recolor — keep them at adequate resolution and let vector elements carry
the scalable parts of the figure.
