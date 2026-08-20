#!/usr/bin/env bash
# Archived 2026-08-20 with the retired stage runtime.
# This wrapper hard-codes 0-lifecycle/4-main/S-Main-* and is not a shared Page
# exporter. The reusable writers now live under board/page-plugins/_shared-export/.
set -euo pipefail
ROOT="$(cd "${1:?usage: build-both.sh <paper-root> [author]}" && pwd)"
AUTHOR="${2:-haipipe}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SHARED="$HERE/../../../../../../board/page-plugins/_shared-export"
BOARD="$HERE/../../../../../../board/haipipe-board"
PAGES=$(ls "$ROOT"/0-lifecycle/4-main/S-Main-[0-9]*.md | sort)

cd "$ROOT"
mkdir -p 3-dist/word 3-dist/tex

echo "── bibliography ───────────────────────────────────────────"
python3 "$BOARD/refs.py" . 2>&1 | sed -n '2p'

echo "── 1/3  source -> LaTeX -> PDF ────────────────────────────"
python3 "$SHARED/md2tex.py" $PAGES --paper-root . --compile 2>&1 | tail -3

echo "── 2/3  source -> Word ────────────────────────────────────"
python3 "$SHARED/md2docx.py" $PAGES -o 3-dist/word/S-Main-all.docx \
        --paper-root . --join-paragraphs --author "$AUTHOR" 2>&1 | sed -n '2,3p'

echo "── 3/3  Word -> PDF ───────────────────────────────────────"
python3 "$SHARED/docx2pdf.py" 3-dist/word/S-Main-all.docx 2>&1 | tail -3

echo "── both PDFs ──────────────────────────────────────────────"
for f in 3-dist/tex/paper.pdf 3-dist/word/S-Main-all.pdf; do
  [ -f "$f" ] || { printf "  %-42s MISSING\n" "$f"; continue; }
  pg=$(pdfinfo "$f" 2>/dev/null | awk '/^Pages/{print $2}')
  sz=$(pdfinfo "$f" 2>/dev/null | awk -F'  +' '/^Page size/{print $2}')
  printf "  %-42s %3s pages  %s\n" "$f" "${pg:-?}" "$sz"
done
