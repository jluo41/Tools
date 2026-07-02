# Lesson 18: Re-add decontextualized detail as vector at compose time

## The Problem
Regenerated icons are drawn in isolation, so context baked into the original is lost:
- the pilot-domain icons had light-blue **badge circles** (stripped at generation for uniform grids),
- the governance-banner **shield is white-on-navy**, but the regenerated shield is solid navy —
  **invisible on the navy banner**.

## The Solution
Add the lost context as **vector at compose time**, not in the raster:
- draw the badge circles as `<circle>` rings behind each icon;
- draw a **white shield as a vector path** on the dark banner instead of embedding the dark raster.
Generate icons plain (no circles/badges) for uniform, sliceable grids; re-add rings and backers in SVG.

## Why It Works
Uniform plain icons keep grids sliceable; badges/backers are simple shapes better authored as
crisp, recolourable vector than baked into a raster. And a dark raster **cannot** be recoloured to
show on a dark fill — a vector can.

## When to Apply
Icons that sit inside badges/circles/rings; any icon whose fill matches its background band
(white-on-dark, dark-on-dark).

## Caveats
Don't use SVG filters (`feColorMatrix`) to recolour the raster for a PPT deliverable — PowerPoint's
Convert to Shape may not honour filters; use a real vector shape (see Lesson 16).
