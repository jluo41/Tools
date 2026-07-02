# image-ppt

Replicate raster figures and icons as clean, **editable** SVGs — so a PNG figure destined for a paper
or slide deck becomes something whose wording, colors, and layout you can still change.

Two work skills (one built to call the other) plus a **knowledge layer** that remembers what the
craft taught us:

## `image-to-svg` — one icon → faithful hand-authored SVG
Decompose a single raster icon/graphic into back-to-front primitives with sampled colors, write
minimal SVG, render side-by-side against the source, self-score, refine, save. Replication, not
"grab a similar stock glyph." Every icon is **centered and self-contained**. Usable standalone.

- `scripts/render_compare.py` — renders an SVG beside its source crop at matched size (visual check).
- `scripts/score_icon.py` — **inner evaluation**: numeric `sim/shape/color/center` + PASS/REVISE, loop until pass.
- `scripts/center_svg.py` — normalize an SVG's viewBox tight to its content (centered, self-contained).
- Venv: `~/.cache/img2svg-venv` (`cairosvg Pillow numpy`; scipy optional, sharper de-noising).

## `figure-to-svg-replica` — whole figure → master SVG
Runs a 4-step pipeline — **analyze → crop → vectorize (per icon, via `image-to-svg`) → compose** —
and reassembles a single master `.svg` sized to the original: panel rects + each icon nested at its
bbox + real `<text>` labels. `items.json` is the source of truth for the whole run.

- `scripts/grid_overlay.py` — labeled coordinate grid for reading bounding boxes.
- `scripts/crop_bboxes.py` — cut each icon out of the source per `items.json`.
- `scripts/crop_qc.py` — **crop inner evaluation (code)**: geometric QC (clip/bleed/loose/off-center) + `--apply` auto-tighten & re-crop.
- `scripts/crop_judge_sheet.py` / `crop_judge_apply.py` — **crop inner evaluation (LLM-as-judge)**: build judge panels (crop + context), apply the semantic verdicts (grow clipped sides, mark `keep_raster`) as pixel-exact re-crops.
- `scripts/compose_svg.py` — assemble the master SVG (nest icon SVGs, draw `connectors`, embed `keep_raster` PNGs, emit text).
- `scripts/evaluate_icons.py` — **batch evaluation**: score every icon vs its crop, worst-first sheet + flags.
- `scripts/render_diff.py` — render the master and diff it side-by-side (`--overlay`) against the original.
- `references/sam_optional.md` — optional SAM-based pixel-tight cropping for busy figures.
- Venv: `~/.cache/fig2svg-venv` (`Pillow numpy cairosvg scipy`; `+ torch` only for SAM).

### Inner evaluation, by layer
- **Crop — code** (`crop_qc.py`): is the *input* clean geometrically? auto-fixes bboxes (pixel-exact).
- **Crop — LLM-as-judge** (`crop_judge_sheet.py` + `crop_judge_apply.py`): the *semantic* half — clipped? which side? neighbour contamination? unclear? The judge says *what/which side*, code makes it *exact*.
- **SVG — per-icon self-score** (`score_icon.py`, in image-to-svg): does each SVG match its crop & center? loop-until-pass.
- **Batch** (`evaluate_icons.py`): which finished icons are still weak, across the whole set.

Guiding split: **code measures pixels, the model measures meaning.** Use the LLM judge blanket or as
escalation for only the crops `crop_qc` flags.

## Fidelity principle
Verify every crop against its source; don't fake matches. Anything that can't reduce to clean
primitives (rendered digits like "120/80", photographic texture) stays a raster crop
(`"keep_raster": true`) and is embedded as-is — honesty about a weak match beats a confident wrong one.

## `image-ppt` — router + knowledge layer
A small entry skill (`skills/image-ppt/`) that routes to the two work skills and owns a shared,
growing knowledge layer so the craft's gotchas outlive any one session:

- **`lesson`** — hard-won vectorization gotchas, **consulted BEFORE drawing** (guardrails). Both
  work skills open by scanning `lesson/` and flagging any that apply.
  `/image-ppt lesson "<...>"` · `lesson list` · `lesson search <kw>`
- **`feedback`** — defects/wishes about the skills or scripts, routed to the right sub-skill/script
  and fixed in a later revision pass. `/image-ppt feedback "<...>"` · `feedback list`
- **`digest`** — bulk-harvest a whole session's transcript into routed lessons + feedback (confirm-
  gated, never auto-files). `/image-ppt digest ["<session>"] [--dry-run]`

Verb definitions live in `skills/image-ppt/fn/{lesson,feedback,digest}.md`; the filed knowledge
lives in `skills/image-ppt/lesson/` and `skills/image-ppt/feedback/`. Seeded lessons cover:
organic glyphs resist primitives → switch to stock/raster (01); keep logos/photos raster (02); the
icon scorer lies on white-on-dark (03); crop_qc over-flags inverted/tiny crops (04); reproduce the
distinctive silhouette detail (06); draw icons axis-aligned — a baked-in rotation reads as tilted
(07); a stylized network sphere is not a photo — vectorize it and lift its baked title into real
text (09); route hub-and-spoke connectors through a shared bus aligned to panel centers (10); a
crop's low resolution is not DPI loss — vectors are resolution-independent (11); cycle diagrams —
circles/curves + crop bleed (12); **regenerate icons instead of cropping a dense source** (13);
**regen grid 3×3 by default** (2×2 fallback, never 4×4) + central-component slice (14); transparentize
only border-connected white (15); SVG→PowerPoint needs one `<text>` per sentence — tspans collapse (16);
measure panel/banner/gradient colours from source (17); re-add badge circles / white-on-dark glyphs as
vector at compose (18).
