---
name: figure-to-svg-replica
description: >-
  Turn a whole figure/diagram/infographic PNG into an editable master SVG that recreates it —
  icons redrawn as vectors plus real <text> labels, laid out at their original positions. Use this
  whenever the user wants to "replicate this figure as svg", "turn this figure/diagram into an
  editable svg", "regenerate this infographic as vector", "rebuild this graphic so I can edit it",
  or vectorize a multi-item figure (panels of icons + labels). Runs a 4-step pipeline
  (analyze → crop → vectorize each crop → compose) and calls the image-to-svg skill for each icon.
  Prefer this over one-shot tracing whenever the user wants an editable, clean, recolorable result.
---

# figure-to-svg-replica

Rebuild a figure image as an **editable SVG**: every icon becomes clean vector art, every label
becomes real `<text>`, and everything is placed where it was in the original. The output is a single
master `.svg` that reads as a faithful copy of the source but can be edited, recolored, and rescaled.

## Before you start — consult the lessons (mandatory)
This plugin keeps a knowledge layer of hard-won gotchas at `../image-ppt/lesson/`. BEFORE analyzing
a figure, scan it (`/image-ppt lesson list`, or `lesson search <keyword>`) and flag any that apply —
e.g. organic/interlocking glyphs → offer a stock/raster route early (Lesson 01); logos/photos →
`keep_raster` from the first pass (Lesson 02); white-on-dark bands → don't trust `score_icon`/
`crop_qc` (Lessons 03–04). When the
session ends, capture new gotchas with `/image-ppt lesson "<...>"` or `/image-ppt digest`.

## Choosing the icon path: REGENERATE (default for dense figures) vs. crop-from-source
Two ways to get each icon. The classic path (Steps 1–3 below) **crops** icons out of the source by
bbox. On **dense multi-icon figures** (icons among text, on coloured panels, touching neighbours)
that path performs badly — crops land on title text or a neighbour and can't be tightened
(lesson/13). Prefer **regeneration**:

1. **Split** the figure into per-part sections; save each clean crop as `part.png` (also the gen reference).
2. **Regenerate** each part's icons as ONE regular grid with `scripts/gen_icon_grid.py` (Codex native
   image-gen; `part.png` is the reference). Grid size: **3×3 by DEFAULT** (≤9 icons); drop to **2×2**
   for sections dense in human/photoreal figures (bigger cells = bleed-proof); **never 4×4** (it bleeds
   — lesson/14). Prompt for ~60% cell fill, large margins, pure-white background, no text (keep only
   baked readings like "72"/"5.8"/"!").
3. **Slice** with `scripts/slice_grid.py` (equal division + central-connected-component keep → drops
   neighbour-bleed; lesson/14).
4. **Transparentize** with `scripts/transparentize.py` (removes only border-connected white; interior
   whites survive — lesson/15).
5. **Compose** each part (embed transparent icons as `<image>`; re-add badge circles / white-on-dark
   glyphs as vector — lesson/18; sample panel/banner/gradient colours from source — lesson/17), then
   assemble the master.

Per-part tree:
```
subimages/partN/
├── part.png          # section crop + gen reference
├── manifest.json     # icons -> grid/cell/desc + text
├── redraw_icon/      # gen_icon_grid.py output grids
├── cropped_icon/     # sliced + transparent icons
└── partN_replica.svg
```
**For SVG→PowerPoint** (Insert SVG → right-click → Convert to Shape): emit **one `<text>` per sentence**
on a single line — PPT collapses `<tspan>` line breaks (lesson/16). Requires the codex-image2 bridge
(haipipe-toolkit) + `codex` CLI on PATH.

### Deliverable, PPT & QC rules (user preferences — treat as hard constraints)
- **Icons are transparent by default** (the transparentize step) so they drop onto any panel with no
  white box. Keep the white-bg slice too (`cropped_icon_raw/`) as a fallback.
