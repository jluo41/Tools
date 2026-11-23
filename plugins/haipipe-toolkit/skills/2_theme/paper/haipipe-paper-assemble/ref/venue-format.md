A venue's format: settled once, the venue template checklist, and the venue profiles (haipipe-paper-assemble).

## 🚧 A venue's format is settled once (JL 261104)

JL 261104: "我觉得这个东西我们早就做过了 为什么现在把模板给我变了". A session downloaded the journal's template and changed a
format the paper had already agreed (the abstract's spacing, the title), with an author watching the PDF change.

```text
before any format change   read 1 the profile's comments · 2 the paper's official-format file in related/
                                3 the last round's files in delivery/<job>/word/
they agree                 that IS the format; say so, and change nothing
a new source differs       (a template, a guidelines page) list the differences with old and new side by side,
                           and ask; it never overrides by itself
a person asks "is it the template?"   answer by comparing; a question is not an order to change
sources disagree           the paper's own paper-build.toml, with a person's dated line, wins over the profile, the older format file and past rounds
```

A journal rule that is a hard limit (a page cap) can force a change: say which rule, what it costs, and ask first.

## 📋 The venue template checklist (JL 261104)

JL 261104: "I think this should be the checklist for the /haipipe-paper-assemble to make sure they follow the venue
template". When a venue publishes a template, every build compares both lanes with it, and the report says which rule differs.
It changes nothing: a person settles each difference, by asking for the fix or by accepting it (§ above).

```toml
[venue_template]                                       # paper-build.toml, paths from that file; none named = not checked
word = "../../venues/MISQ/kit/MISQ_Submission_Template_Word.docx"
latex = "../../venues/MISQ/kit/latex-template/MISQ_Submission_Template_LaTeX.tex"
accepted = []                                          # rule names a person chose to keep different
```

| Lane | The rows `scripts/venue_template_check.py` compares |
|---|---|
| Word | page size and margins; body font, size, spacing; title size, bold, alignment; abstract heading case and spacing; keywords spacing; major heading and subhead alignment, bold, case, numbers; references heading, spacing, hanging indent, new page; appendix heading case, new page |
| LaTeX | the paper's `head` against the template: class, margins, body and abstract stretch; the built PDF's body font |
| Both PDFs | keywords on page 1; page 2 opens with a major heading |

`build.py` prints the result (`venue template, word: ✅ follows it` or each `❌` row) and keeps it as `venue_template` in the manifest. To run it alone, from the SPACE root (it edits nothing, so a read-only audit may use it):

```bash
.venv/bin/python <this skill>/scripts/venue_template_check.py --word-template <template.docx> --docx <main_docx> --docx-pdf <main_docx as .pdf> \
  --latex-template <template.tex> --head <[source] head> --latex-pdf <main_pdf>
```

A rerun newer than the build outranks the manifest's `venue_template`, which a build only refreshes when it runs. The rows are the rules listed above, not every detail of
the template (not reference style or the keyword count): say so when you answer. Before you say a file follows the template, read this report. Numbers a Word style draws do not show in a paragraph's text, so read the
style or run the check, never the text alone.

JL 261104: "we should have the MISQ official word template, why don't we use that one?" When a venue publishes a Word template, write the manuscript
inside it: `word_template = "<path>"` in the paper's `[profile]`. The engine opens that file, removes its sample text and keeps its styles, heading numbers,
page setup and footer. Copying its settings onto a blank document missed things. Only what a template leaves as direct paragraph settings stays in
`[profile]` (their defaults keep the old output): `abstract_heading_upper`, `abstract_line_spacing`, `appendix_heading_upper`, `references_new_page`, `appendix_new_page`.
Without a template file, `heading_numbers` types the numbers.

## 🎭 Venue profiles

A profile is presentation, never claims: `venues/<name>/profile.toml` (one folder per venue, its contract in
`venues/README.md`), selected by
`[paper] venue_profile` in `paper-build.toml`; `[profile]` there may override
single keys. Flat keys drive the Word engine (`layout`, `font`, `line_numbers`,
`venue_label`, `draft_label`, `abstract_heading`, `references_heading`, …); the
`[latex]` table drives `write_master()`:

```text
[latex] key          values                    what it does in the generated master
spacing              single · onehalf · double  \setspace command
bibstyle             a .bst name (apalike)      \bibliographystyle
displays             inline · end               end = endfloat: every float on its own page after the text
appendix_newpage     true · false               \clearpage before each lettered appendix
title_page           inline · separate          separate = blind title page alone, then \clearpage
abstract_page        true · false               abstract (+ keywords) alone on its page
running_head         true · false               false = only the DRAFT word while drafting, nothing once clean
display_page         true · false               each table or figure on a page of its own ([p]), text keeps filling
display_at_first_ref true · false               each float moved after the paragraph that first \ref's it
float_page           top (default) · center     where a display sits on its own page; top = page top
abstract_new_page    true · false               the Abstract starts a page after the Key Points
title_block          maketitle · center         center = a centred title block the venue's Word layout parses
section_headings     ["Introduction", …]        a \section{..} added where a page has none
abstract_as_written  true · false               keep the page's own \section*{Abstract}, no abstract environment
supplement_float_names ["eTable", "eFigure"]    supplement floats restart as eTable 1, eFigure 1
```

Every master starts with `\XeTeXgenerateactualtext=1`, so a copied or searched character is the one the source
wrote: without it Times New Roman's shared glyph made every ";" copy as U+037E, the Greek question mark (261122).

Word-lane keys (flat `[profile]`, 0.12.0): `display_float = "top"` (default; `"inline"` keeps text order),
`display_float_max_rows = 25`, `display_float_max_inches = 5.5` (bigger displays get a page of their own),
`table_header_fill = ""` and `table_borders = "horizontal"` (defaults). On a Mac with Microsoft Word the
.docx preview PDF is drawn by Word, and Word also reports where each page ends, so every display is placed at the
top of the page after its citation with the page before it full (a frame floated to the page top is the fallback
without Word).

Shipped: `jama-internal-medicine` (Word-side layout, eTable/eFigure supplement)
and `misq` (double-spaced, blind title page, abstract page, lettered appendices
on new pages, `displays` switchable inline/end; `apalike` stands in for MISQ's
author-date style because the desk's own `.bst` is not shipped). A paper with no
profile builds as before 0.7.0.
