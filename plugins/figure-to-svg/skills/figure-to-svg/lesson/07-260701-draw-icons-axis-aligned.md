# Lesson 07: Draw device/object icons axis-aligned — a baked-in rotation reads as "tilted"

## The Problem
A CGM glucose-meter icon was hand-authored with a `transform="rotate(-3 37 54)"` wrapping the whole
device, added to mimic the slight lean of the meter in the source photo. In isolation it looked
fine, but nested into the composed figure it read as visibly crooked, and the user asked "why is
this not vertical?".

## The Symptom
An icon that verified OK on its own looks tilted/off once placed at its bbox in the master. A
`rotate(...)` (or a skew) on the icon's outer group.

## The Solution
Draw device/object icons **upright and axis-aligned** by default. Normalize a source's subtle lean
to vertical rather than reproducing it. Only keep a rotation when the source object is *strongly,
deliberately* angled (and even then, prefer baking the angle into the shape coordinates over a
wrapping `transform`, so downstream tools don't compound it). When re-centering, drop the transform
and set the `viewBox` tight to the upright artwork.

## Why It Works
A few degrees of tilt that looks "characterful" at icon scale becomes an obvious defect once the
icon sits in a grid of otherwise-orthogonal cards, because the eye compares it to its neighbors and
the panel edges.

## When to Apply
Any device/product icon (meters, phones, monitors, watches, speakers) and any icon whose source is
slightly rotated. Check every icon's outer group for a stray `rotate`/`skew` before composing.

## Caveats
Genuinely diagonal motifs (a rising arrow, a lean-by-design logo) should keep their angle — this is
about *incidental* tilt, not intentional geometry.
