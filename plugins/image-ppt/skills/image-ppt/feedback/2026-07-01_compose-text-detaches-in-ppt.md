---
status: open
created: 2026-07-01
updated: 2026-07-01
occurrences: 1
context: figure-to-svg-replica
fixed_in: ""
regressed: ""
---
compose_svg.py emits every multi-line label as a single `<text>` with stacked `<tspan>` lines. When
the user imports the master SVG into PowerPoint (Insert → Picture → SVG → Convert to Shape), the
importer splits each such `<text>` into one text box PER LINE — so "Voice &" / "Robots" arrives as
two detached, separately-draggable boxes, and retyping a label means editing fragments. Shapes can
also come in slightly skewed. There is no SVG structure that reliably keeps a wrapped label as one
editable box through that importer.

Wishes (compose / export):
1. A single-line / one-`<text>`-per-label mode (emit `content` on one line, no dy-tspans) so each
   label imports as one box — overflow acceptable (see lesson/08).
2. A first-class **native-textbox PPTX exporter** (`compose_pptx.py`): render the graphics-only
   layer to a hi-res background image (compose with a `--no-text` flag), then place ONE editable
   PowerPoint text box per items.json `texts` entry (multi-line kept inside one box via paragraphs).
   This guarantees clean editable text without the importer mangling — an alternative to the svgBlip
   route in lesson/05.
3. At minimum, a `compose_svg.py --no-text` flag (graphics-only background layer) — the building
   block both the exporter and the single-line workflow need.

Fix:
