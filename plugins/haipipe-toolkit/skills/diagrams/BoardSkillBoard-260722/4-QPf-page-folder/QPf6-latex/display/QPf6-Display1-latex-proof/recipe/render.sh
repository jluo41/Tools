#!/bin/sh
# render the compiled proof into the unit: one PNG per page + the preview
cd "$(dirname "$0")/.."
pdftoppm -png -r 150 ../../latex/QPf6-latex.pdf assets/page
cp ../../latex/QPf6-latex.pdf preview.pdf
