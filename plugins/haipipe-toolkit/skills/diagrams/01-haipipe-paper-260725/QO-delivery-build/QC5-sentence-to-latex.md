# A section, delivered as LaTeX
state: 🟡 PARTIAL
owner: JL
method: translate a whole SECTION, not a sentence, so heading order, float placement and numbering are in scope

## Question
When a whole stage page's `## Content` becomes a `sections/*.tex`, what does each part become and what is allowed to be dropped? The unit here is the SECTION, not the sentence, and that is not a difference of scale: a section is a SEQUENCE, so heading nesting, paragraph order, where each float is placed and what number it ends up carrying all live here and are invisible at sentence grain.

`QC1` to `QC4` already say what one citation, one value or one Display reference becomes, and this face never repeats them. It owns what only appears once those sentences are in order, and the measurement below says that is exactly where the defects are.

This is the first of two delivery columns, and it is the easy one, which is why it goes first. LaTeX was the target the sentence grammar was designed against: `\citep{}` is already LaTeX, `\ref{}` is already LaTeX, and a `%%` comment already has somewhere to live. So the question here is not "can it be represented" but "which parts are read, which are dropped, and who performs the reading". A first generator now exists as `md2tex.py` and writes candidate files under `3-dist/tex/`; it has not round-tripped a submission target, does not consume the QA6 projection manifest, and cannot promote into `sections/` or `appendices/`.

## Boundary
- ✅ Covered here
  A whole section: heading hierarchy, paragraph order, float placement and numbering, the section's own label, the `\input` wiring to `displays/`, what is dropped, and what a generator would have to do.
- ↪ Covered elsewhere
  What one SENTENCE's citation, value or Display reference becomes is `QC1` to `QC4`; this face never re-states them. Which of the two files is the paper, and what a backward edit means, is `QB2d`. The general one-source-many-projections model is `QD7`, and the archived adapter contract is `QD4-format-adapters`. Where the generated files land on disk is `QA6` ⑦. The Word column is `QC6`. What each thing that hangs on a sentence MEANS is `QC1` to `QC4`, and the sentence unit itself is `QC0`.

## Diagram
```
 QC IS A MATRIX (JL 260726). QC1-QC4 are ROWS, what hangs on a
 sentence. QC5 and QC6 are COLUMNS, where it is delivered. Every
 cell differs, which is why one "projections" face was always
 going to be too thin.

                    │ QC5 ──▶ LaTeX          │ QC6 ──▶ Word
   ─────────────────┼────────────────────────┼─────────────────────────
   QC1 citation     │ \citep{key} + .bib     │ author-year baked from
                    │ + .bst does the rest   │ .board-refs.bbl, + the key
                    │                        │ in an anchored comment
   QC2 value        │ the number, inline     │ the number, inline  ✅ same
   QC3 table        │ \input{displays/<u>/   │ a real w:tbl parsed from
                    │ float.tex} + \ref      │ assets/table-body.tex
   QC4 figure       │ \includegraphics in    │ assets/figure.png embedded,
                    │ the unit's float       │ numbered by appearance order
   ─────────────────┼────────────────────────┼─────────────────────────
   ### §6.1         │ \subsection            │ a Heading style
   > lanes          │ DROPPED                │ ANCHORED COMMENT
   %% {CC-*}:       │ survives as a comment  │ ANCHORED COMMENT


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

   S-Main-6-results.md  ## Content
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
   sections/06_empirical_analysis.tex   the prose
   appendices/A-<slug>.tex          same rules, different folder
   \input{displays/display05-…/float.tex}
                                    ⚠️ WHO WRITES THIS LINE? it is not
                                    in the page's Content anywhere. The
                                    page names display05; the wiring is
                                    invented at generate time.


 THE 260726 FLOAT-HOME DEFECT WAS REPAIRED

 The active displays/ root now holds named units; the old Table,
 Figure, AppendixTable and AppendixFigure buckets are archived.
 sections/04_personality_extraction.tex now reaches
 displays/S-Display-2a-distribution/float rather than the retired
 distribution table. Candidate generation follows the same unit rule.

 This does not settle placement semantics. md2tex.py currently inserts
 a unit's float immediately after the first paragraph whose prose
 carries its \ref label. That behavior is implemented and still needs
 the round-trip and human ruling below.

 THE FIRST IMPLEMENTATION NOW EXISTS, BUT STOPS AT THE CANDIDATE
   md2tex.py reads the same Content parser as the Word exporter and
   writes only under 3-dist/tex/. It does not read a page-to-target
   manifest, resolve the master-reachable closure, or promote into
   sections/ and appendices/. So generation can now be diffed, while
   submission replacement remains deliberately unimplemented on QA6.
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

 DERIVED BY THE CANDIDATE ADAPTER
   \input{displays/<unit>/float.tex}      md2tex.py resolves the prose's
                                          first \ref through the Display
                                          registry and inserts the unit
                                          after that paragraph. Implemented,
                                          not yet accepted by round-trip.
```

