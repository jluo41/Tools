---
status: open
created: 2026-06-24
context: display stage, ProjB Paper-Personality2Opioid-MISQ2026
fixed_in: ""
---
"display must make the content follow the predefined display content"

The display stage must conform its output to the PREDEFINED display-unit contract
(ref/display-unit-output-contract.md): every display is a
`displayNN-<slug>/` unit with `README.md` (claim/kind/source/caption-job/
fragility/status) + `float.tex` (caption + \label + asset reference) + `preview.tex`
+ `preview.pdf` + `assets/` (the rendered asset) + `source/` (rebuild spec). It
must NOT be flat loose files (a bare `Figure/` + `Table/` dump) or ad-hoc assets.

What went wrong here: the paper's `0-display/` was a flat `Figure/` + `Table/`
folder of loose `.pdf`/`.tex` files, and my display work added more loose files
(an ad-hoc matplotlib plot, then a copied illustration png) instead of filing each
display as a contract-compliant unit. The display stage did not enforce the
predefined display-unit content/structure.

FIX (proposed): haipipe-paper-display must, at stage entry, (a) reconcile any
legacy flat `0-display(s)/` assets INTO `displayNN-<slug>/` units, and (b) require
every new/rendered display to be filed as a unit per the contract before it counts
as a current-cycle display. No loose assets; the unit IS the deliverable.

Fix:
