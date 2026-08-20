# Shared exporters moved

The reusable `md2tex.py`, `md2docx.py`, and `docx2pdf.py` implementations now
live at `skills/board/page-plugins/_shared-export/`.

They were extracted from the retired Paper stage runtime because current
LaTeX and Word are Page-local plugins, while this directory is historical.
