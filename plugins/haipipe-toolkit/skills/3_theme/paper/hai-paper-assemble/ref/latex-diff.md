The LaTeX diff between two rounds, and its margin notes (scripts/latex_diff.py, hai-paper-assemble).

## 🔍 What changed since the last round · the LaTeX diff (0.19.0)

JL 261113: "could you have the latex version of diff? I think we have some latex_diff command". A co-author reads the
change since the round they saw in the venue's own LaTeX layout: deleted words struck through in red, added words
underlined in blue. `scripts/latex_diff.py` takes two LaTeX rooms (master.tex, sections/, appendices/, displays/,
reference.bib) and writes one PDF.

```text
run    from the SPACE root: .venv/bin/python Tools/plugins/haipipe-toolkit/skills/3_theme/paper/
       hai-paper-assemble/scripts/latex_diff.py --old <room | git:REV:<room path>> --new <room> --out <x>-latexdiff.pdf
old    the room that was sent (a folder, or git:<rev>:<path> when delivery/ was committed at the send)
new    the room after the revision (normally this build's delivery/<job>/latex/)
room   needs master.tex (or --master <name>) and the .bib it names; sections/, appendices/, displays/ as it uses them
does   copies both to scratch, latexdiff --flatten (files inside the room are inlined and diffed),
       compiles with BibTeX; the reference list is not diffed: it holds every entry either round cites
shows  added words: blue wavy underline · deleted words: red strike-through · a deleted citation: struck, its entry
       kept in the list · figures: the new one only · equations: marked whole
not    a file outside the room (a ../ path, e.g. a shared table body) is made absolute, not inlined, so a change
       inside it is not shown; when both rooms point at one shared file, the old version cannot be shown
writes --out and its .tex beside it; never edits a room
```

Keep the room that was sent: commit `delivery/` at each send, or copy `latex/` into the round's folder, because the
next build overwrites it. The diff PDF goes to `delivery/<writing Job>/latex-diff/<paper>-latexdiff.pdf`; the paper
workbench shows it as the item "Paper-Latex-Diff" under LaTeX, beside "Paper-Latex" (workbench-paper CONSTITUTION A01). When the revision lives somewhere other
than the Section pages (a Word round not yet adopted), a review Task builds the new room itself and runs this script
on it; the script does not care where the new room came from.

**Margin notes (0.20.0).** JL 261113: "add the comments to the margin". With `--notes notes.yaml` each change can
carry a short reason, printed in a widened right margin beside it and numbered in reading order:

```text
notes.yaml   notes: [{at: <text in the new room>, note: <why>, who?: <name>, comment?: <their words>}]
page         11 x 11 in, notes in a 2.8 in right margin (the diff is for reading, never submitted)
place        beside the first place `at` occurs, matched across latexdiff's markup, so `at` may span a change; moved out of the latexdiff block it sits in, never into a
             heading or caption (a margin note inside latexdiff's underline box does not compile)
comment      with `comment` + `who`, the note quotes the reviewer in orange, then "-> the reply"
not found    printed "latex_diff: note not placed, text not found: ..." and skipped; the diff still builds
```

Notes are for the co-author reading the change, not process text: one or two plain sentences on why. Drop a
reviewer's note once the text answers it (JL 261113: "no need to leave the comments").