### The two markers that must never ship
`{VAL:? what is wanted}` and `\cite{TOADD}` are states, not text. A generator that copies them into `sections/` has put a placeholder into the thing a reviewer reads: `\cite{TOADD}` compiles to `[?]` and `{VAL:?}` compiles to itself, in the middle of a results sentence.

The board already knows which sentences carry them, because that is exactly what `QC1`'s `owed` and `QC2`'s `ready` chips are.
Ruled with QA6 G1: a live marker in selected prose blocks a promotable candidate.
A marker mentioned inside a code span or apparatus lane describes work and is dropped; it is not live manuscript prose and does not block.

### Why the easy column still has three open rulings
The mapping above is nearly mechanical, and it is still not settled, because three of its lines hide a decision rather than a translation.

The job line is scaffolding, and scaffolding that survives into the manuscript as a comment is a second copy of the paragraph's intent that nobody will update. Dropping it loses the only written statement of what the paragraph is for.

The float path is derivable from the page's prose `\ref{}` and the Display registry, and `md2tex.py` now inserts the unit after the first paragraph that carries that label.
What remains open is whether first-reference placement is the accepted section rule, especially when a Display serves more than one section; the candidate round-trip must expose that choice before it becomes Law.

The submission `.tex` on disk today was not generated by `md2tex.py`, so its first candidate-to-submission comparison will differ in ways that are half rule bugs and half drift the tex accumulated by hand. Until one section is round-tripped and the diff read line by line, nobody knows which half is which.

## Items to Finish
- [x] 💣 Repair the citation-stripping source defect on `S-Main-1`
      The 260727 page carried keys only in Citation lanes and would have lost them when apparatus was dropped.
      Its current prose contains 16 real `\citep{}` calls and the page is `✅ GATED 2026-07-27`, so that live blocker is closed.
      The incident remains the reason G3 compares binding identities rather than citation counts.
- [ ] 📐 Rule the extraction: which parts of `## Content` are read
      Write it into the section-edit contract so two implementations cannot disagree. The table above is the proposal, not the ruling.
      Inherited from `QB2d`'s "rule what sync reads", which is a delivery question and belongs in this column.
- [x] 🔧 A candidate generator now exists
      `md2tex.py` reads the shared S-page Content parser and writes generated `.tex` plus a proof master under `3-dist/tex/`.
      It closes the literal "no generator" finding inherited from `QB2d`; it does not close extraction parity, submission mapping, or promotion, which remain here and on `QA6`.
- [x] 🚨 Reconcile the active float homes
      The four flat buckets are archived and active sections now point at named Display units.
      `sections/04_personality_extraction.tex` reaches `displays/S-Display-2a-distribution/float`, so the former wrong-distribution collision is no longer in the submission path.
- [ ] 🔗 Rule the implemented first-reference placement
      `md2tex.py` resolves a prose `\ref{}` through the Display registry and inserts that unit after the first paragraph carrying the label.
      Round-trip one section and decide whether this behavior is Law, especially for a Display whose first mention and owning section differ.
- [x] 🚦 Block unresolved markers in selected prose
      `{VAL:?}` or `\cite{TOADD}` in selected manuscript prose blocks QA6 G1.
      Code-spanned examples and apparatus-lane mentions are not manuscript input and do not block.
- [ ] 🧪 Round-trip one section and read the diff
      Generate the candidate for `S-Main-1-introduction.md` and diff it against `sections/01_introduction.tex`. It is the only current Main page whose state begins `✅`, and its 16 prose citation calls make evidence regression visible.
      Inherited from `QB2d`'s "round-trip one section". A parity test, not permission to make TeX a second source.

## Where we are
A candidate generator is built and writes `3-dist/tex/`.
The MISQ paper's submission `sections/*.tex` were still hand-carried by agents reading stage pages, and no generated candidate has passed the page-to-target, evidence, compile, and human-diff path needed to replace one.

The 260727 absence finding was true when measured and is now historical.
`haipipe-paper-revise/SKILL.md` still claims it syncs revised `.md` into `.tex`, but the executable that now performs candidate conversion lives under `haipipe-paper-to-word`, does not implement that revise completion state, and does not promote.
QA6 now owns the missing wiring manifest and promotion transaction; this face still owns extraction semantics and the first round-trip diff.

