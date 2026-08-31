---
name: haipipe-plugin-latex
description: >-
  The latex/ plugin of a Board page: compile the page's Content to a derived,
  regenerable PDF in its local latex/ folder via md2tex.py and lualatex.
  Trigger: latex plugin, compile the page, page pdf, tex export, latex tab,
  rebuild the tex, /haipipe-plugin-latex.
metadata:
  version: "0.2.3"
  last_updated: "2026-08-31"
---
# /haipipe-plugin-latex · the page compiled, by the paper family's own writer

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only latex's delta: how the board calls a writer it does not own, and what the result promises.

> 📤 Since 260831 this tab is the 📜 LaTeX SEGMENT inside the one 📤 Delivery tab (`haipipe-plugin-delivery`); the surface below is unchanged, only where it hangs moved.

## 🗂 Storage · derived, regenerable, never hand-edited

```text
<page>/delivery/latex/
├── <stem>.tex           md2tex's section · header says "do not hand-edit"
├── <stem>.pdf           the compiled look · what the tab frames
└── <stem>-view.html     the fallback view: the .tex + the log tail
```

A hand-edited file is overwritten on the next build; that is the derived-plugin rule, not a defect.
The 📂 Folder tab flags this plugin STALE when its newest file predates the page's `.md`.

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
- THE PAGE'S DISPLAY EVIDENCE PRINTS (JL 260816): a unit under `<page>/evidence/display/` that the prose cites by Page-local `DisplayN` or fully qualified `<stem>-DisplayN` is embedded once as a real float after the citing paragraph, in citation order, under MISQ's first-reference rule.
  The float is built from the unit's WINNING asset plus its own authored caption and label, so the wrapper master needs no tikz or renderer package; a ⬜ unit with no render is skipped, and a mention inside a verbatim fence is an illustration, not a citation.

## 📡 Surface · the tab, and what a failure shows

The right-pane 📜 tab frames the PDF; 🔄 rebuild re-runs the route and reloads.
`lualatex` producing no PDF is never a blank frame: the view page shows the `.tex` and the log tail, so the failure is readable where it happened.


> Since 260831 this lane lives under the page's category folder (`evidence/` or `delivery/`, haipipe-page 0.47.0 §📁); a flat lane name on an unmigrated page, or a flat SYMLINK STUB on a migrated one, is the same lane during the migration.

## 📂 Files

- `../../haipipe-board/live/export.py`
  The route, the master wrap, the view pages.
- `../_shared-export/md2tex.py`
  The writer; Word and LaTeX stay two projections of one reader (`md2docx.parse_page`).
- `../../haipipe-plugin/ref/roster.md`
  The row this skill expands.
