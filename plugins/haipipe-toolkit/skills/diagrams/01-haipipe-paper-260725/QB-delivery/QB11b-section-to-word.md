# A section, delivered as Word
state: 🟡 PARTIAL · exporter ships as haipipe-paper-to-word 0.1.0; the coauthor test is open in Items
owner: JL
method: carry the apparatus in ANCHORED WORD COMMENTS, and let the comment author field separate machine provenance from a coauthor's markup

## Opening
What does a whole stage page's `## Content` become in a `paper-xxx.docx`, given that Word has no `.bib`, no `\input`, and nowhere to put a why-comment?
The unit is the SECTION, so heading outline, paragraph order, float placement and float numbering are in scope here exactly as on `QB11a`, and Word answers every one of them differently. Three of the four things that hang on a sentence lose their mechanism in this column, and one loses its home entirely, so this is not the LaTeX column with a different file extension.

The reason to have this column at all is that a coauthor who is not a LaTeX user still has to read and mark up the paper, and the reason it is hard is that the same act makes the output editable. LaTeX delivery is safe because nobody edits a generated `.tex`; a `.docx` is handed to a person precisely so they will edit it. So this face carries the one ruling the whole projection model has been deferring: what happens to the paper when the change comes back in the output rather than in the source.

Scope: This page covers What a citation, a value, a table, a figure, a heading, a lane and a why-comment become in a `.docx`; what tool performs it; and the ruling on an edit that comes back in the output. Neighbouring pages cover The LaTeX column is `QB11a`. Which file is the paper is `QC3d`. The general one-source-many-projections model is `QD7` and the archived adapter contract is `QB11c-format-adapters`. What each thing that hangs on a sentence MEANS is `QB12a` to `QB12d`.

## Diagram
```
 QC IS A MATRIX (JL 260726). QB12a-QB12d are ROWS, what hangs on a
 sentence. QB11a and QB11b are COLUMNS, where it is delivered.

                    │ QB11a ──▶ LaTeX          │ QB11b ──▶ Word
   ─────────────────┼────────────────────────┼─────────────────────────
   QB12a citation     │ \citep{key} + .bib     │ author-year BAKED from
                    │ + .bst does the rest   │ .board-refs.bbl, + the key
                    │                        │ in an anchored comment
   QB12b value        │ the number, inline     │ the number, inline  ✅ same
   QB12c table        │ \input{displays/<u>/   │ a real w:tbl parsed from
                    │ float.tex} + \ref      │ assets/table-body.tex
   QB12d figure       │ \includegraphics in    │ assets/figure.png embedded,
                    │ the unit's float       │ numbered by appearance order
   ─────────────────┼────────────────────────┼─────────────────────────
   ### §6.1         │ \subsection            │ a Heading style
   > lanes          │ DROPPED                │ ANCHORED COMMENT ◄ WORD WINS
   %% {CC-*}:       │ survives as a comment  │ ANCHORED COMMENT ◄ WORD WINS

 THE RATIO INVERTED ON 260727, AND JL'S QUESTION IS WHY
 The old reading of this table was one ✅, three ⚠️ and one 🔴, which made
 Word "the lossy column". Put the apparatus in ANCHORED WORD COMMENTS and
 two rows flip the other way: a `> Value:` lane is DROPPED by QB11a and
 SURVIVES here, bound to the exact number rather than to the sentence.
 So Word carries MORE provenance than the venue's own format, and this
 face stops being an apology for a downgrade.

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

 ✅ THE WHY-COMMENT HAS A HOME, AND IT IS THE NATIVE ONE
   %% {CC-place}: … is how REVISE explains what it changed and why.
   The old reading rejected Word review comments because "they look
   like coauthor comments, which is exactly wrong". That objection
   dissolves on one OOXML field:

     <w:comment w:id="2" w:author="haipipe" w:initials="hp">

   Every comment carries an AUTHOR. Word's review pane already filters
   by it. So the two streams share one mechanism and stay separable,
   and what looked like a collision is a namespace.

 ✅ AND THAT FIELD SETTLES THE EDGE THE MODEL HAS BEEN DEFERRING
   ┌──────────────────────────────────────────────────────────┐
   │ export writes    w:author="haipipe"   machine provenance │
   │ coauthor writes  w:author="<person>"  human input        │
   │ ⇒ backport PARTITIONS on the author field:               │
   │     haipipe   ignore, the S page already knows it        │
   │     anything else   route into the S page                │
   └──────────────────────────────────────────────────────────┘
     A  backport the change into the S page          ◄ takeable NOW
     B  declare the manuscript has CROSSED into a new
        authoritative mode; the S page is no longer the paper
   A was unpickable while "which comments are ours" had no answer.
   It has one, so silence is no longer the only wrong option: B is.

 🧪 PROVEN 260727, 1987 BYTES, ZERO DEPENDENCIES
   A .docx is a zip of XML and a comment is plain OOXML:
     word/comments.xml            the comment bodies + author
     word/_rels/document.xml.rels the .../comments relationship
     commentRangeStart/End        wraps ARBITRARY runs, so the anchor
     + commentReference           can be ONE NUMBER inside a sentence
   Built with stdlib zipfile alone; macOS textutil, a Word-family
   reader, parses it and extracts the prose.
   ⚠️ AND THIS RULES OUT THE OBVIOUS TOOL. pandoc cannot WRITE Word
   comments at all. The carrier decision therefore had to come BEFORE
   the tool, which is what this page's own tool item already said.
```

