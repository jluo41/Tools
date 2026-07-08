---
name: figure-to-svg
description: >-
  Turn a whole figure/diagram/infographic PNG into an editable master SVG that recreates it —
  icons regenerated clean via codex image-gen and vectorized, plus real <text> labels at their
  original positions. Use this whenever the user says /figure-to-svg, wants to "replicate this
  figure as svg", "turn this figure/diagram into an editable svg", "regenerate this infographic
  as vector", "rebuild this graphic so I can edit it", or vectorize a multi-item figure (panels
  of icons + labels). Pipeline: split → regenerate icons → slice → transparentize → vectorize
  (via icon-to-svg) → compose → fresh-eyes review loop. Also home of the plugin's knowledge
  verbs — lesson (capture craft gotchas), feedback (file skill/script defects), digest (harvest
  a session) — use it for those too. Prefer this over one-shot tracing whenever the user wants
  an editable, clean, recolorable result.
---

# figure-to-svg

Rebuild a figure image as an **editable SVG**: every icon becomes clean vector art, every label
becomes real `<text>`, and everything is placed where it was in the original. The output is a
single master `.svg` that reads as a faithful copy of the source but can be edited, recolored,
and rescaled — and survives PowerPoint's **Insert SVG → Convert to Shape** as editable shapes
and text boxes.

## Invocation

```
/figure-to-svg <figure.png>          run the pipeline below on the whole figure
/figure-to-svg <figure.png> png      fast mode: skip vectorize, icons stay PNG (see Step 4)
/figure-to-svg <icon.png>            single icon/logo crop? hand it to /icon-to-svg instead
/figure-to-svg lesson "<...>"        capture a craft gotcha            -> fn/lesson.md
/figure-to-svg lesson list|search    browse / search the archive       -> fn/lesson.md
/figure-to-svg feedback "<...>"      file a skill/script defect        -> fn/feedback.md
/figure-to-svg digest ["<session>"]  harvest a session into knowledge  -> fn/digest.md
```

Bare image path, no verb: open it and route by what it is — a whole figure (panels, labels,
several icons) runs this pipeline; a single icon/logo crop goes to **icon-to-svg**. If genuinely
ambiguous, ask, showing which you'd pick.

The pipeline, one path:

```
split → regenerate → slice → transparentize → vectorize → compose → review (loop until pass)
```

The hard-won rules from past runs are **baked into the steps below** — you don't need to go read
a lessons folder before starting. `lesson/` (in this skill) is the capture inbox and archive:
when this run teaches you something new, file it (`/figure-to-svg lesson "<...>"` or
`/figure-to-svg digest`) and merge the rule into the step it belongs to.

## Setup (hard prerequisites — resolve BEFORE starting)

1. Python venv for the bundled scripts:
   ```bash
   python3 -m venv ~/.cache/fig2svg-venv
   ~/.cache/fig2svg-venv/bin/pip install Pillow numpy cairosvg scipy
   ```
   Reuse it across runs; don't reinstall.
2. Image generation: the regenerate step calls the **`codex` CLI** (native image-gen) through the
   codex-image2 bridge (`haipipe-toolkit` plugin as a sibling of this plugin, or point
   `CODEX_IMAGE2_SERVER` at its `server.py`). `gen_icon_grid.py` fails with a clear error if
   either is missing — fix the setup then; don't improvise a different method mid-run.

## Output layout

Everything lives under `<stem>_regenerated/` next to the source, one folder per part:

```
Figure1_regenerated/
├── subimages/part1/
│   ├── part.png            # section crop + gen reference
│   ├── manifest.json       # this part's inventory: panels, text, icons (grid cell ↔ id ↔ desc)
│   ├── redraw_icon/        # gen_icon_grid.py output grids
│   ├── cropped_icon/       # sliced + transparentized icons (PNG)
│   ├── svg/                # vectorized icons
│   ├── part1_replica.svg   # composed part (PPT-safe) + _wrapped (diff) + _raster (PNG icons)
│   └── part1_diff.png      # original | replica side-by-side
├── Figure1_replica.svg     # assembled master (+ _wrapped + _raster variants)
└── Figure1_replica_diff.png
```

## Step 1 — Split & analyze

Cut the figure into a few natural sections (panels, bands, columns); save each as `part.png`.
Per part, build the inventory that everything downstream reads — panels, text, icons:

```json
{
  "source": "part1.png",
  "width": 880, "height": 560,
  "palette": {"teal": "#007D81", "navy": "#1F2E5A"},
  "panels": [
    {"label": "banner", "bbox": [0,0,880,64],
     "gradient": {"from": "#0B5FA5", "to": "#1F2E5A", "direction": "horizontal"}}
  ],
  "items": [
    {"id":"01_wearables","type":"icon","bbox":[48,120,72,72],"desc":"smartwatch with heart","cell":[0,0]},
    {"id":"t01","type":"text","content":"Wearables + Sensors","content_ppt":["Wearables + Sensors"],
     "bbox":[140,132,220,26],"font_size":22,"weight":"bold","color":"#1F2E5A","anchor":"start"}
  ],
  "connectors": []
}
```

