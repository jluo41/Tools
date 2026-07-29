# A display placed in a section
state: 🔴 OPEN
owner: JL
method: decide which section a float lands in, and make the build actually reach it

## Question
Where does the float go, and does the compiled paper reach it at all? Placement is the last thing the consumer owns and the easiest to assume is automatic. It is not: LaTeX floats near the FIRST mention, so the section that cites a unit earliest decides where it appears, whatever the unit's own page says it serves.

On this paper the question is sharper than that, because the answer today is that **no float is reached at all.** Every display label in the manuscript compiles to `??`.

## Boundary
- ✅ Covered here
  Which section a float lands in, what happens when two sections cite one unit, and whether the build reaches the float at all.
- ↪ Covered elsewhere
  What the caption and label SAY is `QD3`. The folder the float lives in is `QD1`. What a sentence citing it means is `QC3` and `QC4`. Float NUMBERING across the document is `QC5`. The contract for how a selected unit reaches a reader-facing sentence is `QD3@display`, ruled and not re-argued here.

## Content
### Nothing the build reaches declares a display label
Measured 2026-07-27. `Personality-Opioid-MISQ2026.tex` inputs `sections/*` and `appendices/*` and nothing else. No `displays/*/float.tex` is on any path the master reaches, so every one of these compiles to `??`:

```
 fig:research-model              §1, §3
 fig:research-design             §5
 fig:llm-measurement             §4
 tab:agreeableness-distribution  §4
 tab:validation-summary          §4
```

One gap, five symptoms. Three separate section pages had each recorded it as their own display problem, which is what a missing face looks like from the inside.

### First mention decides, and this paper has a live case
`S-Display-1b` declares `serves: Methods §5`. Candidate E folds the measurement workflow into its step ①, and `display03` parks when that lands, so after promotion §4 has no figure of its own and must cite §5's unit. First mention then moves to §4, and the float follows it, into a section whose own page says the unit does not belong there.

That is not a bug in either layer. It is this face being empty: nothing says what happens to placement when a fold gives one unit two consumers, so the two pages disagree and neither is wrong.

### A placed float and a promoted asset are different things
`S-Main-5` shows five figure markers reading `ready`: the candidate landed and the manuscript has not caught up. The sentence is written, the float is placed, and the picture it will compile is not the one that was accepted. Placement does not imply the reader sees the current asset, and nothing currently checks the difference.

## Items to Finish
- [ ] 🔌 Make the build reach the floats
      Either the master inputs the display gallery, or each section `\input`s the units it cites. One decision, and it clears five `??` references. Not a paper-stage edit: it changes what the build reaches.
- [ ] 📍 Rule placement when one unit serves two sections
      First-mention-wins is LaTeX's rule. This face has to say whether the paper accepts it or pins the float deliberately. Live on `S-Display-1b` today.
- [ ] 🧯 Say what a section does when its unit is not promoted
      Five `ready` markers on `S-Main-5`. The prose is final and the picture is not.

## Where we are
Placement is undecided and the build reaches no float, so nothing on the reader-facing side of the display chain currently works end to end. The unit folders are healthy; the wiring between them and the manuscript is absent.

Reframed 2026-07-27. This face was briefly "the two seams: what Paper hands over and what comes back", which was a coined phrase for two contracts that `/haipipe-display` had already ruled at `QD1@display` and `QD2@display`. What was actually missing was not a map of the seams but this: where the float goes, and whether the build reaches it.

## Files
- `Personality-Opioid-MISQ2026.tex`
  Inputs `sections/*` and `appendices/*`; reaches no `displays/*/float.tex`.
- `0-lifecycle/3-display/4-display.tex`
  The gallery that does input the floats, and that the master does not input.
- `0-lifecycle/3-display/S-Display-1b-research-design.md`
  The live two-consumer case.