## Content
### What Word actually costs, row by row
Re-scored 260727, after JL asked whether the citations and the values could be carried as comments. Six of eight rows now have an answer that needs no new engine, because each one resolves against a file the family already generates.

```
 QB12b value        the number, inline                              ✅ free
 heading          ### §6.1  →  a Heading style                    ✅ free
 %% {CC-*}:       an anchored comment, w:author="haipipe"         ✅ SOLVED
 > lanes          the same, anchored to the NUMBER not the ¶      ✅ SOLVED
                  (QB11a drops these; this column keeps them)
 the edit         partition returning comments by author          ✅ SOLVED
 QB12a citation     baked author-year out of .board-refs.bbl,       ⚠️ ruling
                  which refs.py ALREADY generates with the
                  paper's own .bst; the key rides in a comment
 QB12c table        a real w:tbl parsed from the unit's             ⚠️ ruling
                  assets/table-body.tex, so it stays EDITABLE
 QB12d figure       assets/figure.png embedded; numbering is        ⚠️ ruling
                  order-of-appearance, which the exporter
                  computes because it walks sections in order
```
The three remaining rulings are about FIDELITY, not feasibility: each has a working answer above and what is open is whether that answer is good enough to hand a coauthor.

### The citation ruling dissolves rather than resolves
This face framed it as a choice between a live Word field, which needs its source library to travel, and baked text, which becomes a second bibliography somebody must keep true. Both costs are real and neither applies here, because the baked text is not authored.

`refs.py` already synthesizes an `.aux` citing every key the board uses, runs `bibtex` with the paper's own `.bst`, and caches `.board-refs.bbl`. It exists on the MISQ paper today at 62 KB. That is a formatted bibliography, in the manuscript's own style, generated from the one real `.bib`.

So the Word export parses that file rather than formatting anything. There is no second bibliography to keep true because nobody writes one: it is regenerated on every export from the same source the LaTeX column compiles. The dilemma was between two ways of MAINTAINING a copy, and the answer is not to maintain one.

### What a reader sees, and what a checker sees, in the same file
```
 THE COAUTHOR READS               THE RECORD KEEPS
 ─────────────────────────────    ──────────────────────────────────
 normal prose, no markup          every sentence unchanged
 (Thielmann and Hilbig 2020)  💬  key=thielmann2020personality
                                  Personality-Opioid-MISQ2026.bib:412
 +0.0009                      💬  is_high_mme_daily · run=v0618
                                  probe=1-probes/PP03…/QX5_…md
                                  state=verified
 a real, editable table       💬  display05 · target=S-Display-5
 Figure 2                     💬  display02 · candidate-C · promoted=no
```
Two audiences, one file, and the second one is invisible until a bubble is opened. That is the property `QB11a` cannot offer: in LaTeX the apparatus is dropped at generate time, so a reviewer never sees it and neither does anyone else.

