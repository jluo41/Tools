---
name: html-to-svg
description: Convert an html-ppt deck (or any slide outline) into one standalone 1280x720 SVG per slide, ready to drop into PowerPoint as vector graphics. Style contract - white background, Times New Roman, body text as bullets with ONE SENTENCE PER LINE, no emoji in text (rasterizer-safe). Use when the user says "generate SVG slides", "svg for each slide", "convert deck to svg", "slides I can import into PowerPoint", or wants per-slide vector files from an html-ppt deck.
---

# /html-to-svg — per-slide SVG generator

Turn a deck (an `html-ppt` deck, a markdown slide draft, or an outline) into
**one self-contained SVG file per slide**, sized for direct PowerPoint import.
The user then does `Insert → Pictures` per slide — vector stays vector.

## Style contract (non-negotiable defaults)

| Rule | Value | Why |
|---|---|---|
| Canvas | `1280 × 720` viewBox | = PowerPoint 13.33″ × 7.5″ @ 96 dpi, imports 1:1 |
| Background | pure white `#ffffff` | matches PPT canvas, no page-tint seams |
| Font | `'Times New Roman', Times, serif` — everything | user standard for formal decks |
| Body text | **bullets, ONE SENTENCE PER LINE** via `bullets()` | scannable; each sentence its own `•` line, wrapped lines hang-indent |
| Emoji | **never in `<text>`** | rasterizers without an emoji font draw tofu; use color, `todo()` pills, or vector shapes instead |
| Placeholders | dashed amber `todo()` pill | unfilled content is visible, not presentable-by-accident |
| Safe glyphs | `• → ← ▶ · ± ≥ ∨ — –` | in Times/DejaVu everywhere |

Palette: ink `#1c1c1c` · sub `#3f3f46` · muted `#8a8a8a` · accent `#1f5aa8`
· warn `#b45309` · good `#15803d` · border `#d4d4d0` · surface2 `#f2f2f0`.

## Workflow

1. **One generator script per deck**, named `generate_svgs.py`, living in the
   deck's `svg/` folder. Copy `scripts/svg_deck.py` (this skill) next to it —
   decks stay self-contained — and build each slide as a function returning
   `Svg.render(title)`. Number files `NN-slug.svg` in deck order.
2. **Content**: mirror the source deck slide-for-slide. Prose paragraphs must
   be split into sentences and rendered with `bullets()` — never as wrapped
   paragraph blocks. Tables render as row/cell `<text>` grids (see the
   reference implementation's Table 1); charts as `minibar()` rows; flows as
   boxes + `→` text arrows.
3. **Verify visually, always**: rasterize a few layout-heavy slides and LOOK
   at them before declaring done —
   ```bash
   pip install cairosvg   # once
   python3 -c "import cairosvg; cairosvg.svg2png(url='06-table1.svg', write_to='/tmp/x.png', output_width=1280)"
   ```
   cairosvg has no emoji font — tofu boxes in the preview mean the emoji rule
   was violated. Fix the text, don't ignore the preview.
4. **Regenerate** any time numbers change: `python3 generate_svgs.py`.

## Two variants: display vs PPT-editable (figure-to-svg Lesson 16)

PowerPoint's **Convert to Shape ignores `<tspan dy>`** (lines collapse onto
one y) and gives every absolutely-positioned `<text>` its own text box — so
wrapped bullets become stacks of per-line boxes that collide when edited.
Per `figure-to-svg` Lesson 16, keep TWO variants from the one generator:

| Variant | bullets() behavior | Use for |
|---|---|---|
| **display** (default) | sentence wraps, one `<text>` per line, absolute y each — never tspans | presenting as-is, PNG export, visual diffs |
| **PPT-editable** (`--ppt` → `ppt-editable/`) | NO wrap: one single-line `<text>` per sentence, overflowing its column | Convert to Shape → one box per sentence → re-wrap by dragging in PowerPoint |

The one-line variant looks overflowed when rendered raw — that is expected;
its consumer is the human re-wrapping boxes in PowerPoint, not a viewer.

## Assembling a .pptx (`scripts/build_pptx.py`)

Copy `scripts/build_pptx.py` next to the deck's SVGs and run it — it builds a
16:9 `.pptx` with **true vector SVG embedding**: each slide gets the PNG
fallback inserted full-bleed, then the picture's `<a:blip>` is patched with
the `svgBlip` extension pointing at the SVG added as a package part
(the same dual-image structure PowerPoint writes when you Insert an SVG).
PowerPoint 2019/365 renders crisp vector; older versions use the PNG.
Fill the `NOTES` dict to write speaker notes into each slide's notes pane.
Requires `pip install python-pptx cairosvg`. Full loop after edits:
`python3 generate_svgs.py && python3 build_pptx.py`.

## Library (`scripts/svg_deck.py`)

- `Svg` — element buffer: `.rect .line .circle .text .bullets .render`
- `bullets(x, y, items, max_px, …)` — the one-sentence-per-line renderer;
  items are `str` or `(text, color[, weight])`; returns next free y
- `header(s, kicker, title, n, total, footer)` — standard slide chrome
- `card(s, x, y, w, h, title, items, accent=…)` — bordered card w/ bullet body
- `todo(s, x, y, label)` — dashed amber placeholder pill (chainable)
- `minibar(s, x, y, w, label, frac, value)` — horizontal bar-chart row
- `wrap(s, max_px, fs)` — greedy wrapper (~0.48·fs px/char for Times)
- `write_deck(slides, out_dir)` — `[(name, fn), …]` → `NN-slug.svg` files

## Reference implementation

`collaborations/Event-JHU-ADHD-NIH-Team/po-update-deck/svg/generate_svgs.py`
(REACH-SPACE) — 12 slides covering every pattern: stat cards, funnel with
leak-outs, timeline lanes, CONSORT flow + stacked bar, event timeline with
sliding windows, a full Table 1, quadrant cards, bar-panel pairs, pipeline
flow, card grids, roadmap lanes, two-column references.

## PowerPoint import notes (tell the user)

- `Insert → Pictures → This Device` → pick the SVG; it stays vector.
  `Graphics Format → Convert to Shape` makes text/shapes natively editable.
- 1280×720 fills a 16:9 slide exactly; set slide size to 16:9 first.
- Batch: insert all NN-*.svg at once; PowerPoint places one per selection —
  or use one blank slide per SVG and paste in order.
