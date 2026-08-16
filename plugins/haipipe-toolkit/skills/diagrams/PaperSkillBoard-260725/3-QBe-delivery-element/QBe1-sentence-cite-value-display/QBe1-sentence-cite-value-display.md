# Delivery-Sentence: Citation, Value, Display

state: 🟡 PARTIAL · the four types are on one page; two candidate shared rules are still unlifted and each type keeps open work
owner: JL
method: hold every rule whose unit is one sentence, and specify all four attachment types on one page, so a reader meets a marker and finds its rule without opening four pages

## Opening

What may hang off one sentence, and who is allowed to complete it?

A sentence is the smallest thing a reader can check. An attachment is evidence tied to it by a marker, such as `\cite{TOADD}` for a source or `{VAL:? 0.42}` for a number. Four types exist today and more may come. They share one grammar and differ only in who may finish them.

**Where this page sits**: `QBe2` holds the float as an object and `QBe3` holds the rules whose unit is a whole section.
This page is the rung below both: one sentence, and what a reader can verify about it without reading anything around it.

**Why one page and not five**: the four types were written under three different concerns, so their shared rules were each written once, on whichever type happened to need it first.
Two are already visibly series-wide: a marker resolves at BUILD time and never at page load, and staleness is COMPUTED and never declared.
Neither is about citations or tables in particular, and a reader could only find that out by reading four pages side by side.
On 260803 the four became `### 4` to `### 7` of this page, so the shared half is stated once above them and the differing half sits under its own heading.

**What differs between them**: only who may complete the marker, and what a wrong one costs.
A citation is the one type an agent may never complete alone, because the key comes from a bibtex entry only a human may write.
A value has the shortest path to a retraction, so it binds to the RUN rather than to a file.
A table pointer is checkable on sight, while a figure pointer built from the wrong column is invisible, which is why the panel rules sit in `### 7`.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `../BoardSkillBoard-260722/QPs-page-structure/QPs1-overall/QPs1-overall.md` and are not restated here.
Read `QB4 § Writing Style` first; everything below is what this page adds.

**Demonstrate before explaining**: `### 1` is a test sheet, and every type this page rules is a live marker somewhere below it.
A rule added here has to survive being shown on a real sentence on this page, not only described in prose.

**Name the parts, not the retired faces**: the citation, the value, the table pointer and the figure pointer are this page's `### 4` to `### 7`.
`### 4`` to `### 7``, and the older `QB12a` to `QB12d` and `QB3a`/`QB4a`/`QB5a`/`QB5b`, still resolve through `board.md`'s alias map, so old lines keep working; nothing new is written with them.

**The unit is one sentence, and the test is shuffling**: before writing a rule here, ask whether it still holds with the surrounding paragraphs reordered.
If it needs to know what came before, it is a section rule and belongs on `QBe3`.

**Name the four types, never count them**: write "a citation, a value, a table pointer, a figure pointer" rather than "the four attachment types".
A count becomes wrong the day a fifth arrives, and `QB4 §1` already forbids opening with a roster that will grow.

**A shared rule names the part it came from**: when a rule is lifted above `### 4`, say which type wrote it.
The provenance is what lets a later reader check whether it really generalizes, and lifting without it is how a three-of-four rule becomes a false four-of-four rule.

## Diagram

**The four attachments**: what each carries in the prose, in its lane, and on screen.

```text
   📝 PROSE                  🗂 LANE                👁 READER
   ───────────               ──────────             ────────────────
📚 `### 4`  \cite{TOADD}  ━━▶  source record    ━━▶  ❓ owed  · human-only key
🔢 `### 5`  {VAL:? 0.42}  ━━▶  run binding      ━━▶  📦 ready · bound to the RUN
📊 `### 6`  \ref{tab:x}   ━━▶  unit id          ━━▶  🥀 stale · computed, never declared
🖼 `### 7`  \ref{fig:y}   ━━▶  unit id          ━━▶  ⚠️ panel · worst state wins

🔑 one grammar: marker in prose · record in a lane · state computed at BUILD
⚡ they differ ONLY in who may complete the marker, and what a wrong one costs
🚫 never: a state a human has to remember to set
```

## Content

### 1 · Try it yourself: all four types, live on this page

**Before you click**: press `expand all` on `## Content`, because a chip inside a folded division is not painted, so a click on it lands on the page behind it and nothing opens. That is the first thing to check when a chip looks dead (measured 260803).

**The test sheet**: what is on this page to click, and what each one should open.

```text
🖱 CLICK THE CHIPS IN 1.1 TO 1.6 · every one is a real marker, resolved at BUILD
   1.1  a citation that resolves      the .bib entry as the .bst will print it
   1.2  a citation that is OWED       the probe question guarding the gap
   1.3  a citation that is BROKEN     it says so, instead of vanishing
   1.4  a value bound to a run        the run, and every hop back to it
   1.5  a pointer at a table          the table body itself, shown not linked
   1.6  a pointer at a figure         the picture, and its candidates

👀 THE STATE IS COMPUTED, NEVER DECLARED
   ✅ ok  ·  ❓ owed  ·  🥀 stale  ·  ⚠️ broken

🚫 THESE MUST REFUSE YOU
   an agent closing a ❓ citation by writing the bibtex entry itself
   a value chip printing a number with no answering run behind it
   any state a person has to remember to set
📥 OR DOWNLOAD THE EVIDENCE ITSELF · every chip above resolves against these
   _fixture/misq-slice.bib                      2.2 KB   the 6 entries a citation chip reads
   _fixture/.board-refs.bbl                     1.8 KB   the SAME entries as the .bst prints them
   _fixture/1-probes/PP01_seed-feasibility/QX1_novelty.md    the question an owed chip is waiting on
   _fixture/1-probes/PP03_results-values/QX1_opioid-reg-estimates.md   the run a value chip checks against
```

🧪 Establishes every rule below as something to click rather than read, which is the only test that catches a rule that sounds right and was never built.

#### 1.1 · ✅ A citation that resolves
(click the green chip; the panel opens over the prose and clicking away shuts it)
Trait measures predict consequential life outcomes across decades of evidence \citep{ozer2006personality}.
> Citation: ozer2006personality · source=bibliography · state=verified

#### 1.2 · ❓ A citation that is owed
(the amber chip; an agent may search for this key but may never write the `.bib` entry that closes it)
Whether perceived agreeableness predicts prescribing has not been tested against independent clinical behaviour \cite{TOADD} [Q-Seed-1].
> Citation: <reference> · doi=… · bib hits=0 · owed by [Q-Seed-1]

#### 1.3 · ⚠️ A citation that is broken, and looks identical in the source
(the red chip; nothing in the prose distinguishes it from 1.1, which is the whole reason the chip exists)
The first-stage F statistic sits below the conventional weak-instrument threshold \citep{nosuch2019missing}.

#### 1.4 · 🔢 A value bound to the run that produced it
(the number is the claim; the bracket beside it is the bookkeeping, and the two are never fused)
Crossing the CDC 90-MME daily threshold carries an odds ratio of {VAL:? the daily-MME>90 odds ratio} [Q-Section-2].

#### 1.5 · 📊 A pointer at a table
(click it and the rows arrive on this page; you never have to go and find the unit)
Cohort descriptives are reported in Table~\ref{tab:descriptives}.