- **Deliverable = editable master SVG.** Convert to PowerPoint ONLY via **Insert SVG → right-click →
  Convert to Shape**. **NEVER generate PPT with python / python-pptx** — that output was rejected
  outright ("rubbish, cannot be opened"). No `build_pptx`, no `svgBlip`-from-python.
- **Two SVG variants from ONE config:** `<part>_replica.svg` = **one `<text>` per sentence** (single
  line, overflow OK, re-wrap in PPT) for the PowerPoint path (lesson/16); plus a **wrapped** variant
  for the faithful visual diff. Generate both from the same layout data — don't hand-maintain two files.
- **Always produce the combined `<stem>_replica_diff.png`** (original | replica, `render_diff.py`) and
  eyeball it per section — never sign off on the render alone (matches the mandatory eval rule below).
- **Compose faithfully:** measure panel/banner/gradient colours from the source (lesson/17); embed
  transparent icons as `<image>`; re-add badge circles and white-on-dark glyphs as vector (lesson/18);
  match the original's banner, header alignment, panel fills, and layout.

## Why the pipeline is staged
A figure is many small drawings plus text plus layout. Doing it in one pass fails — you lose either
fidelity or editability. So we separate concerns: **find** the items, **crop** them, **redraw** each
one faithfully (delegated to `image-to-svg`), then **reassemble** with correct positions and text.
Each stage is checkable on its own, which is what keeps the final composite honest.

## Evaluate with eyes, not just numbers (mandatory)
Every visual artifact this pipeline produces — `_crop_sheet.png` (crops), `_icon_eval.png` (icon vs
crop), and `<stem>_replica_diff.png` (figure vs original) — **must be looked at, and re-evaluated by
an LLM**, not signed off on a score. The numeric metrics (`crop_qc`, `score_icon`, `evaluate_icons`)
are coverage/geometry heuristics: they catch gross problems and rank work, but a shapeless blob of
the right colour can score `PASS`. Structural/semantic correctness — "does this read as a *smartwatch*,
is that a proper medical *plus*" — is something only eyes catch. So at each sheet: **open it, look at
every pair, and dispatch an LLM-as-judge to flag what's wrong regardless of the number.** Treat a
green score as "maybe done", never "done".

## Setup
Most steps need Python with `Pillow`, `numpy`, `cairosvg`, `scipy` (SAM mode also needs `torch`):
```bash
python3 -m venv ~/.cache/fig2svg-venv
~/.cache/fig2svg-venv/bin/pip install Pillow numpy cairosvg scipy
```
Run the bundled `scripts/*.py` with that interpreter. Reuse it; don't reinstall each time.

## Output layout
For a source `.../Step2.png`, write everything under `<stem>_regenerated/` next to it:
```
Step2_regenerated/
├── items.json            # the inventory (bboxes, colors, text, connectors) — the source of truth
├── grid.png              # gridded source used to read coordinates
├── crop_images/          # <id>.png  per icon
├── svg/                  # <id>.svg  per icon (centered, self-contained)
├── _icon_eval.png        # Step 3.5 icon-vs-crop evaluation sheet (+ .json scores)
├── Step2_replica.svg     # the composed master SVG
└── Step2_replica_diff.png# side-by-side vs original
```
Naming convention for items: zero-padded index + region + label, e.g.
`01_data_foundation_wearables_sensors`, `26_footer_governance_shield`. Match any convention the
project already uses (check for an existing `crop_images` folder first).

---

## Step 1 — Analyze
Understand the figure and inventory every item. Bounding boxes read by eye are unreliable, so use a
coordinate grid:

```bash
~/.cache/fig2svg-venv/bin/python scripts/grid_overlay.py <source.png> <stem>_regenerated/grid.png
```
View `grid.png` (and zoom into sub-regions with the same script's `--crop x0 y0 x1 y1` option for
tight boxes). Then produce `items.json` — the spine of the whole run:

