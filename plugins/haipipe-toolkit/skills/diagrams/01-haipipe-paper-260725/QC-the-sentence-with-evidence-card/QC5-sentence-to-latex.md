# A section, delivered as LaTeX
state: 🔴 OPEN
owner: JL
method: translate a whole SECTION, not a sentence, so heading order, float placement and numbering are in scope

## Question
When a whole stage page's `## Content` becomes a `sections/*.tex`, what does each part become and what is allowed to be dropped? The unit here is the SECTION, not the sentence, and that is not a difference of scale: a section is a SEQUENCE, so heading nesting, paragraph order, where each float is placed and what number it ends up carrying all live here and are invisible at sentence grain.

`QC1` to `QC4` already say what one citation, one value or one Display reference becomes, and this face never repeats them. It owns what only appears once those sentences are in order, and the measurement below says that is exactly where the defects are.

This is the first of two delivery columns, and it is the easy one, which is why it goes first. LaTeX was the target the sentence grammar was designed against: `\citep{}` is already LaTeX, `\ref{}` is already LaTeX, and a `%%` comment already has somewhere to live. So the question here is not "can it be represented" but "which parts are read, which are dropped, and who performs the reading". Today nobody performs it: an agent reads the page and types the `.tex`, which is why this face exists and why its central item is that the generator does not exist.

## Boundary
- ✅ Covered here
  A whole section: heading hierarchy, paragraph order, float placement and numbering, the section's own label, the `\input` wiring to `displays/`, what is dropped, and what a generator would have to do.
- ↪ Covered elsewhere
  What one SENTENCE's citation, value or Display reference becomes is `QC1` to `QC4`; this face never re-states them. Which of the two files is the paper, and what a backward edit means, is `QB2d`. The general one-source-many-projections model is `QD7`, and the adapter contract is `QD4`. Where the generated files land on disk is `QA6` ⑦. The Word column is `QC6`. What each thing that hangs on a sentence MEANS is `QC1` to `QC4`, and the sentence unit itself is `QC0`.

## Diagram
```
 QC IS A MATRIX (JL 260726). QC1-QC4 are ROWS, what hangs on a
 sentence. QC5 and QC6 are COLUMNS, where it is delivered. Every
 cell differs, which is why one "projections" face was always
 going to be too thin.

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


 THE UNIT IS THE SECTION, NOT THE SENTENCE (JL 260726)

 QC1-QC4 translate ONE SENTENCE and everything that hangs on it.
 A column translates a SECTION, and a section is a SEQUENCE. Six
 things exist only once sentences are in order, and no row above
 can see any of them:

   heading hierarchy   ### §6.1 / #### P2  ->  \subsection nesting
   paragraph ORDER     a sentence has none; a section IS an order
   float PLACEMENT     the sentence NAMES display05. Only the section
                       decides WHERE the float is \input, and that
                       position is what a reader sees
   float NUMBERING     "Table 3" is assigned by ORDER OF APPEARANCE
                       in the whole document, so it is not even a
                       section-level fact, it is a document-level one
   the section \label  \label{sec:results}, which nothing at sentence
                       grain declares
   the bibliography    one .bib, one \bibliography, at the end of the
                       DOCUMENT. A section carries citations and
                       cannot carry a bibliography.

 THIS COLUMN, LINE BY LINE

   S-Main-7-results.md  ## Content
   │
   │  ### §6.1 Main Results        ──►  \subsection{Main Results}
   │  #### P2. the job line        ──►  a %% banner, or dropped: it is
   │                                    SCAFFOLDING, not manuscript
   │  one sentence per source line ──►  prose, joined into one paragraph
   │    \citep{graziano1996…}      ──►  VERBATIM. the .bib and .bst
   │                                    finish it downstream
   │    +0.0009                    ──►  VERBATIM
   │    \ref{tab:descriptives}     ──►  VERBATIM, and it only resolves
   │                                    because of the line below
   │    > Value: · > Display:      ──►  DROPPED. apparatus, not prose
   │    %% {CC-place}: …           ──►  survives as a LaTeX comment
   ▼
   sections/06-results.tex          the prose
   appendices/A-<slug>.tex          same rules, different folder
   \input{displays/display05-…/float.tex}
                                    ⚠️ WHO WRITES THIS LINE? it is not
                                    in the page's Content anywhere. The
                                    page names display05; the wiring is
                                    invented at generate time.


 MEASURED 260726, AND IT CHANGES THIS FACE'S PRIORITY

 The MISQ manuscript has TWO parallel homes for its floats:

   what the SECTION \inputs        what the display UNIT holds
   ---------------------------     ------------------------------
   displays/Table/                 displays/displayNN-<slug>/
     table3-main-results.tex         display04-main-regression/float.tex
     \label{tab:main_results}        \label{tab:results}
     table2-descriptive-stats.tex    display05-descriptives/float.tex
     \label{tab:descriptives}  <-->  \label{tab:descriptives}  SAME LABEL

 Every \input in sections/ points at the FLAT legacy folder. Not one
 points at a unit. And tab:descriptives is declared in BOTH files, so
 the board resolves that chip to the unit while the manuscript
 compiles the other one: a GREEN chip naming a float the paper does
 not use.

 Also on disk: one \input target that does not exist at all
 (displays/Table/table-gradient-results, DR10 deferred), and a comment
 in 05_data_variables.tex:18 recording that an \input was REMOVED
 because "wiring + label binding are display-stage work" -- somebody
 already hit this face's open question and left a note in the .tex
 instead of a ruling on a board.

 THE FINDING THAT MATTERS MORE THAN THE MAPPING
   No .py or .sh in the whole family performs this. An AGENT reads the
   page and types the .tex. So "generated, one way" is a discipline
   asked of an agent rather than a step something performs, and a
   discipline cannot be diffed. Every rule below is unexecuted.
```

