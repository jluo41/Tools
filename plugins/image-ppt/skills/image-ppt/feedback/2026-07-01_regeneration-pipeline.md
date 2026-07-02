---
status: open
created: 2026-07-01
updated: 2026-07-01
occurrences: 1
context: figure-to-svg-replica
fixed_in: ""
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

Fix:
