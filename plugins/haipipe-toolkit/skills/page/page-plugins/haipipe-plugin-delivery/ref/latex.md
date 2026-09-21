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
md2tex.py  (skills/page/page-plugins/_shared-export/)     the section
export.py  wraps a standalone master · runs lualatex       the PDF
```

Three caller rules, each earned on 260815:

- `--keep-fences` is the BOARD's default: a board division is often figure-only, and the paper default (drop sketches) exported it as an empty section.
  A kept fence arrives through the configured LuaLaTeX fallback fonts so box glyphs and emoji remain visible when supported.
- `--paper-root` is DISCOVERED, never demanded: walk up from the page toward `--root` for a `0-*.bib`.
  A page outside any paper compiles cite-less, with `\citep` shown literally; inside a paper the master gains natbib, `plainnat`, and a bibtex pass.
- A code span QUOTES and never EXECUTES: backticked TeX commands are escaped on the way out, so `\citep` prints instead of running.
- **The Page title prints**: the standalone master opens with the complete canonical H1, TeX-escaped as plain text. The title is document identity, not a Content division, so it is emitted independently of numbered `###` manuscript headings.
- THE PAGE'S DISPLAY EVIDENCE PRINTS: a current typed DISPLAY Result points to a unit under `<page>/results/<re-run>/payload/<unit>/`. Page prose cites it with `\table{D_<slug>}`, `\figure{D_<slug>}`, or `\algorithm{D_<slug>}`; the Result's `labels:` row binds that token to the unit. Delivery resolves ready tokens to the unit's manuscript label in a TEMP copy of the Page, then embeds the float once after its first citing paragraph, in source order. An authored `\ref{label}` remains a supported manuscript reference. Venue-specific placement overrides come from the resolved Page Face owner. The retired Outline display folder is a read-only migration fallback when no typed DISPLAY Result exists.
  The float is built from the unit's winning asset plus its own authored caption and label, so the wrapper master needs no tikz or renderer package. An unbound token passed directly to the shared writer remains a legible pending marker. Board Delivery requires every cited D_ token to appear in a selected current DISPLAY Result's labels and blocks missing, conflicting, unready, or label-unbound current bindings, as well as ready units without exportable assets. It never falls back to stale evidence. A mention inside a verbatim fence is an illustration, not a citation.

## 📡 Surface · the segment, and what a failure shows

Delivery's right-pane 📜 segment frames the PDF; 🔄 rebuild re-runs the route and reloads.
`lualatex` producing no PDF is never a blank frame: the view page shows the `.tex` and the log tail, so the failure is readable where it happened.


The writer always lands new artifacts in `delivery/latex/`. A pre-migration
flat `latex/` may be read during a sweep, but it is not a current destination
and must not be shown as the canonical Folder row.

## 📂 Files

- `../../../../board/haipipe-board/live/export.py`
  The route, the master wrap, the view pages.
- `../../_shared-export/md2tex.py`
  The writer; Word and LaTeX stay two projections of one reader (`md2docx.parse_page`).
- `../../../haipipe-plugin/ref/roster.md`
  The `delivery/latex/` lane row this category owns.

## Current Evidence selection

Use the exact current Results bound in `outline/<stem>-evidence-items.md`,
shared with Evidence Space. DISPLAY uses the selected Result's `payload.unit`;
every cited D_ token must appear in its `labels:` list. CITE uses its verified
`payload.bibliography`. Missing, conflicting, unready, or label-unbound current
bindings block delivery. Do not scan historical units into the document.
Pages without a ledger use the explicitly recorded legacy migration profile.
The export's `evidence-selection.json` records that mode and selected hashes.