## Content
### What is read, and what is dropped
```
 READ, and becomes manuscript
   ### <section heading>        the section or subsection title
   #### Pn. <job>               scaffolding: a banner comment, or nothing
   prose sentences              the paragraph
   \citep{} \cite{TOADD}        verbatim
   numbers                      verbatim
   \ref{tab:…} \ref{fig:…}      verbatim

 DROPPED, and dropping it is correct
   > Value: · > Display: · > Citation:    apparatus. It exists so a
                                          human can check the sentence,
                                          and a reviewer never sees it.
   > JL: · > CC:                          discussion
   ## Items to Finish · ## Where we are   the stage's own bookkeeping

 NEITHER, and this is the hole
   \input{displays/<unit>/float.tex}      the float wiring. It is not in
                                          Content, so it is not read AND
                                          it is not dropped: it is
                                          invented, by whoever is typing.
```

### The two markers that must never ship
`{VAL:? what is wanted}` and `\cite{TOADD}` are states, not text. A generator that copies them into `sections/` has put a placeholder into the thing a reviewer reads: `\cite{TOADD}` compiles to `[?]` and `{VAL:?}` compiles to itself, in the middle of a results sentence.

The board already knows which sentences carry them, because that is exactly what `QC1`'s `owed` and `QC2`'s `ready` chips are. So the generate step has a check available to it for free, and the ruling this face owes is whether an unresolved marker BLOCKS generation or ships with a loud warning.

### Why the easy column still has three open rulings
The mapping above is nearly mechanical, and it is still not settled, because three of its lines hide a decision rather than a translation.

The job line is scaffolding, and scaffolding that survives into the manuscript as a comment is a second copy of the paragraph's intent that nobody will update. Dropping it loses the only written statement of what the paragraph is for.

The float wiring is not derivable from the page. `display05` names a unit; `\input{displays/display05-descriptives/float.tex}` is a path plus a convention plus a position in the file. Something has to own that, and no face currently does.

And the `.tex` on disk today was not generated from anything, so a first generator run will differ from the shipped file in ways that are half rule bugs and half drift the tex accumulated by hand. Until one section is round-tripped and the diff read line by line, nobody knows which half is which.

