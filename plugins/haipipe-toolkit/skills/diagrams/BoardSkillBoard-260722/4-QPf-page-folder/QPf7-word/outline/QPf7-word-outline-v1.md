# QPf7-word · outline v1
outline-version: v1
supersedes: —
date: 260817
approved: ⬜            🚧 a person ticks this. No machine may.

Generated 260817 from this page's own divisions, face-figure captions and
sentences, so no bullet claims anything the page does not already say.
UNAPPROVED, so it is a working document: rewrite it, delete what is wrong.

## C1 · 🧾 Three files land in `word/`, and each one is rebuilt for you

### C1.P1 · three files, none of them written by hand, all made again on a click
- B1 · A browser has no live editor for a `.docx`, so the tab is preview and download.
- B2 · Above the twin the view prints one line, `the PDF twin below is rendered from the package itself`, with the ⬇ download link beside it.
- B3 · The prose is shaped for the reader, not for the source file.
- B4 · The board's `.md` keeps one sentence per line, because that is how a comment finds the sentence it belongs to.
- B5 · The export passes `--join-paragraphs`, so each block lands in Word as one flowing paragraph.
- B6 · A coauthor reads prose, so the one-line-per-sentence form is board machinery and stops at the export.
- B7 · The reference list prefers the PAGE'S OWN `bibex/<stem>.bib`.
- B8 · ⚠️ 6 more sentences in this division are not planned here yet

## C2 · 💬 Which comments travel into Word, and the one question still open

### C2.P1 · what a plain board page sends, and what a page that owns display units sends
- B1 · A `>` lane is a line written under a sentence, and the board uses lanes for citations, comments, and change records.
- B2 · `QPf6` §2 records md2tex dropping those lanes, but here they have somewhere to go.
- B3 · md2docx turns each one into a Word comment, pinned to the sentence it sits under.
- B4 · The writer's own default is Citation alone: the other two evidence lanes, Value and Display, travel only when a run asks for them.
- B5 · Five comments on one sentence cannot be read, and Citation is the lane a coauthor checks.
- B6 · A plain board page passes no `--lanes` flag, so it rides that default and its Citation comments still reach Word.
- B7 · A page that owns display units is exported with `--lanes Citation,Display`, so the units the export names come through too.
- B8 · ⚠️ 4 more sentences in this division are not planned here yet

## C3 · 🖼 Opening the tab builds the file when it is not there yet

### C3.P1 · the registry's `tab: {url, write}` spec, url first, then a HEAD check, then a build, with the word route behind it
- B1 · A HEAD is a small web question that asks only whether a file is there, and a miss never leaves you with a blank tab.
- B2 · Opening the tab posts the route, says it is building, and lands on the view the writer returns.
- B3 · If the writer fails, its own error prints where that view would have been.

