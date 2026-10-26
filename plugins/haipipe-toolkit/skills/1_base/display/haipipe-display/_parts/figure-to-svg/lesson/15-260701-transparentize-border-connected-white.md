# Lesson 15: Transparentize by removing only *border-connected* white

## The Problem
Making a white-background icon transparent by turning **every** near-white pixel to alpha 0 also
erases the whites INSIDE the icon — a robot's white face, calendar cells, a shield's white fill —
punching holes in it.

## The Solution
Remove only the white region **connected to the border**: label near-white pixels, drop the
components that touch the image edge, keep the rest opaque. Erode the opaque mask ~1px to eat the
anti-aliased halo.

## Why It Works
The background is one contiguous region that touches the border; interior whites are enclosed by
darker outlines and don't reach the border, so a border-connected flood spares them.

## When to Apply
Any time you convert a white-background raster icon to a transparent PNG — e.g. sliced grid icons
before embedding them as `<image>` in an SVG.

## Caveats
Fails if the background isn't clean white, or if an interior white *opens* to the border through a
gap in the outline (that interior gets eaten). Generate icons on pure `#FFFFFF` with closed outlines.
