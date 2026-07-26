# A sentence with a citation
state: 🟡 PARTIAL
owner: JL
method: one stable key in the prose, provenance in the lane, and a chip that shows whether the key exists

## Question
When a sentence rests on a source, what does the prose carry, what does the lane carry, and what does the reader see? A citation is the one attachment type an agent may never complete on its own, because the key comes from a bibtex entry only a human may write. Everything else about this type follows from that.

A citation is the one attachment type an agent may never complete on its own. The key comes from a `.bib` entry that only a human writes, so the sentence has to be able to stand in a legitimate, visible, unfinished state for as long as that takes. Everything else about this type follows from that constraint.


The approach is a stable key in the prose, provenance in the lane beneath it, and a chip that shows the state of both. What we want is that an owed citation is loudly visible rather than silently missing, and that no agent can ever close the gap by writing a bibtex entry itself.
## Boundary
- ✅ Covered here
  The citation marker in prose, the `> Citation:` lane, chip states, the hover card, and the human-only boundary.
- ↪ Covered elsewhere
  The sentence itself is `QC0`; the rendering mechanism is `QA8`; the placeholder grammar shared with values is `QBb3`; how a key becomes LaTeX or Word is `QBa3`.

## Diagram
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

Steps ① to ③ are the paper skill's. Step ④ is the board's, and it only WATCHES: it
never writes a marker, a probe entry, or a `.bib` line. That split is `QBc5`.

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
```

## Content
### What sits where
```
 in the sentence   \citep{key}                    the key EXISTS in the paper's .bib
                   \cite{TOADD} [Q-Section-n]     no key yet; the bracket names the
                                                  question that will produce one
 under it          > Citation: key · source=bibliography · state=verified
                   > Citation: <reference> · doi=… · bib hits=0 · owed by [Q-Seed-1]
```
Marker and bracket sit side by side and are never fused. A placeholder with no bracket is a hole no question will ever fill.

### The human-only boundary
An agent may grep the `.bib` and may report that a key is missing. It may not write a bibtex entry.
This is not a style preference, it is the rule that keeps fabricated references out of the manuscript, and it is why `\cite{TOADD}` is a first-class state rather than an error.
On the MISQ paper this is live: three `> Citation:` lanes carry a reference, a doi, a `.bib` hit count of zero, and the owed `[Q-Seed-1]` bracket, waiting on a human.

### Chip states
```
 ✅ ok         \citep{key} and the key greps in the .bib
 ✦ ready      \cite{TOADD} whose [Q-…] question has ANSWERED; a human still
               has to write the bibtex entry, which is why this is not ok
 ⏳ owed       \cite{TOADD} beside a [Q-…] still in flight
 ⚠️ broken     \citep{key} but the key does not grep: a real defect, never silent
 ❓ unowned    a placeholder with no bracket, or a bracket no probe declares
```

### Where the panel points, and what "the source" means
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

### A broken key is asked the more useful question
When a key does not resolve, saying so is only half an answer. The panel also lists the keys that DO resolve, nearest first, matched on the author run rather than on plain string distance: `stock2005testing` against `stock2002survey` scores about 0.6 and falls off a default fuzzy cutoff, which is exactly the case that matters. Bibtex keys are author-year-word, so the author run is the strong signal.

It suggests and never substitutes. Choosing the key is a claim about what the sentence rests on, and that is the human's.

### How it resolves: build time, and `title=` is the floor
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

### Why the panel, and not just the tooltip (JL 260726)
A tooltip lives in an ATTRIBUTE. The build's assertion counts "chars of body surviving with JS stripped", and an attribute is not body, so the record was passing that test on a technicality: strip the scripts and the evidence was technically still in the file, but not in anything the check measured or a reader could search or print.

Moving the record into a `<div popover>` makes it real body text. The page grew by 42k on the MISQ board, and that growth IS the evidence finally being counted.

`title=` stays underneath, unchanged. The panel is the upgrade, never the only copy, which is the same rule tier 2 was always held to.

The index is built once per build by `src/dialect_paper.py`, which a board opts into by declaring `dialect: paper` and `paper-root:` in its own header. A board that does not declare it never pays for any of this, and `haipipe-board` learns nothing about papers unless asked.

### What it refuses to touch
A page that DISCUSSES placeholders writes `\cite{TOADD}` in backticks. Chipping that turns documentation into a false defect report, which it did on the first run: five of the reported holes were prose about holes. The rewriter now skips anything inside a code span or inside a tag's attributes.

The same trap has a second floor, and the first version fell through it. A human writing

```
 > JL: I think you should use \citep{xxx}
 > CC (REVISE 07-10): Mafi 2013 is the open decision -> add \citep{mafi...}
