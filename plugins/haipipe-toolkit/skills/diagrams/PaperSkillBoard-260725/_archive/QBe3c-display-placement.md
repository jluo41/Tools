# A display placed in a section: which one it lands in, and whether the build reaches it

state: 🔴 OPEN
owner: JL
method: decide which section a float lands in, and make the build actually reach it

## Opening

Where does the float go, and does the compiled paper reach it at all?

Placement is where a float appears in the printed paper. First mention is the earliest sentence that cites it, and LaTeX puts a float near that, so the section citing a unit earliest decides where it appears, whatever the unit's own page says it serves. Reaching it is a separate question: whether the master file inputs the float at all.

**Where this page sits**: QBe3 heads the section series, and placement lives here because first-mention order is a fact about a sequence.
QBe2c owns what the caption and label SAY, QBe2a owns the folder the float lives in, QBe1c and QBe1d own what a citing sentence means, and QBe3a owns float numbering across the document.
`QD3@display` already ruled how a selected unit reaches a reader-facing sentence, and that is not re-argued here.

**Why this face is sharper on this paper than in general**: the answer today is that no float is reached at all.
Every display label in the manuscript compiles to `??`, which makes placement moot until the wiring exists.

**What an empty face costs**: three separate section pages each recorded the same gap as their own display problem.
One missing rule produced five symptoms filed in five places, which is what an absent face looks like from the inside.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Keep reaching and placing apart**: a float that is placed correctly and never reached compiles to `??`, and a float that is reached may still land in the wrong section.
A sentence that blurs the two hides whichever half is broken.

**Never re-argue `QB5@display` or `QD3@display`**: both are settled upstream.
This page decides where a float lands and whether the build reaches it, and cites the rest.

**Name the live case, not the general one**: `S-Display-1b` is a real two-consumer conflict on a real paper.
An invented example would let the rule be written without meeting the case that actually breaks it.

## Diagram

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

## Content

### 1 · Nothing the build reaches declares a display label

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

#### 1.1 · One gap presenting as five symptoms
(it is why the fix belongs on this face and not on any section page)
Three separate section pages had each recorded a `??` as their own display problem.
None of them was wrong, and none could fix it, because the missing edge is between the master and the gallery rather than inside any section.

### 2 · First mention decides, and this paper has a live case

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

#### 2.1 · The choice is accept LaTeX's rule or pin the float
(first-mention-wins is a default, and a default is not a decision)
Either the paper accepts that the earliest citing section decides, or it pins a float deliberately and overrides the default.
Both are defensible; what is not defensible is the current state, where nothing says which, so two pages can each be internally right.

### 3 · A placed float and a promoted asset are different things

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

#### 3.1 · A section needs a rule for its own unpromoted unit
(the prose is final while the picture is not, and the section cannot tell)
Placement does not imply the reader sees the current asset.
Until this face says what a section does when its unit is not promoted, five `ready` markers sit in a finished section with nothing reporting that the pictures are stale.

## Aims

### A1 · 🔌 Nothing the build reaches declares a display label
- A1.1 · The build reaches the floats.
  **Done when:** the five labelled displays resolve in a compiled PDF instead of printing `??`, whether by the master inputting the gallery or by each section inputting the units it cites.

### A2 · 📍 First mention decides, and this paper has a live case
- A2.1 · Placement is ruled when one unit serves two sections.
  **Done when:** this face says whether the paper accepts first-mention-wins or pins the float, and `S-Display-1b` no longer contradicts the section that cites it earliest.

### A3 · 🧯 A placed float and a promoted asset are different things
- A3.1 · A section knows what to do when its unit is not promoted.
  **Done when:** the five `ready` markers on `S-Main-5` either resolve or are reported by a check rather than read as final.

## States

### A1 · 🔌 Nothing the build reaches declares a display label
- ⬜ A1.1 · Not started, and it is the blocker for everything else here. Measured 260727: the master inputs `sections/*` and `appendices/*` and reaches no `displays/*/float.tex`, so all five labels compile to `??`. This is not a paper-stage edit, because it changes what the build reaches.

### A2 · 📍 First mention decides, and this paper has a live case
- ⬜ A2.1 · Not started. The conflict is live on `S-Display-1b` today, and nothing on the board says which of the two answers the paper takes.

### A3 · 🧯 A placed float and a promoted asset are different things
- ⬜ A3.1 · Not started. `S-Main-5` carries five `ready` markers, and nothing checks a placed float against the asset that was accepted.

## Files

- `Personality-Opioid-MISQ2026.tex` · inputs `sections/*` and `appendices/*`, and reaches no `displays/*/float.tex`
- `0-lifecycle/3-display/4-display.tex` · the gallery that does input the floats, and that the master does not input
- `0-lifecycle/3-display/S-Display-1b-research-design.md` · the live two-consumer case
- `QBe3-delivery-section.md` · the series head, which owns why placement is a section rule

## Law

- Placement and reaching are two conditions, and a float satisfies neither by satisfying the other.
  A float that is not on a path the master reaches compiles to `??`, whatever any section page declares about it.

## Glossary

- **First mention**: the earliest sentence citing a unit, which is what LaTeX places the float near, and therefore what decides its section.
- **Reaching**: whether a float is on any `\input` path the master file actually follows.

## Log

260803 · Left `QB · Delivery` for the new `QBe · Delivery Element` group, and `QB11c` became `QBe3c`, then took its place in the unit-size order ruled the same day (JL 260803: sentence, display, section); the old id resolves as a declared alias in `board.md ## Links`.
260802 · Migrated to the QB4 page contract: Writing Style added, Content numbered into three divisions with face figures and captions, Aims regrouped as A1/A2/A3 with `Done when`, States mirrored per Aim, and Law and Glossary written for the first time.
260802 · Moved from the Display concern to the section series as QB11c, because first-mention order is a fact about a sequence.
260727 · Reframed from "the two seams" after `QD1@display` and `QD2@display` turned out to have ruled both contracts already; what was actually missing was where the float goes and whether the build reaches it.