The checking half also exists. The board resolves every `\citep{}`, `\ref{}` and number in a stage page against the paper's own `.bib`, `1-probes/` and `displays/`, and reports what does not resolve.
The remaining asymmetry is that candidate generation exists while manifest-scoped evidence comparison, isolated compile, and promotion do not.

## Files
- `0-lifecycle/4-main/S-Main-*.md`
  The pages this column reads.
- `sections/` · `appendices/`
  What it writes. Unnumbered, per `QA6` ⑦.
- `displays/<unit>/float.tex`
  What the candidate adapter inserts after the first prose reference; the placement rule remains open.
- `haipipe-paper-revise`
  Still claims a `.md` to `.tex` sync completion state that its own executable path does not perform.
- `3-deliver/4-ship/haipipe-paper-to-word/md2tex.py`
  The candidate generator that closed the literal absence; it writes `3-dist/tex/` and leaves submission promotion to QA6.

## Log
- 260729 · Closed the unresolved-marker fork to match QC6 and QA6 G1. A live marker in selected prose blocks a promotable LaTeX candidate; a code-spanned or apparatus-lane mention is working context that the adapter drops, not manuscript text.
- 260729 · Refreshed the live facts after the projection-contract cold read. `S-Main-1` now carries 16 prose citation calls and is gated; a raw Content grep reports 29 only by counting duplicated Citation-lane markup and one `\cite{TOADD}`. The four flat Display buckets are archived; section 04 reaches `S-Display-2a-distribution`; and `md2tex.py` now owns candidate float insertion after first reference. The old blocks remain historical causes, not current blockers. Also repaired the adapter pointer to the archived `QD4-format-adapters` page.
- 260729 · Cleared the stale "no generator" claim after reading the live `md2tex.py`. It reuses the Word exporter's Content parser, generates candidate `.tex` files and a proof master under `3-dist/tex/`, and performs a citation-count refusal against an existing candidate. It does not read QA6's proposed manifest, map S-page names to master-reachable submission targets, or promote. The item is closed as candidate generation only; extraction parity and the first round-trip stay open here, and promotion stays on QA6.
- 260727 · JL asked how this column and `QC6` get made to work, so I re-measured what the page claims before answering, and three claims moved. The citation-stripping item named the wrong page: it is `S-Main-1-introduction.md`, and `S-Main-2` is the control, 49 green citation chips against `S-Main-1`'s zero. The cause is that `S-Main-1`'s real keys live only inside backticks in its `> Citation:` lanes, which the resolver skips by `QC1`'s code-span law, so the board has been reporting "this section cites nothing" since those lanes were written and it read as normal. That also exposed a contradiction in this face's own read-and-drop table, which drops `> Citation:` as apparatus while it is the only carrier of the key on that page. The float homes recounted from two to FIVE, and a third prefix-less `\input` convention turned out to be in live use. And the missing generator has a claimant: `haipipe-paper-revise` states three times that it syncs `.md` → `.tex`, and no executable in the family does.
- 260726 · JL: "remove the icons, just keep different colors", then "only the box fill color to be of opacity, how about you make the font color to be 100% solid". Both done in `board.css`. Every chip carried a kind emoji in `::before` and a state glyph in `::after`, so `QC0`'s eleven-chip paragraph carried twenty-two decorations before a word of prose; both are gone and colour alone says the state. The first attempt at the fade used `opacity` on the whole chip, which dimmed the TEXT as well, and that was the wrong axis: the text is the content and the box is the decoration, so only the box gives ground. Now the fill sits at 6%, the border at 14% and the text at 100%, and hover deepens the fill without ever touching the text. `broken` and `unowned` keep a heavier box on purpose, because a defect that sinks into the prose is a defect nobody acts on. The glyph was the third copy of the state anyway: the `title=` names it in words and the panel repeats it in its header.
- 260726 · JL: "for the display, could we also make the float.tex's pdf to be embedded in the popped out window as well?" Yes, and the file to embed turned out to be `preview.pdf` rather than `assets/figure.pdf`: it is `float.tex` COMPILED STANDALONE, so it carries the caption, the notes and the numbering set by the paper's own class, which `assets/` never does. It leads the panel on the same terms as a citation's `.bbl`: show the thing as the manuscript will set it. All 10 MISQ units already had one. A preview older than the asset it previews is labelled rather than hidden.
- 260726 · Opened on JL's ruling, after I argued the question already had a home on `QB2d` and `QD7` and was wrong about why. The argument that settled it is JL's: `QC1`-`QC4` are ROWS, what hangs on a sentence, and `QC5`/`QC6` are COLUMNS, where it is delivered. Every cell of that matrix differs, so a single "projections" face was always going to be too thin to say anything. Three items moved here from `QB2d` rather than being duplicated.
