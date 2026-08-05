#!/usr/bin/env bash
# build-both.sh -- one source, two projections, and a PDF of each.
#
# JL 2026-07-28: "create both tex and word and then have both of them to be the
# pdf". The point is COMPARISON. Both PDFs come from the same nine stage pages
# and are set to MISQ's stated page setup, so a difference between them is a
# difference in the PROJECTION and not in the content or the paper size.
#
#   0-lifecycle/4-main/S-Main-*.md          the source, and the only source
#        |
#        +-- md2tex.py  --> 3-dist/tex/*.tex   --xelatex+bibtex-->  paper.pdf
#        |                  the manuscript. Lanes DROPPED, per QC5.
#        |
#        +-- md2docx.py --> 3-dist/word/S-Main-all.docx
#                           |                evidence in anchored comments, QC6
#                           +-- docx2pdf.py --> 3-dist/pdf/S-Main-all-from-word.pdf
#                                              the same comments, printed in the
#                                              margin, so the .docx can be read
#                                              by someone with no Word
#
# Usage:  bash build-both.sh <paper-root> [author]
set -euo pipefail
ROOT="$(cd "${1:?usage: build-both.sh <paper-root> [author]}" && pwd)"
AUTHOR="${2:-haipipe}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOARD="$HERE/../../../../board/haipipe-board"
PAGES=$(ls "$ROOT"/0-lifecycle/4-main/S-Main-[0-9]*.md | sort)

cd "$ROOT"
mkdir -p 3-dist/word 3-dist/tex

echo "── bibliography ───────────────────────────────────────────"
python3 "$BOARD/refs.py" . 2>&1 | sed -n '2p'

echo "── 1/3  source -> LaTeX -> PDF ────────────────────────────"
python3 "$HERE/md2tex.py" $PAGES --paper-root . --compile 2>&1 | tail -3

echo "── 2/3  source -> Word ────────────────────────────────────"
python3 "$HERE/md2docx.py" $PAGES -o 3-dist/word/S-Main-all.docx \
        --paper-root . --join-paragraphs --author "$AUTHOR" 2>&1 | sed -n '2,3p'

echo "── 3/3  Word -> PDF ───────────────────────────────────────"
# beside its .docx, not in a pdf/ of its own. The pair belongs together, and a
# separate folder is how a stale 13-page textutil render sat next to the real one
# looking equally authoritative (JL 2026-07-28).
python3 "$HERE/docx2pdf.py" 3-dist/word/S-Main-all.docx 2>&1 | tail -3

echo "── both PDFs ──────────────────────────────────────────────"
for f in 3-dist/tex/paper.pdf 3-dist/word/S-Main-all.pdf; do
  [ -f "$f" ] || { printf "  %-42s MISSING\n" "$f"; continue; }
  pg=$(pdfinfo "$f" 2>/dev/null | awk '/^Pages/{print $2}')
  sz=$(pdfinfo "$f" 2>/dev/null | awk -F'  +' '/^Page size/{print $2}')
  printf "  %-42s %3s pages  %s\n" "$f" "${pg:-?}" "$sz"
done
