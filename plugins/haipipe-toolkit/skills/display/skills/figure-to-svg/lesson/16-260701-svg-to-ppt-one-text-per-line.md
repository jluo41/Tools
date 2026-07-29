# Lesson 16: SVG → PowerPoint — one `<text>` per line (tspan line-breaks collapse)

## The Problem
An SVG with multi-line text (one `<text>` holding `<tspan>` line children) imported into
PowerPoint via **Insert SVG → right-click → Convert to Shape** comes in with **every line stacked
at the same y** — overlapping, unreadable garble. Single-line `<text>` (banner, column headers)
converts perfectly.

## The Symptom
Headers crisp; every wrapped question/subheader collapsed into overlapping text (confirmed by the
selection handles on one box).

## The Solution
For the PPT-targeted SVG, emit **one absolutely-positioned `<text>` per line** — ideally **one per
SENTENCE on a single line** (let it overflow the column; re-wrap by dragging the box in PowerPoint).
Do NOT use `<tspan dy>` for line breaks. One `<text>` per sentence = one editable text box per
sentence = the fewest, most manageable boxes.

## Why It Works
PowerPoint's SVG→shape converter maps each `<text>` to one text box but **ignores `<tspan>` dy
offsets**, so all tspans land at the parent's y. Separate `<text>` elements each carry their own
absolute position.

## When to Apply
Whenever the deliverable is an SVG converted to editable PowerPoint via Convert to Shape.

## Caveats
One-line-per-sentence overflows the column in the raw SVG render — fine for PPT (you re-wrap there)
but not a faithful auto-render. Keep **two variants from one config**: a wrapped one (for visual
diffs) and a one-line one (for PPT). Don't rely on SVG filters either — PPT may not honour them.
