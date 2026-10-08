# RETIRED: crop-from-source pipeline

**Status: retired 2026-07-04.** The live workflow regenerates icons via codex image-gen
(SKILL.md). This crop-based path performed badly on dense figures — crops landed on title text
and neighbours and couldn't be tightened — and was replaced. Kept only for provenance; the
scripts still work.

## What it was

analyze → crop → QC → vectorize each crop → compose.

1. **Analyze**: `grid_overlay.py` renders a labeled coordinate grid; read every icon/text bbox
   into `items.json` (`[x, y, w, h]` in source pixels).
2. **Crop**: `crop_bboxes.py <source> items.json crop_images/` cuts each `type:"icon"` out of
   the source; `contact_sheet.py` builds a review sheet that had to be eyeballed + LLM-judged.
3. **Crop QC (code)**: `crop_qc.py <source> items.json crop_images/ --apply` — geometric checks
   (clipped ink, detached specks, dead padding, off-center) with pixel-exact bbox auto-fix and
   re-crop. Backs up `items.json.bak`. Known open defect: assumes dark-on-light; over-flags
   white-on-dark icons (see feedback/2026-07-01_crop-qc-detect-inverted-polarity.md).
4. **Crop QC (LLM-as-judge)**: `crop_judge_sheet.py` builds judge panels (isolated crop +
   context with the box drawn); subagents return
   `{"id","usable","clipped_sides":["bottom"],"contaminated","unclear"}` verdicts to
   `_judge/verdicts.json`; `crop_judge_apply.py` applies them (grow clipped sides, mark
   `keep_raster`), then `crop_qc.py --apply` snaps tight. Division of labour: the LLM said
   *what/which side*, code made it pixel-exact.
5. **Vectorize + compose**: same tail as the live pipeline.

For pixel-tight, background-free crops on busy figures there was an optional SAM route:
`references/sam_optional.md` (needs torch + a 375 MB model).

## Scripts that belong to this path

`crop_bboxes.py`, `contact_sheet.py`, `crop_qc.py`, `crop_judge_sheet.py`,
`crop_judge_apply.py`, `sam_optional.md`. (`grid_overlay.py` survives in the live pipeline for
reading layout coordinates; `evaluate_icons.py`, `compose_svg.py`, `render_diff.py` were always
shared.)
