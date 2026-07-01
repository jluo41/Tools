# Lesson 09: A stylized "network sphere" hero is not a photo — vectorize it, and lift its baked title into real text

## The Problem
The figure's center hero was a dark-navy "AI Care Transformation Platform" sphere: a radial gradient
disc with a light node-mesh (dots joined by faint lines), a broken teal "orbit" ring with accent
dots, and the title baked into the pixels. It was first kept as a raster crop (`keep_raster`, per
Lesson 02's "keep photos/gradients raster"). The user then asked to make it a real vector — and it
vectorized cleanly, with the title becoming editable `<text>`.

## The Solution
Distinguish a *true photo/texture* (raster) from a **stylized gradient graphic** (vectorizable).
For a network-sphere hero, build it back-to-front from primitives:
- `radialGradient` disc (sample center vs. edge navy: e.g. `#002959` → `#000B44`), offset the
  gradient center up-left for a lit look.
- Node **mesh**: ~12–18 `circle` dots placed around the disc (leave the center open for the title),
  joined by thin low-opacity `polyline`/`path` lines.
- A **broken orbit ring**: a `circle` (fill none) with `stroke-dasharray` giving a few long arcs +
  gaps, plus a couple of small accent dots at the breaks.
- **Lift the baked-in title out**: don't leave it in the raster — emit it as real `<text>` (here,
  three centered lines) so it's editable and recolorable. Mask the raster's corners if any residual
  raster is kept, so no bounding-box halo shows on a tinted background.

## Why It Works
A "network sphere" is *illustration*, not photography: gradients, dots, and lines are exactly what
SVG primitives express. Lesson 02's raster rule is about trademarked marks and true photos/textures
that a redraw would falsify — a synthetic gradient graphic isn't that. And any text baked into a
raster hero is the highest-value thing to make editable, since titles get reworded most.

## When to Apply
Central "platform/ecosystem" spheres, glowing orbs, network/constellation graphics, gradient
badges — any richly-shaded but *synthetic* element, especially one with baked-in text. Refines
Lesson 02: gradient ≠ photo.

## Caveats
The exact node positions don't need to match the source — a pleasing scatter that leaves the center
clear for the title reads as the same object. If a hero truly is a photograph, Lesson 02 still holds:
keep it raster.