### Why this column exists at all
A `.docx` is not a delivery format the venue wants. MISQ takes LaTeX. The `.docx` exists for one reason: a coauthor or advisor who does not use LaTeX has to read the paper and mark it up.

That single purpose decides most of the rulings above. If the file is for reading and marking up, then a picture of a table is wrong because they cannot fix a typo in it, baked citation text is tolerable because they are not going to re-run the bibliography, and Word review comments must be left EMPTY on export, because that is the channel their own comments will arrive in.

### The ruling this face owes the rest of the board
The retired `QD7` carried "rule external edits" as an open item from the day it opened, and `QC3d` carries the same thing worded differently. Neither can close it, because the edit is not hypothetical in the abstract: it is what happens when you hand someone a Word file. So the ruling belongs where the Word file is made, which is here.

Two answers, and the reason to pick rather than defer is that the failure mode of silence is total: the S page and the `.docx` both look like the paper, and the person editing either one cannot tell which is being reviewed.

## Aims
- [x] 🔴 Rule where a why-comment goes, or that it is dropped
      Ruled 260727 on JL's question: an ANCHORED WORD COMMENT, `w:author="haipipe"`. The old objection was that review comments "look like coauthor comments, which is exactly wrong"; the author field is what makes that a namespace rather than a collision, and Word's review pane already filters on it. The same carrier takes the `> Value:`, `> Citation:` and `> Display:` lanes, which `QB11a` drops.
- [x] 🔧 Name the tool that performs it
      Ruled 260727: stdlib `zipfile` writing OOXML directly. NOT pandoc, and the reason is the ruling above rather than taste: pandoc cannot write Word comments at all, so the tool that looked obvious cannot carry this column's central feature. `python-docx` is absent on this machine and would add a dependency for something the standard library does in a page.
      Proven the same day at 1987 bytes, two comments anchored, one on a citation and one on a single number inside a sentence; macOS `textutil` parses the package and extracts the prose.
- [x] 🔁 Rule the external edit, and stop deferring it
      Ruled 260727: BACKPORT, and the `.docx` never becomes authoritative. This was unpickable while "which comments are ours" had no answer. It has one now: the export writes `w:author="haipipe"`, a coauthor writes their own, so backport partitions on the author field and routes only the human half into the S page.
      Inherited from `QC3d` and the retired `QD7`, which both carried it and neither could close it. Both should now point here rather than restating it.
- [x] 📚 Confirm the citation carrier: baked out of `.board-refs.bbl`
      Confirmed 260727, and the in-text form needed no deriving because the `.bbl` already carries it. natbib writes `\bibitem[{SHORT(YEAR)FULL}]{key}`, packing both forms into one bracket: `\bibitem[{Wang et~al.(2022)Wang, Luo, Dugas, Gao, Agarwal, and Werner}]{key}`. Taking the part up to the year gives `(Wang et al. 2022)`, set by the paper's own `.bst`.
      Taking the WHOLE bracket was the first bug the exporter shipped, and it printed `(Wang et al.(2022)Wang, Luo, Dugas, Gao, Agarwal, and Werner)` into the prose. Worth keeping because it is the failure mode of treating a `.bbl` label as one string rather than two forms.
      So the dilemma dissolved rather than resolved: the baked text is authored by nobody, and there is no second bibliography to keep true.
- [x] 🧾 Confirm what a Display becomes
      Confirmed 260727 by parsing all six MISQ table units rather than arguing: 108 rows total, zero TeX leakage, `maxcols` 3 to 6. `\multirow`, the one construct that would have needed a vertical merge, appears in NONE of them; what does appear is booktabs rules, `\multicolumn` and `\textbf`, and all three map onto `w:tbl` directly. A figure embeds `assets/figure.png`, which exists on all four figure units. Numbering is order-of-appearance, owned by the exporter because Word has no float and no `\ref`.
