# A sentence with a value
state: 🟡 PARTIAL
owner: JL
method: never let a number into prose without the run that produced it

## Opening
When a sentence states a number, where does that number come from and how does the reader check it?
A value has the shortest path to a retraction of any attachment: a coefficient that silently changed after a re-run is a false claim in a published paper, so the binding is to the RUN, never to a file that can be overwritten.

A value is the attachment type with the shortest path to a retraction. A citation that is wrong is embarrassing; a coefficient that silently changed after a re-run is a false claim in a published paper. So the binding here is not to a source document but to a RUN, and the state that matters is whether the prose still matches the run it came from.


The approach is to bind a number to the RUN that produced it rather than to a file path, since paths get reused and runs do not. What we want is a manuscript where a coefficient that changed after a re-run is detectable, instead of a claim that was true once and nobody noticed stopped being true.
Scope: This page covers The value marker in prose, the `> Value:` lane, chip states, the panel a chip opens, and staleness against the producing run. Neighbouring pages cover The sentence itself is `QC5`; the rendering mechanism is `QA9`; how a question reaches the bank and comes back is `QC4b`; the placeholder grammar is `QC4a`.

## Diagram
```
 A VALUE BINDS TO A RUN, NOT TO A FILE. THE PATH IS REUSED.

   the sentence   …at a mean absolute error of {VAL:? the deployed
                  model's MAE} [Q-Section-4]
                       ╰─ what is WANTED ─╯  ╰─ who owes it ─╯
                                │
                                │  ONE resolver, shared with QBe1a
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
   the prose      QBe1b-sentence-value.md  ## Content   (S4)
   the bracket    _fixture/1-probes/PP03_results-values/QX5_binary-exposure-flags.md
                    q-consumer Q-Section-7 · state: answered
   the digits     the same file's ### a-executor
                    +0.0045 · +0.0009 · the figures each chip is checked against
   the chain      probe → bank QA file → run folder, opened by the panel
```

## Content
### What sits where
```
 in the sentence   the real number, once it has landed
                   {VAL:? what the number is} [Q-Section-n]   before it lands
 under it          > Value: main-beta · source=tasks/C04/.../source_data.csv
                            · run=<run id> · state=verified
```
The `{VAL:?}` marker carries a description of what is wanted, not a guess at it. Never invent a number to avoid a placeholder.

### S4 of the paragraph on `QC5`
`QC5` carries one paragraph with all four attachment types. This is its fourth sentence, the one that measures something, written here and checked against `_fixture/1-probes/PP03_results-values/QX5_binary-exposure-flags.md`:

Physicians flagged as high-agreeableness are more likely to write a high-dose or long-duration prescription (+0.0045, p = 0.007) and to exceed the CDC high-risk level of 90 MME per day (+0.0009, p < 0.001) [Q-Section-7].
> Value: is_high_mme_daily · probe=`_fixture/1-probes/PP03_results-values/QX5_binary-exposure-flags.md` · run=v0618 · state=verified

`+0.0045`, `90` and `+0.0009` are each green because each appears in the run behind `[Q-Section-7]`, which is the fourth chip. Click any of them and the panel opens the probe entry, the bank's answer and the run folder. `p = 0.007` and `p < 0.001` are deliberately NOT chipped: a number after a comparison is a bound, not a measurement.

The paragraph's other sentences are the sibling pages': S1 to S3 the citations are `QBe1a`, S5 the table is `QBe1c`, S6 the figure is `QBe1d`.

### The case this page exists for
One digit changed in that fourth sentence, nothing else:

Physicians flagged as high-agreeableness are more likely to exceed the CDC high-risk level of 90 MME per day (+0.0019, p < 0.001) [Q-Section-7].

`+0.0019` renders grey and dotted, `unver`. Note what that does and does not claim: the chip cannot call it WRONG, because an unmatched figure may equally be derived. What it does is make the difference visible between `+0.0009`, which matched a recorded figure, and `+0.0019`, which matched nothing, in a sentence where the prose showed no difference at all.

### Evidence enters through one door
A paper stage may not compute. The number arrives through PROBE, from a task or discovery answer, and the lane records which one.
That is why the lane names a run and not just a file: the same path can hold a different number tomorrow.

### The bracket is the join key, and it is not value grammar
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

So the resolver was built once, on the bracket, and both `QBe1a` and `QBe1b` consume it. Three citation chips that yesterday could only say "owed" now say the answer landed.

Two decorations are in live use for the q-consumer bullet (`* **Q-Section-2**: …` in `PP03`, `- Q-Section-1 (§7.2): …` in `PP04`), so the resolver reads the ID and ignores the bullet. Tightening that grammar is not worth a migration.

### `answered` is checked, never believed
A probe entry may carry `state: answered` while its `### a-executor` block is empty. From the prose side that reads as done and is not, so the chip verifies the block before it agrees. `read` is the honest name for that condition when the entry admits it: the bank answers, and nothing has been harvested into the entry yet.

### Chip states as built
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

### The number is the claim; the bracket is the bookkeeping
The first build had the emphasis backwards, and JL caught it on `S-Main-7` (260726):

```
 before   …(odds ratio 1.21, p < 0.001) [Q-Section-2]
                                         ▔▔▔▔▔▔▔▔▔▔▔  the pointer was loud
 after    …(odds ratio 1.21, p < 0.001) [Q-Section-2]
                          ▔▔▔▔  ▔▔▔▔▔                  the FIGURE is loud
```

A reader checks the number. The bracket is still there and still clickable, demoted to a quiet trailing marker, because it remains the binding. This closes the "unbound number" item in the only way that was ever going to work: a bare numeral gets no marker of its own, but a numeral in a sentence that ALREADY names its question can be chipped by inheriting that binding.

### The chip opens the whole chain, not just the probe
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

### What a number chip actually checks
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

### `amb` came out of a bug worth keeping
The first version returned the FIRST recorded figure that matched. On JL's own sentence it reported `1.21 MATCHES the run (recorded as 1.20879)`, which is the lower bound of a 95% CI on the CONTINUOUS exposure. The sentence means `1.21494`, the odds ratio on the BINARY exposure. The number in the prose is right; the provenance the chip asserted was wrong, which is precisely the failure this page exists to prevent, committed by the thing built to prevent it.

So a match is now collected over DISTINCT values rather than occurrences. One value is a match. Two different values are an ambiguity, and both are named. That `1.21` is ambiguous is not a false positive: the same probe folder carries a recorded contradiction about which trait form that logit used, and a reader cannot tell from the sentence alone.

### What the panel carries
The rendered value, its unit, the source path, the producing run, and the verification state.

## Aims
- [ ] 🩻 `{VAL:?}` written INSIDE prose about markers is chipped as a placeholder
      Measured on `S-Main-4` 260727. That page's only `{VAL:?}` hit is the token quoted in the sentence "`{VAL:?}` count = 0", which is prose REPORTING that there are none. It carries no bracket, so it renders as a hole, and there is no number for any probe entry to carry.
      Same defect as the one filed on `QBe1a`, on the other marker: the detector cannot tell a marker that is USED from a marker that is NAMED. Three confirmations now across two pages and both marker types, so the fix belongs in the resolver, not in an authoring rule. A fenced span already opts out; prose does not.
- [x] 🆔 Bind a value to its producing run
      Identity is the run, not the path, because the path is reused.
- [x] 🎨 Build the value chip
      `{VAL:? …}` renders as a chip resolved against `1-probes/`, with `ready` split out from `owed`. Half of `QA9`'s blocked inline-marker item, since the bracket resolver it needed also upgraded `QBe1a`.
- [x] 🔗 Resolve the `[Q-…]` bracket once, for every marker type
      One resolver in `dialect_paper.Paper.question()`; citation, value and bare brackets all read it.
- [ ] 📐 Define staleness
      State exactly what makes a value stale, and whether a stale value blocks the section's gate or only flags it. The chip has no `stale` state yet because nothing records WHEN a number was woven in against when its run last executed.
- [x] 🔍 Chip the number itself
      Numerals in a sentence that names its question are chipped and checked against the answering run. JL 260726: "make the value to be highlighted, instead of the Q-Section-xxx". 65 on the MISQ board.
- [x] 🔗 Open the whole chain from the number
      probe entry, bank QA answer, and the run folder, each linked only when the path exists. JL 260726.
- [x] ⁉ Report ambiguity rather than picking one
      A prose number that rounds to two different recorded figures is reported as ambiguous with both named, not silently matched to whichever was found first.
- [ ] 🔍 Numbers in a sentence with NO bracket
      Still invisible, and deliberately: chipping every numeral on the board would make the signal worthless. A sentence stating a measured figure with no question attached is the real defect, and detecting it needs a way to tell a measurement from a section number.
- [ ] 🧹 Close the four unowned brackets
      `Q-Resource-1`, `Q-Resource-2`, `Q-Resource-3`, `Q-Venue-1` are promised by 9 brackets and declared by no probe entry. Either open the entries or drop the brackets.
- [ ] 🧪 One live example plus one stale case

## States
The value chip is built and live on the MISQ board. Measured there, 258 chips resolve at build time:

```
 🔢 value    ✦ ready 13   ⏸ parked 11   ❓ unowned  1
 📚 citation ✅ ok   121   ✦ ready  3   ⏳ owed  7   ❓ unowned 11   ⚠️ broken 0
 🎯 bracket  ✅ ok    10   ⏳ owed  3   ❓ unowned  9
 🔢 number   ✓ ok    33   ⁉ amb    4   ? unver 10   ❓ unowned  6
 🖼 display  ✅ ok    11   ✦ ready  2   ⚠️ broken 3
```
The citation row is lower than the one this page carried earlier, and the two `broken` are gone, because `> JL:`/`> CC:` lanes and `## Log` narration stopped being read as claims. Nothing was fixed to make that happen; the detector stopped counting people talking about citations as citations.

The 13 `ready` values are the finding: thirteen sentences still say `{VAL:?}` while the answering probe entry already carries the number in its `### a-executor`. That is weaving work, not probing work, and nothing on the page said so before today.

Numbers are now chipped and checked against the run behind them. 65 on the MISQ board:

```
 ✓ ok       33   a recorded figure rounds to it
 ⁉ amb       4   it rounds to two or more DIFFERENT recorded figures
 ? unver    10   nothing recorded rounds to it; derived or definitional
 ❓ unowned   6   its bracket names a question no probe entry declares
```

The 4 ambiguous ones are the finding. They are not wrong numbers; they are numbers whose provenance the prose cannot pin down, and one of them was reported as a confident match by the first version of this checker.

Two gaps remain: staleness still has no recorded timestamp to compare against, and a measured figure in a sentence with no bracket at all is still invisible, now by choice rather than by accident.

- 260726 CC · 🔗 Closing this unblocks `QA9`'s chip renderer
  `QA9` on the boardform board owns the MECHANISM: the fold, the badge, the drawer, the tint, the click-to-add.
  Its one unbuilt item, inline-marker chips, is blocked on four rulings, and this face is the value one: what the chip means, what states it has, and what resolves it, which here is a number bound to the run that produced it.
  The mechanism cannot be built against a guess, so that item stays open until all four of `QBe1a` to `QBe1d` say what to render.

## Law
- The bracket is the join key, not part of any marker. `[Q-…]` sits BESIDE `\cite{TOADD}` or `{VAL:? …}`, never fused into it, and one resolver serves every marker type.
- A probe's `state:` is a claim, not a fact. `answered` is honoured only when its `### a-executor` block is non-empty; otherwise the chip reports the contradiction.
- A landed answer under an owed marker gets its own state. Folding `ready` into `owed` hides the cheapest work in the paper.
- The NUMBER carries the emphasis, not the bracket. A reader checks the figure; the pointer is bookkeeping and is styled as such.
- A match is asserted only when it is UNIQUE. Two different recorded figures rounding to one prose number is an ambiguity to report, never a match to pick from.
- A number that cannot be checked is reported as unchecked, never as wrong. Derived and definitional figures are normal, and alarming on them would retire the feature within a day.

## Log
- 260803 · Left `QB · Delivery` for the new `QBe · Delivery Element` group, and `QB12b` became `QBe1b`, then took its place in the unit-size order ruled the same day (JL 260803: sentence, display, section); the old id resolves as a declared alias in `board.md ## Links`.
- 260726 · JL: "remove the icons, just keep different colors", then "only the box fill color to be of opacity, how about you make the font color to be 100% solid". Both done in `board.css`. Every chip carried a kind emoji in `::before` and a state glyph in `::after`, so `QC5`'s eleven-chip paragraph carried twenty-two decorations before a word of prose; both are gone and colour alone says the state. The first attempt at the fade used `opacity` on the whole chip, which dimmed the TEXT as well, and that was the wrong axis: the text is the content and the box is the decoration, so only the box gives ground. Now the fill sits at 6%, the border at 14% and the text at 100%, and hover deepens the fill without ever touching the text. `broken` and `unowned` keep a heavier box on purpose, because a defect that sinks into the prose is a defect nobody acts on. The glyph was the third copy of the state anyway: the `title=` names it in words and the panel repeats it in its header.
- 260726 · JL: "for the display, could we also make the float.tex's pdf to be embedded in the popped out window as well?" Yes, and the file to embed turned out to be `preview.pdf` rather than `assets/figure.pdf`: it is `float.tex` COMPILED STANDALONE, so it carries the caption, the notes and the numbering set by the paper's own class, which `assets/` never does. It leads the panel on the same terms as a citation's `.bbl`: show the thing as the manuscript will set it. All 10 MISQ units already had one. A preview older than the asset it previews is labelled rather than hidden.
- 260726 · JL: "add the google scholar search link"; and "for the values, displays, figures, I cannot click them". The citation panel's link row gained a `🔎 Scholar` search, last and with its own glyph because everything above it is an identifier and a query is not; on this paper 195 of 216 entries had no clickable pointer before it. The dead chips were a CSS class collision: `.fig`, meant for markdown images, also matched every figure panel (`chipcard disp fig <state>`) and its `display:block` un-hid the closed popover, so five invisible full-width panels lay over the page eating clicks. Scoped to `img.fig`, with `.chipcard:not(:popover-open){display:none}` as a guard. My first diagnosis blamed `<summary>` and added a script handler; the A/B showed the handler changed nothing and it was reverted, so the chip is script-free again. Verified in headless Chrome 150: 11/11 on `QC5` and 25/25 on the MISQ board's first slide, reachable, opening, and landing on screen.
- 260726 · JL: "read QA6 ⑦ The paper folder, we have done many changes here, right?" Correct, and the board was teaching the superseded layout. QA6 ruled 260726 that the deliverable is UNNUMBERED (`displays/`, `sections/`) and the resolver still had `0-displays` hardcoded in six places. Proved it by renaming the fixture and rebuilding: four id chips went `unowned` and both `\ref{}` chips went GREEN through the "a \label that is not a display unit" branch, which is the silent false-green `QBe1c` and `QBe1d` exist to prevent. `Paper` now resolves `displays/` first and falls back to `0-displays/`; the fixture moved to the ruled name. Still open on QA6's side: `.board-refs.bbl` is machinery sitting in the unnumbered half.
- 260726 · JL, on the embed: "I don't want you to refer something, please just make it real in the content, not refer a markdown". Reverted. The example prose is written directly in each page's `## Content`: `QC5` carries the whole paragraph, `QBe1a`-`QBe1d` carry only their own sentences from it, labelled by position. The rule that came out of it is the one on `QC5`: PROSE lives on the page, EVIDENCE lives in `_fixture/` (`.bib`, `.bst`, `0-displays/`, `1-probes/`), and `_fixture/` never holds a paragraph. Same visit fixed the panel: without `position-area` support the base `.chipcard` had no `max-height`, so a two-image figure panel grew past the viewport and spilled over the page.
- 260726 · JL: "include the Probe folder, and the task folder for each value". The number chip's panel now opens the four-hop chain (sentence, probe, bank answer, run folder), which is `QD6`'s chain applied to a value. Two refinements came out of reading the result: `p < 0.001` was being flagged ambiguous, which is wrong because an inequality is a bound and not a measurement; and a match now says whether it came from the answer block or from the question text, since a threshold the question named is weaker evidence than a figure the run returned. Ambiguous count fell 6 to 4.
- 260726 · JL, reading `S-Main-7`: "could you make the value to be highlighted, instead of the Q-Section-xxx". Numbers in a bracketed sentence are now chips checked against the answering run, and `.qref` was demoted to a quiet marker. Shipping it immediately produced the bug it exists to prevent: `1.21` was reported as matching `1.20879`, a CI bound on the wrong exposure, because the checker took the first hit. Distinct-value collection and an `amb` state replaced it.
- 260726 · The value chip and the shared `[Q-…]` resolver shipped. Building it changed the ruling: the bracket was going to be re-parsed per marker type, and it is one thing, so it resolves in one place. Four bracket ids turned out to be claimed by no probe entry at all, which no marker could previously show.

## Files
**The skills this ruling binds.** A rule made here is a rule these must follow, and each now cites this face by id so the pair is greppable in both directions.

- `haipipe-paper-probe`
  Writes the `[Q-X-n]` bracket under `### q-consumer`. The id it spells and the id in the prose are the same string or the sentence reports `unowned`.
- `haipipe-paper-revise-place`
  Substitutes a landed number into the prose and discharges its bracket. It may not compute one: a paper stage does not compute, which is this face's first law.
- `5-section-edit/`
  May ship `{VAL:? …}` standing. The state this page defines as legitimate is the one that stage is allowed to leave behind.
- `haipipe-board/src/dialect_paper.py`
  Resolves and reports; never writes. Boundary ruled in `QA8`.

**Where the evidence lives**
- `1-probes/`
  Where the answering run is recorded.
- `haipipe-board/src/dialect_paper.py`
  The resolver: the `.bib` index, the probe index, and `question()`.
- `haipipe-paper-revise-place`
  The worker that substitutes a landed answer into the prose.
