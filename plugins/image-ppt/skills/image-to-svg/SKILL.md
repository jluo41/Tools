---
name: image-to-svg
description: >-
  Faithfully replicate a single raster icon/graphic image as a hand-authored SVG — reproducing
  the actual drawing, NOT swapping in a similar stock glyph. Use this whenever the user wants to
  "vectorize", "redraw as SVG", "replicate this icon as svg", "hand-write an svg of this", "make an
  editable/scalable version of this icon", or turn a cropped PNG/JPG of a logo, icon, or small
  graphic into clean vector code. Prefer this over grabbing a Font Awesome/Tabler/Material icon
  whenever fidelity to the original matters. Also used as the per-crop worker for the
  figure-to-svg-replica skill.
---

# image-to-svg

Turn one raster image of an icon or small graphic into an SVG that **looks like that specific
image**. The goal is replication, not "find a close-enough icon." A stock glyph is a different
drawing; here we reproduce the shapes, colors, and proportions actually present in the crop.

## Before you start — consult the lessons (mandatory)
This plugin keeps hard-won gotchas at `../image-ppt/lesson/` (`/image-ppt lesson list` /
`lesson search <keyword>`). Scan them before drawing. The load-bearing one: **organic/interlocking
glyphs** (handshakes, clasped hands, faces, gestures) have a LOW ceiling for primitive
hand-authoring — if the user rejects your drawing on look twice, STOP re-drawing and switch methods
(a recolored open-license stock glyph, or keep the crop as raster), or ask which they prefer
(Lesson 01). Judge white-on-dark icons by eye, not `score_icon` (Lesson 03). Capture new gotchas at
session end with `/image-ppt lesson "<...>"`.

## Why hand-author instead of auto-trace

Auto-tracers (potrace/vtracer) reproduce every pixel including blur and background artifacts, and
emit messy paths. A human-authored SVG built from primitives (`ellipse`, `rect`, `circle`, `line`,
`path`) is clean, tiny, editable, and recolorable — and for the flat/line/solid icons common in
figures it can match the original very closely. So we read the image, decompose it into a handful
of shapes, and write those shapes directly.

## Setup (one-time)

The verification script needs a Python env with `cairosvg`, `Pillow`, `numpy`:

```bash
python3 -m venv ~/.cache/img2svg-venv
~/.cache/img2svg-venv/bin/pip install cairosvg Pillow numpy
```

Use that interpreter to run `scripts/render_compare.py`. (Reuse it across runs; don't reinstall.)

## Workflow

### 1. Look, then decompose
Open the image and study it. Enlarge it if small (nearest-neighbor) so edges are visible. Write
down, explicitly:
- **Component shapes**, back to front (e.g. "grey rim ellipse → white top ellipse → navy button
  circle → light highlight → dark dash on the right").
- **Exact colors** — don't guess. Sample hex values from the pixels (open in Python and read a few
  representative pixels, or use the palette the parent figure already defined). Muddy guesses are
  the #1 cause of a bad replica.
- **Style**: flat solid fills, outline/stroke line-art, or pseudo-3D with shading. Match it — an
  outline original should become `fill="none" stroke="..."`, a solid original should become filled
  shapes.
- **Proportions**: the crop's width:height ratio sets the `viewBox`.

### 2. Write the SVG
Author it directly with primitives:
- **Make it make sense.** The aim is a *good, coherent drawing* of the object — the version a
  competent illustrator would produce — not a shape that merely overlaps the crop. Every element
  should correspond to a real part of the thing: a smartwatch has a hollow outlined face + a strap +
  a heart; a folder has a tab + a pocket + an actual "+"; a test tube has a body + a cap + liquid. If
  you can't say what a shape represents, it probably shouldn't be there, and if a required part is
  missing the icon is wrong even if it "reads" colorful. A viewer should recognize the object at a
  glance. This — not the score — is the bar.
- **Self-contained & centered.** Draw the icon centered in its `viewBox`, and size the `viewBox`
  tight to the icon's *own* content with small, roughly EQUAL margins on all sides. Do **not** copy
  the crop's framing: crops are often off-center or padded on one side, and reproducing that (drawing
  the glyph shoved into a corner of an oversized viewBox) is a bug. The crop tells you the *shape and
  colors*; the icon's placement in the larger figure is handled elsewhere (the composer's bbox). A
  good icon fills most of its viewBox and is visually centered.