```

is ASKING for a citation, not making one. Both got chipped `broken`, and both were reported as this page's headline finding on 260726. They were the only two, so the page claimed a payoff it had not earned.

Backticks are optional in a comment and nobody will remember them, so the rule is now structural: a DISCUSSION lane (`> JL:`, `> CC:`, and `## Comments`) never chips. A TYPED evidence lane (`> Citation:`, `> Value:`, `> Display:`) still does, because those are claims about the sentence and their state is the whole point.

### What a chip can never see
A chip exists only where the board RENDERS text, and the board renders its faces. `0-sections/*.tex` is the actual manuscript and is reached only when a face embeds it. So the one genuinely broken key in this paper, `\citep{stock2005testing}` in `0-sections/D_iv_analysis.tex:30`, was invisible while two false positives sat on the board wearing its colour.

`dialect_paper.audit()` now walks the `.tex` directly and `build.py` prints what it finds, labelled as NOT rendered here. That is deliberately a build warning and not a chip: pretending the board covers the manuscript would be the same mistake in a new place.

## Items to Finish
- [x] 🆔 Choose a stable key as the anchor
      Citation identity does not depend on output syntax or citation style.
- [x] 🚫 The human-only rule is stated and honoured
      Agents grep, report, and leave `\cite{TOADD}` standing; the MISQ paper carries three such lanes today.
- [x] 🎨 Build the citation chip
      Shipped 260726. `src/dialect_paper.py` indexes the paper's `.bib` at build time; `body.py`'s `cite_chips()` rewrites every marker into a chip carrying its state as a class and its record as a native `title=`. One quarter of `QA8`'s blocked inline-marker item is now closed.
- [x] 🧪 One live example plus one broken key
      Live on the MISQ board: 125 resolved, 7 owed, 3 ready, 12 unowned. The one real broken key, `stock2005testing`, is in `0-sections/D_iv_analysis.tex:30` and is reported by `build.py` because no face renders that file.
- [x] 🚧 Stop chipping prose ABOUT citations
      Discussion lanes (`> JL:`, `> CC:`, `## Comments`) opt out; typed evidence lanes still chip. This removed 2 false `broken` and 19 other false chips.
- [x] 🔭 See past the board's own faces
      `dialect_paper.audit()` walks the paper's `.tex` and `build.py` prints what no chip can show, labelled as not rendered here.
- [x] 🎨 Click a chip, get the record in an attached panel
      Native `popover`, no script, `title=` kept underneath. JL 260726.
- [ ] 📐 Define the card schema
      Which fields a citation card shows, and what a broken key shows instead. The panel currently prints the resolver's tooltip lines verbatim, which is a placeholder for a real schema, not a schema.
- [x] 🔗 Point the panel at the source
      Three pointers: the `.bib` file and line where the key is DEFINED, the doi / eprint / url where the SOURCE is, and the raw entry as written. JL 260726: "where we link to the source?"
- [x] 💡 Suggest keys that DO resolve
      A broken key lists its nearest real neighbours, matched on the author run. It suggests and never substitutes.
- [x] 🗺 Name the skills this ruling binds
      `## Files` maps each step of the diagram to its owning skill. JL 260726: a QC page should say what it governs.
- [ ] ⚠️ A key that resolves is not a claim that was checked
      `ok` today means only that the key greps. Nothing records whether the SOURCE supports the sentence.

## Where we are
Live on the MISQ paper board. The counts below are after the discussion-lane fix, and they are LOWER than the ones this page carried earlier the same day because those were partly false.

```
 ON THE BOARD, in rendered face text
   ✅ ok        125    the key resolves in the .bib
   ✦ ready       3    \cite{TOADD} whose question is ANSWERED: the source is
                      recorded, the sentence has not been rewritten
   ⏳ owed        7    \cite{TOADD} beside a [Q-…] still in flight
   ❓ unowned    12    \cite{TOADD} with NO bracket: nothing will ever fill it
   ⚠️ broken      0

 IN THE .tex THE BOARD DOES NOT RENDER, reported by build.py
   ⚠️ broken      1    \citep{stock2005testing}  0-sections/D_iv_analysis.tex:30
   ❓ unowned      8    across 04_personality_extraction and 05_data_variables
```

The one real broken key had been found by hand before and written into `S-Appendix-0-control.md:397`, which names `stock2002survey` as the key that does resolve. It is still in the tex. That is the argument for the chip in one line: a note in a stage page does not mark the manuscript.

Nothing has been fixed. The `.bib` is human-only, so the broken key is JL's call, and the 20 unowned placeholders need either a question or a source. What this page delivers is that all of them are now visible, and that none of what is visible is invented.

Two states remain unbuilt and both are named in Items: no chip yet distinguishes a citation whose key resolves but whose CLAIM was never checked, and the `> Citation:` lane's own verification state is not read.