- [x] 🔧 An unresolved marker WARNS here and BLOCKS in LaTeX
      Not one ruling for both columns, which is how it was framed. The audiences differ: a reviewer must never see `[?]` in a results sentence, and a coauthor must see exactly where the paper stands, so a hidden hole is worse than a visible one. The export emits the marker, reports it, and continues. `QB11a` should rule its own half the other way.
- [x] 📏 The citation comment is the REFERENCE and the KEY, and nothing else (JL 260727)
      The generated half and the hand-written half were merged on the key first, on the reasoning that neither is droppable. JL, reading the result: "Too long, I think we only need: Citation: <the reference> key=<the key>". One merged comment ran to 605 characters for a reference of 240.
      Ruled: the GENERATED half goes to Word, the hand-written `> Citation:` lane stays on the board. The reference plus the key is what a coauthor checks. The `.bib` line number, where the key sits in the tex, the hit count and a de-duplication history are all true and all useful, and none of them is evidence FOR THE SENTENCE, so they belong with `Note` and `Check`.
      Measured: 224 comments to 203, citation comments 127 to 106, median 262 characters. 27 hand-written Citation lanes now print in the "working lanes NOT exported" line rather than in the margin.
      The general form: a lane's evidence value and its WORKING value are different things, and Word gets only the first. The board is where a lane's history lives, because the board is where the work happens.
- [x] 🧿 Only an EVIDENCE lane becomes a comment, and there are exactly three (JL 260727)
      JL: "for the sentences, we might have multiple comments, don't render them to the word, only the evidence card." The exporter had five lanes in `EVIDENCE_LANES`, and two of them are not evidence. The board's own definition is three, at `haipipe-board/src/body.py:288`: `> Citation:`, `> Value:`, `> Display:`. Each answers "what backs this sentence" and resolves against a file, the `.bib`, a run, or a display unit.
      A `> Note:` is a PENDING candidate edit, so it is a review artifact about prose nobody has accepted. A `> Check:` is a gate REPORT about the whole section. Neither backs the sentence, and neither belongs in a file handed to a coauthor: it hands them our unresolved internal queue and asks them to tell it apart from the evidence.
      Measured on `S-Main-all.docx`: 260 comments became 228, all three kinds only, Citation 131 · Value 65 · Display 32, with Note 0 and Check 0. The 25 Notes and 7 Checks stay on the board and are COUNTED on the way out, printed as "working lanes NOT exported", because a silent drop of a review queue is how a queue gets forgotten.
      This also supersedes the compaction rule above for Notes specifically: a Note no longer reaches Word at all, so there is nothing left to compact there. The compaction code stays, because the board may add an evidence lane that carries a diff, and the rule it encodes is the one below.
- [x] ✂️ A comment carries the CHANGE, never a restatement of the sentence (JL 260727)
      JL, reading the export in Word: "Now every sentences get the citaiton, I don't want it. Just add the comments for the evidence card, don't add the whole sentences." A `> Note:` lane holds a COMPLETE candidate sentence with `~~removed~~ **inserted**` inside it, and that is right on the Board, where the original sits directly above it and the eye compares the two. In Word the sentence is already in the body, so restating it put a whole paragraph in the margin and buried the one or two words that actually changed.
      Ruled: a Note is reduced to its EDITS. `across → from`, `, predicting → that predict`, `in prescribing → (removed)`. Measured on the 25 Note comments in `S-Main-all.docx`: each is now a phrase rather than a sentence. Value and Display lanes are untouched, because neither restates anything; a Value lane IS the evidence card.
      The general form of the rule, which this face should have had from the start: the Board and Word have opposite defaults. On the Board the apparatus sits BESIDE the prose and may repeat it, because repetition is how a reader diffs. In Word the apparatus sits in the MARGIN and may not, because the margin is narrow and the prose is already on the page.
