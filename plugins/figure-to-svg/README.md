# figure-to-svg

Replicate raster figures and icons as clean, **editable** SVGs — so a PNG figure destined for a paper
or slide deck becomes something whose wording, colors, and layout you can still change, and that
survives PowerPoint's **Insert SVG → Convert to Shape** as editable shapes and text boxes.

Two skills — the figure pipeline calls the icon painter only in `svg` mode:

```
figure-to-svg      whole figure → master SVG (entry point + knowledge verbs)
  └── icon-to-svg  one icon image → faithful hand-authored SVG (svg mode only)
```

## `figure-to-svg` — whole figure → master SVG

One pipeline: **split → regenerate (codex image-gen) → slice → transparentize → [vectorize if
svg mode] → compose → fresh-eyes review loop**. Icons are never cropped out of a dense source —
they're regenerated as clean grids with the section as style reference, sliced, and made
transparent. By default icons embed as transparent PNGs (fast, visually faithful — text/panels/
connectors are still editable vector); pass `svg` to hand-vectorize each icon via `icon-to-svg`
for full editability. A fresh subagent (no run context) judges every original|replica diff and
reopens steps until it passes. The result is a single master `.svg` sized to the original:
panels (fills/gradients measured from source) + each icon nested at its bbox + real `<text>`
labels. Per-part `manifest.json` is the source of truth. Requires the codex-image2 bridge
(sibling `haipipe-toolkit` plugin) + `codex` CLI — a hard prerequisite, resolved before starting.

- `scripts/gen_icon_grid.py` / `slice_grid.py` / `transparentize.py` — the regeneration trio:
  codex image-gen grid → slice (central connected component) → border-connected-white transparency.
- `scripts/grid_overlay.py` — labeled coordinate grid for reading layout bounding boxes.
- `scripts/compose_svg.py` — assemble the master SVG (nest icon SVGs, draw `connectors`, embed `keep_raster` PNGs, gradient panels); writes a **PPT-safe** main output (one `<text>` per line/sentence) + a `_wrapped` variant for the visual diff.
- `scripts/evaluate_icons.py` — **batch evaluation**: score every icon SVG vs its slice, worst-first sheet + flags.
- `scripts/render_diff.py` — render the replica and diff it side-by-side (`--overlay`) against the original.
- `references/legacy-crop-path.md` — the retired crop-from-source pipeline (+ its scripts), archived for provenance.
- Venv: `~/.cache/fig2svg-venv` (`Pillow numpy cairosvg scipy`).

### Knowledge verbs (live in this skill)

- **`lesson`** — capture hard-won vectorization gotchas. Load-bearing lessons get **merged into
  the skills' steps** (the baked-in rules there came from this folder); the folder itself is
  inbox + archive, not a runtime read.
  `/figure-to-svg lesson "<...>"` · `lesson list` · `lesson search <kw>`
- **`feedback`** — defects/wishes about the skills or scripts, routed to the right skill/script
  and fixed in a later revision pass. `/figure-to-svg feedback "<...>"` · `feedback list`
- **`digest`** — bulk-harvest a whole session's transcript into routed lessons + feedback
  (confirm-gated, never auto-files). `/figure-to-svg digest ["<session>"] [--dry-run]`

Verb definitions: `skills/figure-to-svg/fn/{lesson,feedback,digest}.md`; the filed knowledge:
`skills/figure-to-svg/lesson/` and `skills/figure-to-svg/feedback/`. The lessons range from craft
calls (which glyphs resist primitives, when to keep raster) through scorer gotchas to delivery
tricks (PPT-safe text, measured gradients); the rules they taught live inline in the skills.

## `icon-to-svg` — one icon → faithful hand-authored SVG

Decompose a single raster icon/graphic into back-to-front primitives with sampled colors, write
minimal SVG, render side-by-side against the source, self-score, refine, save. Replication, not
"grab a similar stock glyph." Every icon is **centered and self-contained**. Usable standalone.

- `scripts/render_compare.py` — renders an SVG beside its source at matched size (visual check).
- `scripts/score_icon.py` — **inner evaluation**: numeric `sim/shape/color/center` + PASS/REVISE, loop until pass.
- `scripts/center_svg.py` — normalize an SVG's viewBox tight to its content (centered, self-contained).
- Venv: `~/.cache/img2svg-venv` (`cairosvg Pillow numpy`; scipy optional, sharper de-noising).

## Evaluation, by layer

- **Icon — self-score** (`score_icon.py`, in icon-to-svg): does each SVG match its slice & center? loop-until-pass at the leaf.
- **Batch** (`evaluate_icons.py`): which finished icons are still weak, across the whole set — ranks work, never signs off.
- **Replica — fresh-eyes judge**: a FRESH subagent (no run context) reads every original|replica diff and returns pass/revise issues; each issue reopens its step. The author never signs off on their own render.

Guiding split: **code measures pixels, the model measures meaning** — and the final meaning-check
comes from eyes that didn't draw it.

## Fidelity principle

Don't fake matches. Anything that can't reduce to clean primitives (rendered digits like
"120/80", photographic texture, organic interlocking glyphs) stays a transparent raster
(`"keep_raster": true`) and is embedded as-is — honesty about a weak match beats a confident wrong one.
