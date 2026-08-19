#!/bin/sh
# render the compiled proof into the unit: one PNG per page, the winning asset,
# and the preview. `figure.png` is the WINNING asset name check.py looks for
# (src/page_evidence.py:34); page-N.png are the loose pages beside it.
cd "$(dirname "$0")/.."
pdftoppm -png -r 150 ../../latex/QPf6-latex.pdf assets/page
cp ../../latex/QPf6-latex.pdf preview.pdf
cp assets/page-1.png assets/figure.png
pdfseparate -f 1 -l 1 ../../latex/QPf6-latex.pdf assets/figure.pdf   # the EXPORTER only embeds figure.pdf
