# LaTeX lane · the page compiled by the paper family's writer

This is an internal lane contract of `haipipe-plugin-delivery`. The category
skill owns the public surface; this reference owns how the Board calls a writer
it does not own and what the Result promises.

> 📤 Since 260831 this is the 📜 LaTeX SEGMENT inside the one 📤 Delivery tab (`haipipe-plugin-delivery`).

## 🗂 Storage · derived, regenerable, never hand-edited

```text
<page>/delivery/latex/
├── <stem>.tex           md2tex's section · header says "do not hand-edit"
├── <stem>.pdf           the compiled look · what the segment frames
└── <stem>-view.html     the fallback view: the .tex + the log tail
```

A hand-edited file is overwritten on the next build; that is the derived-lane rule, not a defect.
The 📂 Folder tab flags this lane STALE when its newest file predates the page's `.md`.

## ⚙️ Writer · a caller by path, never a copy

The one door is `POST /_board/latex` (`live/export.py`), and it runs the paper family's writer:

```text
md2tex.py  (skills/board/page-plugins/_shared-export/)     the section
export.py  wraps a standalone master · runs lualatex       the PDF
```

Three caller rules, each earned on 260815:

- `--keep-fences` is the BOARD's default: a board division is often figure-only, and the paper default (drop sketches) exported it as an empty section.
  A kept fence arrives through the configured LuaLaTeX fallback fonts so box glyphs and emoji remain visible when supported.
- `--paper-root` is DISCOVERED, never demanded: walk up from the page toward `--root` for a `0-*.bib`.
  A page outside any paper compiles cite-less, with `\citep` shown literally; inside a paper the master gains natbib, `plainnat`, and a bibtex pass.
- A code span QUOTES and never EXECUTES: backticked TeX commands are escaped on the way out, so `\citep` prints instead of running.
- **The Page title prints**: the standalone master opens with the complete canonical H1, TeX-escaped as plain text. The title is document identity, not a Content division, so it is emitted independently of numbered `###` manuscript headings.
- THE PAGE'S DISPLAY EVIDENCE PRINTS (JL 260816): a unit under `<page>/outline/evidence/display/` that the prose cites by Page-local `DisplayN` or fully qualified `<stem>-DisplayN` is embedded once as a real float after the citing paragraph, in citation order, under MISQ's first-reference rule.
  The float is built from the unit's WINNING asset plus its own authored caption and label, so the wrapper master needs no tikz or renderer package; a ⬜ unit with no render is skipped, and a mention inside a verbatim fence is an illustration, not a citation.

## 📡 Surface · the segment, and what a failure shows

Delivery's right-pane 📜 segment frames the PDF; 🔄 rebuild re-runs the route and reloads.
`lualatex` producing no PDF is never a blank frame: the view page shows the `.tex` and the log tail, so the failure is readable where it happened.


The writer always lands new artifacts in `delivery/latex/`. A pre-migration
flat `latex/` may be read during a sweep, but it is not a current destination
and must not be shown as the canonical Folder row.

## 📂 Files

- `../../../haipipe-board/live/export.py`
  The route, the master wrap, the view pages.
- `../../_shared-export/md2tex.py`
  The writer; Word and LaTeX stay two projections of one reader (`md2docx.parse_page`).
- `../../../haipipe-plugin/ref/roster.md`
  The `delivery/latex/` lane row this category owns.
