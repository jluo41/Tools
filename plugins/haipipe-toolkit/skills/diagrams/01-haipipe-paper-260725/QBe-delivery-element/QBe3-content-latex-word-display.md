# Delivery-Content: LaTeX, Word, Display

state: 🟡 PARTIAL · the three faces are absorbed into one page; the aggregate rule is now admitted but not checked, the shared loss list is unwritten, and placement is undecided
owner: JL
method: hold every rule whose unit is a whole section, so a format adapter is judged on sequence rather than on wording

## Opening

What has to survive when a section becomes a file a journal accepts?

A section here is one stage page's `## Content`, delivered as one file such as `sections/03_method.tex`. A sequence is everything about it that only exists in the ordering: which heading sits inside which, which paragraph comes before which, where a float lands. Those are the facts a per-sentence check cannot see.

**Where this page sits**: `QB9` Build owns generating, checking, and promoting candidate files.
This page is where Build's adapters are specified, and `QBe1` holds the rules whose unit is one sentence.

**Why this is not a matter of scale**: a sentence rule can be checked one sentence at a time, in any order.
A section rule cannot, and it fails that check in one of two ways: a sequence rule needs the section read top to bottom because its claim is about what comes before what, and an aggregate rule needs the whole section counted because its claim is about how much there is.
The old filenames denied this outright: the two adapters were called `sentence-to-latex` and `sentence-to-word` while their own openings said the unit was the SECTION.

**Why one page and not four**: on 260803 the three faces became `### 3` to `### 5`, which puts both adapters and the placement rule where their shared debt is visible.
That debt is one loss list, not one per adapter: both drop things, and while each says so in its own words nobody can tell whether they drop the same things.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `../01-boardform-260722/QB-delivery/QB4-overall.md` and are not restated here.

**Demonstrate before explaining**: `### 1` is a test sheet, and this one is RUN rather than clicked.
A section is a file the browser never builds, so the honest demonstration is a command and its expected output, never a button that does not exist.

**Name the parts, not the retired faces**: the LaTeX adapter, the Word adapter and float placement are this page's `### 3` to `### 5`.
`### 3`` to `### 5``, and the older `QB11a` to `QB11c` and `QB9a`/`QB9b`/`QB5f`, still resolve through `board.md`'s alias map; nothing new is written with them.

**The admission test is two questions, and the shuffle is the SECOND one**: a rule belongs here when one sentence read alone cannot settle it, and the shuffle then says whether it is a sequence rule or an aggregate rule.
A rule one sentence can settle belongs on `QBe1`; the shuffle alone never sends a rule away from this page.

**`## Content` and `section` name the same unit**: the title says Content because that is the block an adapter reads, and the rules below say section because that is what a reader of the journal receives (JL 260803).
Use either, never a third word, and never `sentence`.

**Never write "sentence" for the unit**: that word cost this series its own name until 260802.
Say section, or say `## Content`, and let `QBe1` own the other word.

**Name a dropped element, never "some formatting"**: a loss list is only useful if a reader can check it.
"Word cannot carry why-comments" can be verified; "some things do not survive" cannot.

## Diagram

**What the whole section carries**: the facts no single sentence holds, in the two kinds this page admits.

```text
   ✍️ S-page ## Content
        │
        │  📐 adapter
        ▼
   📄 one delivered file

   📐 WHAT ONLY THE SEQUENCE KNOWS        a rule about ORDER
   ───────────────────────────────
   🔡 heading nesting   ━━▶  the outline
   ¶  paragraph order   ━━▶  the argument's order
   🖼 float citation     ━━▶  placement + numbering   ← `### 5`

   📏 WHAT ONLY THE WHOLE SECTION KNOWS   a rule about AMOUNT
   ────────────────────────────────────
   #  word budget       ━━▶  the venue's `## Word budget`   ← `### 2.3`
   ¶  paragraph count   ━━▶  how many P the arc needs
   🔗 citation density  ━━▶  keys per sentence, across the section

   🔍 test: can ONE sentence, read alone, settle it?
      yes ━━▶ it is a SENTENCE rule, it lives on QBe1
      no  ━━▶ it lives HERE; the shuffle then says which kind