- Set the `viewBox` to the icon's aspect ratio (e.g. a ~74×42 icon → `viewBox="0 0 200 120"`); pick
  round numbers so coordinates are easy to reason about.
- Draw **back to front** so later shapes sit on top (rim before top face, body before details).
- Reuse the sampled palette exactly. For multi-tone icons (e.g. a two-color brain), keep each color
  as its own shape/group.
- Keep it minimal — a good icon is usually 4–15 elements. Resist adding noise the eye won't miss.
- Comment each shape (`<!-- sensor button -->`) so it stays editable.

Prefer geometric primitives where they fit; fall back to `<path>` only for genuinely irregular
outlines (organic curves, silhouettes). For a `<path>`, sketch with a few cubic Béziers rather than
hundreds of trace points.

### 3. Verify against the original
Never ship unseen. Render and compare:

```bash
~/.cache/img2svg-venv/bin/python scripts/render_compare.py <your.svg> <source_crop.png> /tmp/cmp.png
```

Then view `/tmp/cmp.png` — it's the source and your render side by side at matched size. Check:
silhouette/aspect, color accuracy, placement of internal details, solid-vs-outline, overall "reads
as the same thing."

Then get a **numeric self-score** (the icon's inner evaluation) so you don't ship on a hunch:

```bash
~/.cache/img2svg-venv/bin/python scripts/score_icon.py <your.svg> <source_crop.png>
```

It trims both to content (robust to crop edge-bleed), then prints `sim / shape / color / center_off`
and a `PASS`/`REVISE` verdict (exit 0 = pass), so you can **loop until it passes**: `REVISE` with a
low `shape` means the silhouette/details are off, low `color` means a fill is wrong, high `center_off`
means re-center.

**But PASS is not proof.** The score is coverage + colour, so a shapeless mass of the right colour can
still pass — a watch that came out as a teal blob, or a "+" that collapsed into a notch, may read
`PASS`. So the visual compare in `/tmp/cmp.png` is the *real* gate: look at it and ask "does my render
read as the SAME OBJECT — right parts, right structure?" If not, fix it no matter what the number
says. The number tells you when you *might* be done; your eyes decide if you actually are.

### 4. Refine, then save
Iterate on the shapes until the comparison looks right (usually 1–3 passes). Save the final `.svg`
to the requested path (or `<name>.svg` next to the source). Report what you changed and any
intentional simplifications.

### 5. Normalize centering (self-contained check)
Even a well-drawn icon can end up off-center if you inherited the crop's framing. Re-frame the
`viewBox` tight to the drawn content with equal margins:

```bash
~/.cache/img2svg-venv/bin/python scripts/center_svg.py <your.svg> --inplace
```

It renders the SVG, finds the true content bounding box, and rewrites only the `viewBox`/size (shapes
untouched) so the icon is centered and self-contained. It prints the center-offset before/after;
aim for a near-zero offset. Do this as the last step so the saved asset drops cleanly into any layout.

## Fidelity bar
"As close as possible" means a viewer glancing at both sees the same object with the same colors and
layout — not a pixel-perfect trace. If an element genuinely can't be reduced to clean primitives
(fine photographic texture, tiny rendered text like "120/80"), say so and either approximate it or
recommend keeping the raster crop for that one. Honesty about a weak match beats a confident wrong
one.

## Example decomposition
**Input:** a small oval biosensor crop — white puck, navy button left-of-center with a light
highlight, a short dark dash on the right, subtle 3-D rim.
**Output shapes (back→front):** grey rim ellipse; white top ellipse with thin grey stroke; navy
button ellipse; light-blue highlight ellipse (rotated); rounded dark `rect` for the dash. ~6
elements, matches the crop.