- [ ] 🧪 Export one real section and give it to a human
      Built and run 260727; the human half is what remains. `S-Main-4-measurement` exported at 70 paragraphs, 19 anchored comments, 2 embedded editable tables, 1 embedded figure and 12 references. `S-Main-6-results` exported at 50 paragraphs and 38 anchored comments, the densest apparatus in `4-main`.
      The acceptance test is not a diff, it is whether a coauthor can read it and mark it up without asking what anything means. That has not happened yet.
- [x] 🔍 Opened in Microsoft Word (JL 260727)
      JL opened `S-Main-all.docx` in real Word and read it. Comments render anchored in the review pane with the author shown, tables render as editable Word tables, and the reference text renders inside the citation comments. What `textutil` could only prove about the PACKAGE is now confirmed about the RENDERING.
      It also cost four defects, which is the point of the item: a fenced ASCII sketch shipped as prose, a two-reference comment ran its entries together with no break, `$\times$` printed as `$$`, and a Note comment restated its whole sentence. None of these were visible from a well-formed package.
      `textutil` parses the package and extracts the prose and the table cells, and the package check confirms every `commentReference` has a matching definition, range start and range end. That shows the OOXML is valid and a Word-family reader accepts it. It does not show that Word renders the bubbles, and until it does the claim stops there.
- [ ] 🚨 Eight of the nine `4-main` pages reference NO display in their prose
      Measured 260727 while exporting, and it is the same defect `QB11a` found for citations on `S-Main-1`, one row down. Only `S-Main-4` carries a `\ref{}` in prose at all, and it carries three. Every other display pointer in the Main lifecycle lives in a `> Display:` lane, which both columns drop, so an export or a sync of any of those eight pages produces prose that points at no table and no figure.
      The board reads GREEN on this, which is why it survived: those 36 table and 18 figure chips resolve markers sitting in APPARATUS. `S-Main-6` is the clean demonstration, because its prose carries `Table [main-results]`, a placeholder naming no unit, while its lanes carry the real `\ref{tab:results}`.
      This is page work in `4-main`, not exporter work. Fixing it at export time would hide a defect the LaTeX column has too.
- [ ] 📐 Reconcile the two other copies of the matrix
      The row-by-column table in this page's Diagram is duplicated in `QB11a`'s Diagram and in `board.md`'s `QC` group intro. Two cells changed here on 260727 and those copies still read `> lanes DROPPED` and `%% {CC-*}: 🔴 NOWHERE TO PUT IT`. Three copies of one table is the drift `QC5` was split apart to stop.

## States
Every ruling on this face is closed and the exporter exists and runs. It ships as
`haipipe-paper-to-word` 0.1.0 in the paper skill set's `3-deliver/4-ship/`, beside `to-overleaf`, because both move the argument to a target that is not the repo.

```
 RUN 260727, on real pages, not a fixture
 S-Main-4-measurement   70 ¶ · 19 anchored comments · 2 tables · 1 figure · 12 refs
 S-Main-6-results       50 ¶ · 38 anchored comments · 0 displays · 1 ref
 package check on both  every commentReference id has a matching definition,
                        a matching range start, and a matching range end
 six table units        108 rows parsed, zero TeX leakage
```

The export FORMATS nothing. The in-text label and the reference entry come out of `.board-refs.bbl`, written by `refs.py` with the paper's own `.bst`; the Display kind and `\label` come out of the unit's own `float.tex`; a table comes out of `assets/table-body.tex` and a figure out of `assets/figure.png`. That is why there is no second bibliography to keep true: nobody authors the baked text.

Two defects were found by running it rather than by reading it, and both are recorded in the skill's CHANGELOG: the `.bbl` label was printed whole, and an overlapping comment anchor emitted a range end with no matching start. The second one was caught by the package check, which is the argument for having one.

⚠️ Two limits, stated because the artifact reads stronger than the evidence. Nobody has opened the output in Microsoft Word, so the claim is "valid OOXML that a Word-family reader parses", not "Word renders the bubbles". And no coauthor has read one, which is this column's actual acceptance test.