```

## Content

### 1 · Try it yourself: download what the two adapters just produced

**Two files to open**: both were generated from one real S page, and both are on this server.

```text
📥 DOWNLOAD THESE · generated 260803 from S06-main/S-Main-4-measurement.md
   _tools/adapter-out/S-Main-4-measurement.tex     9.4 KB   the LaTeX adapter
   _tools/adapter-out/S-Main-4-measurement.docx  611.4 KB   the Word adapter
   _tools/adapter-out/paper.tex                   1.7 KB   the wrapper that
                                                            compiles the .tex

👀 IN THE .tex, CHECK THE SEQUENCE · never the wording, which is QBe1's unit
   1 \section + 4 \subsection      the five numbered headings, in order
   \input{displays/...} x3         INSERTED after the first reference to each
   ### Stage Record · ### Needs JL  DROPPED: board apparatus is not manuscript
   > lanes                          all 29 DROPPED: they have nowhere to go

📝 IN THE .docx, CHECK THE APPARATUS · what a coauthor actually receives
   9 anchored comments, every one authored `haipipe`
   the first one carries the reference as the paper's own .bst prints it
   1 image embedded · 6 styled headings · 12 references
   ⚠️ and one thing it reports about itself: a \cite{TOADD} shipped to a reader

🚫 THIS MUST REFUSE YOU
   feeding the LaTeX adapter a page that LOST a citation. Tested 260803:
   "REFUSED degraded: 11 citations, the file it replaces has 12."
   Sync runs one way, so a page that quietly dropped a source would empty
   that section's bibliography on the next run.
```

📥 Establishes the one demonstration this page can honestly offer: two files a reader downloads and opens, rather than a button that does not exist.

#### 1.1 · Why this section is downloaded and not clicked
(the other two groups in QBe demo in the browser, and saying so is more useful than pretending)
`QBe1`'s markers and `QBe2`'s units both resolve when this board builds, so their sheets are clickable in place.
A section is delivered as a `.tex` or a `.docx`, and neither is something a board page can open.
Faking a click here would teach a reader the wrong thing about what the board can check.

#### 1.2 · Regenerate them yourself, in one command each
(the files above are a snapshot; the command is the real deliverable)
`md2tex.py <S-page.md> --paper-root <paper> -o <dir>` writes the LaTeX.
`md2docx.py <S-page.md> -o <out.docx> --paper-root <paper>` writes the Word file.
`build-both.sh` runs the pair, which is the round trip `A3.3` asks for.
`_tools/qbe-tests.py --only QBe3` runs both into a temp dir and checks 19 things about the result.

#### 1.3 · The placement trace, measured on the live paper
(the third thing this page owns, and the only failing row in the harness)
Following every `\input` from the master: 4 float labels are cited, 1 resolves, and 3 compile to `??`.
Thirteen display units sit on disk, 4 are reached, 9 are never inputted, and 2 inputs name files that do not exist.
The citing SECTION now inputs its own float, so placement and reaching stopped being two questions and became one act.
That is the paper voting for first-mention-wins by wiring it that way, and `### 5` is where the rule gets written down.

### 2 · What makes a rule a section rule

**Two questions, asked in this order**: the first decides whether the rule is a section rule at all, and the second decides which of the two kinds it is.

```text
   a candidate rule
        │
        ▼
   ❶ 🔍 can ONE sentence, read alone, settle it?
        │
   ┌────┴──────────────┐
   ▼                   ▼
  ✅ yes              ❌ no
   │                   │
   ▼                   ▼
  QBe1            ❷ 🔀 reorder the paragraphs
  one sentence         │
  at a time       ┌────┴────┐
                  ▼         ▼
              💥 breaks   ✅ still holds
                  │            │
                  ▼            ▼
             📐 SEQUENCE   📏 AGGREGATE
             a rule about  a rule about
             ORDER         AMOUNT
             §3 §4 §5      word budget · ¶ count
                  └──────┬─────┘
                         ▼
                       QBe3
```

🔍 Establishes the admission test for this page, and the two kinds of section rule it admits.

#### 2.1 · The unit was denied by its own filenames
(the pages said SECTION in their openings and said sentence in their names, and the names won)
`### 3`'s opening states it directly: the unit is the section, and that is not a difference of scale.
Because the files were named `sentence-to-latex` and `sentence-to-word`, both sat filed under the sentence work, and nothing read them as one series until 260802.

#### 2.2 · Placement is a section rule, which is why `### 5` is here
(the float's own page does not decide where the float goes)
LaTeX floats near the FIRST mention, so the section that cites a unit earliest decides where it appears.
That makes placement a fact about citation order, which is a sequence, so it left QBe2 for this series.

#### 2.3 · A size rule survives the shuffle, and still cannot be checked one sentence at a time
(the admission test above sorts by ORDER, so it has no answer for a rule about AMOUNT)
How many words a section may run is a fact about the whole section, but reordering its paragraphs does not change the count, so the shuffle test sends it to QBe1, where a per-sentence check can never see it.
The number itself already exists and is read, never written, by this plugin: it sits in `paper/venue/playbook-*/<outlet>/<outlet>-<kind>/style.md` under `## Word budget`, present in 78 of the 95 `style.md` files and absent from all 13 `*-appendix` packs and from four of the five `*-related-work` packs.
The measuring side already exists too: `../../paper/route/haipipe-paper-stage/section-stats.py` counts P, sentences, and prose words per section, and its `--dashboard` mode prints a `floor` column transcribed from the venue blueprint with a `LOW` flag.
So neither the budget nor the counter is missing; what is missing is any page on this Board that says a section HAS a size, which is why no reader of QBe3 can find one.
Measured 260802: npj Digital Medicine 2025 main text runs 7,313 prose words, MISQ 2026 runs 9,600, and the medical-journal draft runs 2,654; across all three one paragraph is about 5 sentences and about 110 words, and one sentence is about 22 words.

### 3 · A section, delivered as LaTeX

**What LaTeX must carry across**: the sequence facts a per-sentence check cannot see.

`QBe1 §4` to `QBe1 §7` already say what one citation, one value or one Display reference becomes, and this face never repeats them. It owns what only appears once those sentences are in order, and the measurement below says that is exactly where the defects are.

```
 QC IS A MATRIX (JL 260726). QBe1 §4-QBe1 §7 are ROWS, what hangs on a
 sentence. `### 3` and `### 4` are COLUMNS, where it is delivered. Every
 cell differs, which is why one "projections" face was always
 going to be too thin.

                    │ `### 3` ──▶ LaTeX          │ `### 4` ──▶ Word
   ─────────────────┼────────────────────────┼─────────────────────────
   QBe1 §4 citation     │ \citep{key} + .bib     │ author-year baked from
                    │ + .bst does the rest   │ .board-refs.bbl, + the key
                    │                        │ in an anchored comment
   QBe1 §5 value        │ the number, inline     │ the number, inline  ✅ same
   QBe1 §6 table        │ \input{displays/<u>/   │ a real w:tbl parsed from
                    │ float.tex} + \ref      │ assets/table-body.tex
   QBe1 §7 figure       │ \includegraphics in    │ assets/figure.png embedded,
                    │ the unit's float       │ numbered by appearance order
   ─────────────────┼────────────────────────┼─────────────────────────
   ### §6.1         │ \subsection            │ a Heading style
   > lanes          │ DROPPED                │ ANCHORED COMMENT
   %% {CC-*}:       │ survives as a comment  │ ANCHORED COMMENT


 THE UNIT IS THE SECTION, NOT THE SENTENCE (JL 260726)

 QBe1 §4-QBe1 §7 translate ONE SENTENCE and everything that hangs on it.
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

📐 Establishes what the LaTeX adapter must carry across, and what it is allowed to drop. Absorbed from `QBe3a` on 260803; its full design history stays in `_archive/QBe3a-section-to-latex.md`.

#### What is read, and what is dropped
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

#### The two markers that must never ship
`{VAL:? what is wanted}` and `\cite{TOADD}` are states, not text. A generator that copies them into `sections/` has put a placeholder into the thing a reviewer reads: `\cite{TOADD}` compiles to `[?]` and `{VAL:?}` compiles to itself, in the middle of a results sentence.

The board already knows which sentences carry them, because that is exactly what `QBe1 §4`'s `owed` and `QBe1 §5`'s `ready` chips are.
Ruled with QA6 G1: a live marker in selected prose blocks a promotable candidate.
A marker mentioned inside a code span or apparatus lane describes work and is dropped; it is not live manuscript prose and does not block.

#### Why the easy column still has three open rulings
The mapping above is nearly mechanical, and it is still not settled, because three of its lines hide a decision rather than a translation.

The job line is scaffolding, and scaffolding that survives into the manuscript as a comment is a second copy of the paragraph's intent that nobody will update. Dropping it loses the only written statement of what the paragraph is for.

The float path is derivable from the page's prose `\ref{}` and the Display registry, and `../../paper/S09-build/haipipe-paper-to-word/md2tex.py` now inserts the unit after the first paragraph that carries that label.
What remains open is whether first-reference placement is the accepted section rule, especially when a Display serves more than one section; the candidate round-trip must expose that choice before it becomes Law.

The submission `.tex` on disk today was not generated by `../../paper/S09-build/haipipe-paper-to-word/md2tex.py`, so its first candidate-to-submission comparison will differ in ways that are half rule bugs and half drift the tex accumulated by hand. Until one section is round-tripped and the diff read line by line, nobody knows which half is which.

### 4 · A section, delivered as Word

**What Word can and cannot carry**: the apparatus that becomes a comment, and the rest.

The reason to have this column at all is that a coauthor who is not a LaTeX user still has to read and mark up the paper, and the reason it is hard is that the same act makes the output editable. LaTeX delivery is safe because nobody edits a generated `.tex`; a `.docx` is handed to a person precisely so they will edit it. So this face carries the one ruling the whole projection model has been deferring: what happens to the paper when the change comes back in the output rather than in the source.

```
 QC IS A MATRIX (JL 260726). QBe1 §4-QBe1 §7 are ROWS, what hangs on a
 sentence. `### 3` and `### 4` are COLUMNS, where it is delivered.

                    │ `### 3` ──▶ LaTeX          │ `### 4` ──▶ Word
   ─────────────────┼────────────────────────┼─────────────────────────
   QBe1 §4 citation     │ \citep{key} + .bib     │ author-year BAKED from
                    │ + .bst does the rest   │ .board-refs.bbl, + the key
                    │                        │ in an anchored comment
   QBe1 §5 value        │ the number, inline     │ the number, inline  ✅ same
   QBe1 §6 table        │ \input{displays/<u>/   │ a real w:tbl parsed from
                    │ float.tex} + \ref      │ assets/table-body.tex
   QBe1 §7 figure       │ \includegraphics in    │ assets/figure.png embedded,
                    │ the unit's float       │ numbered by appearance order
   ─────────────────┼────────────────────────┼─────────────────────────
   ### §6.1         │ \subsection            │ a Heading style
   > lanes          │ DROPPED                │ ANCHORED COMMENT ◄ WORD WINS
   %% {CC-*}:       │ survives as a comment  │ ANCHORED COMMENT ◄ WORD WINS

 THE RATIO INVERTED ON 260727, AND JL'S QUESTION IS WHY
 The old reading of this table was one ✅, three ⚠️ and one 🔴, which made
 Word "the lossy column". Put the apparatus in ANCHORED WORD COMMENTS and
 two rows flip the other way: a `> Value:` lane is DROPPED by `### 3` and
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

📝 Establishes the same for the coauthor-facing format, where the apparatus becomes comments or is lost. Absorbed from `QBe3b` on 260803; its full design history stays in `_archive/QBe3b-section-to-word.md`.

#### What Word actually costs, row by row
Re-scored 260727, after JL asked whether the citations and the values could be carried as comments. Six of eight rows now have an answer that needs no new engine, because each one resolves against a file the family already generates.

```
 QBe1 §5 value        the number, inline                              ✅ free
 heading          ### §6.1  →  a Heading style                    ✅ free
 %% {CC-*}:       an anchored comment, w:author="haipipe"         ✅ SOLVED
 > lanes          the same, anchored to the NUMBER not the ¶      ✅ SOLVED
                  (`### 3` drops these; this column keeps them)
 the edit         partition returning comments by author          ✅ SOLVED
 QBe1 §4 citation     baked author-year out of .board-refs.bbl,       ⚠️ ruling
                  which refs.py ALREADY generates with the
                  paper's own .bst; the key rides in a comment
 QBe1 §6 table        a real w:tbl parsed from the unit's             ⚠️ ruling
                  assets/table-body.tex, so it stays EDITABLE
 QBe1 §7 figure       assets/figure.png embedded; numbering is        ⚠️ ruling
                  order-of-appearance, which the exporter
                  computes because it walks sections in order
```
The three remaining rulings are about FIDELITY, not feasibility: each has a working answer above and what is open is whether that answer is good enough to hand a coauthor.

#### The citation ruling dissolves rather than resolves
This face framed it as a choice between a live Word field, which needs its source library to travel, and baked text, which becomes a second bibliography somebody must keep true. Both costs are real and neither applies here, because the baked text is not authored.

`refs.py` already synthesizes an `.aux` citing every key the board uses, runs `bibtex` with the paper's own `.bst`, and caches `.board-refs.bbl`. It exists on the MISQ paper today at 62 KB. That is a formatted bibliography, in the manuscript's own style, generated from the one real `.bib`.

So the Word export parses that file rather than formatting anything. There is no second bibliography to keep true because nobody writes one: it is regenerated on every export from the same source the LaTeX column compiles. The dilemma was between two ways of MAINTAINING a copy, and the answer is not to maintain one.

#### What a reader sees, and what a checker sees, in the same file
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
Two audiences, one file, and the second one is invisible until a bubble is opened. That is the property `### 3`` cannot offer: in LaTeX the apparatus is dropped at generate time, so a reviewer never sees it and neither does anyone else.

#### Why this column exists at all
A `.docx` is not a delivery format the venue wants. MISQ takes LaTeX. The `.docx` exists for one reason: a coauthor or advisor who does not use LaTeX has to read the paper and mark it up.

That single purpose decides most of the rulings above. If the file is for reading and marking up, then a picture of a table is wrong because they cannot fix a typo in it, baked citation text is tolerable because they are not going to re-run the bibliography, and Word review comments must be left EMPTY on export, because that is the channel their own comments will arrive in.

#### The ruling this face owes the rest of the board
The retired `QD7` carried "rule external edits" as an open item from the day it opened, and `QC3d` carries the same thing worded differently. Neither can close it, because the edit is not hypothetical in the abstract: it is what happens when you hand someone a Word file. So the ruling belongs where the Word file is made, which is here.

Two answers, and the reason to pick rather than defer is that the failure mode of silence is total: the S page and the `.docx` both look like the paper, and the person editing either one cannot tell which is being reviewed.

### 5 · Where a float lands, and whether the build reaches it

**Two independent failures**: landing in the wrong section, and never being reached at all.

Placement is where a float appears in the printed paper. First mention is the earliest sentence that cites it, and LaTeX puts a float near that, so the section citing a unit earliest decides where it appears, whatever the unit's own page says it serves. Reaching it is a separate question: whether the master file inputs the float at all.

**Two independent failures**: one about order, one about wiring.

```text
  ❶ WHICH SECTION?                    ❷ IS IT REACHED?
  ────────────────                    ─────────────────
  LaTeX puts a float near the         Personality-Opioid-MISQ2026.tex
  FIRST mention                       inputs sections/* and appendices/*
       │                                   │  and NOTHING else
       ▼                                   ▼
  the earliest citing section         no displays/*/float.tex is on
  decides, whatever the unit's        any path the master reaches
  own page says it serves                  │
       │                                   ▼
       ▼                              💥 every label compiles to ??
  ⚠️ S-Display-1b declares
     serves: Methods §5, but a        fig:research-model         §1 §3
     fold moves first mention         fig:research-design        §5
     to §4                            fig:llm-measurement        §4
                                      tab:agreeableness-distribution §4
                                      tab:validation-summary     §4

  🔑 ONE gap, FIVE symptoms, filed on THREE different section pages
```

📍 Establishes the two independent failures a placed float has: landing in the wrong section, and never being reached at all. Absorbed from `QBe3c` on 260803; its full design history stays in `_archive/QBe3c-display-placement.md`.

#### 1 · Nothing the build reaches declares a display label

**Measured 260727**: what the master actually inputs, against what the sections cite.

```text
  📄 Personality-Opioid-MISQ2026.tex
       ├── \input sections/*        ✅
       ├── \input appendices/*      ✅
       └── displays/*/float.tex     ❌ NEVER
                                     │
  📁 0-lifecycle/3-display/4-display.tex
       the gallery that DOES input the floats
       └── and the master does not input IT either
```

🔌 Establishes the wiring gap, and that it is a single missing edge rather than five separate display problems.

##### 1.1 · One gap presenting as five symptoms
(it is why the fix belongs on this face and not on any section page)
Three separate section pages had each recorded a `??` as their own display problem.
None of them was wrong, and none could fix it, because the missing edge is between the master and the gallery rather than inside any section.

#### 2 · First mention decides, and this paper has a live case

**One unit, two consumers**: what happens when a fold moves the earliest citation.

```text
  📄 S-Display-1b   declares  serves: Methods §5
         │
         │  Candidate E folds the measurement workflow into step ①
         │  display03 parks when that lands
         ▼
  after promotion §4 has no figure of its own
         │
         ▼
  §4 must cite §5's unit  ━━▶  FIRST MENTION moves to §4
         │
         ▼
  📍 the float follows it into §4, a section whose own page
     says the unit does not belong there

  🚫 not a bug in either layer ── this face is EMPTY, so the two
     pages disagree and neither is wrong
```

📍 Establishes the live conflict this face has to rule on, rather than a hypothetical one.

##### 2.1 · The choice is accept LaTeX's rule or pin the float
(first-mention-wins is a default, and a default is not a decision)
Either the paper accepts that the earliest citing section decides, or it pins a float deliberately and overrides the default.
Both are defensible; what is not defensible is the current state, where nothing says which, so two pages can each be internally right.

#### 3 · A placed float and a promoted asset are different things

**Placed is not current**: what a `ready` marker means for a reader.

```text
  ✍️ the sentence is written
  📍 the float is placed
  🖼 the picture it will compile is NOT the one that was accepted

  S-Main-5 shows FIVE figure markers reading `ready`
  ── the candidate landed and the manuscript has not caught up
  🚫 nothing currently checks the difference
```

🧯 Establishes that placement says nothing about whether the reader sees the accepted asset.

##### 3.1 · A section needs a rule for its own unpromoted unit
(the prose is final while the picture is not, and the section cannot tell)
Placement does not imply the reader sees the current asset.
Until this face says what a section does when its unit is not promoted, five `ready` markers sit in a finished section with nothing reporting that the pictures are stale.

## Aims

### A1 · 📥 Try it yourself: download what the two adapters just produced
- A1.1 · The one demonstration this page can honestly offer is a file a reader downloads and opens.
  **Done when:** a reader opens the `.docx` in Word and the `.tex` in an editor, and can say from those two alone whether each adapter passed.

### A2 · What makes a rule a section rule
- A2.1 · The unit is named consistently across the page.
  **Done when:** no division, title, or opening here calls a section a sentence.
- A2.2 · Both adapters declare the same loss list, stated once.
  **Done when:** `### 2` carries one list of what a delivered section may lose, and `### 3` and `### 4` each say only where they differ from it.
- A2.3 · Where a float lands is decided, rather than left to whatever LaTeX does.
  **Done when:** `### 5` states the placement rule and a compiled paper is checked against it.
- A2.4 · A rule about how much a section may contain has a home on this Board.
  **Done when:** the admission test names the aggregate rule as a second kind of section rule, pointing at the venue `## Word budget` as its source and `section-stats.py --dashboard` as its check.
- A2.5 · The aggregate rule is checked rather than merely admitted.
  **Done when:** every section of one real paper carries a `floor` from its venue pack, the dashboard reports each one as inside or outside it, and a section outside its budget blocks the same gate a live `\cite{TOADD}` blocks.
- A2.6 · The 17 packs with no `## Word budget` are either filled or declared budget-free.
  **Done when:** each of the 13 `*-appendix` packs and the four `*-related-work` packs either carries a number or says in the pack that this venue sets none, so a missing budget is an answer rather than a gap.

### A3 · 📐 A section, delivered as LaTeX
- A3.1 · The extraction is ruled: which parts of `## Content` are read.
- A3.2 · The implemented first-reference placement is ruled rather than observed.
- A3.3 · One section is round-tripped and the diff is read.
  **Done when:** all three are written into `### 3`, and the round-trip is run on a real section rather than described.

### A4 · 📝 A section, delivered as Word
- A4.1 · One real section is exported and given to a human coauthor.
- A4.2 · The eight `4-main` pages that reference no display in their prose are explained or fixed.
- A4.3 · The two other copies of the lane-to-comment matrix are reconciled with this one.
  **Done when:** the export has been read by someone who does not use the board, and one matrix exists rather than three.

### A5 · 📍 Where a float lands, and whether the build reaches it
- A5.1 · The build reaches the floats.
- A5.2 · Placement is ruled when one unit serves two sections.
- A5.3 · A section knows what to do when its own unit is not promoted.
  **Done when:** the trace in `### 1` shows every cited label resolving, and `### 5` states which of first-mention-wins or pinning this paper uses.

### P · 🏁 Page-level
- P1 · An adapter can be judged without reading its prose output.
  **Done when:** a delivered section is accepted or rejected on outline, paragraph order, and float positions alone.

## States

### A1 · 📥 Try it yourself: download what the two adapters just produced
- 🔨 A1.1 · Active. Both adapters were run on `S-Main-4-measurement.md` on 260803 and their output is downloadable from `### 1`; nobody has opened the `.docx` in Word yet, which is `A4.1`.

### A2 · What makes a rule a section rule
- ✅ A2.1 · Done 260802 when the two adapters were renamed off the word sentence, and held through the 260803 absorption.
- ⬜ A2.2 · Not started, and absorption is what makes it cheap: both loss lists now sit on one page, so the comparison is a read rather than a hunt.
- 🔨 A2.3 · Active. `### 5` arrived 🔴 and `### 1` now carries the trace that decides it.
- ✅ A2.4 · Done 260803. The admission test is now two questions, the Diagram lists the aggregate facts beside the sequence facts, and `### 2.3` names the source and the counter.
- ⬜ A2.5 · Not started, and it is the cheap half: the dashboard already prints a `floor` column with a `LOW` flag, but it transcribes a number for only 4 of the MISQ paper's 9 sections and nothing acts on the flag.
- ⬜ A2.6 · Not started. Measured 260803: 78 of the 95 `style.md` files carry a `## Word budget`.

### A3 · 📐 A section, delivered as LaTeX
- ⬜ A3.1 · Not started.
- ⬜ A3.2 · Not started.
- ⬜ A3.3 · Not started, and it is the cheapest real test on this page.

### A4 · 📝 A section, delivered as Word
- ⬜ A4.1 · Not started. The exporter ships as `haipipe-paper-to-word` 0.1.0, so only the human half is missing.
- ⬜ A4.2 · Not started, and it is a finding about the manuscript rather than about the adapter.
- ⬜ A4.3 · Not started.

### A5 · 📍 Where a float lands, and whether the build reaches it
- 🔨 A5.1 · Active, and measured again by `_tools/qbe-tests.py` on 260803: of 4 labels cited from the sections, 1 resolves and 3 compile to `??`, and two `\input` lines name files that do not exist, `displays/S-Display-4a-main-regression/float` and `displays/Table/table-gradient-results`. The gap this division was opened for is no longer that the master reaches nothing; it is that what it reaches is half wired. This is the only failing row in the harness.
- ⬜ A5.2 · Not started. `S-Display-1b` is the live two-consumer case.
- ⬜ A5.3 · Not started.

### P · 🏁 Page-level
- 🔨 P1 · Active. The criterion is written; nothing enforces it yet.

## Files

### 🗄 Archived · the faces this page absorbed on 260803
- `_archive/QBe3a-section-to-latex.md` · became `### 3`. Its measurements and history stay there rather than being rewritten.
- `_archive/QBe3b-section-to-word.md` · became `### 4`.
- `_archive/QBe3c-display-placement.md` · became `### 5`.

### 📏 The aggregate rule · where the number and the counter already live
- `../../paper/venue/playbook-*/<outlet>/<outlet>-<kind>/style.md` · `## Word budget`, the source. Read by the `2a-venue` stage, never written by this plugin.
- `../../paper/route/haipipe-paper-stage/section-stats.py` · the counter. `<S-page.md>` prints P, sentences and words per paragraph; `--dashboard <4-main>` prints the whole section set with a `floor` column and a `LOW` flag.
- `QBv1`–`QBv16` · one venue page each, and `QBv4` already rules that a venue page reports the pack's number and never asserts one of its own.

## Log

260803 · Answered JL's question "why does no section state a size". Added `### 2.3`, corrected the pack coverage to 78 of 95 after a recount, rewrote the admission test as two questions so the aggregate rule is admitted rather than misfiled to `QBe1`, added the aggregate block to the Diagram and the count commands to the `### 1` test sheet, closed A2.4 and opened A2.5 and A2.6.
260802 2205 · Opened the size gap as A2.4 on the page's previous path, `QB-delivery/QB11-delivery-section.md`; the 260803 absorption carried it here.
