# Word lane · one page as a document a coauthor can mark up

This is an internal lane contract of `haipipe-plugin-delivery`. The category
skill owns the public surface; this reference owns the Word writer, storage,
and projection guarantees. The export exists for one reader: a coauthor who
marks up in Word and does not use LaTeX.
The design record is the board's `QPf7-word` page; the writer's own truth is `md2docx.py`'s docstring; this skill is the operating knowledge between them.

> 📤 Since 260831 this is the 📝 Word SEGMENT inside the one 📤 Delivery tab (`haipipe-plugin-delivery`).

## 📦 What lands in `<page>/delivery/word/`

```
<stem>.docx        the ARTIFACT · what the coauthor opens
<stem>.pdf         the TWIN · Chrome-rendered from the package itself,
                   comments and all · what the 📝 segment frames
<stem>-view.html   the segment surface: twin inline + ⬇ download
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

**The page's display evidence embeds (typed DISPLAY Result payloads)**: the Board selects each current envelope from `outline/<stem>-evidence-items.md`, resolves its `payload.unit` under `<page>/results/<re-run>/payload/<unit>/`, and stages only those selected units in a short-lived directory for `md2docx`. Page prose cites the Result with `\table{D_<slug>}`, `\figure{D_<slug>}`, or `\algorithm{D_<slug>}`; the Result's `labels:` row binds that token to the unit's manuscript `\label`. `export.py` resolves ready tokens to `\ref{<label>}` in a TEMP copy of the Page, then passes the staged root as `--display-root` with `--lanes Citation,Display`; `md2docx` scans that selected set, so historical same-label units cannot override it. An authored `\ref{label}` remains a supported manuscript reference. The retired Outline display folder is a read-only migration fallback when no typed DISPLAY Result exists.
The docx carries the figure (rasterized from the selected unit's winning `figure.pdf`) or native table body with the unit's own caption, the inline figure/table reference, and a 🖼 Display comment on the citing sentence. The Page source is never edited and the temporary source and selected-unit staging directory are removed after the run. An unbound token passed directly to the shared writer stays readable as pending text. Board Delivery requires every cited D_ token to appear in a selected current DISPLAY Result's labels and blocks missing, conflicting, unready, or label-unbound current bindings, as well as ready units without exportable assets; it never falls back to stale evidence.

**Tables remain native and editable**: booktabs `tabular` and `tabularx` assets, including balanced column specifications such as `@{}X r@{}` and `\multicolumn`, are parsed into Word table rows. TeX wrappers and note minipages do not leak into cell text.

## 🖥 How to run it

Through the Board: Delivery's 📝 segment; click rebuilds.
Headless, through the server: `POST /_board/word {path: "<board>/board.md", file: "<group>/<stem>/<stem>.md"}` — the response carries the view, docx, and twin URLs.
The writer directly, board conventions included:

```bash
python3 skills/page/page-plugins/_shared-export/md2docx.py <page.md> \
        -o <page-dir>/delivery/word/<stem>.docx --join-paragraphs \
        [--document-title "Full Page H1"] [--paper-root DIR]
```

## ⚠️ Known warts

The Board's `**Name**:` caption markers are Page scaffolding; the shared reader strips them before Word output.
The twin needs Chrome on the machine; without it the view keeps the ⬇ download and names the failure.


The writer always lands new artifacts in `delivery/word/`. A pre-migration
flat `word/` may be read during a sweep, but it is not a current destination
and must not be shown as the canonical Folder row.

## Current Evidence selection

Use the exact current Results bound in `outline/<stem>-evidence-items.md`,
shared with Evidence Space. DISPLAY uses the selected Result's `payload.unit`;
every cited D_ token must appear in its `labels:` list. CITE uses its verified
`payload.bibliography`. Missing, conflicting, unready, or label-unbound current
bindings block delivery. Do not scan historical units into the document.
Pages without a ledger use the explicitly recorded legacy migration profile.
The export's `evidence-selection.json` records that mode and selected hashes.
