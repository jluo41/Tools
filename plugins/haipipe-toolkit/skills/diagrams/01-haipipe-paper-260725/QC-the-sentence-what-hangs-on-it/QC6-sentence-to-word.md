# A section, delivered as Word
state: 🔴 OPEN
owner: JL
method: translate a whole SECTION, name what Word cannot carry, and rule what happens when a coauthor edits the file

## Question
What does a whole stage page's `## Content` become in a `paper-xxx.docx`, given that Word has no `.bib`, no `\input`, and nowhere to put a why-comment? The unit is the SECTION, so heading outline, paragraph order, float placement and float numbering are in scope here exactly as on `QC5`, and Word answers every one of them differently. Three of the four things that hang on a sentence lose their mechanism in this column, and one loses its home entirely, so this is not the LaTeX column with a different file extension.

The reason to have this column at all is that a coauthor who is not a LaTeX user still has to read and mark up the paper, and the reason it is hard is that the same act makes the output editable. LaTeX delivery is safe because nobody edits a generated `.tex`; a `.docx` is handed to a person precisely so they will edit it. So this face carries the one ruling the whole projection model has been deferring: what happens to the paper when the change comes back in the output rather than in the source.

## Boundary
- ✅ Covered here
  What a citation, a value, a table, a figure, a heading, a lane and a why-comment become in a `.docx`; what tool performs it; and the ruling on an edit that comes back in the output.
- ↪ Covered elsewhere
  The LaTeX column is `QC5`. Which file is the paper is `QB2d`. The general one-source-many-projections model is `QD7` and the adapter contract is `QD4`. What each thing that hangs on a sentence MEANS is `QC1` to `QC4`.

## Diagram
```
 QC IS A MATRIX (JL 260726). QC1-QC4 are ROWS, what hangs on a
 sentence. QC5 and QC6 are COLUMNS, where it is delivered.

                    │ QC5 ──▶ LaTeX          │ QC6 ──▶ Word
   ─────────────────┼────────────────────────┼─────────────────────────
   QC1 citation     │ \citep{key} + .bib     │ ⚠️ no .bib. a field, or
                    │ + .bst does the rest   │    baked text somebody
                    │                        │    must then maintain
   QC2 value        │ the number, inline     │ the number, inline  ✅ same
   QC3 table        │ \input{displays/<u>/   │ ⚠️ must EMBED the rendered
                    │ float.tex} + \ref      │    table. No \input exists.
   QC4 figure       │ \includegraphics in    │ ⚠️ must EMBED the image, and
                    │ the unit's float       │    invent its own numbering
   ─────────────────┼────────────────────────┼─────────────────────────
   ### §6.1         │ \subsection            │ a Heading style
   > lanes          │ DROPPED                │ DROPPED             ✅ same
   %% {CC-*}:       │ survives as a comment  │ 🔴 NOWHERE TO PUT IT

 ONE ✅, THREE ⚠️, ONE 🔴. THAT RATIO IS THE PAGE.

 AND THE SECTION-ONLY ROWS, WHICH THE MATRIX ABOVE CANNOT SHOW
   heading hierarchy   a Heading style, and the styles ARE the outline
   paragraph order     preserved, free
   float PLACEMENT     Word has no float. A table or a figure sits
                       exactly where it is put, so "near its first
                       mention" stops being the compiler's job and
                       becomes the exporter's
   float NUMBERING     LaTeX numbers by order of appearance across the
                       document. Word does it with a field, or not at
                       all, and "Table 3" becomes a literal string that
                       is wrong the moment anything is reordered
   the bibliography    document-level in both, and in Word it has no
                       engine at all: see the citation row above

 ⚠️ THE CITATION LOSES ITS ENGINE
   \citep{key} works because the .bib holds the entry and the .bst
   formats it. Word has neither. Two answers and they are not close:
     A  a Word citation FIELD, backed by a source library
        live, re-formattable, and it needs the library to travel
     B  BAKED TEXT, formatted once at export
        travels anywhere, and is now a SECOND copy of the
        bibliography that somebody has to keep true
   B is the one that quietly rots. A is the one that breaks on
   a coauthor's machine.

 ⚠️ THE DISPLAYS LOSE \input
   A table cannot be referenced, it must be PRESENT. So the unit
   needs a Word-embeddable rendering, and `displays/<u>/assets/`
   holds table-body.tex and figure.pdf, neither of which is one.
   A picture of a table is the cheap answer and it is the wrong
   one: the coauthor you made this file for cannot fix a typo in
   a picture.
   And \ref has no equivalent unless numbering is generated, so
   "Table 3" becomes a literal string that goes stale on reorder.

 🔴 THE WHY-COMMENT HAS NOWHERE TO GO
   %% {CC-place}: … is how REVISE explains what it changed and why.
   In LaTeX it survives as a comment nobody has to read. In a .docx
   there is no equivalent that is both invisible to a reader and
   attached to the sentence. Three candidates, all with a cost:
     Word review comments   visible, and they look like coauthor
                            comments, which is exactly wrong
     drop them              the reader is fine, the RECORD is lost
     a trailing note block  survives, detached from its sentence,
                            which is the failure QC0 calls out

 ⚠️ AND THE EDGE THE WHOLE MODEL HAS BEEN DEFERRING
   ┌──────────────────────────────────────────────────────────┐
   │ safe   while conversion stays ONE-WAY                    │
   │ ⚠️     the moment a coauthor edits the .docx and sends   │
   │        it back, which is the ONLY reason it was made     │
   └──────────────────────────────────────────────────────────┘
     A  backport the change into the S page
     B  declare the manuscript has CROSSED into a new
        authoritative mode; the S page is no longer the paper
   silence is the one option that is certainly wrong.
```

## Content
### What Word actually costs, row by row
```
 QC2 value        the number, inline                              ✅ free
 heading          ### §6.1  →  a Heading style                    ✅ free
 > lanes          dropped, same as LaTeX                          ✅ free
 QC1 citation     the .bib and .bst are gone                      ⚠️ ruling
 QC3 table        must be embedded, not referenced                ⚠️ ruling
 QC4 figure       embedded, and numbered by something new         ⚠️ ruling
 %% {CC-*}:       no home that is both invisible and attached     🔴 ruling
 the edit         it comes back in the output, by design          ⚠️ ruling
```
One row of eight is free. That is the honest reason this is a face and not a paragraph on `QC5`.

### Why this column exists at all
A `.docx` is not a delivery format the venue wants. MISQ takes LaTeX. The `.docx` exists for one reason: a coauthor or advisor who does not use LaTeX has to read the paper and mark it up.

That single purpose decides most of the rulings above. If the file is for reading and marking up, then a picture of a table is wrong because they cannot fix a typo in it, baked citation text is tolerable because they are not going to re-run the bibliography, and Word review comments must be left EMPTY on export, because that is the channel their own comments will arrive in.

### The ruling this face owes the rest of the board
`QD7` has carried "rule external edits" as an open item since it opened, and `QB2d` carries the same thing worded differently. Neither can close it, because the edit is not hypothetical in the abstract: it is what happens when you hand someone a Word file. So the ruling belongs where the Word file is made, which is here.

Two answers, and the reason to pick rather than defer is that the failure mode of silence is total: the S page and the `.docx` both look like the paper, and the person editing either one cannot tell which is being reviewed.

## Items to Finish
- [ ] 📚 Rule the citation carrier: a Word field, or baked text
      A field is live and needs its source library to travel. Baked text travels and becomes a second bibliography to keep true. Pick one and say what happens on the other machine.
- [ ] 🧾 Rule what a Display becomes
      A table must be embedded and must stay editable, so `displays/<unit>/assets/` needs a Word-embeddable rendering that today does not exist there. A figure must be embedded and numbered by something, since `\ref` has no counterpart.
- [ ] 🔴 Rule where a why-comment goes, or that it is dropped
      `%% {CC-*}:` has no home in a `.docx` that is both invisible to a reader and attached to its sentence. Word review comments are the wrong channel because that is where the coauthor's own comments will arrive.
- [ ] 🔁 Rule the external edit, and stop deferring it
      A coauthor edits the `.docx` and sends it back. Backport into the S page, or declare the manuscript has crossed into a new authoritative mode. Silence is the only certainly wrong answer.
      Inherited from `QB2d` and `QD7`, which both carried it and neither could close it.
- [ ] 🔧 Name the tool that performs it
      Pandoc from a generated intermediate, a `python-docx` writer, or an export out of the LaTeX. Each decides the three rulings above differently, so this is not an implementation detail to settle last.
- [ ] 🧪 Export one real section and give it to a human
      The acceptance test for this column is not a diff, it is whether a coauthor can read it and mark it up without asking what anything means.

## Where we are
Nothing is built and nothing is ruled. No `.docx` has ever been produced from a stage page in this family.

What exists is the input: a stage page's Content is already structured enough to convert, and the board already resolves every citation, value and Display in it. What is missing is every decision above, and one of them, the external edit, has been open on two other faces since they were written.

## Files
- `0-lifecycle/4-main/S-Main-*.md`
  The pages this column reads.
- `displays/<unit>/assets/`
  Holds `table-body.tex` and `figure.pdf` today. Neither is Word-embeddable, which is one of the rulings above.
- `QD4-format-adapters.md`
  The adapter contract this column would be an instance of.

## Log
- 260726 · JL: "remove the icons, just keep different colors", then "only the box fill color to be of opacity, how about you make the font color to be 100% solid". Both done in `board.css`. Every chip carried a kind emoji in `::before` and a state glyph in `::after`, so `QC0`'s eleven-chip paragraph carried twenty-two decorations before a word of prose; both are gone and colour alone says the state. The first attempt at the fade used `opacity` on the whole chip, which dimmed the TEXT as well, and that was the wrong axis: the text is the content and the box is the decoration, so only the box gives ground. Now the fill sits at 6%, the border at 14% and the text at 100%, and hover deepens the fill without ever touching the text. `broken` and `unowned` keep a heavier box on purpose, because a defect that sinks into the prose is a defect nobody acts on. The glyph was the third copy of the state anyway: the `title=` names it in words and the panel repeats it in its header.
- 260726 · JL: "for the display, could we also make the float.tex's pdf to be embedded in the popped out window as well?" Yes, and the file to embed turned out to be `preview.pdf` rather than `assets/figure.pdf`: it is `float.tex` COMPILED STANDALONE, so it carries the caption, the notes and the numbering set by the paper's own class, which `assets/` never does. It leads the panel on the same terms as a citation's `.bbl`: show the thing as the manuscript will set it. All 10 MISQ units already had one. A preview older than the asset it previews is labelled rather than hidden.
- 260726 · Opened on JL's ruling, with `QC5`. The matrix is the argument: `QC1`-`QC4` are ROWS, what hangs on a sentence, and these two are COLUMNS, where it is delivered. One row of eight crosses into Word unchanged, three need a ruling and one has nowhere to go at all, which is what a single shared "projections" face could never have shown. The external-edit ruling moved here from `QB2d` and `QD7`, where it had been open on both and closable on neither.
