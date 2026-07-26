# A sentence with a value
state: ✅ RULED
owner: JL
method: never let a number into prose without the run that produced it

## Question
When a sentence states a number, where does that number come from and how does the reader check it? A value has the shortest path to a retraction of any attachment: a coefficient that silently changed after a re-run is a false claim in a published paper, so the binding is to the RUN, never to a file that can be overwritten.

A value is the attachment type with the shortest path to a retraction. A citation that is wrong is embarrassing; a coefficient that silently changed after a re-run is a false claim in a published paper. So the binding here is not to a source document but to a RUN, and the state that matters is whether the prose still matches the run it came from.


The approach is to bind a number to the RUN that produced it rather than to a file path, since paths get reused and runs do not. What we want is a manuscript where a coefficient that changed after a re-run is detectable, instead of a claim that was true once and nobody noticed stopped being true.
## Boundary
- ✅ Covered here
  The value marker in prose, the `> Value:` lane, chip states, the hover card, and staleness against the producing run.
- ↪ Covered elsewhere
  The sentence itself is `QC0`; the rendering mechanism is `QA8`; how a question reaches the bank and comes back is `QBb1`; the placeholder grammar is `QBb3`.

## Diagram
```
 A VALUE BINDS TO A RUN, NOT TO A FILE. THE PATH IS REUSED.

   the sentence   …at a mean absolute error of {VAL:? the deployed
                  model's MAE} [Q-Section-4]
                       ╰─ what is WANTED ─╯  ╰─ who owes it ─╯
                                │
                                │  ONE resolver, shared with QC1
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

So the resolver was built once, on the bracket, and both `QC1` and `QC2` consume it. Three citation chips that yesterday could only say "owed" now say the answer landed.

Two decorations are in live use for the q-consumer bullet (`* **Q-Section-2** — …` in `PP03`, `- Q-Section-1 (§7.2): …` in `PP04`), so the resolver reads the ID and ignores the bullet. Tightening that grammar is not worth a migration.

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

This is `QD6`'s provenance chain applied to a value rather than a display, and it makes the number the entry point to its own audit. Each link is offered only if the path really exists: a link that 404s is worse than no link, because it looks like provenance.

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

### The hover card
The rendered value, its unit, the source path, the producing run, and the verification state.

## Items to Finish
- [x] 🆔 Bind a value to its producing run
      Identity is the run, not the path, because the path is reused.
- [x] 🎨 Build the value chip
      `{VAL:? …}` renders as a chip resolved against `1-probes/`, with `ready` split out from `owed`. Half of `QA8`'s blocked inline-marker item, since the bracket resolver it needed also upgraded `QC1`.
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

## Where we are
The value chip is built and live on the MISQ board. Measured there, 215 chips resolve at build time:

```
 🔢 value    ✦ ready 13   ⏸ parked 11   ❓ unowned  2
 📚 citation ✅ ok   135   ✦ ready  3   ⏳ owed  7   ❓ unowned 20   ⚠️ broken 2
 🎯 bracket  ✅ ok    10   ⏳ owed  3   ❓ unowned  9
```

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

- 260726 CC · 🔗 Closing this unblocks `QA8`'s chip renderer
  `QA8` on the boardform board owns the MECHANISM: the fold, the badge, the drawer, the tint, the click-to-add.
  Its one unbuilt item, inline-marker chips, is blocked on four rulings, and this face is the value one: what the chip means, what states it has, and what resolves it, which here is a number bound to the run that produced it.
  The mechanism cannot be built against a guess, so that item stays open until all four of `QC1` to `QC4` say what to render.

## Law
- The bracket is the join key, not part of any marker. `[Q-…]` sits BESIDE `\cite{TOADD}` or `{VAL:? …}`, never fused into it, and one resolver serves every marker type.
- A probe's `state:` is a claim, not a fact. `answered` is honoured only when its `### a-executor` block is non-empty; otherwise the chip reports the contradiction.
- A landed answer under an owed marker gets its own state. Folding `ready` into `owed` hides the cheapest work in the paper.
- The NUMBER carries the emphasis, not the bracket. A reader checks the figure; the pointer is bookkeeping and is styled as such.
- A match is asserted only when it is UNIQUE. Two different recorded figures rounding to one prose number is an ambiguity to report, never a match to pick from.
- A number that cannot be checked is reported as unchecked, never as wrong. Derived and definitional figures are normal, and alarming on them would retire the feature within a day.

## Log
- 260726 · JL: "include the Probe folder, and the task folder for each value". The number chip's panel now opens the four-hop chain (sentence, probe, bank answer, run folder), which is `QD6`'s chain applied to a value. Two refinements came out of reading the result: `p < 0.001` was being flagged ambiguous, which is wrong because an inequality is a bound and not a measurement; and a match now says whether it came from the answer block or from the question text, since a threshold the question named is weaker evidence than a figure the run returned. Ambiguous count fell 6 to 4.
- 260726 · JL, reading `S-Main-7`: "could you make the value to be highlighted, instead of the Q-Section-xxx". Numbers in a bracketed sentence are now chips checked against the answering run, and `.qref` was demoted to a quiet marker. Shipping it immediately produced the bug it exists to prevent: `1.21` was reported as matching `1.20879`, a CI bound on the wrong exposure, because the checker took the first hit. Distinct-value collection and an `amb` state replaced it.
- 260726 · The value chip and the shared `[Q-…]` resolver shipped. Building it changed the ruling: the bracket was going to be re-parsed per marker type, and it is one thing, so it resolves in one place. Four bracket ids turned out to be claimed by no probe entry at all, which no marker could previously show.

## Files
- `1-probes/`
  Where the answering run is recorded.
- `haipipe-board/src/dialect_paper.py`
  The resolver: the `.bib` index, the probe index, and `question()`.
- `haipipe-paper-revise-place`
  The worker that substitutes a landed answer into the prose.