The run also found something that is not about Word at all: eight of the nine `4-main` pages reference no display in their PROSE, so both columns would deliver sections pointing at no table and no figure. It is in Items to Finish above, and it belongs to those pages.

## Files
**The skill this face ships.** A rule made here is a rule it must follow, and its `SKILL.md` cites this face by id so the pair is greppable in both directions.

- `haipipe-paper-to-word`
  `3-deliver/4-ship/haipipe-paper-to-word/`, version 0.1.0. `md2docx.py` is the whole exporter; `SKILL.md` carries the read-and-drop contract and the author-field law; `CHANGELOG.md` records the two defects the first runs found.

**What it reads, and formats none of**
- `0-lifecycle/4-main/S-Main-*.md`
  The pages this column reads.
- `.board-refs.bbl`
  The in-text label AND the reference entry, generated by `haipipe-board/refs.py` with the paper's own `.bst`. The `\bibitem[{…}]` bracket packs `SHORT(YEAR)FULL`; only the part up to the year is the in-text call.
- `displays/<unit>/float.tex`
  The `\label` and the unit's kind. Never guessed from the label prefix, per `QB12c`.
- `displays/<unit>/assets/`
  `table-body.tex` parses into a real `w:tbl`, so a table stays editable; `figure.png` embeds. Both were measured present on all ten units.
- `QB11c-format-adapters.md`
  The adapter contract this column is an instance of.

## Log
- 260727 · Built it, and running it settled the two rulings that reading could not. The in-text citation form needed no deriving: natbib packs `SHORT(YEAR)FULL` into the one `\bibitem[{…}]` bracket, so the label already IS the in-text call. The table question was answered by parsing all six MISQ units instead of arguing about `\multicolumn`: 108 rows, zero TeX leakage, and `\multirow`, the only construct that would have needed a vertical merge, is in none of them. A third ruling appeared that had been mis-framed as one: an unresolved marker must WARN here and BLOCK in LaTeX, because a reviewer must not see a hole and a coauthor must. Two defects came out of the runs, both worth keeping: the `.bbl` label printed whole as `(Wang et al.(2022)Wang, Luo, …)`, and an overlapping comment anchor emitted a range end with no matching start, caught by the package check rather than by reading. Ships as `haipipe-paper-to-word` 0.1.0. What is left is human: nobody has opened the file in Word, and no coauthor has read one.
- 260727 · The export also found something that is not about Word. Eight of the nine `4-main` pages reference NO display in their prose; only `S-Main-4` carries a `\ref{}` there at all. `S-Main-6` says `Table [main-results]`, a placeholder naming no unit, while its real `\ref{tab:results}` sits in a `> Display:` lane that both columns drop. This is the same defect `QB11a` found for citations on `S-Main-1`, one row down, and the board reads green on it because those chips resolve markers sitting in apparatus.
- 260727 · JL: "Could we generate the work with citaitons and the values as the comments? Do you know whther it is doable?" Yes, and the question closed three of this face's items rather than one. The 🔴 had no home for `%% {CC-*}:` because review comments "look like coauthor comments"; the `w:author` field makes that a namespace, and the same field is what finally made the external-edit ruling takeable, since backport can partition returning comments into ours and theirs. It also reversed the page's own framing: `> Value:` lanes are DROPPED by `QB11a` and SURVIVE here, anchored to the exact number, so Word carries more provenance than the venue's format and this column is not the lossy one. Proven with stdlib `zipfile` at 1987 bytes rather than argued; `textutil` parses it. The tool ruling fell out of the carrier ruling and went against the obvious choice: pandoc cannot write Word comments at all. Not yet opened in Word itself, which is the one thing the proof does not show.
- 260726 · JL: "remove the icons, just keep different colors", then "only the box fill color to be of opacity, how about you make the font color to be 100% solid". Both done in `board.css`. Every chip carried a kind emoji in `::before` and a state glyph in `::after`, so `QC5`'s eleven-chip paragraph carried twenty-two decorations before a word of prose; both are gone and colour alone says the state. The first attempt at the fade used `opacity` on the whole chip, which dimmed the TEXT as well, and that was the wrong axis: the text is the content and the box is the decoration, so only the box gives ground. Now the fill sits at 6%, the border at 14% and the text at 100%, and hover deepens the fill without ever touching the text. `broken` and `unowned` keep a heavier box on purpose, because a defect that sinks into the prose is a defect nobody acts on. The glyph was the third copy of the state anyway: the `title=` names it in words and the panel repeats it in its header.
- 260726 · JL: "for the display, could we also make the float.tex's pdf to be embedded in the popped out window as well?" Yes, and the file to embed turned out to be `preview.pdf` rather than `assets/figure.pdf`: it is `float.tex` COMPILED STANDALONE, so it carries the caption, the notes and the numbering set by the paper's own class, which `assets/` never does. It leads the panel on the same terms as a citation's `.bbl`: show the thing as the manuscript will set it. All 10 MISQ units already had one. A preview older than the asset it previews is labelled rather than hidden.
- 260726 · Opened on JL's ruling, with `QB11a`. The matrix is the argument: `QB12a`-`QB12d` are ROWS, what hangs on a sentence, and these two are COLUMNS, where it is delivered. One row of eight crosses into Word unchanged, three need a ruling and one has nowhere to go at all, which is what a single shared "projections" face could never have shown. The external-edit ruling moved here from `QC3d` and `QD7`, where it had been open on both and closable on neither.

