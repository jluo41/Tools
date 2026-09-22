# Shared Page document exporters

These writers implement the derived `latex/` and `word/` projections used by
Board Page workbenches:

- `md2tex.py` reads one accepted Page and emits TeX.
- `md2docx.py` reads the same Page and emits DOCX.
- `docx2pdf.py` renders the DOCX twin used by the Word surface.

They are server code beside their caller, not Paper routing logic and not a
skill: `servers/workbench-page/export.py` (the `/_board/latex` and
`/_board/word` doors) runs them by path, and
`skills/page/haipipe-workbench-page/ref/delivery.md` is the
contract they implement. They left `paper/haipipe-paper/scripts/to-word/`
when the Paper family retired its stage runtime on 2026-08-20 and left
`skills/` on 2026-09-21 so that no server code remains under a skill.
`test_md2docx.py` is their unit test; run it from this folder.
# Shared delivery writers

The shared Markdown reader removes HTML comments before creating Word or
LaTeX blocks. These comments may carry invisible Board receipts such as stable
Bullet realization addresses, but they are never manuscript prose.

