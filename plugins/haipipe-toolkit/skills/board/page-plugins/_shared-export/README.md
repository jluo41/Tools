# Shared Page document exporters

These writers implement the derived `latex/` and `word/` projections used by
Board Page plugins:

- `md2tex.py` reads one accepted Page and emits TeX.
- `md2docx.py` reads the same Page and emits DOCX.
- `docx2pdf.py` renders the DOCX twin used by the Word surface.

They are shared Page-plugin implementation, not Paper routing logic. They moved
from `paper/haipipe-paper/scripts/to-word/` when the Paper family retired its
stage runtime on 2026-08-20. `haipipe-board/live/export.py` is the caller.