260727 · Opened in real Word by JL, and the four defects that surfaced were all invisible to the package check. A fenced ``` block in `S-Main-4`'s Content shipped as prose, so an ASCII bar chart with its own fence marks landed in the manuscript; fences are now skipped AND counted, because the sketch is usually a display unit nobody built and a silent drop would read as a missing table. A two-reference comment ran its entries together, because `comment()` built its own `<w:t>` and never went through `run()`, where the `<w:br/>` fix lived. `$\times$` lost its command to the catch-all strip and printed `person$$ situation`. And a Note comment restated its entire sentence in the margin.
260727 · The last of those produced the rule this face should have opened with: the Board and Word have OPPOSITE defaults for apparatus. On the Board the apparatus sits beside the prose and may repeat it, because repetition is how a reader diffs a candidate against the original. In Word the apparatus sits in a narrow margin while the prose is already on the page, so repeating it buries the change. Same lane, same content, different projection, and `QB9a` needs neither rule because it drops the lanes entirely.

260727 · Two rulings in one session, and the second narrowed the first. The comment body was compacted so a Note carried `across → from` rather than its whole sentence; JL then ruled that a Note has no business in the Word file at all, because only an evidence lane is an evidence card. The lane set is now the board's own three rather than a list this skill invented, which is the correct relationship: `QB9b` rules how a lane PROJECTS into Word and does not get to decide what counts as evidence. That belongs upstream, and taking it from `body.py` means the two cannot drift.

260727 · Four rounds on one question, each narrowing the last, and worth keeping in order because the end state does not explain itself. A comment carried the whole candidate sentence; compacted to its edits. Then Note and Check were found not to be evidence at all and stopped being exported. Then a citation produced TWO comments, generated and hand-written, and they were merged on the key. Then the merge was too long, and the ruling settled where it should have started: the citation comment is the reference and the key. Everything a person wrote ABOUT that citation stays on the board.
260727 · The anchoring bug behind all of it was separate and worse, because it was invisible in the markdown. Joining sentences into real paragraphs made "no number found, highlight the whole thing" mean the whole PARAGRAPH rather than the whole SENTENCE, so one Value lane highlighted all eleven sentences of the abstract. Three causes stacked: the paragraph fallback, then two lanes sharing a sentence window being treated as an overlap and demoted, then a number NESTED in its own sentence window being demoted the same way. 69 paragraph-sized ranges, then 19, then 2, and the two that remain are single sentences that really are 483 and 660 characters long. The emitter is now an event walk, so a start and an end come from one sorted list and neither can appear without the other.
