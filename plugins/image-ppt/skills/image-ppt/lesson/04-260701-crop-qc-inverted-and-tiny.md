# Lesson 04: crop_qc over-flags inverted-polarity and tiny anti-aliased crops — don't blindly --apply

## The Problem
`crop_qc.py` flagged nearly every icon (41/45): footer white-on-navy icons as LOOSE/OFF-CTR, and
small ~30px resource line-icons as CLIP with fill% >100. Running `--apply` on the white-on-dark
ones would have tightened them to noise.

## The Solution
Read the QC report, but split trust by icon type:
- Dark-on-light, normal-size icons: `crop_qc --apply` is reliable — let it tighten bboxes.
- White-on-dark (footer) icons: QC geometry is unreliable; set those bboxes by hand and let the
  vectorizing model (which SEES the crop) judge semantics.
- Tiny/anti-aliased crops (CLIP with fill%>100): the box is genuinely a bit tight — nudge width/
  height by hand rather than auto-applying.
Skim a contact sheet of the crops and fix by eye; a few stray neighbor-label letters are fine —
tell the sub-agent to draw only the named glyph and ignore them.

## Why It Works
QC's fill/centroid math assumes dark ink on a light background. Inverted polarity and near-white
anti-aliased edges break that assumption, producing spurious flags. The model reading the crop is
the right judge of "is the whole icon here", per the skill's split (code measures pixels, model
measures meaning).

## When to Apply
Whenever the resources/footer/header bands have light icons on dark fills, or icons are small
(≲32px) with soft edges.

## Caveats
`--apply` backs up items.json.bak, so mistakes are recoverable — but re-cropping inverted icons to
"content" can still delete the glyph. Prefer manual bbox edits there.