```json
{
  "source": "Step2.png",
  "width": 1774, "height": 887,
  "palette": {"teal": "#007D81", "navy": "#1F2E5A", "blue": "#0B5FA5"},
  "panels": [
    {"label": "A. Multimodal Data Foundation", "bbox": [60,120,380,560], "fill": "#ffffff", "stroke": "#dfe3e8"}
  ],
  "items": [
    {"id":"01_data_foundation_wearables_sensors","type":"icon","region":"data_foundation",
     "bbox":[88,200,60,95],"colors":["#1F2E5A"]},
    {"id":"t01_wearables_label","type":"text","content":"Wearables + Sensors",
     "bbox":[160,205,190,24],"font_size":22,"weight":"bold","color":"#1F2E5A","anchor":"start"}
  ]
}
```
`bbox` is `[x, y, w, h]` in original pixels. Capture **icons and text separately**. Sample real hex
colors (read pixels), don't guess. Tag each with a `region`/panel so the naming and layout stay
organized. Also record panel/background rectangles — they carry most of the "layout feel."

Default cropping is these model-read boxes. For pixel-tight, background-free crops on busy figures,
see `references/sam_optional.md` (heavier: needs torch + a 375 MB model).

## Step 2 — Crop
Cut each icon out of the source using the boxes in `items.json`:
```bash
~/.cache/fig2svg-venv/bin/python scripts/crop_bboxes.py <source.png> <stem>_regenerated/items.json \
    <stem>_regenerated/crop_images
```
This writes `crop_images/<id>.png` for every `type:"icon"`. Then build the contact sheet and
**look at it** — this review is mandatory, not optional:
```bash
~/.cache/fig2svg-venv/bin/python scripts/contact_sheet.py <stem>_regenerated/crop_images \
    <stem>_regenerated/_crop_sheet.png
```
**You MUST eyeball `_crop_sheet.png` AND have an LLM re-evaluate it** (same as you'd visually compare
the finished figure to the original — never sign off on numbers alone). Dispatch an LLM judge over
the sheet:

> *"Read `_crop_sheet.png` (a labeled grid of icon crops). For each crop, is it a clean, complete
> crop of a single icon — not clipped, not showing a neighbour's icon/text/line, not empty? Return
> JSON `{"bad":[{"id","why"}...]}`."*

For anything flagged, fix that item's `bbox` in `items.json` and re-crop (or use Step 2.5/2.6). Good
crops now save a lot of rework later.

## Step 2.5 — Crop QC (inner evaluation of the crops)
Imperfect crops are the #1 upstream cause of a bad replica, so evaluate them before vectorizing.
Split the check by what each judge is good at:

- **Geometry → code** (`crop_qc.py`): does ink run off an edge? is there a detached speck (a
  neighbor's panel line bled in)? too much dead padding? off-center? These are pixel-exact and free,
  and — crucially — code can compute the corrected bbox to the pixel and re-crop:
  ```bash
  ~/.cache/fig2svg-venv/bin/python scripts/crop_qc.py <source.png> <stem>_regenerated/items.json \
      <stem>_regenerated/crop_images --apply
  ```
  `--apply` rewrites each `bbox` to the icon's true content box (drops specks that don't belong to
  the icon, reclaims clipped parts just outside, strips padding), backs up `items.json.bak`, and
  re-crops. Think of it as `center_svg` for crops: a deterministic normalizer. Run without `--apply`
  first to just see the report.
- **Semantics → the model** (no extra call needed): "is the *whole intended* icon here, and nothing
  from a neighbor?" needs to know what the icon *is* — a judgement, not geometry. Don't spend an LLM
  call per crop to grade this: the Step-3 vectorizing agent **already opens the crop first** and will
  flag a clipped/contaminated one, which sends you back to fix that `bbox` and re-crop. Use the model
  where it's strong (meaning) and code where it's strong (pixels); don't pay tokens to measure what a
  numpy check states exactly.