## Items to Finish
- [ ] 💣 Syncing `S-Main-1` as written would STRIP EVERY CITATION from §1
      Measured 260727, and it is the sharpest argument this face has for why the extraction rule cannot stay a discipline. The page is `S-Main-1-introduction.md`, not `S-Main-2` as this item first said; `S-Main-2` is the opposite case and is the control that makes the defect legible.
      That page's `## Content` carries its references as PLAIN-TEXT author-year: `(Gray et al. 2021)`, `(Barnett et al. 2017; Dowell 2022)`. `sections/01_introduction.tex` carries them as real `\citep{}`. They agree key for key, so nothing looks wrong from either side.
      But sync runs `.md` → `.tex` one way. Run it on this page today and every `\citep{}` command is replaced by prose, and the section's bibliography silently empties. Nobody would notice until a compile, and the diff would look like ordinary prose editing.
      The detector was already running and nobody read it. `S-Main-1` renders 8 chips and NOT ONE of them is a citation; `S-Main-2`, whose prose carries real `\citep{}`, renders 49 green ones. The 18 `\citep{}` strings that DO appear in `S-Main-1` all sit inside backticks in its `> Citation:` lanes, and the resolver skips a code span by `QC1`'s law, correctly. So the page's own board rendering has been reporting "this section cites nothing" since the day the lanes were written.
      That also contradicts this face's own read-and-drop table. It drops `> Citation:` as apparatus. On `S-Main-1` the lane is the ONLY place the key exists, so dropping it destroys the citation rather than discarding bookkeeping. Either the lane is not pure apparatus, or a page in that shape may not be synced until its prose carries the key.
      Two things follow. The extraction rule must say what a plain-text reference in Content BECOMES, and the answer cannot be "pass it through". And a generator needs a refuse-to-regress check: never emit a section with fewer resolving keys, refs or checked numbers than the file it replaces.
- [ ] 📐 Rule the extraction: which parts of `## Content` are read
      Write it into the section-edit contract so two implementations cannot disagree. The table above is the proposal, not the ruling.
      Inherited from `QB2d`'s "rule what sync reads", which is a delivery question and belongs in this column.
- [ ] 🔧 There is no generator, and that is the real finding
      No `.py` or `.sh` in the whole family turns a page into a section: an AGENT writes the `.tex`. "Generated, one way" is therefore a rule an agent is asked to obey rather than a step something performs, which is why the extraction rule has never been executed once.
      Inherited from `QB2d`, where it was filed before this column existed.
- [ ] 🚨 Reconcile the float homes, before anything else here
      Measured 260726: every `\input` in `sections/` points at the flat legacy `displays/Table/`, not one points at a unit, and `tab:descriptives` is declared in BOTH `displays/Table/table2-descriptive-statistics.tex` and `displays/display05-descriptives/float.tex`. So a display chip can be green while naming a float the manuscript does not compile, which silently weakens what `QC3` and `QC4` claim. `QA6` ⑦ already forbids a second home for an asset; this is that rule broken one level down, and it settles before any extraction rule is worth writing.
      Recounted 260727, and it is worse than two. `displays/` holds the ten unit folders AND four flat legacy folders: `Table/`, `Figure/`, `AppendixTable/`, `AppendixFigure/`. Five homes, not two.
      A third path convention is also in live use: `\input{table2-descriptive-statistics}` appears with no folder prefix at all, beside `\input{displays/Table/table2-descriptive-statistics}` for the same file. So "who writes the `\input` line" is not one open question, it is three conventions already shipped, and reconciling has to pick one rather than add a fourth.
- [ ] 📕 A THIRD collision, and this one ships the wrong numbers to the reader
      `sections/04_personality_extraction.tex:126` inputs the legacy `displays/Table/table1-agreeableness-distribution.tex`. That file declares `\label{tab:distribution}`, a DIFFERENT label from the unit's `tab:agreeableness-distribution`, and prints the bell shape 8.1 / 18.5 / 35.1 / 25.9 / 12.4 that DR01 was filed to replace. The unit's own finding is the opposite: scores are polarized, 43% at the highest level.
      So the compiled manuscript currently shows a distribution the paper's own analysis contradicts, and the reference in the section resolves to the legacy file rather than to the unit. The other two collisions (`tab:descriptives`, `tab:results`) are provenance defects; this one is a wrong figure in front of a reviewer.
- [ ] 🔗 Rule who writes the `\input` line for a Display
      The page names `display05`. The manuscript needs a path, a convention and a position. That line is in neither the read set nor the dropped set today, so it is invented at generate time by whoever is typing.
- [ ] 🚦 Rule what an unresolved marker does at generate time
      Block, or ship with a warning. The board already computes which sentences carry one, so the check is free; what is missing is the decision.
