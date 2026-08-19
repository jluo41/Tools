# QPf6-latex · outline v1
outline-version: v1
supersedes: —
date: 260817
approved: ⬜            🚧 a person ticks this. No machine may.

Generated 260817 from this page's own divisions, face-figure captions and
sentences, so no bullet claims anything the page does not already say.
UNAPPROVED, so it is a working document: rewrite it, delete what is wrong.

## C1 · What sits in the folder, and what a rebuild overwrites

### C1.P1 · three files, all built for you, and every one can be built again
- B1 · Edit one of these files by hand and the next build overwrites it.   ✅ have it
- B2 · That is the rule for a folder the machine rebuilds, not a fault.   ✅ have it
- B3 · Nobody keeps the view page up to date by hand.   ✅ have it
- B4 · `export.py` writes it again at the end of every run, whether or not xelatex produced a PDF.   ✅ have it
- B5 · The bibliography looks first at the page's own bibex/ list (QPf8).   ✅ have it
- B6 · When `bibex/<stem>.bib` holds an entry, the PDF cites exactly what the page cites.   ✅ have it
- B7 · With no page bib, the export looks for a `0-*.bib` by walking up from the page toward the server's root folder.   🎯 A1.2
- B8 · ⚠️ 2 more sentences in this division are not planned here yet   🎯 A1.2

## C2 · What survives the trip to LaTeX, and what is lost

### C2.P1 · most of it lines up, and the losses are written down, not hidden
- B1 · The Content parts map cleanly, because a part already is a section.   ✅ have it
- B2 · `\citep{}` and `\ref{}` come through untouched, because they were LaTeX before the export started.   ✅ have it
- B3 · The `>` lanes are the one real loss.   🎯 A2.1
- B4 · The Word export lands them as comments pinned to a spot, and a LaTeX section has nowhere to put them.   ✅ have it
- B5 · The writer also refuses to go backwards: a rewrite that loses citations is refused, not written quietly.   🧮 proof
- B6 · The proof run is `QPf4b`'s Content: ten parts became a real nine-page PDF, driven in a browser through the tab.   ✅ have it
- B7 · The board's emoji-heavy ascii figures do not survive.   🔢 value · PP01
- B8 · ⚠️ 2 more sentences in this division are not planned here yet   🎯 A2.1

## C3 · The tab shows something even when the build fails

### C3.P1 · the registry's `tab: {url, write}` spec, url first, then a HEAD check, then a build, with the latex route behind it
- B1 · One view page is written either way, so the tab is never empty.   ✅ have it
- B2 · A run that works shows the PDF, with the raw source folded under it.   ✅ have it
- B3 · A run that fails opens that fold and prints the tail of the log, so the error sits where the finished page would have been.   🧮 proof

## C4 · Evidence this page already carries

### C4.P1 · Cite each where it belongs, or drop it
- B1 · Display1 is on disk and no bullet cites it yet   🖼 Display1