## Step 2.6 — Crop judge (LLM-as-judge, semantic)
`crop_qc` (Step 2.5) measures *geometry*; it can't tell "the icon fills its box" from "the icon is
clipped", or spot a neighbour's stray mark. Those are semantic calls — so hand them to the model.
This stage is the LLM half of the crop inner-evaluation. Use it **as escalation** (judge only the
crops `crop_qc` flagged) or **blanket** (all crops) if you want maximum robustness.

1. Build the judge inputs (isolated crop + source context with the box drawn):
   ```bash
   ~/.cache/fig2svg-venv/bin/python scripts/crop_judge_sheet.py <source.png> \
       <stem>_regenerated/items.json <stem>_regenerated/_judge   # add --only id,id for escalation
   ```
2. Dispatch judge subagent(s) — one per crop for hard cases, or a batch reading several panel PNGs.
   Each **reads the panel image** and returns a verdict. Judge only what needs meaning:
   ```json
   {"id": "<id>", "usable": true, "clipped_sides": ["bottom"], "contaminated": false,
    "unclear": false, "note": "clock cut off at the bottom edge"}
   ```
   - `clipped_sides`: any of `top|bottom|left|right` where the icon is cut by the box (the LLM is
     good at *which side*; it does **not** need to give pixel coordinates — code handles that).
   - `contaminated`: a neighbour's icon/text/line intrudes into the box.
   - `unclear`: the source itself is too blurry/garbled to reduce to clean primitives.
   Collect the verdicts into `<stem>_regenerated/_judge/verdicts.json` as `{"verdicts": [ ... ]}`.
3. Apply — the model said *what*, code makes it *exact*:
   ```bash
   ~/.cache/fig2svg-venv/bin/python scripts/crop_judge_apply.py <source.png> \
       <stem>_regenerated/items.json <stem>_regenerated/crop_images <stem>_regenerated/_judge/verdicts.json
   ~/.cache/fig2svg-venv/bin/python scripts/crop_qc.py <source.png> \
       <stem>_regenerated/items.json <stem>_regenerated/crop_images --apply   # snap tight
   ```
   Clipped sides get grown then snapped tight to the revealed content; `unclear` crops are marked
   `keep_raster`; contamination is cleaned by `crop_qc`'s component filter. This is the division in
   practice: **the LLM judges meaning and direction, code computes the pixel-exact crop.**

## Step 3 — Vectorize each crop
For **every** crop, use the **image-to-svg** skill to hand-author a faithful SVG. That skill carries
its own **inner evaluation**: it renders a side-by-side *and* self-scores with `score_icon.py`
(`sim / shape / color / center_off` → `PASS`/`REVISE`), looping until the icon passes and is
centered. Save results to `svg/<id>.svg` (same base name as the crop). This is also the **semantic
crop check**: if, on opening a crop, it's clearly clipped or has a neighbor's marks in it, stop and
fix that item's `bbox` in `items.json` + re-crop (Step 2/2.5) rather than faithfully redrawing a bad
crop. A crop that truly can't reduce to clean primitives (rendered digits, photographic texture) may
stay raster — set `"keep_raster": true` and the composer embeds the PNG instead.

When farming this out to subagents (one per icon or small batch), have each run `score_icon.py` and
only return once it reports `PASS` — so quality is enforced at the leaf, not just at the end.

Standard, unambiguous glyphs (a plain database, calendar, shield) can be drawn quickly; spend the
effort on the distinctive ones where a generic icon would be wrong.

**Every icon SVG must be centered and self-contained** — its `viewBox` tight to its own content with
equal margins, not a copy of the crop's off-center framing. After authoring, normalize the whole
folder in one shot:
```bash
~/.cache/fig2svg-venv/bin/python <image-to-svg>/scripts/center_svg.py <stem>_regenerated/svg --inplace
```
(this rewrites only each `viewBox`, leaving shapes alone, so every icon sits centered in its canvas).