- [ ] 🧪 Round-trip one section and read the diff
      Generate `sections/06-results.tex` from `S-Main-7-results.md` and diff against the shipped file. Differences are either rule bugs or drift the tex accumulated by hand, and until this runs nobody knows the ratio.
      Inherited from `QB2d`'s "round-trip one section". A parity test, not permission to make TeX a second source.

## Where we are
Nothing here is built. The MISQ paper's `sections/*.tex` were written by agents reading stage pages, which is the discipline this face is trying to turn into a step.

The absence has a claimant, which is worse than an absence nobody promised. `haipipe-paper-revise/SKILL.md` states that it "syncs the revised .md → .tex" in three separate places and lists `revise ✅ tex synced from revised outline` as a completion state. Searched 260727: the only executable in the whole family that touches a `.tex` is `haipipe-paper-diffpdf/scripts/make-diff.sh`, which diffs two PDFs. So a shipped skill reports a step it does not perform, and the step it does not perform is the one this face owns.

The one thing that DOES exist is the checking half. The board resolves every `\citep{}`, `\ref{}` and number in a stage page against the paper's own `.bib`, `1-probes/` and `displays/`, and reports what does not resolve. So the inputs to a generator are already validated even though the generator is absent, which is the useful half of the asymmetry.

## Files
- `0-lifecycle/4-main/S-Main-*.md`
  The pages this column reads.
- `sections/` · `appendices/`
  What it writes. Unnumbered, per `QA6` ⑦.
- `displays/<unit>/float.tex`
  What it must `\input`, and the line nobody owns.
- `haipipe-paper-revise`
  The skill that today performs this by hand.

## Log
- 260727 · JL asked how this column and `QC6` get made to work, so I re-measured what the page claims before answering, and three claims moved. The citation-stripping item named the wrong page: it is `S-Main-1-introduction.md`, and `S-Main-2` is the control, 49 green citation chips against `S-Main-1`'s zero. The cause is that `S-Main-1`'s real keys live only inside backticks in its `> Citation:` lanes, which the resolver skips by `QC1`'s code-span law, so the board has been reporting "this section cites nothing" since those lanes were written and it read as normal. That also exposed a contradiction in this face's own read-and-drop table, which drops `> Citation:` as apparatus while it is the only carrier of the key on that page. The float homes recounted from two to FIVE, and a third prefix-less `\input` convention turned out to be in live use. And the missing generator has a claimant: `haipipe-paper-revise` states three times that it syncs `.md` → `.tex`, and no executable in the family does.
- 260726 · JL: "remove the icons, just keep different colors", then "only the box fill color to be of opacity, how about you make the font color to be 100% solid". Both done in `board.css`. Every chip carried a kind emoji in `::before` and a state glyph in `::after`, so `QC0`'s eleven-chip paragraph carried twenty-two decorations before a word of prose; both are gone and colour alone says the state. The first attempt at the fade used `opacity` on the whole chip, which dimmed the TEXT as well, and that was the wrong axis: the text is the content and the box is the decoration, so only the box gives ground. Now the fill sits at 6%, the border at 14% and the text at 100%, and hover deepens the fill without ever touching the text. `broken` and `unowned` keep a heavier box on purpose, because a defect that sinks into the prose is a defect nobody acts on. The glyph was the third copy of the state anyway: the `title=` names it in words and the panel repeats it in its header.
- 260726 · JL: "for the display, could we also make the float.tex's pdf to be embedded in the popped out window as well?" Yes, and the file to embed turned out to be `preview.pdf` rather than `assets/figure.pdf`: it is `float.tex` COMPILED STANDALONE, so it carries the caption, the notes and the numbering set by the paper's own class, which `assets/` never does. It leads the panel on the same terms as a citation's `.bbl`: show the thing as the manuscript will set it. All 10 MISQ units already had one. A preview older than the asset it previews is labelled rather than hidden.
- 260726 · Opened on JL's ruling, after I argued the question already had a home on `QB2d` and `QD7` and was wrong about why. The argument that settled it is JL's: `QC1`-`QC4` are ROWS, what hangs on a sentence, and `QC5`/`QC6` are COLUMNS, where it is delivered. Every cell of that matrix differs, so a single "projections" face was always going to be too thin to say anything. Three items moved here from `QB2d` rather than being duplicated.