#### 1.6 · 🖼 A pointer at a figure
(the same grammar, and a wrongness a reader cannot see, which is why `### 7` carries more apparatus than `### 6`)
The discretion gradient across the five cohorts is plotted in Figure~\ref{fig:discretion-gradient}.

#### 1.7 · The paragraph these types come from lives on `QC5`
(this page carries its own examples above, and its own sentences from that paragraph in `### 4` to `### 7`)
`QC5` holds one continuous paragraph with all four types, because a paragraph is where a reader meets markers in the wild.
Everything above is real prose against real evidence: `_fixture/` holds the `.bib`, the probe entries and the display units they resolve against.
If a chip above renders as grey text, the resolver did not find its record, and that is a defect to report rather than a state to interpret.

### 2 · The shared grammar

**One shape, four fillings**: the three parts every attachment has, whichever type it is.

```text
     ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
     │ 📝 MARKER    │──▶│ 🗂 RECORD    │──▶│ 👁 CHIP      │
     │ in the prose │   │ in its lane  │   │ on the page  │
     └──────────────┘   └──────────────┘   └──────────────┘
      author writes      probe or unit      build computes

  🔑 the join key `[Q-…]` sits BESIDE the marker, never fused into it

  📂 AND THE RECORD COMES FROM THE PAPER'S OWN STAGE FOLDER (JL 260803)
     📚 a citation  ━━▶  S03-literature/     the source, and who read it
     🔢 a value     ━━▶  S04-value/          the run, and what it produced
     📊🖼 a display  ━━▶  S05-display/        the unit, and whether it is accepted
     one type, one folder, and the marker is the only thing in the prose
```

🔑 Establishes the one grammar all four types obey, and the two rules already proven series-wide.

#### 2.1 · A marker resolves at build time, never at page load
(lifted from `### 4`, and it holds for all four because none of the four records live in the browser)
The chip a reader sees is computed while the page is generated, so what they read is what the repository held at that moment.
Resolving at page load would make the same page say different things to two readers, and neither could quote it.

#### 2.2 · Staleness is computed, never declared
(lifted from `### 6`, and it holds wherever the evidence can change without the sentence changing)
A state a human has to remember to set is a state that will be wrong.
The rule survives the harder case too: a re-render only stales a state, while renaming the units stales the WORDS a page used to name them.

#### 2.3 · Each type's record will live in the stage folder that owns it
(JL 260803, after the MISQ paper regrouped its lifecycle into `S01-opening` to `S10-round`)
The three parts of the grammar do not all live in the same place, and the middle one is moving.
A citation's record belongs to `S03-literature`, a value's to `S04-value`, and a display pointer's to `S05-display`, because each of those stages is what produces the evidence in the first place.
That is why this page rules one sentence and never the source behind it: the sentence carries the marker, and the stage folder carries the answer.
The retired `1-probes/PPNN_topic/` layout put all three in one place and hid that split.

#### 2.4 · What is not yet proven shared
(the honest gap, kept visible rather than assumed away)
`### 5`'s bracket rule and `### 7`'s worst-state-wins panel are each written on one face and look general.
Neither has been tested against the other three, so neither is lifted here yet.
A rule that turns out to hold for only three of the four stays on its face.

### 3 · What separates the four

**Who may finish it**: the one axis on which the four genuinely differ.

```text
  🧠 HUMAN ONLY            🤖 AGENT MAY COMPLETE
  ─────────────            ─────────────────────
  📚 citation              🔢 value      ━▶ binds to the RUN, not a file
   the key comes from      📊 table ref  ━▶ checkable on sight
   a bibtex entry only     🖼 figure ref  ━▶ ⚠️ a wrong column is INVISIBLE
   a person may write

  💥 cost of a wrong one   value ━━▶ retraction    figure ━━▶ silent
                           citation ━━▶ visible    table  ━━▶ visible
```

⚖️ Establishes why one grammar still needs four faces, and what each face must therefore specify alone.

#### 3.1 · Completion authority is the real split
(it decides what an agent may do unattended, which is the only thing the distinction is for)
A citation may be searched and verified by an agent but never invented or silently written.
The other three may be completed from evidence the repository already holds, so the difference is not difficulty but authority.

#### 3.2 · Visibility of a wrong one decides how much checking a face owes
(a defect a reader can see needs less apparatus than one they cannot)
A wrong table is checkable on sight, because the numbers are printed.
A plausible-looking plot built from the wrong column is not, so `### 7` carries the panel that names every asset and every candidate separately.

### 4 · A sentence with a citation

**What a citation carries**: the marker in the prose, the lane beneath it, and the chip a reader clicks.

A citation is the one attachment type an agent may never complete on its own. The key comes from a `.bib` entry that only a human writes, so the sentence has to be able to stand in a legitimate, visible, unfinished state for as long as that takes. Everything else about this type follows from that constraint.

[1/2] ONE CITATION, END TO END, AND THE FOUR SKILLS IT CROSSES

```
 ① the sentence is written                        `5-section-edit/`  (the stage)
    "…discretion rises when guidelines are ambiguous \cite{TOADD} [Q-Section-1]"
    the marker is LEGITIMATE here. The sentence may ship in this state.
                          │
 ② PROBE asks the bank                            `haipipe-paper-probe`
    writes 1-probes/PP04_discussion-citations/QX1_situational-strength.md
      ### q-consumer   Q-Section-1  ← the bracket, claimed
      ### bank binding route: discovery · target: …/QA/1-….md
                          │
 ⑦ the bank answers                               discovery / task layer
      ### a-executor   the reference, with identifiers
      state: answered │ read │ commissioned │ planned │ deferred
                          │
 ⑧ a HUMAN writes the .bib entry            ⛔ NO AGENT MAY DO THIS STEP
    the one hard stop in the chain, and the reason ⑦ can sit for weeks
                          │
 ③ REVISE places the key                          `haipipe-paper-revise-place`
    \cite{TOADD} [Q-Section-1]  ──►  \citep{meyer2010review}
                          │
 ④ the board resolves and shows state             `dialect_paper.py`  (build time)
```

Steps ① to ③ are the paper skill's.
Step ④ is the board's, and it only WATCHES: it never writes a marker, a probe entry, or a `.bib` line.
That split is `QA8`.

[2/2] WHAT THE READER GETS, AND WHERE THE SOURCE ACTUALLY IS