- `bbox` is `[x, y, w, h]` in part pixels; use `scripts/grid_overlay.py <part.png> grid.png`
  (and `--crop x0 y0 x1 y1` to zoom) to read coordinates — boxes read by naked eye are unreliable.
- **Measure, don't guess**: sample panel/banner/gradient colours from actual pixels. A guessed
  gray-blue panel where the original had white panels + navy banner + gradient headers is the
  classic failure. Panels take a flat `fill` or a measured `gradient` — the composer renders both.
- Capture icons and text **separately**; record every icon's `desc` (what it is) and target grid
  `cell` for the regenerate step.
- Straight/curved arrows and dashed flow lines are figure-level geometry, not icons — list them
  under `connectors` (see Step 5) instead of trying to redraw them per-icon.

## Step 2 — Regenerate the icons (codex image-gen)

**Reuse before regenerate.** Image-gen calls are the most expensive step, so first check whether
this exact figure was processed before: checksum the source (`md5 -q <source.png>`) and look for
prior `*_regenerated/` runs of the same figure (workspace folders, earlier versions — a renamed
file with the same checksum counts). If a prior run's sliced icons exist for an **identical**
source, reuse them and **tell the user explicitly** ("Step 2 skipped — reusing N icons from
<path>, source checksums match"). Silent reuse looks like a broken pipeline; reuse on a source
that actually changed produces stale icons. Any icon the prior run got wrong still goes through
fresh regeneration.

Otherwise, regenerate. Icons are NOT cropped out of the source — dense figures put text and
neighbours inside every crop. Instead, regenerate each part's icons as ONE clean regular grid,
with `part.png` as the style reference:

```bash
~/.cache/fig2svg-venv/bin/python scripts/gen_icon_grid.py <workspace> <part.png> part1_grid.png prompt.txt
```

`gen_icon_grid.py` is a thin driver: it **shells out to the `codex` CLI** (native image
generation) via the codex-image2 bridge — the Python only pins down cwd, reference image, output
path, and logging so every call is reproducible.

**Launch ALL grid calls in parallel** — one background call per grid, then collect. Each call
takes 1.5–4 minutes and they are fully independent (different parts, different output paths);
running seven of them serially wastes ~10 minutes for nothing. Write each part's prompt first,
fire every `gen_icon_grid.py` as a background process, and move on to slicing each grid as it
lands. The prompt matters:

- Grid **3×3 by DEFAULT** (≤9 icons per call); drop to **2×2** for sections heavy in
  human/photoreal figures (bigger cells resist bleed); **never 4×4** — it bleeds across cells.
- Ask for ~60% cell fill, large margins, **pure-white background**, matching the reference's
  style and colours, **no text labels** (keep only baked-in readings like "72" / "5.8" / "!").

## Step 3 — Slice & transparentize

```bash
~/.cache/fig2svg-venv/bin/python scripts/slice_grid.py   part1_grid.png cropped_icon_raw/ --grid 3x3
~/.cache/fig2svg-venv/bin/python scripts/transparentize.py cropped_icon_raw/ cropped_icon/
```

- `slice_grid.py` divides the grid equally and keeps each cell's **central connected component**,
  which drops any neighbour-bleed.
- `transparentize.py` removes only **border-connected** white, so interior whites (a white cross
  on a shield, highlights) survive. Icons are transparent by default so they drop onto any panel
  fill; keep the white-bg slices (`cropped_icon_raw/`) as fallback.

## Step 4 — Vectorize each icon (via icon-to-svg)

**PNG mode skips this step entirely.** If the user asked for the fast path (`png` after the
figure path, or "就用 PNG icon"), set `"keep_raster": true` on every icon item and go straight
to Step 5 — every compose variant then embeds the transparent PNG crops. The result is visually
faithful and the text/panels/arrows are still editable in PPT; only the icons stay pictures.
This trades roughly half the wall-clock time for icon editability — offer it when the user cares
more about speed than recolorable icons.

Otherwise, for every sliced icon, use the **icon-to-svg** skill to hand-author a faithful SVG →
`svg/<id>.svg`. The regenerated icons are the ideal input for it: pure-white background, no
neighbours, no text, generous resolution.

This step is what makes the final PPT editable: **Convert to Shape only converts vector shapes —
an embedded PNG stays a picture** whose colours can never be fixed in PPT.

- **Fan the icons out to parallel subagents — this is the default, not an option.** Hand-drawing
  37 icons serially is an hour by itself; it is the pipeline's dominant cost and the step where
  past runs died of exhausted context. Batch per part (one subagent per part, or per ~6 icons),
  give each subagent only its slice paths + `desc`s + palette, and let them run concurrently.
- icon-to-svg carries its own inner loop (side-by-side render + `score_icon.py` → PASS/REVISE);
  each subagent returns only on PASS — quality enforced at the leaf, so parallelism costs no
  fidelity.
- **Know when NOT to vectorize**: organic/interlocking glyphs (handshakes, faces, gestures) and
  photoreal figures have a low ceiling for primitive hand-authoring. Keep those as the
  transparent raster (`"keep_raster": true`) or swap a recolored open-license stock glyph — don't
  ship a confident wrong vector. If the user rejects a drawing twice, change the method, not the
  parameters.
- Every icon SVG must be **centered and self-contained**; normalize the folder once at the end:
  ```bash
  ~/.cache/fig2svg-venv/bin/python ../icon-to-svg/scripts/center_svg.py svg/ --inplace
  ```
- Optional batch check before composing: `scripts/evaluate_icons.py svg/ cropped_icon/ _icon_eval.png`
  scores every SVG vs its slice and writes a worst-first sheet. The number ranks; it never
  signs off — a shapeless blob of the right colour can PASS. Eyes decide.

## Step 5 — Compose

```bash
~/.cache/fig2svg-venv/bin/python scripts/compose_svg.py manifest.json svg/ part1_replica.svg --crops cropped_icon/
```

`compose_svg.py` sizes the canvas, paints panels (flat fill or measured `gradient`), draws
`connectors`, nests each icon SVG at its bbox, embeds `keep_raster` PNGs, and emits real `<text>`
per label. It writes **three variants in one run**: the main output is **PPT-safe** (one
absolutely-positioned `<text>` per line, or one per `content_ppt` sentence — PPT collapses
`<tspan>` line breaks); `*_wrapped.svg` (tspans) for the visual diff; and `*_raster.svg`,
which embeds EVERY icon as its transparent PNG crop while text/panels/connectors stay vector —
maximum icon fidelity for users who prefer the generated look over hand-drawn vectors (icons
stay pictures in PPT; white-on-dark icons may need `keep_raster` judgement as usual). Ship the
main one and the raster one as the two deliverables; diff the wrapped one.

- **Re-add stripped context as vector at compose**: badge circles, white-on-dark footer glyphs —
  anything the regeneration deliberately left out — comes back here as cheap vector shapes.
- Connectors are `arrow` primitives in source coordinates
  (`{"x1","y1","x2","y2","color","width","dashed","heads","curve"}`) — drawn on the master
  canvas beneath icons and text, so every arrow tweak is a JSON edit.
- Assemble the master from the parts, sized to the original figure.
- **Deliverable = the editable master SVG.** PowerPoint ONLY via Insert SVG → right-click →
  Convert to Shape. **NEVER generate PPT with python/python-pptx** — that output was rejected
  outright ("rubbish, cannot be opened").

## Step 6 — Fresh-eyes review, then reopen (mandatory)

Render the diff for every part and the master:

```bash
~/.cache/fig2svg-venv/bin/python scripts/render_diff.py part1_replica_wrapped.svg part.png part1_diff.png
```

Then dispatch a **FRESH subagent** — one with no context from this run — to judge each diff.
This must not be you: after hours on the replica you see what you *meant*, not what's on the
canvas; ownership bias is exactly what this gate exists to remove. Judge prompt:

> *"Read `part1_diff.png` (left = original figure, right = SVG replica). List every visible
> discrepancy: layout drift, wrong/missing colours or gradients, icons that don't read as the
> same object, text that is mis-placed / mis-sized / wrong, missing elements (badges, arrows,
> bands). Return JSON `{"verdict":"pass"|"revise","issues":[{"region","what","severity","fix_hint"}]}`.
> Ignore any similarity scores; judge only with your eyes."*

Route each issue back to its step and **reopen**:

- icon doesn't read right → Step 4, re-vectorize that icon (or `keep_raster`)
- layout / colour / text wrong → edit `manifest.json`, recompose (Step 5)
- missing badge/glyph/arrow → add it as vector at compose (Step 5)
- a whole section came out wrong → regenerate that part's grid (Step 2)

Recompose, re-diff, **re-judge with a fresh subagent** — loop until the verdict is `pass`, or the
only remaining issues are deviations the user has explicitly accepted (record those in the final
report). Never sign off on your own render, and never on a score alone.

## Guidance

- **`manifest.json` is the source of truth** per part. Every step reads/writes it; most
  refinement is a JSON edit + re-running one script. The run is resumable at any step.
- **Fonts** won't match exactly; approximate family/size/weight, prioritize position and colour,
  and note the substitution if the exact font matters.
- **Don't fake fidelity.** A region too complex to redraw stays raster (`keep_raster`) — say
  which items you kept as raster. Honesty about a weak match beats a confident wrong one.

---
*A retired crop-from-source pipeline (bbox cropping + geometric/LLM crop QC) is archived in
`references/legacy-crop-path.md` — kept for provenance only; it is not part of the workflow.*
