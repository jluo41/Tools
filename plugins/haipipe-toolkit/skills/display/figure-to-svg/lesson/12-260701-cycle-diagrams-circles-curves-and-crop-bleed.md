# Lesson 12: Cycle/hub diagrams need circle backings + curved arrows; loose raster crops bleed

## The Problem
Three defects showed up composing the SHIFT figure's outer regions:
1. **Pilot "domain" icons and cycle nodes lost their circular ring backings** — `compose_svg.py`
   only drew rects (`panels`), so the light-blue rings around each icon simply vanished.
2. **A 4-node care cycle rendered with straight diagonal arrows** — the composer's only connector
   was a straight `arrow`, so the elegant curved arcs became clunky diagonals that cut through the
   node labels ("Outcomes", "AI-Supported").
3. **`keep_raster` crops showed ghost text** — a loose bbox baked in a *neighbour's* label
   ("from wearables" inside the smartwatch crop, "delayed" in the doctor crop, "Mi" from "Missed"
   in the scale crop) and stray dashes from adjacent arrows.

## The Solution
- Added **`ellipses`** support to `compose_svg.py` (`{cx,cy,rx,ry,fill,stroke,stroke_width}`,
  drawn after panels) — draw ring backings as real, editable vector circles behind the icons.
- Added a **`curve`** field to the `arrow` connector: a signed perpendicular bow offset that turns
  the shaft into a quadratic Bézier, with the arrowhead following the **end tangent**. For a cycle,
  place 4 arrows between node rims and give each the same-sign `curve` so they all bow *outward*
  (sign flips relative to chord direction, so compute or just eyeball-and-flip).
- **Tighten every `keep_raster` bbox to the icon's own ink.** Ghost text/arrows in a crop are the
  #1 tell of a loose box. Shrink the offending side (or run `crop_qc --apply`) and re-crop.

## Why It Works
Circles and arcs are first-class figure geometry, not icons — drawing them on the master canvas is
faithful *and* keeps them editable/recolorable, and avoids a per-arc nested SVG. Tight raster boxes
keep the "keep it real" pixels while excluding pixels that belong to a neighbour.

## When to Apply
Any radial/cycle/hub-and-spoke layout (circle-backed icon badges, curved flow arrows). And review
EVERY raster crop for neighbour bleed before composing — see [[02-260701-keep-logos-and-photos-raster]].