## Step 3.5 — Evaluate the icons (numbers AND eyes)
Before composing, score every SVG against its crop:
```bash
~/.cache/fig2svg-venv/bin/python scripts/evaluate_icons.py <stem>_regenerated/svg \
    <stem>_regenerated/crop_images <stem>_regenerated/_icon_eval.png
```
Both images are trimmed to content first, so the score reflects **shape + color**, not framing. It
writes a **worst-first contact sheet** (`_icon_eval.png`: crop | your svg) + `.json`, and prints
per-icon `sim / shape / color / center_off` with a FLAGGED list.

**The number is necessary but NOT sufficient — you MUST eyeball the sheet.** The metric is coverage +
colour, so a shapeless blob of the right colour scores high: a broken smartwatch that renders as a
teal blob, or a folder whose "+" collapsed into a notch, can still read `sim≈0.82 PASS`. Structure is
something only eyes catch. So **open `_icon_eval.png` and look at every pair**, or dispatch an
**SVG-judge** subagent to do it:

> Judge subagent prompt: *"Read `_icon_eval.png` (rows: left=source crop, right=my SVG). For each
> row, does the right image read as the SAME OBJECT as the left — correct parts, structure, style?
> Return JSON `{"bad": [{"id","why"}...]}` for any that don't, ignoring the sim numbers."*

Regenerate every icon that fails the *visual* check (back to `image-to-svg`) even if its `sim`
passed, then re-evaluate. Don't proceed on the number alone.

## Step 4 — Compose
Assemble the master SVG from `items.json` + the per-item SVGs, then diff against the original:
```bash
~/.cache/fig2svg-venv/bin/python scripts/compose_svg.py <stem>_regenerated/items.json \
    <stem>_regenerated/svg <stem>_regenerated/<stem>_replica.svg
~/.cache/fig2svg-venv/bin/python scripts/render_diff.py <stem>_regenerated/<stem>_replica.svg \
    <source.png> <stem>_regenerated/<stem>_replica_diff.png
```
`compose_svg.py` sizes the canvas to the original, paints panel/background rects, draws any
`connectors`, nests each icon SVG into its `bbox`, embeds any `keep_raster` PNGs, and emits `<text>`
for every label with the recorded font size/weight/color/anchor. View the diff and refine: nudge
`bbox`es, fix font sizes and colors, adjust panel fills — small placement fixes in `items.json` +
recompose. Iterate until the replica reads as the same figure.

**Connectors (arrows / dashed lines).** Straight arrows and dashed bias/flow lines between panels
are pure figure-level geometry — don't crop and vectorize them as icons. Instead list them under a
top-level `connectors` array and let the composer draw them directly on the master canvas (in source
coordinates, beneath the icons and text). Each is an `arrow` primitive:
```json
"connectors": [
  {"id": "X01_arrow_a_m1", "type": "arrow", "x1": 350, "y1": 380, "x2": 376, "y2": 380,
   "color": "#007D81", "width": 11, "heads": "end", "head_size": 20, "head_width": 30},
  {"id": "X05_dash_a", "type": "arrow", "x1": 191, "y1": 692, "x2": 191, "y2": 774,
   "color": "#007D81", "width": 3, "dashed": true, "heads": "both", "head_size": 12}
]
```
Fields: `x1,y1,x2,y2` (endpoints), `color`, `width`, `dashed`(+`dash` pattern), `heads`
(`"end"`|`"both"`|`"none"`), `head_size`, `head_width`. Works at any angle. This is faster and
cleaner than nesting a tiny SVG per arrow, and keeps every arrow tweak in `items.json`.

## Guidance
- **`items.json` is the source of truth.** Every step reads/writes it; keep it accurate and it keeps
  the run coherent. Most refinement is editing this file and re-running one script.
- **Fonts** won't match exactly; approximate family/size/weight and prioritize position and color.
  If the exact font matters, ask the user or pick a close web-safe/Google font and note it.
- **Don't fake fidelity.** If a region is too complex to redraw, keep its raster crop rather than
  ship a wrong vector — and say which items you kept as raster.
- The whole thing is resumable: because state lives in `items.json` and the crop/svg folders, you
  can stop after any step and pick up later.