```
  \citep{Doyle2013PatientExperience}
        │  resolved at BUILD time, never at page load
        ▼
  ┌ 📚 Doyle2013PatientExperience ┐  ✅ ok        the chip, a real <button>
  └───────────────────────────────┘

        │  click  ·  native <div popover>  ·  still no script
        ▼
  ┌────────────────────────────────────────────────────────────┐
  │ CITE · OK          Doyle2013PatientExperience              │
  │ Doyle et al. · 2013 · A systematic review of evidence …    │
  │ ──────────────────────────────────────────────────────────│
  │ 📄 …MISQ2026.bib:1620    where the key is DEFINED          │
  │ 🔗 doi 10.1136/bmjopen-2012-001570    where the SOURCE is  │
  │ 🔗 bmjopen.bmj.com/content/3/1/e001570                     │
  │ ┌────────────────────────────────────────────────────────┐ │
  │ │ @article{Doyle2013PatientExperience,                   │ │
  │ │   author = {Catherine Doyle and Laura Lennox and …},   │ │  the entry
  │ │   journal = {BMJ Open}, year = {2013}, …               │ │  as written
  │ └────────────────────────────────────────────────────────┘ │
  └────────────────────────────────────────────────────────────┘

  a broken key answers the other question instead:
  ┌────────────────────────────────────────────────────────────┐
  │ CITE · BROKEN      stock2005testing              ⚠️         │
  │ NOT IN .bib — does not resolve and will compile to [?]     │
  │ keys that DO resolve, nearest first:  stock2002survey      │
  └────────────────────────────────────────────────────────────┘

 WHERE THIS PAGE'S EVIDENCE LIVES IN THE BOARD FOLDER
   the prose      `### 4`-sentence-citation.md  ## Content   (S1 S2 S3)
   the keys       _fixture/misq-slice.bib         6 real entries, copied
   the style      _fixture/misq.bst               that paper's own
   what prints    _fixture/.board-refs.bbl        GENERATED by refs.py
   the bracket    _fixture/1-probes/PP01_seed-feasibility/QX1_novelty.md
                    q-consumer Q-Seed-1 · state: read  → the chip is owed
   ⚠️ stock2005testing is ABSENT from the .bib, exactly as on the paper
```

📚 Establishes the whole of a citation: the marker in the prose, the `> Citation:` lane, the chip states, the panel a chip opens, and the human-only boundary. Absorbed from `QBe1a` on 260803; its full design history stays in `_archive/QBe1a-sentence-citation.md`.

#### What sits where
```
 in the sentence   \citep{key}                    the key EXISTS in the paper's .bib
                   \cite{TOADD} [Q-Section-n]     no key yet; the bracket names the
                                                  question that will produce one
 under it          > Citation: key · source=bibliography · state=verified
                   > Citation: <reference> · doi=… · bib hits=0 · owed by [Q-Seed-1]
```
Marker and bracket sit side by side and are never fused. A placeholder with no bracket is a hole no question will ever fill.

#### S1 to S3 of the paragraph on `QC5`
`QC5` carries one paragraph with all four attachment types. These are its first three sentences, the citation-bearing ones, written here and chipped by the same resolver against `_fixture/misq-slice.bib`:

The accommodation hypothesis predicts that perceived-agreeable physicians prescribe more opioids. Their interpersonal orientation leads them to accommodate patient preferences, particularly when clinical guidelines leave discretion \citep{graziano1996perceiving}.

The norm-adherence hypothesis predicts the opposite: agreeable physicians, motivated by prosocial concern, adhere more carefully to prescribing guidelines and resist patient pressure that could lead to harm \citep{thielmann2020personality}.

Whether either mechanism holds for prescribing specifically has not been tested against independent clinical behavior \cite{TOADD} [Q-Seed-1].

Two are `ok`: the key greps in the `.bib`. The third is `owed`, and the bracket beside it says why. Click any of them and the panel prints the reference as `_fixture/misq.bst` will actually set it, links the `.bib` line, and offers the doi.

The paragraph's other three sentences are the sibling pages': S4 the numbers is `### 5``, S5 the table is `### 6``, S6 the figure is `### 7``.

#### The one that is broken, and looks identical
`\citep{stock2005testing}` sits in `appendices/D_iv_analysis.tex` on this paper today and resolves to nothing, so it will compile to `[?]`:

The first-stage F falls below the Stock-Yogo critical value \citep{stock2005testing}.

Nothing in the source distinguishes it from the two green ones above. Its panel names the key that DOES resolve, `stock2002survey`, which is the same key a human already identified by hand and wrote into `S-Appendix-0-control.md` without the tex ever being changed.

#### The link row, and why a search sits in it
The panel's link row goes from strongest pointer to weakest, and the last one is a search rather than an identifier.

```
 📄 misq-slice.bib:25        WHERE IT IS DEFINED. the file and the line
 🔗 doi 10.1037/…            THE WORK. resolves to exactly one thing
 🔗 arXiv:2510.03997         THE WORK, preprint
 🔗 example.org/paper        whatever url the entry declared
 🔎 Scholar                  A SEARCH. can be wrong, and says so with its
                             own glyph rather than borrowing the 🔗
```

The query is the title in quotes plus the first author's surname, and deliberately no year: a preprint and its published version disagree by one, and the year is the field most likely to exclude the very result you wanted.

It earns its place on a count. Of the 216 entries in this paper's `.bib`, 21 carry a doi, an arXiv id or a url. The other **195 had no clickable pointer at all** until this row existed, so for nine entries in ten the panel could show you the reference and give you no way to go and read it. A search that might be wrong beats nothing to click, as long as the glyph does not claim otherwise.

It is offered only where there IS an entry. An `owed` chip's panel points at the question that will produce a key, not at a work, so searching from it would be searching for something nobody has named yet.

#### The human-only boundary
An agent may grep the `.bib` and may report that a key is missing. It may not write a bibtex entry.
This is not a style preference, it is the rule that keeps fabricated references out of the manuscript, and it is why `\cite{TOADD}` is a first-class state rather than an error.
On the MISQ paper this is live: three `> Citation:` lanes carry a reference, a doi, a `.bib` hit count of zero, and the owed `[Q-Seed-1]` bracket, waiting on a human.

#### Chip states
```
 ✅ ok         \citep{key} and the key greps in the .bib
 ✦ ready      \cite{TOADD} whose [Q-…] question has ANSWERED; a human still
               has to write the bibtex entry, which is why this is not ok
 ⏳ owed       \cite{TOADD} beside a [Q-…] still in flight
 ⚠️ broken     \citep{key} but the key does not grep: a real defect, never silent
 ❓ unowned    a placeholder with no bracket, or a bracket no probe declares
```

#### Where the panel points, and what "the source" means
"Link to the source" turned out to be two different questions, and the panel answers both (JL 260726).

```
 📄 the DEFINITION   0-Personality-Opioid-MISQ2026.bib:1620
                     which file, which line. Answers "does this key exist"
                     and "who wrote this entry" without a grep.
 🔗 the SOURCE       doi 10.1136/bmjopen-2012-001570  ·  bmjopen.bmj.com/…
                     the actual work, off-site. From the entry's own
                     doi / eprint / url fields, in that order.
 📋 the ENTRY        the raw bibtex, as written
                     answers "is this the right paper" in the panel itself.
```

A `.bib` line has no anchor a browser can jump to, so the line number is printed rather than linked into. That is a deliberate stop, not an oversight: making it jumpable would mean the board serving a rendered view of the `.bib`, and the `.bib` is human territory.

On the MISQ paper 21 of 216 entries carry a doi, eprint, or url, so most panels show the definition and the entry and no off-site link. That is a property of the bibliography, not of the panel.

#### A broken key is asked the more useful question
When a key does not resolve, saying so is only half an answer. The panel also lists the keys that DO resolve, nearest first, matched on the author run rather than on plain string distance: `stock2005testing` against `stock2002survey` scores about 0.6 and falls off a default fuzzy cutoff, which is exactly the case that matters. Bibtex keys are author-year-word, so the author run is the strong signal.

It suggests and never substitutes. Choosing the key is a claim about what the sentence rests on, and that is the human's.

#### How it resolves: build time, and `title=` is the floor
The trap is doing this in JavaScript. The board asserts that stripping every script block leaves the substance intact, so evidence resolved at page load would vanish under that test.

```
 tier 0   NO script     title="Meisenberg et al. · 2018 · Assessment of opioid
                              prescribing practices · JAMA network open"
                        a NATIVE browser tooltip. Hover already works.
 tier 1   CSS only      the chip's icon and colour carry the STATE
 tier 1b  native HTML   CLICK the chip, an anchored panel opens beside it
                        <button popovertarget> + <div popover>. Still no script.
 tier 2   script        may upgrade it further, may never be the only copy
```

#### Why the panel, and not just the tooltip (JL 260726)
A tooltip lives in an ATTRIBUTE. The build's assertion counts "chars of body surviving with JS stripped", and an attribute is not body, so the record was passing that test on a technicality: strip the scripts and the evidence was technically still in the file, but not in anything the check measured or a reader could search or print.

Moving the record into a `<div popover>` makes it real body text. The page grew by 42k on the MISQ board, and that growth IS the evidence finally being counted.

`title=` stays underneath, unchanged. The panel is the upgrade, never the only copy, which is the same rule tier 2 was always held to.

The index is built once per build by `src/dialect_paper.py`, which a board opts into by declaring `dialect: paper` and `paper-root:` in its own header. A board that does not declare it never pays for any of this, and `haipipe-board` learns nothing about papers unless asked.

#### What it refuses to touch
A page that DISCUSSES placeholders writes `\cite{TOADD}` in backticks. Chipping that turns documentation into a false defect report, which it did on the first run: five of the reported holes were prose about holes. The rewriter now skips anything inside a code span or inside a tag's attributes.

The same trap has a second floor, and the first version fell through it. A human writing

```
 > JL: I think you should use \citep{xxx}
 > CC (REVISE 07-10): Mafi 2013 is the open decision -> add \citep{mafi...}
```

is ASKING for a citation, not making one. Both got chipped `broken`, and both were reported as this page's headline finding on 260726. They were the only two, so the page claimed a payoff it had not earned.

Backticks are optional in a comment and nobody will remember them, so the rule is now structural: a DISCUSSION lane (`> JL:`, `> CC:`, and `## Comments`) never chips. A TYPED evidence lane (`> Citation:`, `> Value:`, `> Display:`) still does, because those are claims about the sentence and their state is the whole point.

#### What a chip can never see
A chip exists only where the board RENDERS text, and the board renders its faces. `sections/*.tex` is the actual manuscript and is reached only when a face embeds it. So the one genuinely broken key in this paper, `\citep{stock2005testing}` in `appendices/D_iv_analysis.tex:30`, was invisible while two false positives sat on the board wearing its colour.

`dialect_paper.audit()` now walks the `.tex` directly and `build.py` prints what it finds, labelled as NOT rendered here. That is deliberately a build warning and not a chip: pretending the board covers the manuscript would be the same mistake in a new place.

### 5 · A sentence with a value

**What a value carries**: the number, the bracket naming its question, and the run it must still match.

A value is the attachment type with the shortest path to a retraction. A citation that is wrong is embarrassing; a coefficient that silently changed after a re-run is a false claim in a published paper. So the binding here is not to a source document but to a RUN, and the state that matters is whether the prose still matches the run it came from.

```
 A VALUE BINDS TO A RUN, NOT TO A FILE. THE PATH IS REUSED.

   the sentence   …at a mean absolute error of {VAL:? the deployed
                  model's MAE} [Q-Section-4]
                       ╰─ what is WANTED ─╯  ╰─ who owes it ─╯
                                │
                                │  ONE resolver, shared with `### 4`
                                ▼
   1-probes/PP03_results-values/QX1_opioid-reg-estimates.md
     ### q-consumer    Q-Section-4  ◄ the bracket, claimed
     ### bank binding  route: task · target: tasks/Z01/QA/1-….md
     ### a-executor    coef 12.90242, SE 3.676822, p 4.50e-04, N 765,701
                                │
   under the sentence           ▼
     > Value: main-beta · source=tasks/…/source_data.csv
              · run=<run id> · state=verified
              ╰── the RUN, because the same path holds a different
                  number tomorrow ──╯

 CHIP STATES, ORDERED BY DISTANCE FROM THE PROSE
   ✦ ready    the probe LANDED and the sentence still says {VAL:?}
              nobody's fault, and still costs the paper something
   ⏳ owed     read / commissioned / planned — nothing to weave yet
   ⏸ parked   DEFERRED on purpose at a cost ceiling, not forgotten
   ⚠️ broken   the probe claims answered and a-executor is EMPTY
   ❓ unowned  no bracket, or a bracket no probe entry declares

 LIVE ON MISQ, 260726        ✦13   ⏸11   ❓1

 THE STATE THAT HAS NO CHIP, AND IT IS THE WORST ONE  ⚠️
   a bare numeral typed straight into prose.
   no marker ──► no chip ──► no colour ──► invisible.
   Indistinguishable from a correct one until someone tries to
   reproduce it. Every other state on this page is now visible;
   this one is invisible BY CONSTRUCTION.

 WHERE THIS PAGE'S EVIDENCE LIVES IN THE BOARD FOLDER
   the prose      `### 5`-sentence-value.md  ## Content   (S4)
   the bracket    _fixture/1-probes/PP03_results-values/QX5_binary-exposure-flags.md
                    q-consumer Q-Section-7 · state: answered
   the digits     the same file's ### a-executor
                    +0.0045 · +0.0009 · the figures each chip is checked against
   the chain      probe → bank QA file → run folder, opened by the panel
```

🔢 Establishes the whole of a value: the marker, the `> Value:` lane, the bracket that joins it to a question, and staleness against the producing run. Absorbed from `QBe1b` on 260803; its full design history stays in `_archive/QBe1b-sentence-value.md`.

#### What sits where
```
 in the sentence   the real number, once it has landed
                   {VAL:? what the number is} [Q-Section-n]   before it lands
 under it          > Value: main-beta · source=tasks/C04/.../source_data.csv
                            · run=<run id> · state=verified
```
The `{VAL:?}` marker carries a description of what is wanted, not a guess at it. Never invent a number to avoid a placeholder.

#### S4 of the paragraph on `QC5`
`QC5` carries one paragraph with all four attachment types. This is its fourth sentence, the one that measures something, written here and checked against `QX5_binary-exposure-flags.md`:

Physicians flagged as high-agreeableness are more likely to write a high-dose or long-duration prescription (+0.0045, p = 0.007) and to exceed the CDC high-risk level of 90 MME per day (+0.0009, p < 0.001) [Q-Section-7].
> Value: is_high_mme_daily · probe=`QX5_binary-exposure-flags.md` · run=v0618 · state=verified

`+0.0045`, `90` and `+0.0009` are each green because each appears in the run behind `[Q-Section-7]`, which is the fourth chip. Click any of them and the panel opens the probe entry, the bank's answer and the run folder. `p = 0.007` and `p < 0.001` are deliberately NOT chipped: a number after a comparison is a bound, not a measurement.

The paragraph's other sentences are the sibling pages': S1 to S3 the citations are `### 4``, S5 the table is `### 6``, S6 the figure is `### 7``.

#### The case this page exists for
One digit changed in that fourth sentence, nothing else:

Physicians flagged as high-agreeableness are more likely to exceed the CDC high-risk level of 90 MME per day (+0.0019, p < 0.001) [Q-Section-7].

`+0.0019` renders grey and dotted, `unver`. Note what that does and does not claim: the chip cannot call it WRONG, because an unmatched figure may equally be derived. What it does is make the difference visible between `+0.0009`, which matched a recorded figure, and `+0.0019`, which matched nothing, in a sentence where the prose showed no difference at all.

#### Evidence enters through one door
A paper stage may not compute. The number arrives through PROBE, from a task or discovery answer, and the lane records which one.
That is why the lane names a run and not just a file: the same path can hold a different number tomorrow.

#### The bracket is the join key, and it is not value grammar
Building this slice turned up the thing that actually matters here. `[Q-Section-4]` is not part of the value marker and not part of the citation marker. It is the paper's ONE pointer from a sentence to the question that owes it, and it resolves in exactly one place:

```
 prose         {VAL:? the deployed model's MAE} [Q-Section-4]
               \cite{TOADD}                     [Q-Section-4]
                       │  same bracket, one resolver
                       ▼
 1-probes/PPnn_*/QXn_*.md
   ### q-consumer   the sentences this entry serves, by bracket id
   ### bank binding  route · bank · target · state
   ### a-executor    the harvested answer, or empty
```

So the resolver was built once, on the bracket, and both `### 4`` and `### 5`` consume it. Three citation chips that yesterday could only say "owed" now say the answer landed.

Two decorations are in live use for the q-consumer bullet (`* **Q-Section-2**: …` in `PP03`, `- Q-Section-1 (§7.2): …` in `PP04`), so the resolver reads the ID and ignores the bullet. Tightening that grammar is not worth a migration.

#### `answered` is checked, never believed
A probe entry may carry `state: answered` while its `### a-executor` block is empty. From the prose side that reads as done and is not, so the chip verifies the block before it agrees. `read` is the honest name for that condition when the entry admits it: the bank answers, and nothing has been harvested into the entry yet.

#### Chip states as built
Ordered by distance from the prose, which is the only ordering a writer cares about.

```
 ✦ ready     the answering probe LANDED and the sentence still says {VAL:?}
             not an error and not fine: work sitting on the table
 ⏳ owed      the probe is read / commissioned / planned, nothing to weave yet
 ⏸ parked    the probe is DEFERRED on purpose at a cost ceiling, not forgotten
 ⚠️ broken    the probe claims answered and its a-executor block is empty
 ❓ unowned   no [Q-…] bracket at all, or a bracket no probe entry declares
```

`ready` earns its own colour because it is the only state that is nobody's fault and still costs the paper something: the evidence exists and the manuscript has not caught up.

#### The number is the claim; the bracket is the bookkeeping
The first build had the emphasis backwards, and JL caught it on `S-Main-7` (260726):

```
 before   …(odds ratio 1.21, p < 0.001) [Q-Section-2]
                                         ▔▔▔▔▔▔▔▔▔▔▔  the pointer was loud
 after    …(odds ratio 1.21, p < 0.001) [Q-Section-2]
                          ▔▔▔▔  ▔▔▔▔▔                  the FIGURE is loud
```

A reader checks the number. The bracket is still there and still clickable, demoted to a quiet trailing marker, because it remains the binding. This closes the "unbound number" item in the only way that was ever going to work: a bare numeral gets no marker of its own, but a numeral in a sentence that ALREADY names its question can be chipped by inheriting that binding.

#### The chip opens the whole chain, not just the probe
JL 260726: "include the Probe folder, and the task folder for each value". A number chip's panel now carries every hop between the sentence and the run:

```
 ⑧ the sentence      …(odds ratio 1.21, p < 0.001) [Q-Section-2]
 ⑦ probe             1-probes/PP03_results-values/QX5_binary-exposure-flags.md
                     the paper's binding: which question, and its state
 ② answer            tasks/Z01_Display_PhyTraitOpioid/QA/4-binary-exposure-flags.md
                     the bank's harvested answer
 ① run               tasks/Z01_Display_PhyTraitOpioid/
                     where it was actually computed
```

This is the provenance chain now ruled at `QD1@display` and `QB2@display` applied to a value rather than a display, and it makes the number the entry point to its own audit. Each link is offered only if the path really exists: a link that 404s is worse than no link, because it looks like provenance.

The `target:` a probe records is written relative to the PROJECT, not the paper, so the bank root is found by walking up for the folder that actually holds `tasks/` or `discoveries/` rather than assuming a depth.

An ambiguous number links EVERY probe involved, so both candidate runs are one click apart and the reader can settle it.

#### What a number chip actually checks
Not that it looks like a number. That it appears in the run the sentence points at.

```
 ✓ ok        one recorded figure rounds to it. The tooltip names the figure
             and quotes the line it came from.
 ⁉ amb       TWO OR MORE DIFFERENT recorded figures round to it, so the prose
             cannot identify which run it came from
 ? unver     no recorded figure rounds to it. NOT an error: a derived
             percentage or a chosen threshold will never appear in a run
 ❓ unowned   the sentence's bracket names a question no probe declares, so
             nothing can check any of its numbers
```

Matching is numeric and precision-aware rather than string equality, because the prose rounds: `1.21` has to match a recorded `1.21494`, so the recorded figure is rounded to the prose's own decimals before comparing.

Two things are deliberately NOT checked. A number after a comparison is a bound, not a measurement: `p < 0.001` never claimed the figure equals a thousandth, and checking it found every recorded p-value below one and called the sentence ambiguous. And the tooltip says whether a match came from the probe's `### a-executor` block or from its question text, because a threshold the question named is weaker evidence than a figure the run returned.

`unver` is deliberately quiet, with no alarm colour. Asserting a defect on every unmatched number would make the feature worthless within a day, because most sentences carry at least one derived or definitional figure. Only a MATCH is an assertion; everything else says it was not checked.

#### `amb` came out of a bug worth keeping
The first version returned the FIRST recorded figure that matched. On JL's own sentence it reported `1.21 MATCHES the run (recorded as 1.20879)`, which is the lower bound of a 95% CI on the CONTINUOUS exposure. The sentence means `1.21494`, the odds ratio on the BINARY exposure. The number in the prose is right; the provenance the chip asserted was wrong, which is precisely the failure this page exists to prevent, committed by the thing built to prevent it.

So a match is now collected over DISTINCT values rather than occurrences. One value is a match. Two different values are an ambiguity, and both are named. That `1.21` is ambiguous is not a false positive: the same probe folder carries a recorded contradiction about which trait form that logit used, and a reader cannot tell from the sentence alone.

#### What the panel carries
The rendered value, its unit, the source path, the producing run, and the verification state.

### 6 · A sentence with a Display · table

**What a table pointer carries**: a stable display id, and the rows the panel shows without leaving the page.

A table is two things with two owners. The numbers are computed by the task layer and land as `source_data.csv` with provenance. The framing, which rows and columns the argument needs, the venue formatting, and the caption, belongs to the paper. A sentence points at the unit, not at either half, which is what lets the numbers be re-run without touching a word of prose.

```
 A TABLE IS TWO THINGS WITH TWO OWNERS, AND THE SENTENCE
 POINTS AT NEITHER HALF

   the sentence           …the effect concentrates in low-back pain
                          (Table~\ref{display08})
                                   │  a STABLE ID, never a filename
                                   ▼
   ┌ display08 ─ the UNIT ─────────────────────────────────────┐
   │                                                           │
   │  TASK layer owns          PAPER owns                      │
   │  source_data.csv          which rows and columns the      │
   │  + provenance             argument needs                  │
   │  the numbers              venue formatting                │
   │                           the caption                     │
   │                           \label / \ref wiring            │
   └───────────────────────────────────────────────────────────┘
   under the sentence
     > Display: display08 · target=S-Display-8 · kind=table
              · state=rendered

 WHY THE ID AND NOT THE FILE
   the id survives a re-render, a candidate promotion, a citation
   style and an output format. So the numbers can be RE-RUN without
   touching a word of prose. A Section never names
   table3-main-results.tex.

 CHIP STATES
   ✅ rendered    the unit exists and its source data is current
   ⏳ requested   a row exists for it; nothing built
   ⚠️ stale       built, but the source data has been RE-RUN since
   ⚠️ orphan      the sentence names an id no unit owns

 THE DEFECT THIS EXISTS TO PREVENT
   hand-typing a number into the unit's .tex.  It looks identical
   and it has cut the link back to the run that produced it.

 WHY A TABLE IS NOT A FIGURE (and `### 7` is a separate face)
   the panel shows the ROWS, not a thumbnail of them: a table's evidence
   IS its numbers, so the reader can check the claim on sight.

 WHERE THIS PAGE'S EVIDENCE LIVES IN THE BOARD FOLDER
   the prose      `### 6`-sentence-display-table.md  ## Content   (S5)
   the unit       _fixture/displays/display05-descriptives/
     float.tex              \label{tab:descriptives}   ← what \ref{} greps
     assets/table-body.tex  the ROWS the panel prints
     source/REBUILD.md      no source_data.csv here, so no staleness to show
```

📊 Establishes the whole of a table pointer: the stable display id, the two halves and their owners, and what the panel shows. Absorbed from `QBe1c` on 260803; its full design history stays in `_archive/QBe1c-sentence-display-table.md`.

#### What sits where
```
 in the sentence   a stable display id, projected as \ref{} in LaTeX
 under it          > Display: display08 · target=S-Display-8 · kind=table
                            · state=rendered
```
The id survives a new rendering, a candidate promotion, a citation style, and an output format. A Section refers to `display08`, never to `table3-main-results.tex` or a candidate filename.

#### S5 of the paragraph on `QC5`
`QC5` carries one paragraph with all four attachment types. This is its fifth sentence, the one that sends the reader to a table, written here and resolved against `_fixture/displays/display05-descriptives/`:

Operationalization details and descriptive statistics for all variables are presented in \ref{tab:descriptives}.
> Display: display05 · target=S-Display-5 · kind=table · state=rendered

Two chips, one unit. The sentence writes `\ref{tab:descriptives}`; the lane writes `display05`. Both resolve to `display05-descriptives`, as would its folder name: three ways to name one unit, one resolver. Click either and the panel shows the table's ROWS, so a number in a sentence can be checked against the row it came from without leaving the page.

The paragraph's other sentences are the sibling pages': S1 to S3 the citations are `### 4``, S4 the numbers is `### 5``, S6 the figure is `### 7``.

#### A reference that resolves to nothing, and reads the same
`\ref{tab:cohort-descriptives}` is cited in `sections/05_data_variables.tex:112` on this paper and matches no `\label` anywhere, so it compiles to `??`:

Cohort composition is reported in \ref{tab:cohort-descriptives}.

One hyphenated word longer than the one that works, and nothing in the prose says so.

#### The two halves and their owners
```
 bank deliverable    source_data.csv + provenance     the TASK layer computes it
 consumer deliverable which rows and columns the       the PAPER frames it,
                     argument needs, venue format,     and owns the caption
                     \label / \ref wiring
```
A reference naming only one half is incomplete. Hand-typing a number into the unit's `.tex` is a defect, because it breaks the link back to the run.

#### Chip states as built
```
 ✅ ok         the unit is built and its source data is not newer than it
 ✦ ready      a candidate is waiting while assets/ still holds the old one
 ⏳ owed       the unit folder exists and assets/ is EMPTY
 ⚠️ broken     STALE: source_data.csv is NEWER than the built asset, so the
               manuscript is showing numbers the data no longer says
 ❓ unowned    the id, or the \ref{} label, resolves to nothing
```
Staleness is computed rather than declared: the mtime of `source/source_data.*` against the newest file in `assets/`. Nobody has to remember to mark it, which is the only way a stale state ever gets reported.

#### Three ways a face names a display, and all three resolve
```
 display04                  the SHORT id. What the S-Display faces actually
                            write: "kind: table · registry id display04"
 display04-main-regression  the LONG id, folder-shaped. What a Section writes.
 \ref{tab:results}          the LaTeX form, resolved through the unit's own
 `tab:results`              float.tex \label{}. Backticked or bare.
```
The kind comes from `\begin{table}` in that same `float.tex`, which is why the chip can put a table icon on one and a figure icon on the other without being told.

#### The panel as built
Click a display chip and the panel gives the unit id, its kind, its `\label`, the state sentence, the README's Reader Takeaway, and a link row: `float.tex`, `README`, `source_data.csv`, every asset, and every waiting candidate, plus the Placement line.

The table body IS shown, not linked (JL 260726): `_fixture/displays/display05-descriptives/assets/table-body.tex` renders in the panel, first 40 lines with a count of what was cut. That is what this page meant by "a preview of the table itself, not a thumbnail of one": a reader checking whether a sentence's claim matches the rows can do it without leaving the page.

It shows the LaTeX source rather than typeset rows. For a `booktabs` body that is readable enough to check a coefficient against a sentence, which is the job; typesetting it in the browser would mean the board rendering LaTeX, and that is a different project.

### 7 · A sentence with a Display · figure

**What a figure pointer adds**: candidates, promotion, and a wrongness the reader cannot see.

Mechanically, nothing: both are display units behind a stable id. The difference is what a reader can verify. A table shows its numbers, so a wrong one is checkable on sight. A figure shows a rendering, and a plausible-looking plot built from the wrong column is invisible. A figure also has candidates in a way a table rarely does, so the id has to keep pointing at the same unit while the picture behind it changes.

```
 MECHANICALLY IDENTICAL TO A TABLE. VERIFIABLY, THE OPPOSITE.

   a TABLE            shows its numbers
                      a wrong one is checkable ON SIGHT
   a FIGURE           shows a rendering
                      a plausible plot built from the WRONG COLUMN
                      is invisible                             ⚠️

 CANDIDATES ARE THE OTHER DIFFERENCE

   the sentence   …the gradient is monotone (Figure~\ref{display02})
                          │  the id must not move
                          ▼
   ┌ display02 ─ the UNIT ────────────────────────────────────┐
   │  candidates/  a  b  c ◄live   d                          │
   │  promoted:    no                                    ⚠️    │
   │  the picture behind the id CHANGES; the id does not      │
   └──────────────────────────────────────────────────────────┘
     > Display: display02 · target=S-Display-2 · kind=figure
              · state=candidate-c · promoted=no

 LIVE ON MISQ RIGHT NOW (re-read 260727 evening, AFTER the id regroup)
   S-Display-4c   candidate C-enriched rendered, awaiting promotion
                  ── the unit this page calls display02 throughout; the
                     MISQ ids were regrouped twice on 260727, see Content
   S-Display-1b   PROMOTED, and it is the case this page wanted: candidate H
                  is live as a VECTOR assets/figure.pdf and the raster it
                  replaced is preserved as candidates/G-codex-4panel.png
   a sentence citing 4c today is citing something about to change; a
   sentence citing 1b is citing something that changed TWICE in one day.

 CHIP STATES
   ✅ promoted    the live asset IS what the argument was written against
   🟡 candidate   rendered, not promoted: the prose may be describing a
                  picture that will not ship        ◄ no table equivalent
   ⏳ requested   a row exists; nothing rendered
   ⏸️ folded      merged into another unit (S-Display-3 into Figure 2)
   ⚠️ orphan      the sentence names an id no unit owns

 THE CARD'S ONE OBLIGATION
   a thumbnail is a PREVIEW, never the evidence. The card must name
   WHICH CANDIDATE it is showing, or it reassures the reader about
   the wrong picture.

 WHERE THIS PAGE'S EVIDENCE LIVES IN THE BOARD FOLDER
   the prose      `### 7`-sentence-display-figure.md  ## Content   (S6)
   the unit       _fixture/displays/display02-discretion-gradient/
     float.tex                    \label{fig:discretion-gradient}
     assets/figure.png            LIVE, what the manuscript compiles
     candidates/C-enriched.png    WAITING, and why the chip is amber
   both pictures are in the panel; neither tells you it used the right column
```

🖼 Establishes what a figure pointer adds over a table pointer: candidates, promotion, and a wrongness a reader cannot see. Absorbed from `QBe1d` on 260803; its full design history stays in `_archive/QBe1d-sentence-display-figure.md`.

#### What sits where
```
 in the sentence   a stable display id, projected as \ref{} in LaTeX
 under it          > Display: display02 · target=S-Display-2 · kind=figure
                            · state=candidate-c · promoted=no
```

#### S6 of the paragraph on `QC5`
`QC5` carries one paragraph with all four attachment types. This is its last sentence, the one that sends the reader to a figure, written here and resolved against `_fixture/displays/display02-discretion-gradient/`:

The association concentrates in the cohorts where the physician has prescribing latitude and flattens where opioids are protocolized (\ref{fig:discretion-gradient}).
> Display: display02 · target=S-Display-2 · kind=figure · state=candidate-C · promoted=no

Two chips, one unit, and both amber. Click either and the panel shows BOTH pictures, captioned LIVE and CANDIDATE, because `_fixture/displays/display02-discretion-gradient/assets/figure.png` is what the manuscript compiles while `_fixture/displays/display02-discretion-gradient/candidates/C-enriched.png` is what is waiting. These are the real files, and the amber says the prose may be describing a picture that will not ship.

The paragraph's other sentences are the sibling pages': S1 to S3 the citations are `### 4``, S4 the numbers is `### 5``, S5 the table is `### 6``.

#### Why this is not `### 6`` with a different file extension
Look at the two display chips in that one paragraph. `### 6``'s table puts its ROWS in the panel, so a wrong number is checkable on sight. This one puts two PICTURES in the panel: you can see that both exist and which is live, and you still cannot tell from either image whether it was built from the right column. Same grammar, same resolver, same lane, and a reader's ability to check collapses. That asymmetry is the whole reason these are two faces rather than one.

#### A reference that resolves to nothing
`\ref{fig:agreeableness_dist}` is cited in `sections/05-2_data_construction.tex:152` on this paper and matches no `\label`:

The trait distribution is shown in \ref{fig:agreeableness_dist}.

#### Candidates are the difference
A figure unit typically holds several candidates and one promoted asset.
The sentence must keep referring to the unit while the candidate behind it changes, and the lane must say which candidate is live and whether it has been promoted.
This is live on the MISQ paper right now: `S-Display-2` sits at "candidate C rendered, awaiting promotion" and `S-Display-1B` at "v1 live, candidate E awaiting promotion". A sentence citing either one today is citing something that is about to change.

#### The MISQ ids in this page were renamed twice on 260727
This page cites the MISQ paper as its live example, and that paper's display registry moved under it twice in one day. Pass 1 renumbered the units to reading order in the morning. Pass 2, in the evening, regrouped them into BLOCK plus MEMBER, where the number is the narrative block a unit serves and the letter is its position inside that block.

```
 what this page says      pass 1 (morning)       live id (evening)      unit
 ──────────────────────   ────────────────────   ────────────────────   ──────────────────────
 S-Display-2              S-Display-8            S-Display-4c           discretion gradient
 S-Display-3              S-Display-9            S-Display-2c           llm measurement, folded
 S-Display-4              S-Display-6            S-Display-4a           main regression
 S-Display-5              S-Display-4            S-Display-3b           cohort descriptives
 S-Display-7              S-Display-7            S-Display-4b           context regression
 S-Display-8              S-Display-5            S-Display-3c           variable operationalization
 S-Display-9              S-Display-2            S-Display-2a           agreeableness distribution
 S-Display-10             S-Display-3            S-Display-2b           validation summary
 S-Display-11             S-Display-10           S-Display-3a           inclusion funnel, no folder
 S-Display-1A / 1B        unchanged              S-Display-1a / 1b      the pinned pair, block 01
```

Two things about this table are the point rather than the bookkeeping. The `_fixture/` ids on this page are NOT in it and were deliberately left alone: the fixture is this board's own frozen evidence, so its `display02-discretion-gradient` stays what it is no matter what the paper does. And the historical rows in Items and Log keep the ids they were written with, because a record rewritten to today's names stops being a record. Only LIVE ROUTES were repointed, which is the `## Files` block below.

#### Chip states as built, and the five this page first proposed
```
 what this page      what a chip        why
 first proposed      actually renders
 ─────────────────   ────────────────   ──────────────────────────────────
 ✅ promoted          ✅ ok              the live asset IS what the argument
                                        was written against
 🟡 candidate         ✦ ready           a candidate is rendered and not
                                        promoted: the prose may be describing
                                        a picture that will not ship
 ⏳ requested         ⏳ owed            the unit folder exists, assets/ is empty
 ⏸️ folded            —                  no detector; nothing computes it yet
 ⚠️ orphan            ❓ unowned         the id, or the \ref{} label, resolves
                                        to nothing
```
Same five rows as `### 6`` except `candidate`, which the table page has no equivalent for and which is the state most likely to produce a sentence that quietly stops being true. Two rows are worth reading twice: `promoted` and `candidate` collapsed into states `### 5`` had already built, for the reason below, and `folded` is still only a word on this page.

#### The panel as built
The chip carries the unit id, its kind, its `\label`, the state sentence, the README's Reader Takeaway, and a link row that names **every asset and every candidate separately**, so the panel cannot be read as showing one picture when another is live.

The picture is SHOWN, not linked (JL 260726). A figure's evidence is the image, so linking to it and calling that a preview was never the right shape.

