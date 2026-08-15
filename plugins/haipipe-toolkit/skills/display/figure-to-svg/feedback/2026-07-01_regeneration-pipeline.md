---
status: fixed
created: 2026-07-01
updated: 2026-07-04
occurrences: 1
context: figure-to-svg
fixed_in: "v1.2.0"
regressed: ""
---
figure-to-svg-replica is built entirely around CROPPING icons out of the source
(grid_overlay -> items.json bboxes -> crop_bboxes -> crop_qc), which performs badly on dense
multi-icon figures: crops land on title text / neighbours, and the user rejected them outright
("the performance is very bad, I delete them"). Add a first-class REGENERATION pipeline as the
default path for busy figures:

  full -> per-part sections; per part:
    regenerate icons via image-gen (codex-image2 bridge, reference = the section crop) as a
    **3x3 grid BY DEFAULT** (2x2 for human-figure-heavy sections; never 4x4)
    -> slice by equal division, keeping the central connected component (drops neighbour-bleed)
    -> transparentize by removing border-connected white (preserve interior whites)
    -> compose each part -> assemble a master.

This session hand-rolled the pieces as gen_grid.py / slice_grid.py / transparentize.py /
build_pipeline.py — vendor them into the skill as scripts, and document the per-part tree
(subimages/partN/{part.png,manifest.json,redraw_icon/,cropped_icon/,partN_replica.svg}).
See lesson/13, lesson/14, lesson/15, lesson/18.

Fix: 2026-07-04 — scripts vendored (`gen_icon_grid.py`, `slice_grid.py`, `transparentize.py`) and
the per-part tree documented. SKILL.md now structures this as "Path A — regenerate (default for
dense figures)" vs "Path B — crop from source", with an availability check (bridge missing → Path B,
enforced by a clear error in `gen_icon_grid.py`, whose bridge path is now resolved relative to the
plugin instead of a hardcoded home directory) and a new Path-A step 5: vectorize each sliced icon
via image-to-svg so PPT Convert-to-Shape yields editable shapes.
Later the same day (v1.3.0): regeneration became the ONLY pipeline — the crop path was retired to
references/legacy-crop-path.md, and a mandatory fresh-subagent review loop was added after compose.