- 260726 CC · 🔗 Closing this unblocks `QA8`'s chip renderer
  `QA8` on the boardform board owns the MECHANISM: the fold, the badge, the drawer, the tint, the click-to-add.
  Its one unbuilt item, inline-marker chips, is blocked on four rulings, and this face is the citation one: what the chip means, what states it has, and what resolves it, which here is a `.bib` key that only a human may write.
  The mechanism cannot be built against a guess, so that item stays open until all four of `QC1` to `QC4` say what to render.

## Files
**The skills this ruling binds** (JL 260726: a QC page should name what it governs, not only what it decides). Each step of Diagram [1/2] has an owner, and a rule made here is a rule those skills must follow.

- `5-section-edit/`
  ① Writes the sentence, and may leave `\cite{TOADD} [Q-…]` standing. The state this page defines as legitimate is the one this stage is allowed to ship.
- `haipipe-paper-probe`
  ② Opens the probe entry and claims the bracket under `### q-consumer`. The bracket grammar ruled here is what it must write, or the chip cannot resolve.
- `haipipe-paper-revise-place`
  ③ Substitutes a landed key into the prose. It may only run after a human has written the `.bib` entry, which is the human-only rule enforced at the one place that would otherwise break it.
- `haipipe-paper-revise-content`
  Rewrites sentences around a placed citation; must not fuse marker and bracket.
- `dialect_paper.py`
  ④ Resolves and reports. Never writes. Owned by `/haipipe-board`, boundary ruled in `QBc5`.

**Where the evidence lives**
- `0-lifecycle/0-seed/S-Seed-0-seed.md`
  The three live owed-citation lanes on the MISQ paper.
- `1-probes/`
  The probe entries that claim the brackets.
- `0-sections/`
  The manuscript itself, which no face renders and `build.py` therefore audits.

## Law
A marker resolves at BUILD time, never at page load. Every chip carries its state as a class and its record as a native `title=`, so hover works with no script at all and a script may only enrich what is already there.

Evidence belongs in BODY TEXT, not in an attribute. An attribute survives the strip-the-scripts check without being readable, searchable or printable, which passes the test while missing its point. The panel is the record; `title=` is the fallback.

A marker inside a DISCUSSION lane is a person asking for evidence, not supplying it, and is never chipped. Typed evidence lanes are the opposite and always are.

A checker reports what it can see and says what it cannot. The board renders faces, so a defect in an unrendered `.tex` is printed as a build warning rather than left to a clean-looking page.

`dialect: paper` is opt-in and declared by the board that wants it. Board tooling does not assume a paper, and a board that says nothing gets no chips and pays no cost.

A rewriter never touches a marker inside a code span or a tag attribute. Prose about a placeholder is documentation, not a defect.

## Log
- 260726 · JL: "where we link to the source? could we find it in the bib.tex?" The panel now carries the `.bib` file and line, the entry's own doi / eprint / url, and the raw bibtex. The `.bib` line is printed rather than linked into, because jumping to it would mean the board rendering a view of the bibliography, and that is human territory. Broken keys gained nearest-neighbour suggestions after the default fuzzy cutoff missed `stock2005testing` -> `stock2002survey`, which is the one case that mattered.
- 260726 · Added the two diagrams and the skill map. The first is the reason this page exists: one citation crosses four skills plus a human, and the hard stop at step ⑧ is what makes `\cite{TOADD}` a state rather than an error.
- 260726 · Two corrections to what this page claimed the same morning. The 2 `broken` keys it called "the payoff" were prose inside `> JL:` and `> CC:` discussion lanes, asking for citations rather than making them; discussion lanes now opt out, which also removed 19 other false chips. And the one real broken key was never on the board at all, because it lives in `0-sections/D_iv_analysis.tex` and no face embeds that file; `build.py` now audits the `.tex` and prints it. Net: the detector went from 2 false positives and 1 miss, to 0 and 0.
- 260726 · JL: "maybe not hover, how about click it, and when I click it, it will be an attached window". Built with native `popover`, no script. The argument that settled it was not comfort: a `title=` is an attribute, so the record was passing the survive-with-JS-stripped assertion without being counted by it. The page grew 42k, which is that evidence becoming real body text.
260726 · Built the citation slice. `src/dialect_paper.py` (bib index + resolver), `body.py` `cite_chips()` with the code-span guard, `.chip` styles in `board.css`, `dialect:`/`paper-root:` parsed in `parse.py`, wired in `build.py`. Live on the MISQ board: 135 ok, 10 owed, 20 unowned, 2 broken. Two build bugs found and fixed on the way: a CSS comment containing a literal script tag broke the zero-script assertion, and the first version chipped inside backticks.

260726 · `QC2`'s bracket resolver landed and this page consumed it without a change of its own. The owed bucket split 10 into 7 owed and 3 ready. Recorded here because it is the first evidence that the four attachment types share a resolver rather than four parallel ones: building the second slice improved the first.