```
 ┌ disp fig · broken     display02 ──────────────────────────┐
 │ STALE — source_data.csv was re-run AFTER figure.pdf …     │
 │ It ALSO has 2 candidate(s) waiting                        │
 │                                                           │
 │  LIVE · figure.png            ← what the manuscript shows │
 │  ┌───────────────────────┐                                │
 │  │      [the picture]    │                                │
 │  └───────────────────────┘                                │
 │  CANDIDATE · C-enriched.png   ← what is waiting           │
 │  ┌───────────────────────┐                                │
 │  │      [the picture]    │                                │
 │  └───────────────────────┘                                │
 └───────────────────────────────────────────────────────────┘
```

Both are shown, each captioned LIVE or CANDIDATE, which is this page's own rule made structural: the card cannot show one picture while another is what compiles, because it shows BOTH and names them. That turns `display02` from a sentence about staleness into a side-by-side you can just look at.

A `.pdf` asset cannot be an `<img>`, so a unit holding only a PDF still shows nothing and its links row says where the file is. Images are referenced and `loading="lazy"`, never embedded as data URIs, so the page carries no image weight until a panel opens.

#### `candidate` and `ready` turned out to be one state
`### 7`` proposed 🟡 `candidate` and `### 5`` had already built ✦ `ready`. Building this made it obvious they are the same fact in two vocabularies: something landed, and the manuscript has not caught up. A landed probe answer under a `{VAL:?}` and a rendered candidate under a stale `assets/` are the same colour of problem, so they are the same colour of chip.

## Aims

### A1 · 🧪 Try it yourself: all four types, live on this page
- A1.1 · Every type this page rules is clickable on this page.
  **Done when:** a reader opens a citation, a value, a table and a figure panel from `### 1`'s list without leaving the page.

### A2 · The shared grammar
- A2.1 · The rules that hold for all four types are stated once, above `### 4`, with the type each came from.
  **Done when:** the build-time rule and the computed-staleness rule appear in `### 2` with their provenance, and no division below repeats the general statement.
- A2.2 · Every candidate shared rule has been tested against all four types before being lifted.
  **Done when:** the bracket rule from `### 5` and the worst-state-wins rule from `### 7` each carry a written verdict in `### 2`: general, or type-specific and why.

### A3 · What separates the four
- A3.1 · The completion-authority split is stated once and not re-argued under each type.
  **Done when:** each of `### 4` to `### 7` names its completion authority in one line and points at `### 3` for the reasoning.

### A4 · 📚 A sentence with a citation
- A4.1 · `unowned` stops conflating three different failures.
  **Done when:** a key that is absent, a key that is malformed, and a key that resolves outside the bib each render as their own state.
- A4.2 · The card schema is defined rather than implied by what the renderer happens to emit.
  **Done when:** one written schema names every field a citation panel may carry, and the renderer is checked against it.
- A4.3 · A key that resolves is not reported as a claim that was checked.
  **Done when:** the panel distinguishes "this key exists" from "a person read this source and it supports the sentence".

### A5 · 🔢 A sentence with a value
- A5.1 · A `{VAL:?}` written inside prose ABOUT markers stops being chipped as a real placeholder.
  **Done when:** a marker inside a code span or an apparatus lane is documentation, and the resolver treats it as such.
- A5.2 · Staleness is defined for a number rather than assumed from the display rule.
  **Done when:** the page states which file's mtime, or which run id, decides that a number no longer matches its run.
- A5.3 · A number written with no bracket is found rather than trusted.
  **Done when:** the audit lists every numeral in a gated section that carries no question id, and each is either bracketed or ruled prose.
- A5.4 · The four unowned brackets on the live paper are closed.
  **Done when:** each bracket names a question that exists, or the bracket is removed.

### A6 · 📊 A sentence with a Display · table
- A6.1 · The panel stops reading the README as if it were the authority.
  **Done when:** the S-Display page is what the panel quotes for state, and the README's takeaway is either dropped or labelled as unauthoritative.
- A6.2 · The rows are typeset rather than shown as source.
  **Done when:** a table panel opens on the rows as the manuscript will set them, which `preview.pdf` already makes possible.

### A7 · 🖼 A sentence with a Display · figure
- A7.1 · What a citation of an unpromoted candidate MEANS is ruled.
  **Done when:** a sentence citing a unit whose candidate is not promoted renders in a state that says so, and the page says which.
- A7.2 · A PDF-only unit previews.
  **Done when:** a unit carrying only a PDF opens a picture rather than an empty panel.

### P · 🏁 Page-level
- P1 · A reader finds the rule governing one sentence without reading the page end to end.
  **Done when:** a reader given a sentence with an unfamiliar marker reaches the right division from `### 1` in one hop.
- P2 · Nothing on this page specifies how a display is MADE.
  **Done when:** a reader applying `QB5`'s Law to `### 6` and `### 7` finds no sentence about recipes, renderers, or promotion.

## States

### A1 · 🧪 Try it yourself: all four types, live on this page
- 🔨 A1.1 · Active. The four types are on this page as live markers and the chips build; whether all four panels open is what a reader is being asked to check.

### A2 · The shared grammar
- ✅ A2.1 · Done 260802, and unchanged by the absorption: `### 2` carries both lifted rules with the type each came from.
- ⬜ A2.2 · Not started. Both candidates are still written under one type only, which is why `### 2.3` names them as unproven rather than lifting them.

### A3 · What separates the four
- 🔨 A3.1 · Active. `### 3` states the split; the one-line pointer under each of `### 4` to `### 7` is what absorption made possible and has not been written yet.

### A4 · 📚 A sentence with a citation
- ⬜ A4.1 · Not started. Measured on `4-main` 260726, and the three failures still share one word.
- ⬜ A4.2 · Not started.
- ⬜ A4.3 · Not started, and it is the one on this list that can mislead a reader rather than merely fail them.

### A5 · 🔢 A sentence with a value
- ⬜ A5.1 · Not started. It is a documentation-versus-marker collision, which `### 5` names.
- ⬜ A5.2 · Not started.
- ⬜ A5.3 · Not started.
- ⬜ A5.4 · Not started, and it is the only item here measured on the live paper.

### A6 · 📊 A sentence with a Display · table
- 🔨 A6.1 · Half closed 260727: the panel now carries a one-click anchor to the owning S-Display face and quotes that page's own `state:`. Open: whether it should stop reading the README's takeaway at all.
- ⬜ A6.2 · Not started, and `preview.pdf` already exists on every unit, so this is a panel change rather than a build change.

### A7 · 🖼 A sentence with a Display · figure
- ⬜ A7.1 · Not started.
- ⬜ A7.2 · Not started.

### P · 🏁 Page-level
- 🔨 P1 · Active, and it is the reason this page exists rather than four. The test sheet is the instrument; a fresh reader has not run it yet.
- 🔨 P2 · Active and unverified for the two display divisions, which arrived from faces written before `QB5`'s Law was stated.

## Files

### 🗄 Archived · the faces this page absorbed on 260803
- `_archive/QBe1a-sentence-citation.md` · became `### 4`. Its measurements and design history stay there rather than being rewritten.
- `_archive/QBe1b-sentence-value.md` · became `### 5`.
- `_archive/QBe1c-sentence-display-table.md` · became `### 6`.
- `_archive/QBe1d-sentence-display-figure.md` · became `### 7`.
