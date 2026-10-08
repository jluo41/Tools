#!/usr/bin/env python3
"""Merge the NN-*.svg slides into one vector PDF (16:9 pages).

Each SVG page converts via cairosvg (vector-preserving), then pypdf
concatenates them. Uses the display (wrapped) variant.

Requires:  pip install cairosvg pypdf
Run:       python3 build_pdf.py   → deck.pdf
"""
import io
from pathlib import Path

import cairosvg
from pypdf import PdfReader, PdfWriter

HERE = Path(__file__).parent
OUT = HERE / "deck.pdf"

writer = PdfWriter()
svgs = sorted(HERE.glob("[0-9][0-9]-*.svg"))
if not svgs:
    raise SystemExit("no NN-*.svg files found")
for svg in svgs:
    pdf_bytes = cairosvg.svg2pdf(url=str(svg))
    writer.append(PdfReader(io.BytesIO(pdf_bytes)))
    print(f"page {svg.name}")
with open(OUT, "wb") as f:
    writer.write(f)
print(f"\nwrote {OUT.name} ({OUT.stat().st_size // 1024} KB, {len(svgs)} pages)")
