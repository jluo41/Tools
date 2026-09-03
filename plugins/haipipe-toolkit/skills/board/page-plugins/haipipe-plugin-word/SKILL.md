---
name: haipipe-plugin-word
description: >-
  The WORD plugin of a Board page: export the page's prose as a coauthor .docx
  with a PDF twin — flowing paragraphs, citations and References resolved from
  the page's own bibex/ bib, evidence as anchored Word comments. Trigger: word
  plugin, word export, docx export, page to word, coauthor docx,
  /haipipe-plugin-word.
metadata:
  version: "0.3.0"
  last_updated: "2026-08-31"
---

# /haipipe-plugin-word · one page, as a document a coauthor can mark up

`haipipe-plugin` defines what any plugin is; this skill is the word/ row, loadable on its own.
The export exists for one reader: a coauthor who marks up in Word and does not use LaTeX.
The design record is the board's `QPf7-word` page; the writer's own truth is `md2docx.py`'s docstring; this skill is the operating knowledge between them.

> 📤 Since 260831 this tab is the 📝 Word SEGMENT inside the one 📤 Delivery tab (`haipipe-plugin-delivery`); the surface below is unchanged, only where it hangs moved.

## 📦 What lands in `<page>/delivery/word/`

```
<stem>.docx        the ARTIFACT · what the coauthor opens
<stem>.pdf         the TWIN · Chrome-rendered from the package itself,
                   comments and all · what the 📝 tab frames
<stem>-view.html   the tab's surface: twin inline + ⬇ download
```

All three are DERIVED: a rebuild overwrites them, and a lasting correction belongs on the page.

## 📜 The rules the export obeys

**Paragraph per paragraph (JL 260815)**: the board's `.md` keeps one sentence per line for its sentence-anchor grammar, and the export passes `--join-paragraphs` so each block lands as one flowing paragraph.
The one-line form is board machinery and stops at the writer.

**The Page title prints**: the Board passes the complete canonical H1 through `--document-title`; md2docx emits it once with Word's editable `Title` paragraph style before the numbered Content headings. It is independent of the writer's paper-section H1 inference, so a Page that begins Content with `### 1 ...` cannot suppress its document title.

**The page's bib comes first**: when `bibex/<stem>.bib` holds an entry, `cli/refs.py` compiles `.board-refs.bbl` beside it and md2docx renders the in-text label and a References section from it — the same store that feeds the page's cite chips and the LaTeX PDF.
With no page store, a paper's `0-*.bib` found upward rides along; outside any paper the export degrades cite-less rather than refusing.

**The twin, not a converter**: `docx2pdf.py` reads the OOXML this family itself wrote; macOS's `textutil` was measured dropping all 239 anchored comments, which for an evidence-carrying file is a different document.

**Evidence rides as comments**: `--lanes` defaults to Citation alone (the paper family's ruling); whether a BOARD page's export wants lanes at all is QPf7's open A2.1, answered by a real coauthor's markup.

**The page's display evidence embeds (JL 260816)**: when `<page>/outline/evidence/display/` holds units, the board's caller bridges the grammar gap; md2docx keys floats on `\ref` and a board page cites by Page-local `DisplayN` or fully qualified `<stem>-DisplayN`, so `export.py` hands the writer a TEMP copy with `(\ref{<label>})` appended to each unit's first prose mention, plus `--display-root <page>/outline/evidence/display` and `--lanes Citation,Display`. Aliases identify one unit and therefore embed it only once.
The docx then carries the figure (rasterized from the unit's winning `figure.pdf`) with the unit's own caption, the inline `(Figure n)`, and a 🖼 Display comment on the citing sentence; the page source is never edited and the temp is deleted after the run.

**Tables remain native and editable**: booktabs `tabular` and `tabularx` assets, including balanced column specifications such as `@{}X r@{}` and `\multicolumn`, are parsed into Word table rows. TeX wrappers and note minipages do not leak into cell text.

## 🖥 How to run it

Through the board: the 📝 tab or the Plugin menu; lit-click rebuilds.
Headless, through the server: `POST /_board/word {path: "<board>/board.md", file: "<group>/<stem>/<stem>.md"}` — the response carries the view, docx, and twin URLs.
The writer directly, board conventions included:

```bash
python3 skills/board/page-plugins/_shared-export/md2docx.py <page.md> \
        -o <page-dir>/word/<stem>.docx --join-paragraphs \
        [--document-title "Full Page H1"] [--paper-root DIR]
```

## ⚠️ Known warts

The Board's `**Name**:` caption markers are Page scaffolding; the shared reader strips them before Word output.
The twin needs Chrome on the machine; without it the view keeps the ⬇ download and names the failure.


The writer always lands new artifacts in `delivery/word/`. A pre-migration
flat `word/` may be read during a sweep, but it is not a current destination
and must not be shown as the canonical Folder row.
