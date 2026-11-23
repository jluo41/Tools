How the Word lane places every display at the top of a page and makes every table arrive in Word (haipipe-paper-assemble).

## 🔝 Word: every display at the top of a page (0.12.2, JL 261028)

JL 261028: "when doing the word, keep the displays to the top." The Word lane places each table and figure the way
the LaTeX `[t]` float does, and a paper does not switch this off.

1. **Top, always**: `display_float = "top"` is the default and the rule; do not set `"inline"` in a paper's
   `paper-build.toml`. Inline placement put a figure mid-page with its legend running into the next paragraph.
2. **At the page after its citing paragraph**: with Microsoft Word on the Mac, `save_docx` lets Word lay the text
   out and puts each display at the top of the page after the one its citing paragraph ends on.
3. **Never inside a sentence**: when that page ends inside a paragraph, the paragraph is split only at a sentence
   end (`boundary_target`); if the page ends in its first sentence, the display goes in front of the whole paragraph.
   The second part carries on without a first-line indent.
4. **A gap under the legend**: the display's last paragraph gets 18 pt after it, with the style's contextual
   spacing turned off (`no_contextual_spacing`), so the legend never reads as body text.
5. **Check the render**: after a build, render Word's own PDF (`word/<name>.pdf`) page by page and look at every
   display page before saying the file is ready (haipipe-delivery).

Builds take turns in Word (`scripts/word_lock.py`, 0.17.2; one lock per machine). Word is asked one question first; no
answer in 30 seconds and the build skips measuring and says so (0.17.1). A build quits Word only if it started it and no
document is open. On a working Word a whole 52-page build with 14 displays took 40 to 80 seconds (three runs, 261104).

## 📊 Tables must arrive in Word (0.7.1)

The Word engine parses each `table` float into rows itself. Its column-spec
reader is brace-aware (`p{3cm}`, `@{}`, `>{\raggedright\arraybackslash}`,
`*{6}{X}`, `tabularx` width argument, `tabular*`, `longtable`); rows split on
`\\` only at brace depth 0 so `\shortstack{a\\b}` stays one cell; a
`\multicolumn{n}` cell pads `n-1` empties. Supplement displays are numbered
(`Table S1.`, `Figure S1.`; profile keys `supplement_table_prefix`,
`supplement_figure_prefix`). After both `.docx` files are written the engine
counts their real `<w:tbl>` elements against the table displays it meant to
emit and against the master's table floats, records
`build.checks.tables_rendered` in the manifest, and exits non-zero on any
mismatch: a table that reaches the PDF and not the Word file is a loud failure,
never a caption with nothing under it (found by Paper-Example-Misq, 260908: 3 of 4
main tables and 7 of 12 appendix tables were lost). `tests/test_latex_room_to_docx.py`
drives the real engine over a room with those exact column specs.

## 🧾 Table cells read as the PDF prints them (261118)

ScalingGlucose ED Table 5 in Word (JL 261118: "how do you think the display of the word? it think it should be
better?"). The parts: `scripts/latex_table.py` reads rows and cells, `scripts/docx_table.py` writes them into Word.

- **Header rows**: the rows above the first `\midrule`, only when there are 3 or fewer. More rows there means a panel
  (its title, its column names, its data), so only row 0 is the header; before, every data row printed bold.
- **Math in a cell**: `^{...}` and `^x` inside `$...$` are raised (`math_scripts_raised`); before, "A N-α" printed.
- **Emphasis**: `\textbf` and `\textit` in a cell print bold and italic (`mark_emphasis`, `add_marked_runs`).
- **Panel titles**: `\multicolumn{n}{l}{...}` stays left-aligned (the mark `CELL_LEFT`); a `{c}` span is centered.

Tests: `tests/test_table_cells.py`.

## 🔍 Is the co-authors' Word file the same as the build? (261122)

AgreeableJama-Board asked this four times in one session and nothing answered it: `word_round.py pull` reports
comments and versions, not sentence equality. One command compares, by section:

    python scripts/word_compare.py <theirs.docx> <build.docx>           sentences and table cells: same, changed, only in one
    python scripts/word_compare.py <theirs.docx> <build.pdf> [--reverse] every Word sentence and cell looked up in the PDF
    python scripts/word_compare.py <file.docx> --citations              only the citation-order check
    ... --out report.md

1. **When**: after every `pull`, and as the acceptance check of any change to a builder (the same text before and after).
2. **Accepted view**: deleted text dropped, inserted text kept, equations (OMML) read as their text.
3. **Folding**: NFKC on both sides (a PDF's U+037E is a semicolon), curly quotes and dashes plain; for the PDF, line breaks, hyphenation and punctuation folded away.
4. **Three tries**: as written; digits ignored ("digits differ", usually a citation number); its pieces in order ("a mark placed elsewhere", a superscript the PDF prints apart).
5. **Citation order**: numbered citations (superscript runs or `[n]`) from the first heading to References must run in the order first cited (AMA). A reference cited late is named with the higher numbers cited before it ("16 is first cited after 17, 18"); numbers it did not find cited in the text are listed as "not found ... by this tool", never as "never cited". Author affiliation marks and powers (R², a superscript touching a one-letter word) are not citations; a number after punctuation, as in "(eAppendix 4 in Supplement 1)²³", is. A supplement (its name or title lines say "supplement") reuses the main list's numbers, so its order is not checked and the report says so. `word_round.py pull` prints this check on every file that comes back.

Limits: `--reverse` is rough, since pdftotext glues captions and table cells to their neighbours; a sentence the PDF
splits across a float can come back "not found". The report reads files only and writes nothing but `--out`.

## 🔖 Author-date citations read as the PDF prints them (261122)

The Word copy takes each author-date label from `master.bbl`, the file BibTeX wrote with the venue's style
(`scripts/bbl_labels.py`), so both copies cite the same way: "(Lu & Rui, 2018)" in parentheses, "Lu and Rui (2018)"
in a sentence, and one name for one author's works with LaTeX's year letters, "(Centers for Medicare & Medicaid
Services, 2026a, 2026b)". apacite and natbib labels are read; with no `.bbl` (a Word-only build) the label falls back
to the `.bib` reading. Pp-AgreeableRx 261122: the Word file printed "Lu and Rui" and the same author twice with no
year letters.

A display placed after the one before it never crosses into the next Section or Appendix: it stops in front of that
heading (`scripts/docx_held.py`, `place_held`).

## 🖥 A build never uses the person's open Word (261122)

A build prints a `.docx` to PDF and measures page tops in Microsoft Word only when Word is not running or holds no
document of the person's (`word_lock.word_in_use`); otherwise displays follow their citing paragraphs and the
preview comes from the HTML renderer, and the build says so. `HAIPIPE_WORD_PREVIEW=word` uses Word anyway.
Pp-AgreeableRx 261122: every build opened, printed and closed windows in a Word open for 36 hours with shared OneDrive
files, stole focus, and left a preview copy open.
