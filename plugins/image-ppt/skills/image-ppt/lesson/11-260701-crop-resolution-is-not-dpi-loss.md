# Lesson 11: "The crops look low-DPI" → they aren't; per-icon pixels are just few

## The Problem
Users see the `crop_images/<id>.png` files, blow one up, and ask "why did the crop lose DPI —
can we keep the original resolution?" It reads like the pipeline downsamples. It does not.

## The Solution
Explain the arithmetic and the pipeline, don't "fix" a non-bug:
- `crop_bboxes.py` does a plain `Image.crop(box)` — **1:1 pixels, no resample**. Each crop is
  exactly the pixels that icon occupies in the source.
- A crop looks soft only because one icon is ~100 px in a ~1600 px-wide figure. That is the icon's
  *native* resolution in the source; "keeping the original" adds no pixels that were never there.
- It mostly doesn't matter: every vector icon is **redrawn as SVG → resolution-independent**, sharp
  at any zoom. The crop is only a reference the vectorizer looks at, never the output.
- The ONLY place raster DPI survives into the output is `keep_raster` items (logos/photos/rendered
  digits). There the real lever is **the source figure's resolution**, not the crop step.

## Why It Works
Separates two different things the word "DPI" conflates: the crop step (lossless) vs. the source's
per-icon pixel budget (fixed). Vectorization sidesteps it entirely for glyphs.

## When to Apply
Whenever a user raises crop sharpness / DPI. Answer the concept, then act: if they care about the
`keep_raster` items specifically, ASK for a higher-res export (2x/3x PNG, or the original PPT/vector)
and re-crop the raster items from that — that is the only thing that actually makes them sharper.

## Caveats
Don't upscale a small crop to fake DPI — it just blurs. See [[02-260701-keep-logos-and-photos-raster]].
