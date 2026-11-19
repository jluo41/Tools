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
